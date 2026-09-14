"""
Tests for governance quality rules and PII classification checks.
"""
import pytest
from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    GovernanceMetadata,
    ProjectGovernance,
    SemanticAttribute,
    SemanticEntity,
    SemanticMetric,
)
from src.core.quality.scorer import SemanticQualityScorer
from src.core.quality.rules import (
    validate_certified_metrics,
    validate_pii_classification,
    validate_project_governance,
)
from tests.fixtures.enterprise_fixture import create_enterprise_project


@pytest.fixture
def enterprise_project():
    return create_enterprise_project()


def test_validate_project_governance_rule(enterprise_project):
    """Verify project governance rule passes when owner is present and flags when absent."""
    # Present
    diags = validate_project_governance(enterprise_project)
    assert len(diags) == 0

    # Absent
    project_no_gov = CanonicalSemanticProject(id="p1", name="NoGovProject")
    diags_absent = validate_project_governance(project_no_gov)
    assert len(diags_absent) == 1
    assert diags_absent[0].code == "GOV_PROJ_001"


def test_validate_pii_classification_rule():
    """Verify PII attributes without restricted or confidential sensitivity are flagged."""
    project = CanonicalSemanticProject(
        id="p2",
        name="PiiTestProject",
        entities=[
            SemanticEntity(
                id="e1",
                name="users",
                attributes=[
                    SemanticAttribute(
                        id="a1",
                        name="email",
                        governance=GovernanceMetadata(is_pii=True, sensitivity_classification="Public")
                    ),
                    SemanticAttribute(
                        id="a2",
                        name="credit_card",
                        governance=GovernanceMetadata(is_pii=True, sensitivity_classification="Restricted")
                    )
                ]
            )
        ]
    )

    diags = validate_pii_classification(project)
    assert len(diags) == 1
    assert diags[0].code == "GOV_PII_001"
    assert "users.email" in diags[0].message


def test_quality_scorer_with_governance_inheritance(enterprise_project):
    """Verify SemanticQualityScorer evaluates enterprise model with high quality score."""
    scorer = SemanticQualityScorer(enterprise_project)
    result = scorer.evaluate()

    assert result.score >= 85.0
    assert result.blocking_errors == 0
