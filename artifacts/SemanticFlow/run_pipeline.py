#!/usr/bin/env python3
"""
Orquestador de Pipeline de SemanticFlow (SMaC Engine).
Ejecuta el ciclo de vida completo: Validación cQS -> Compilación PBIP/TMDL -> dbt MetricFlow -> DocGen -> Leadership Cockpit -> Lentes.
"""
import argparse
import sys
from pathlib import Path
import shutil

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import yaml
from src.core.ast.canonical.models import ProjectGovernance
from src.core.ast.semantic import TableRole
from src.core.emitter.pbip_writer import PbipWriter
from src.core.emitter.dbt_emitter import DbtSemanticEmitter
from src.core.engine.compiler import SemanticCompiler
from src.core.docs.emitter import DocumentationEmitter
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.parsers.yaml_parser import YamlSchemaParser
from src.core.personas.cockpit import DataLeadershipCockpitEngine
from src.core.quality.scorer import SemanticQualityScorer
from src.core.security.sanitize import sanitize_company_id, resolve_within, safe_filename, validate_culture_code
from src.core.security.secret_scanner import scan_file_for_secrets
from src.core.security.concurrency import acquire_company_lock

console = Console()

LENS_FOLDER_MAP = {
    "data_analyst": "01_data_analyst",
    "analytics_engineer": "02_analytics_engineer",
    "data_engineer": "03_data_engineer",
    "data_scientist": "04_data_scientist",
    "bi_developer": "05_bi_developer",
    "data_architect": "06_data_architect",
    "data_governance_officer": "07_data_governance_officer",
    "platform_engineer": "08_platform_engineer",
    "domain_owner": "09_domain_owner",
    "audit_risk": "10_audit_risk",
    "analytics_leader": "11_analytics_leader",
    "data_product_manager": "12_data_product_manager",
    "finops_specialist": "13_finops_specialist",
    "ai_systems_engineer": "14_ai_systems_engineer",
    "business_consumer": "15_business_consumer",
    "compliance_auditor": "16_compliance_auditor",
}


def get_parser_for_file(file_path: Path):
    ext = file_path.suffix.lower()
    if ext in (".yaml", ".yml", ".json"):
        return YamlSchemaParser()
    return MarkdownSchemaParser()


def run_pipeline(
    company_id: str,
    input_file: Path,
    base_output_dir: Path,
    min_score: float = 45.0,
    culture: str = "es-CL",
):
    company_id = sanitize_company_id(company_id)
    culture = validate_culture_code(culture)

    with acquire_company_lock(company_id, base_output_dir):
        _execute_pipeline_locked(
            company_id=company_id,
            input_file=input_file,
            base_output_dir=base_output_dir,
            min_score=min_score,
            culture=culture,
        )


