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
        Path("output/PBIP"),
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


@app.command()
def explain(
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
    format: str = typer.Option(
        "human",
        "--format",
        "-f",
        help="Formato de salida: 'human' (consola), 'json', 'md' (Markdown), o 'mermaid'.",
    ),
    persona: Optional[str] = typer.Option(
        None,
        "--persona",
        "-p",
        help="Proyectar a través de una Persona Lens específica (ej. 'executive', 'data_governance', 'bi_engineer', 'finops', 'ai_systems_engineer', 'compliance_auditor', etc.).",
    ),
):
    """
    Explica la procedencia y evidencia del modelo, o proyecta la perspectiva de una Persona Lens.
    """
    from src.core.mappers.raw_to_canonical import raw_to_canonical
    from src.core.engine.explainer import SemanticExplainer
    import json

    parser = _get_parser_for_file(input_path)
    raw_schema = parser.parse(input_path)
    canonical_project = raw_to_canonical(raw_schema)

    if persona:
        from src.core.personas.projector import PersonaProjector
        from src.core.personas.renderers import (
            MarkdownPersonaRenderer,
            JsonPersonaRenderer,
            MermaidPersonaRenderer,
        )

        projector = PersonaProjector(canonical_project)
        projection = projector.project_lens(persona)

        fmt = format.lower()
        if fmt == "json":
            console.print_json(JsonPersonaRenderer.render_projection(projection))
        elif fmt in ("md", "markdown"):
            console.print(MarkdownPersonaRenderer.render(projection))
        elif fmt == "mermaid":
            console.print(MermaidPersonaRenderer.render_erd_subgraph(projection))
        else:
            # Human Console Output
            console.print(
                Panel.fit(
                    f"[bold cyan]{projection.title}[/bold cyan]\n"
                    f"[dim]Persona Role:[/dim] [yellow]{projection.role.value}[/yellow] | [dim]Technical Depth:[/dim] [green]{projection.technical_depth.value}[/green]\n\n"
                    f"[white]{projection.summary}[/white]",
                    title="[bold magenta]Persona Lens Projection[/bold magenta]",
                    box=box.ROUNDED,
                )
            )
            if projection.certified_metrics:
                console.print(f"[bold green]Certified KPIs:[/bold green] {', '.join(projection.certified_metrics)}")
            console.print(f"[bold cyan]Primary Entities ({len(projection.primary_entities)}):[/bold cyan] {', '.join(projection.primary_entities)}")
            if projection.recommendations:
                rec_table = Table(title="Actionable Recommendations", box=box.SIMPLE, header_style="bold cyan")
                rec_table.add_column("ID", style="bold")
                rec_table.add_column("Prioridad", justify="center")
                rec_table.add_column("Título")
                rec_table.add_column("Impacto", style="dim")
                for r in projection.recommendations:
                    rec_table.add_row(r.id, r.priority.value, r.title, r.impact)
                console.print(rec_table)
    else:
        explainer = SemanticExplainer(canonical_project)
        if format.lower() == "json":
            console.print_json(json.dumps(explainer.to_dict()))
        else:
            explainer.explain_entity_roles()


personas_app = typer.Typer(
    name="personas",
    help="Gestión, inspección y exportación de Persona Lenses organizacionales.",
)
app.add_typer(personas_app, name="personas")


@personas_app.command("list")
def personas_list():
    """
    Lista las 10 Persona Lenses estándar registradas y sus aliases organizacionales.
    """
    from src.core.personas.registry import PersonaRegistry

    registry = PersonaRegistry.create_default()
    table = Table(
        title="Persona Lenses Registradas (SemanticFlow Enterprise)",
        box=box.ROUNDED,
        header_style="bold magenta",
    )
    table.add_column("Persona ID", style="bold cyan")
    table.add_column("Nombre / Rol", style="bold")
    table.add_column("Nivel Técnico", justify="center")
    table.add_column("Aliases Soportados", style="dim")

    for defn in registry.list_definitions():
        aliases_str = ", ".join(defn.aliases) if defn.aliases else "-"
        table.add_row(
            defn.persona_id,
            defn.display_name,
            defn.technical_depth.value,
            aliases_str,
        )

    console.print(table)


