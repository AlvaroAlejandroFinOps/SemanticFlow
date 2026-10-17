"""
Tests for Strict Determinism (Zero-Diff Invariant) in TMDL, PBIP, and dbt emission,
plus D-011 (Direct Lake) and D-012 (VertiPaq) Quality Gate regression.
"""
import hashlib
from pathlib import Path
import random
import pytest

from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    DataType,
    EntityRole,
    ProjectGovernance,
    SemanticAttribute,
    SemanticEntity,
    SemanticMetric,
    SemanticRelationship as CanonicalRelationship,
)
from src.core.ast.schema import ColumnRaw, RelationshipRaw, RelationalSchemaRaw, TableRaw
from src.core.ast.semantic import (
    CrossFilteringBehavior,
    PbiDataType,
    SemanticColumn,
    SemanticMeasure,
    SemanticModel,
    SemanticRelationship,
    SemanticTable,
    TableRole,
)
from src.core.emitter.dbt_emitter import DbtSemanticEmitter
from src.core.emitter.pbip_writer import PbipWriter
from src.core.engine.relationship_resolver import RelationshipResolver
from src.core.quality.rules import (
    validate_direct_lake_compatibility,
    validate_vertipaq_performance,
)
from src.core.quality.scorer import SemanticQualityScorer


