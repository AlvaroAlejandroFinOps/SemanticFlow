"""
Tests for Macro-Stage III: Quality, Governance, and Capability Planner.
"""
from pathlib import Path

from src.core.ast.canonical.models import SemanticMetric
from src.core.capabilities.planner import CompatibilityStatus, TargetCapabilities, TargetCapabilityPlanner
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.quality.scorer import SemanticQualityScorer


def test_semantic_quality_scorer_evaluation():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(schema_path)
    canonical = raw_to_canonical(raw_schema)

    scorer = SemanticQualityScorer(canonical)
    result = scorer.evaluate()

    assert result.score >= 0.0
    assert result.max_score == 100.0
    assert len(result.diagnostics) > 0
    assert result.blocking_errors == 0
    assert result.warnings == 10  # 10 Fact entities without explicit grain


def test_certified_metric_gevernance_rule():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(schema_path)
    canonical = raw_to_canonical(raw_schema)

    # Add a certified metric without owner to test blocking error
    fact_entity = canonical.get_entity("Fact_Validacion")
    assert fact_entity is not None
    fact_entity.metrics.append(
        SemanticMetric(
            id="Fact_Validacion.Certified_Test",
            name="Certified_Test",
            expression="COUNTROWS('Fact_Validacion')",
            governance={"certification_status": "CERTIFIED", "owner": None},
        )
    )

    scorer = SemanticQualityScorer(canonical)
    result = scorer.evaluate()

    assert result.blocking_errors == 1
    assert any(d.code == "GOV_CERT_001" for d in result.diagnostics)


def test_target_capability_planner():
    score_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(score_path)
    canonical = raw_to_canonical(raw_schema)

    pbi_capabilities = TargetCapabilities(target_name="Power BI")
    planner = TargetCapabilityPlanner(pbi_capabilities)
    plan_reports = planner.plan(canonical)

    assert len(plan_reports) == len(canonical.entities) + len(canonical.relationships)
    assert all(r.status == CompatibilityStatus.SUPPORTED for r in plan_reports)