@personas_app.command("export")
def personas_export(
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
        Path("output/personas"),
        "--output",
        "-o",
        help="Directorio de destino para las 10 Lenses y el Leadership Cockpit.",
    ),
    formats: str = typer.Option(
        "md,json",
        "--formats",
        "-f",
        help="Formatos a exportar separados por coma (ej. 'md,json').",
    ),
):
    """
    Exporta las 10 Persona Lenses individuales y el Data Leadership Cockpit en Markdown y JSON.
    """
    from src.core.mappers.raw_to_canonical import raw_to_canonical
    from src.core.personas.cockpit import DataLeadershipCockpitEngine

    parser = _get_parser_for_file(input_path)
    raw_schema = parser.parse(input_path)
    canonical_project = raw_to_canonical(raw_schema)

    format_list = [fmt.strip().lower() for fmt in formats.split(",")]
    engine = DataLeadershipCockpitEngine(canonical_project)
    res = engine.export_all(output_dir, include_individual_lenses=True, formats=format_list)

    console.print(
        Panel(
            f"[bold green]Exportación de Persona Lenses completada exitosamente![/bold green]\n\n"
            f"- Data Leadership Cockpit: [bold white]{res.get('cockpit_markdown', res.get('cockpit_json', output_dir))}[/bold white]\n"
            f"- Lentes Individuales: [bold cyan]{len([k for k in res if k.startswith('lens_')])}[/bold cyan] archivos generados en [bold]{output_dir}/lenses[/bold]",
            title="[bold cyan]Exportación de Personas & Cockpit[/bold cyan]",
            box=box.ROUNDED,
        )
    )


@app.command()
def cockpit(
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
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Directorio opcional para exportar el Cockpit en Markdown/JSON.",
    ),
    format: str = typer.Option(
        "human",
        "--format",
        "-f",
        help="Formato de salida: 'human' (consola), 'json', o 'md'.",
    ),
):
    """
    Sintetiza y visualiza el C-Level Data Leadership Cockpit para el proyecto semántico.
    """
    from src.core.mappers.raw_to_canonical import raw_to_canonical
    from src.core.personas.cockpit import DataLeadershipCockpitEngine
    from src.core.personas.renderers import LeadershipCockpitRenderer, JsonPersonaRenderer

    parser = _get_parser_for_file(input_path)
    raw_schema = parser.parse(input_path)
    canonical_project = raw_to_canonical(raw_schema)

    engine = DataLeadershipCockpitEngine(canonical_project)
    cockpit_model = engine.generate_cockpit()

    if output_dir:
        res = engine.export_all(output_dir, include_individual_lenses=False, formats=["md", "json"])
        console.print(f"[bold green][OK][/bold green] Cockpit exportado a: {res.get('cockpit_markdown')}")

    fmt = format.lower()
    if fmt == "json":
        console.print_json(JsonPersonaRenderer.render_cockpit(cockpit_model))
    elif fmt in ("md", "markdown"):
        console.print(LeadershipCockpitRenderer.render_markdown(cockpit_model))
    else:
        # Human Console Display
        console.print(
            Panel.fit(
                f"[bold cyan]Data Leadership Cockpit: {cockpit_model.project_name}[/bold cyan]\n"
                f"[dim]Versión:[/dim] {cockpit_model.project_version} | [dim]Generado:[/dim] {cockpit_model.generated_at}\n\n"
                f"[white]{cockpit_model.executive_summary}[/white]",
                title="[bold magenta]C-Level Leadership Cockpit[/bold magenta]",
                box=box.ROUNDED,
            )
        )

        radar_table = Table(title="Radar de Madurez por Dominio", box=box.SIMPLE, header_style="bold green")
        radar_table.add_column("Persona / Dominio", style="bold")
        radar_table.add_column("Puntuación de Madurez", justify="right")
        radar_table.add_column("Banda de Estado", justify="center")

        for role_name, score in cockpit_model.maturity_radar.items():
            color = "green" if score >= 80 else ("yellow" if score >= 65 else "red")
            band = "Óptimo" if score >= 80 else ("Satisfactorio" if score >= 65 else "Atención Requerida")
            radar_table.add_row(role_name, f"[{color}]{score:.1f}%[/{color}]", f"[{color}]{band}[/{color}]")

        console.print(radar_table)