def _execute_pipeline_locked(
    company_id: str,
    input_file: Path,
    base_output_dir: Path,
    min_score: float = 45.0,
    culture: str = "es-CL",
):

    console.print(
        Panel.fit(
            f"[bold cyan]SemanticFlow[/bold cyan] - Enterprise SMaC Orchestrator\n"
            f"[dim]Empresa / Proyecto:[/dim] [bold yellow]{company_id}[/bold yellow]\n"
            f"[dim]Esquema Fuente:[/dim] {input_file}\n"
            f"[dim]Directorio de Salida:[/dim] {base_output_dir}\n"
            f"[dim]Umbral de Calidad cQS:[/dim] {min_score} puntos | [dim]Cultura:[/dim] {culture}",
            box=box.ROUNDED,
            title="[bold green]Pipeline de Compilación Semántica[/bold green]",
        )
    )

    if not input_file.exists():
        console.print(f"[bold red][ERROR][/bold red] El archivo de esquema no existe: {input_file}")
        sys.exit(1)

    # 0. Escaneo de Seguridad y Fuga de Secretos
    secret_findings = scan_file_for_secrets(input_file)
    profile_path = input_file.parent / "company_profile.yaml"
    if not profile_path.exists():
        profile_path = input_file.parent / "company_profile.yml"
    if profile_path.exists():
        secret_findings.extend(scan_file_for_secrets(profile_path))

    if secret_findings:
        console.print(
            "\n[bold red][SECURITY ERROR][/bold red] Se detectó una posible credencial o secreto hardcodeado en los inputs."
        )
        for f in secret_findings:
            console.print(f"   [red]•[/red] {f.format_diagnostic()}")
        sys.exit(1)

    # 1. Parsing
    console.print("\n[bold cyan]1. Ingesta y Parsing de Esquema...[/bold cyan]")
    parser = get_parser_for_file(input_file)
    raw_schema = parser.parse(input_file)
    console.print(
        f"   [green][OK][/green] Ingestadas [bold]{len(raw_schema.tables)}[/bold] tablas y "
        f"[bold]{len(raw_schema.relationships)}[/bold] relaciones brutas."
    )

    # 2. Canonical Model & Quality Gate
    console.print("\n[bold cyan]2. Evaluación del Semantic Quality Gate (cQS)...[/bold cyan]")
    canonical_project = raw_to_canonical(raw_schema)

    # Enriquecer con Company Profile si existe en la carpeta de la empresa
    profile_path = input_file.parent / "company_profile.yaml"
    if not profile_path.exists():
        profile_path = input_file.parent / "company_profile.yml"

    if profile_path.exists():
        try:
            with open(profile_path, "r", encoding="utf-8") as pf:
                profile_data = yaml.safe_load(pf) or {}
            gov_data = profile_data.get("semantic_governance", {})
            compliance_list = [
                f.get("code") or f.get("name")
                for f in profile_data.get("regulatory_and_compliance", {}).get("frameworks", [])
                if isinstance(f, dict)
            ]
            bus_units = [u.get("name") for u in profile_data.get("business_units", []) if isinstance(u, dict)]
            
            project_gov = ProjectGovernance(
                domain_id=profile_data.get("company_id", company_id),
                domain_name=gov_data.get("data_domain", profile_data.get("industry", "Enterprise")),
                classification=gov_data.get("confidentiality_tier", "Internal"),
                data_product_status="Certified",
                owner=gov_data.get("owner", profile_data.get("company_name")),
                steward=gov_data.get("steward"),
                criticality="High",
                compliance_frameworks=compliance_list,
                tags=[profile_data.get("industry", "Enterprise"), profile_data.get("country", "Chile")] + bus_units,
                custom_properties={
                    "company_name": profile_data.get("company_name"),
                    "website": profile_data.get("website"),
                    "industry": profile_data.get("industry"),
                    "sub_industry": profile_data.get("sub_industry"),
                    "technology_ecosystem": profile_data.get("technology_ecosystem", {}),
                    "direct_lake_rules": gov_data.get("direct_lake_rules", []),
                    "key_performance_indicators": profile_data.get("key_performance_indicators", {}),
                    "business_units": profile_data.get("business_units", []),
                    "strategic_objectives": profile_data.get("strategic_objectives", []),
                },
            )
            canonical_project.governance = project_gov
            if profile_data.get("overview", {}).get("summary"):
                canonical_project.description = profile_data["overview"]["summary"].strip()
            console.print(
                f"   [green][OK][/green] Perfil de empresa integrado: [bold]{profile_data.get('company_name', company_id)}[/bold] "
                f"([cyan]{len(compliance_list)}[/cyan] marcos normativos, [cyan]{len(bus_units)}[/cyan] unidades de negocio)"
            )
        except Exception as e:
            console.print(f"   [yellow][WARN][/yellow] No se pudo cargar company_profile.yaml: {e}")

    scorer = SemanticQualityScorer(canonical_project)
    quality_result = scorer.evaluate()

    score_color = "green" if quality_result.score >= min_score else "red"
    console.print(
        f"   Puntaje cQS obtenido: [{score_color}][bold]{quality_result.score:.1f}[/bold] / {quality_result.max_score:.1f}[/{score_color}] "
        f"(Errores bloqueantes: [red]{quality_result.blocking_errors}[/red], Advertencias: [yellow]{quality_result.warnings}[/yellow])"
    )

    if quality_result.score < min_score or quality_result.blocking_errors > 0:
        console.print(
            f"\n[bold red][FALLO QUALITY GATE][/bold red] El modelo no cumple con el estándar mínimo requerido ({min_score}). Compilación detenida."
        )
        if quality_result.diagnostics:
            diag_table = Table(title="Diagnósticos de Bloqueo", box=box.SIMPLE, header_style="bold red")
            diag_table.add_column("Código", style="bold")
            diag_table.add_column("Mensaje")
            diag_table.add_column("Acción Sugerida")
            for d in quality_result.diagnostics:
                if d.severity == "ERROR":
                    diag_table.add_row(d.code, d.message, d.suggested_action or "Revisar relaciones")
            console.print(diag_table)
        sys.exit(1)

    console.print("   [green][OK][/green] Quality Gate aprobado exitosamente.")

    # 3. Compile Power BI TMDL/PBIP
    console.print("\n[bold cyan]3. Compilación a Microsoft Power BI (TMDL/PBIP)...[/bold cyan]")
    compiler = SemanticCompiler()
    semantic_model = compiler.compile(raw_schema, culture=culture)
    pbip_output_dir = base_output_dir / "pbip" / company_id
    writer = PbipWriter()
    pbip_file = writer.write_bundle(semantic_model, pbip_output_dir)
    console.print(f"   [green][OK][/green] Proyecto PBIP generado en: [bold]{pbip_file}[/bold]")

    # 4. Export dbt MetricFlow
    console.print("\n[bold cyan]4. Compilación a dbt Semantic Layer (MetricFlow)...[/bold cyan]")
    dbt_file = base_output_dir / "dbt" / company_id / "semantic_models.yml"
    dbt_file.parent.mkdir(parents=True, exist_ok=True)
    dbt_emitter = DbtSemanticEmitter(canonical_project)
    dbt_emitter.write_to_file(str(dbt_file))
    console.print(f"   [green][OK][/green] Especificación dbt YAML generada en: [bold]{dbt_file}[/bold]")

    # 5. Generate Enterprise Documentation
    console.print("\n[bold cyan]5. Generación de Documentación Técnica y Diagrama ERD...[/bold cyan]")
    docs_dir = base_output_dir / "docs" / company_id
    docs_dir.mkdir(parents=True, exist_ok=True)
    doc_emitter = DocumentationEmitter(canonical_project)
    doc_res = doc_emitter.export_all(str(docs_dir))
    console.print(f"   [green][OK][/green] Diccionario de Datos: [bold]{doc_res['dictionary']}[/bold]")
    console.print(f"   [green][OK][/green] Diagrama ERD (Mermaid): [bold]{doc_res['erd']}[/bold]")

    # 6. Generate Leadership Cockpit & Individual Lenses
    console.print("\n[bold cyan]6. Síntesis del Data Leadership Cockpit & Persona Lenses...[/bold cyan]")
    from src.core.personas.registry import PersonaRegistry
    registry = PersonaRegistry.create_default()
    company_lenses_dir = input_file.parent / "lenses"
    if company_lenses_dir.exists():
        custom_lenses = registry.load_company_lenses(company_lenses_dir, company_id=company_id)
        if custom_lenses:
            console.print(f"   [green][OK][/green] [bold]{len(custom_lenses)}[/bold] lentes personalizadas cargadas para [yellow]{company_id}[/yellow].")

    cockpit_dir = base_output_dir / "leadership_cockpit" / company_id
    cockpit_dir.mkdir(parents=True, exist_ok=True)
    cockpit_engine = DataLeadershipCockpitEngine(canonical_project, registry=registry)
    cockpit_res = cockpit_engine.export_all(cockpit_dir, include_individual_lenses=True, formats=["md", "json"])
    console.print(f"   [green][OK][/green] Cockpit C-Level generado en: [bold]{cockpit_res.get('cockpit_markdown')}[/bold]")

    # Distribute lenses to dedicated folders under outputs/lenses/
    lenses_base_dir = base_output_dir / "lenses"
    lenses_source_dir = cockpit_dir / "lenses"
    if lenses_source_dir.exists():
        distributed_count = 0
        for pid, folder_name in LENS_FOLDER_MAP.items():
            target_lens_dir = lenses_base_dir / folder_name / company_id
            target_lens_dir.mkdir(parents=True, exist_ok=True)
            
            src_md = lenses_source_dir / f"{pid}_lens.md"
            src_json = lenses_source_dir / f"{pid}_lens.json"
            
            if src_md.exists():
                shutil.copy2(src_md, target_lens_dir / f"{company_id}_projection.md")
            if src_json.exists():
                shutil.copy2(src_json, target_lens_dir / f"{company_id}_projection.json")
            distributed_count += 1

        for custom_lens_file in sorted(lenses_source_dir.glob("*.md"), key=lambda p: p.name.lower()):
            lens_stem = custom_lens_file.stem
            if lens_stem.endswith("_lens"):
                clean_pid = safe_filename(lens_stem[:-5])
                if clean_pid not in LENS_FOLDER_MAP:
                    target_custom_dir = lenses_base_dir / clean_pid / company_id
                    target_custom_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(custom_lens_file, target_custom_dir / f"{company_id}_projection.md")
                    custom_json = lenses_source_dir / f"{clean_pid}_lens.json"
                    if custom_json.exists():
                        shutil.copy2(custom_json, target_custom_dir / f"{company_id}_projection.json")
                    distributed_count += 1

        console.print(f"   [green][OK][/green] Proyecciones distribuidas a [bold]{distributed_count}[/bold] carpetas especializadas en [bold]{lenses_base_dir}[/bold].")

    console.print(
        Panel(
            f"[bold green]PIPELINE COMPLETADO EXITOSAMENTE[/bold green]\n\n"
            f"[bold white]Resumen de Artefactos Exportados:[/bold white]\n"
            f"- [cyan]Power BI PBIP/TMDL:[/cyan] {pbip_file}\n"
            f"- [cyan]dbt MetricFlow:[/cyan] {dbt_file}\n"
            f"- [cyan]Documentación & ERD:[/cyan] {docs_dir}\n"
            f"- [cyan]Leadership Cockpit:[/cyan] {cockpit_dir}\n"
            f"- [cyan]Lentes Organizacionales:[/cyan] {lenses_base_dir}\n\n"
            f"[dim]Los resultados están listos para ser abiertos o sincronizados en producción.[/dim]",
            title="[bold green]SemanticFlow Final Result[/bold green]",
            box=box.DOUBLE,
        )
    )


