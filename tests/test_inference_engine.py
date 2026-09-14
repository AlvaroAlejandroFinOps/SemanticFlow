from pathlib import Path
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.engine.compiler import SemanticCompiler
from src.core.ast.semantic import TableRole, CrossFilteringBehavior


def test_semantic_compiler_metro_santiago():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(schema_path)

    compiler = SemanticCompiler()
    semantic_model = compiler.compile(raw_schema)

    # 1. Validar tablas y roles
    assert len(semantic_model.tables) == 20
    dim_tables = [t for t in semantic_model.tables if t.role == TableRole.DIMENSION]
    fact_tables = [t for t in semantic_model.tables if t.role == TableRole.FACT]
    assert len(dim_tables) == 10
    assert len(fact_tables) == 10

    # 2. Validar gobernanza en Fact_Validacion: FKs ocultas
    fact_val = semantic_model.get_table("Fact_Validacion")
    assert fact_val is not None
    col_sk_estacion = fact_val.get_column("SK_Estacion")
    assert col_sk_estacion is not None
    assert col_sk_estacion.is_hidden is True, "SK_Estacion en Fact debe estar oculta"

    col_fecha_sk = fact_val.get_column("Fecha_SK")
    assert col_fecha_sk is not None
    assert col_fecha_sk.is_hidden is True, "Fecha_SK en Fact debe estar oculta"

    # 3. Validar medidas DAX automáticas
    measure_names = [m.name for m in fact_val.measures]
    assert "# Registros Validacion" in measure_names
    assert "Total Tarifa Cobrada CLP" in measure_names

    # 4. Validar relaciones 1:N y prevención de caminos ambiguos (is_active)
    assert len(semantic_model.relationships) >= 20
    active_rels = [r for r in semantic_model.relationships if r.is_active]
    inactive_rels = [r for r in semantic_model.relationships if not r.is_active]

    for rel in semantic_model.relationships:
        assert rel.cross_filtering_behavior == CrossFilteringBehavior.ONE_DIRECTION

    # Debe haber al menos una relación inactiva para romper el ciclo ambiguo Dim_Equipamiento -> Dim_Estacion / Dim_Tren_Coche -> Dim_Linea
    assert len(active_rels) > 0
    assert len(inactive_rels) >= 1