@app.command()
def validate(
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
    min_score: float = typer.Option(
        70.0,
        "--min-score",
        "-s",
        help="Puntuación mínima de calidad requerida para pasar la validación (0-100).",
    ),
):
    """
    Evalúa el Semantic Quality Score (cQS) y valida el modelo contra reglas de gobierno y calidad.
    """
    from src.core.mappers.raw_to_canonical import raw_to_canonical
    from src.core.quality.scorer import SemanticQualityScorer

    parser = _get_parser_for_file(input_path)
    raw_schema = parser.parse(input_path)
    canonical_project = raw_to_canonical(raw_schema)

    scorer = SemanticQualityScorer(canonical_project)
    result = scorer.evaluate()

    score_color = "green" if result.score >= min_score else "red"
    console.print(
        Panel.fit(
            f"[bold]Semantic Quality Score (cQS):[/bold] [{score_color}]{result.score:.1f} / {result.max_score:.1f}[/{score_color}]\n"
            f"[dim]Errores Bloqueantes:[/dim] [red]{result.blocking_errors}[/red] | "
            f"[dim]Advertencias:[/dim] [yellow]{result.warnings}[/yellow]",
            title="[bold cyan]Calificación de Calidad Semántica[/bold cyan]",
            box=box.ROUNDED,
        )
    )

    if result.diagnostics:
        diag_table = Table(
            title="Diagnósticos de Calidad y Gobierno",
            box=box.SIMPLE,
            header_style="bold yellow",
        )
        diag_table.add_column("Código", style="bold")
        diag_table.add_column("Severidad", justify="center")
        diag_table.add_column("Mensaje")
        diag_table.add_column("Acción Sugerida", style="dim")

        for d in result.diagnostics:
            sev_color = "red" if d.severity == "ERROR" else "yellow"
            diag_table.add_row(
                d.code,
                f"[{sev_color}]{d.severity.value}[/{sev_color}]",
                d.message,
                d.suggested_action or "N/A",
            )
        console.print(diag_table)

    if result.score < min_score or result.blocking_errors > 0:
        console.print(
            f"\n[bold red][FAIL][/bold red] La compilación no cumple con la calidad mínima requerida ({min_score})."
        )
        raise typer.Exit(code=1)
    else:
        console.print("\n[bold green][PASS][/bold green] Validación de calidad exitosa.")


@app.command()
def docgen(
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
        Path("output/docs"),
        "--output",
        "-o",
        help="Directorio donde se guardará el Data Dictionary y el Diagrama ERD.",
    ),
):
    """
    Genera documentación enterprise automáticamente (Diccionario de Datos Markdown y Diagrama ERD Mermaid).
    """
    from src.core.mappers.raw_to_canonical import raw_to_canonical
    from src.core.docs.emitter import DocumentationEmitter

    parser = _get_parser_for_file(input_path)
    raw_schema = parser.parse(input_path)
    canonical_project = raw_to_canonical(raw_schema)

    emitter = DocumentationEmitter(canonical_project)
    res = emitter.export_all(str(output_dir))

    console.print(
        Panel(
            f"[bold green]Documentación generada exitosamente![/bold green]\n\n"
            f"- Diccionario de Datos: [bold white]{res['dictionary']}[/bold white]\n"
            f"- Diagrama ERD (Mermaid): [bold white]{res['erd']}[/bold white]",
            title="[bold cyan]Documentación Enterprise[/bold cyan]",
            box=box.ROUNDED,
        )
    )


if __name__ == "__main__":

    app()