def _hash_file(path: Path) -> str:
    """Calcula el hash SHA-256 exacto de un archivo."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_directory_files(dir_path: Path) -> dict[str, str]:
    """Calcula el hash SHA-256 de todos los archivos en un directorio relativo."""
    result = {}
    for p in sorted(dir_path.rglob("*")):
        if p.is_file():
            rel_name = p.relative_to(dir_path).as_posix()
            result[rel_name] = _hash_file(p)
    return result


def _build_test_model(shuffle_order: bool = False, seed: int = 42) -> SemanticModel:
    """Construye un SemanticModel de prueba con múltiples tablas, columnas y medidas."""
    cols_a = [
        SemanticColumn(name="SK_Cliente", data_type=PbiDataType.INT64, is_hidden=True),
        SemanticColumn(name="Nombre", data_type=PbiDataType.STRING),
        SemanticColumn(name="Email", data_type=PbiDataType.STRING),
        SemanticColumn(name="Ciudad", data_type=PbiDataType.STRING),
    ]
    cols_b = [
        SemanticColumn(name="SK_Venta", data_type=PbiDataType.INT64, is_hidden=True),
        SemanticColumn(name="SK_Cliente", data_type=PbiDataType.INT64),
        SemanticColumn(name="Monto", data_type=PbiDataType.DECIMAL),
        SemanticColumn(name="Cantidad", data_type=PbiDataType.INT64),
    ]
    measures_b = [
        SemanticMeasure(name="Total Ventas", expression="SUM('Fact_Ventas'[Monto])"),
        SemanticMeasure(name="# Transacciones", expression="COUNTROWS('Fact_Ventas')"),
        SemanticMeasure(name="Ticket Promedio", expression="DIVIDE([Total Ventas], [# Transacciones])"),
    ]

    if shuffle_order:
        rng = random.Random(seed)
        rng.shuffle(cols_a)
        rng.shuffle(cols_b)
        rng.shuffle(measures_b)

    tables = [
        SemanticTable(name="Dim_Cliente", role=TableRole.DIMENSION, columns=cols_a),
        SemanticTable(name="Fact_Ventas", role=TableRole.FACT, columns=cols_b, measures=measures_b),
    ]

    relationships = [
        SemanticRelationship(
            name="AutoRel_Fact_Ventas_SK_Cliente_Dim_Cliente_SK_Cliente",
            from_table="Fact_Ventas",
            from_column="SK_Cliente",
            to_table="Dim_Cliente",
            to_column="SK_Cliente",
            cross_filtering_behavior=CrossFilteringBehavior.ONE_DIRECTION,
            is_active=True,
        )
    ]

    if shuffle_order:
        rng.shuffle(tables)

    return SemanticModel(
        name="ZeroDiffModel",
        tables=tables,
        relationships=relationships,
        culture="es-CL",
    )


# ==============================================================================
# 1. Determinismo en Emisión TMDL / PBIP (Zero-Diff Invariant)
# ==============================================================================

def test_tmdl_deterministic_output(tmp_path: Path):
    """
    Verifica que dos compilaciones consecutivas sobre el mismo modelo con elementos
    agregados en orden desordenado generan paquetes con hashes SHA-256 100% idénticos.
    """
    writer = PbipWriter()

    # Compilación 1: Orden estándar
    model_1 = _build_test_model(shuffle_order=False)
    out_1 = tmp_path / "run_1"
    writer.write_bundle(model_1, out_1)
    hashes_1 = _hash_directory_files(out_1)

    # Compilación 2: Mismo modelo pero con orden interno barajado
    model_2 = _build_test_model(shuffle_order=True, seed=99)
    out_2 = tmp_path / "run_2"
    writer.write_bundle(model_2, out_2)
    hashes_2 = _hash_directory_files(out_2)

    assert hashes_1 == hashes_2, (
        f"Se detectó divergencia no determinista (Diff Noise):\n"
        f"Run 1: {hashes_1}\nRun 2: {hashes_2}"
    )


def test_relationship_activity_is_order_independent():
    """
    Verifica que la resolución de relaciones activas/inactivas (V-8)
    no dependa del orden en que las relaciones vienen declaradas en el esquema bruto.
    """
    t1 = TableRaw(name="Dim_A", columns=[ColumnRaw(name="id", raw_type="int", pbi_type=PbiDataType.INT64)])
    t2 = TableRaw(name="Fact_B", columns=[ColumnRaw(name="a_id", raw_type="int", pbi_type=PbiDataType.INT64)])
    tables = [t1, t2]
    table_roles = {"Dim_A": TableRole.DIMENSION, "Fact_B": TableRole.FACT}

    r1 = RelationshipRaw(from_table="Fact_B", from_column="a_id", to_table="Dim_A", to_column="id")
    r2 = RelationshipRaw(from_table="Dim_A", from_column="id", to_table="Fact_B", to_column="a_id")

    schema_order_1 = RelationalSchemaRaw(name="Order1", tables=tables, relationships=[r1, r2])
    schema_order_2 = RelationalSchemaRaw(name="Order2", tables=tables, relationships=[r2, r1])

    resolver = RelationshipResolver()
    res_1 = resolver.resolve_relationships(schema_order_1, table_roles)
    res_2 = resolver.resolve_relationships(schema_order_2, table_roles)

    assert len(res_1) == len(res_2)
    assert [r.name for r in res_1] == [r.name for r in res_2]
    assert [r.is_active for r in res_1] == [r.is_active for r in res_2]


def test_dbt_output_deterministic():
    """Verifica que la especificación dbt semantic layer sea determinista ante desorden de entidades."""
    ent_1 = SemanticEntity(
        id="ent_b",
        name="Fact_Ventas",
        role=EntityRole.FACT,
        attributes=[
            SemanticAttribute(id="a2", name="Monto", data_type=DataType.DECIMAL),
            SemanticAttribute(id="a1", name="ID", is_key=True, data_type=DataType.INT64),
        ],
        metrics=[
            SemanticMetric(id="m2", name="Ticket_Promedio", expression="1"),
            SemanticMetric(id="m1", name="Total_Ventas", expression="1"),
        ],
    )
    ent_2 = SemanticEntity(
        id="ent_a",
        name="Dim_Cliente",
        role=EntityRole.DIMENSION,
        attributes=[
            SemanticAttribute(id="a3", name="Nombre", data_type=DataType.STRING),
            SemanticAttribute(id="a0", name="SK_Cliente", is_key=True, data_type=DataType.INT64),
        ],
    )

    proj_1 = CanonicalSemanticProject(id="p1", name="Proj", entities=[ent_1, ent_2])
    proj_2 = CanonicalSemanticProject(id="p2", name="Proj", entities=[ent_2, ent_1])

    emitter_1 = DbtSemanticEmitter(proj_1)
    emitter_2 = DbtSemanticEmitter(proj_2)

    assert emitter_1.to_yaml() == emitter_2.to_yaml()


# ==============================================================================
# 2. Quality Gate Rules D-011 y D-012 Tests
# ==============================================================================

def test_direct_lake_quality_rule_penalizes_nn_and_datetime():
    """
    Verifica que la regla D-011 penalice relaciones N:N activas (-15)
    y atributos DATETIME sin particionar (-10) en Microsoft Fabric Direct Lake.
    """
    project = CanonicalSemanticProject(
        id="dl_proj",
        name="DirectLakeProject",
        governance=ProjectGovernance(
            owner="Data Architecture Lead",
            custom_properties={
                "direct_lake_rules": True,
                "storage_mode": "DirectLake"
            }
        ),
        entities=[
            SemanticEntity(
                id="f_tickets",
                name="Fact_Tickets",
                role=EntityRole.FACT,
                grain=["id"],
                attributes=[
                    SemanticAttribute(id="a1", name="id", is_key=True, data_type=DataType.INT64),
                    SemanticAttribute(id="a2", name="FechaHoraIngreso", data_type=DataType.DATETIME),
                ],
            ),
            SemanticEntity(
                id="d_usuarios",
                name="Dim_Usuarios",
                role=EntityRole.DIMENSION,
                grain=["id"],
                attributes=[
                    SemanticAttribute(id="u1", name="id", is_key=True, data_type=DataType.INT64),
                ],
            ),
        ],
        relationships=[
            CanonicalRelationship(
                id="rel_nn",
                name="Rel_Fact_Dim_NN",
                from_entity_id="f_tickets",
                from_attribute_id="id",
                to_entity_id="d_usuarios",
                to_attribute_id="id",
                cardinality="N:N",
                is_active=True,
            )
        ]
    )

    diags = validate_direct_lake_compatibility(project)
    codes = {d.code for d in diags}
    assert "QUAL_DL_DATETIME_011" in codes
    assert "QUAL_DL_NN_011" in codes

    scorer = SemanticQualityScorer(project)
    result = scorer.evaluate()

    # Deducción esperada: N:N (-15) + DATETIME (-10) = -25 puntos
    assert result.score <= 75.0
    assert result.warnings >= 2


def test_vertipaq_quality_rule_detects_antipatterns():
    """
    Verifica que la regla D-012 detecte FILTER(ALL()) sobre tablas grandes
    y filtrado bidireccional sobre tablas de hechos.
    """
    project = CanonicalSemanticProject(
        id="vpaq_proj",
        name="VertiPaqProject",
        governance=ProjectGovernance(owner="FinOps Lead"),
        entities=[
            SemanticEntity(
                id="f_ventas",
                name="Fact_Ventas",
                role=EntityRole.FACT,
                grain=["id"],
                estimated_rows=5_000_000,  # 5 Millones > 1M
                attributes=[
                    SemanticAttribute(id="v1", name="id", is_key=True, data_type=DataType.INT64),
                ],
                metrics=[
                    SemanticMetric(
                        id="m1",
                        name="Ventas_Totales_Mercado",
                        expression="CALCULATE(SUM('Fact_Ventas'[id]), FILTER(ALL('Fact_Ventas'), [id] > 0))",
                    )
                ],
            ),
            SemanticEntity(
                id="d_tienda",
                name="Dim_Tienda",
                role=EntityRole.DIMENSION,
                grain=["id"],
                attributes=[
                    SemanticAttribute(id="t1", name="id", is_key=True, data_type=DataType.INT64),
                ],
            ),
        ],
        relationships=[
            CanonicalRelationship(
                id="rel_bidir",
                name="Rel_Bidir_Fact",
                from_entity_id="f_ventas",
                from_attribute_id="id",
                to_entity_id="d_tienda",
                to_attribute_id="id",
                is_active=True,
                cross_filtering="bothDirections",
            )
        ],
    )

    diags = validate_vertipaq_performance(project)
    codes = {d.code for d in diags}
    assert "QUAL_VPAQ_FILTER_012" in codes
    assert "QUAL_VPAQ_BIDIR_012" in codes

    scorer = SemanticQualityScorer(project)
    result = scorer.evaluate()
    # Ambos antipatrones aplican deducción de 5 puntos
    assert result.score <= 90.0
