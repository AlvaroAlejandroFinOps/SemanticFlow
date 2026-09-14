"""
Interfaz de línea de comandos (CLI) para SemanticFlow.
Permite inspeccionar esquemas relacionales y compilar modelos PBIP/TMDL nativos.
"""
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.parsers.yaml_parser import YamlSchemaParser
from src.core.engine.compiler import SemanticCompiler
from src.core.emitter.pbip_writer import PbipWriter
from src.core.ast.semantic import TableRole

app = typer.Typer(
    name="semanticflow",
    help="Compilador local de modelos semánticos Power BI (TMDL/PBIP) desde esquemas relacionales.",
    add_completion=False,
)
console = Console()


def _get_parser_for_file(file_path: Path):
    ext = file_path.suffix.lower()
    if ext in (".md", ".markdown"):
        return MarkdownSchemaParser()
    elif ext in (".yaml", ".yml", ".json"):
        return YamlSchemaParser()
    else:
        # Fallback a Markdown si es texto estructurado
        return MarkdownSchemaParser()


@app.command()
def compile(
    input_path: Path = typer.Option(
        ...,
        "--input",
        "-i",
        help="Ruta al archivo del esquema relacional (.md, .yaml, etc.).",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_dir: Path = typer.Option(
        Path("Artefactos/PBIP"),
        "--output",
        "-o",
        help="Directorio destino donde se generará el proyecto PBIP y TMDL.",
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Nombre personalizado para el modelo semántico.",
    ),
    culture: str = typer.Option(
        "es-CL",
        "--culture",
        "-c",
        help="Código de cultura regional para el modelo Power BI.",
    ),
):
    """
    Compila un esquema relacional a un modelo semántico nativo Power BI (TMDL/PBIP).
    """
    console.print(
        Panel.fit(
            f"[bold cyan]SemanticFlow[/bold cyan] -> Compilador Local TMDL/PBIP\n"
            f"[dim]Origen:[/dim] {input_path}\n"
            f"[dim]Destino:[/dim] {output_dir}\n"
            f"[dim]Cultura:[/dim] {culture}",
            box=box.ROUNDED,
        )
    )

    parser = _get_parser_for_file(input_path)
    raw_schema = parser.parse(input_path)
    if name:
        raw_schema.name = name

    console.print(
        f"[green][OK][/green] Ingestion exitosa: [bold]{len(raw_schema.tables)}[/bold] tablas detectadas, "
        f"[bold]{len(raw_schema.relationships)}[/bold] relaciones brutas."
    )

    compiler = SemanticCompiler()
    semantic_model = compiler.compile(raw_schema, culture=culture)

    dim_count = sum(1 for t in semantic_model.tables if t.role == TableRole.DIMENSION)
    fact_count = sum(1 for t in semantic_model.tables if t.role == TableRole.FACT)
    total_measures = sum(len(t.measures) for t in semantic_model.tables)

    console.print(
        f"[green][OK][/green] Inferencia semantica completada:\n"
        f"   - Dimensiones: [bold cyan]{dim_count}[/bold cyan]\n"
        f"   - Tablas de Hechos: [bold yellow]{fact_count}[/bold yellow]\n"
        f"   - Relaciones 1:N unidireccionales: [bold magenta]{len(semantic_model.relationships)}[/bold magenta]\n"
        f"   - Medidas DAX sintetizadas: [bold green]{total_measures}[/bold green]"
    )

    writer = PbipWriter()
    pbip_file = writer.write_bundle(semantic_model, output_dir)

    console.print(
        Panel(
            f"[bold green]Compilacion exitosa![/bold green]\n\n"
            f"Proyecto Power BI listo para abrir:\n"
            f"[bold white]{pbip_file.resolve()}[/bold white]\n\n"
            f"[dim]Puedes abrir directamente este archivo en Power BI Desktop.[/dim]",
            title="[bold cyan]Resultado Final[/bold cyan]",
            box=box.ASCII,
        )
    )


@app.command()
def inspect(
    input_path: Path = typer.Option(
        ...,
        "--input",
        "-i",
        help="Ruta al archivo del esquema relacional (.md, .yaml, etc.).",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
):
    """
    Inspecciona un esquema relacional y muestra el análisis de tablas, roles y claves.
    """
    parser = _get_parser_for_file(input_path)
    raw_schema = parser.parse(input_path)

    compiler = SemanticCompiler()
    semantic_model = compiler.compile(raw_schema)

    table_report = Table(
        title=f"Esquema Relacional: {raw_schema.name}",
        box=box.ROUNDED,
        header_style="bold magenta",
    )
    table_report.add_column("Tabla", style="bold")
    table_report.add_column("Rol Inferido", justify="center")
    table_report.add_column("Columnas", justify="right")
    table_report.add_column("Claves Ocultas", justify="right")
    table_report.add_column("Medidas DAX", justify="right")

    for t in semantic_model.tables:
        role_style = "cyan" if t.role == TableRole.DIMENSION else "yellow"
        hidden_cols = sum(1 for c in t.columns if c.is_hidden)
        table_report.add_row(
            t.name,
            f"[{role_style}]{t.role.value}[/{role_style}]",
            str(len(t.columns)),
            str(hidden_cols),
            str(len(t.measures)),
        )

    console.print(table_report)
    console.print(
        f"\n[bold]Total Relaciones 1:N Resueltas:[/bold] {len(semantic_model.relationships)}"
    )


if __name__ == "__main__":
    app()
