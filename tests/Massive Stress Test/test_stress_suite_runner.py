import time
from pathlib import Path
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.engine.compiler import SemanticCompiler
from src.core.emitter.pbip_writer import PbipWriter
from src.core.ast.semantic import TableRole


def test_massive_stress_suite_runner():
    base_schemas_path = Path("tests/Massive Stress Test/schemas")
    all_schema_files = sorted(list(base_schemas_path.rglob("*.md")))

    assert len(all_schema_files) == 12, f"Se esperaban 12 esquemas relacionales, se encontraron {len(all_schema_files)}"

    parser = MarkdownSchemaParser()
    compiler = SemanticCompiler()
    writer = PbipWriter()

    output_root = Path("Artefactos/Massive_Stress_PBIP")
    output_root.mkdir(parents=True, exist_ok=True)

    summary_metrics = []
    start_total_time = time.time()

    for schema_file in all_schema_files:
        t0 = time.time()
        raw_schema = parser.parse(schema_file)
        t_parse = time.time() - t0

        t1 = time.time()
        semantic_model = compiler.compile(raw_schema)
        t_compile = time.time() - t1

        tier_folder = schema_file.parent.name
        schema_out_dir = output_root / tier_folder / semantic_model.name

        t2 = time.time()
        pbip_file = writer.write_bundle(semantic_model, schema_out_dir)
        t_emit = time.time() - t2

        total_time = t_parse + t_compile + t_emit

        dim_count = sum(1 for t in semantic_model.tables if t.role == TableRole.DIMENSION)
        fact_count = sum(1 for t in semantic_model.tables if t.role == TableRole.FACT)
        total_tables = len(semantic_model.tables)
        total_rels = len(semantic_model.relationships)
        total_measures = sum(len(t.measures) for t in semantic_model.tables)

        summary_metrics.append(
            {
                "schema": semantic_model.name,
                "tier": tier_folder,
                "tables": total_tables,
                "dims": dim_count,
                "facts": fact_count,
                "rels": total_rels,
                "measures": total_measures,
                "time_ms": round(total_time * 1000, 2),
                "pbip_path": str(pbip_file),
            }
        )

        assert pbip_file.exists()
        assert (schema_out_dir / f"{semantic_model.name}.SemanticModel" / "definition" / "database.tmdl").exists()

    elapsed_total = time.time() - start_total_time

    # Reporte por consola
    print("\n" + "=" * 80)
    print("        MASSIVE STRESS TEST SUITE - BENCHMARK & SUMMARY REPORT        ")
    print("=" * 80)
    print(f"{'Esquema':<35} | {'Tables':<6} | {'Dims':<5} | {'Facts':<5} | {'Rels':<5} | {'DAX':<4} | {'Time (ms)':<9}")
    print("-" * 80)
    for m in summary_metrics:
        print(
            f"{m['schema']:<35} | {m['tables']:<6} | {m['dims']:<5} | {m['facts']:<5} | {m['rels']:<5} | {m['measures']:<4} | {m['time_ms']:<9}"
        )
    print("-" * 80)
    total_tables_sum = sum(m['tables'] for m in summary_metrics)
    total_rels_sum = sum(m['rels'] for m in summary_metrics)
    total_dax_sum = sum(m['measures'] for m in summary_metrics)
    print(
        f"TOTALES: 12 Esquemas | {total_tables_sum} Tablas | {total_rels_sum} Relaciones | {total_dax_sum} Medidas DAX | Tiempo Total: {elapsed_total:.2f}s"
    )
    print("=" * 80 + "\n")