def main():
    parser = argparse.ArgumentParser(description="SemanticFlow Enterprise SMaC Orchestrator")
    parser.add_argument(
        "--company",
        "-c",
        type=str,
        default="metro_santiago",
        help="Identificador de la empresa (busca en inputs/companies/<company>/schema.md por defecto)",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        default=None,
        help="Ruta explícita al archivo de esquema (anula la ruta por defecto de --company)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directorio base para los outputs generados",
    )
    parser.add_argument(
        "--min-score",
        "-s",
        type=float,
        default=45.0,
        help="Puntuación mínima cQS para aprobar el Quality Gate (default: 45.0)",
    )
    parser.add_argument(
        "--culture",
        type=str,
        default="es-CL",
        help="Código de cultura para Power BI (default: es-CL)",
    )
    parser.add_argument(
        "--allow-external-input",
        action="store_true",
        default=False,
        help="Permite especificar archivos de entrada fuera del directorio del repositorio",
    )

    args = parser.parse_args()

    try:
        company_id = sanitize_company_id(args.company)
    except ValueError as e:
        console.print(f"[bold red][SECURITY ERROR][/bold red] {e}")
        sys.exit(1)

    base_inputs = (PROJECT_ROOT / "artifacts" / "SemanticFlow" / "inputs" / "companies").resolve()
    try:
        company_dir = resolve_within(base_inputs, base_inputs / company_id)
    except PermissionError as e:
        console.print(f"[bold red][SECURITY ERROR][/bold red] {e}")
        sys.exit(1)

    if args.input:
        input_file = args.input.resolve()
        if not args.allow_external_input:
            try:
                input_file = resolve_within(PROJECT_ROOT, input_file)
            except PermissionError as e:
                console.print(
                    f"[bold red][SECURITY ERROR][/bold red] {e} "
                    "Use --allow-external-input si desea permitir rutas externas explícitamente."
                )
                sys.exit(1)
    else:
        if (company_dir / "schema.md").exists():
            input_file = company_dir / "schema.md"
        else:
            candidates = list(company_dir.glob("*.md")) + list(company_dir.glob("*.yaml")) + list(company_dir.glob("*.yml"))
            candidates = [
                c for c in candidates
                if "profile" not in c.name.lower() and "readme" not in c.name.lower()
            ]
            if candidates:
                input_file = candidates[0]
            else:
                input_file = company_dir / "schema.md"

    try:
        run_pipeline(
            company_id=company_id,
            input_file=input_file,
            base_output_dir=args.output,
            min_score=args.min_score,
            culture=args.culture,
        )
    except (ValueError, PermissionError, RuntimeError, TimeoutError) as e:
        console.print(f"[bold red][SECURITY/CONCURRENCY ERROR][/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

