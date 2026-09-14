"""
Tests for Persona Lens Framework contracts, ProjectGovernance, and interfaces.
"""
from pathlib import Path
import pytest
from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    GovernanceMetadata,
    ProjectGovernance,
    SemanticAttribute,
    SemanticEntity,
)
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.personas.models import (
    LeadershipCockpit,
    LensFocus,
    MaturityDimension,
    OverrideSafetyLevel,
    OverrideValidationResult,
    PersonaDefinition,
    PersonaMaturityAssessment,
    PersonaProjection,
    PersonaRecommendation,
    PersonaRole,
    RaciRole,
    RecommendationPriority,
    ResponsibilityAssignment,
    TeamInteraction,
    TechnicalDepth,
)
from src.core.personas.interfaces import PersonaLens
from tests.fixtures.enterprise_fixture import create_enterprise_project


@pytest.fixture
def metro_canonical_project() -> CanonicalSemanticProject:
    schema_path = Path("docs/architecture/esquema_relacional.md")
    parser = MarkdownSchemaParser()
    raw_schema = parser.parse(schema_path)
    return raw_to_canonical(raw_schema)


@pytest.fixture
def enterprise_project() -> CanonicalSemanticProject:
    return create_enterprise_project()


def test_project_governance_model_creation():
    """Verify ProjectGovernance instantiated with full enterprise metadata."""
    gov = ProjectGovernance(
        domain_id="DOM-001",
        domain_name="Finance & Risk",
        classification="Restricted",
        data_product_status="Certified",
        owner="Chief Risk Officer",
        steward="Risk Data Steward",
        criticality="High",
        sla="99.9% availability",
        tags=["risk", "basel-iii"],
        compliance_frameworks=["SOX", "GDPR"],
        custom_properties={"tier": 1}
    )
    assert gov.domain_id == "DOM-001"
    assert gov.classification == "Restricted"
    assert gov.data_product_status == "Certified"
    assert len(gov.compliance_frameworks) == 2


def test_project_governance_inheritance():
    """Verify that child entities and attributes inherit project governance defaults when unset."""
    project = CanonicalSemanticProject(
        id="proj_gov_test",
        name="GovTestProject",
        governance=ProjectGovernance(
            classification="Confidential",
            owner="Data Governance Council",
            steward="Lead Steward",
            tags=["inherited_tag"]
        ),
        entities=[
            SemanticEntity(
                id="ent_1",
                name="sample_entity",
                attributes=[
                    SemanticAttribute(id="a1", name="col1", governance=GovernanceMetadata(tags=["local_tag"])),
                    SemanticAttribute(id="a2", name="col2", governance=GovernanceMetadata(owner="Custom Owner"))
                ]
            )
        ]
    )

    # 1. Attribute col1 inherits owner, steward, classification, and merges tags
    col1 = project.entities[0].attributes[0]
    resolved_col1 = project.resolve_asset_governance(col1)
    assert resolved_col1.owner == "Data Governance Council"
    assert resolved_col1.steward == "Lead Steward"
    assert resolved_col1.sensitivity_classification == "Confidential"
    assert "local_tag" in resolved_col1.tags
    assert "inherited_tag" in resolved_col1.tags

    # 2. Attribute col2 overrides owner explicitly, but inherits steward and classification
    col2 = project.entities[0].attributes[1]
    resolved_col2 = project.resolve_asset_governance(col2)
    assert resolved_col2.owner == "Custom Owner"  # Explicit override preserved
    assert resolved_col2.steward == "Lead Steward"
    assert resolved_col2.sensitivity_classification == "Confidential"


def test_persona_definition_and_projection_contracts():
    """Verify PersonaDefinition and PersonaProjection instantiation and serialization."""
    definition = PersonaDefinition(
        persona_id="analytics_leader",
        role=PersonaRole.ANALYTICS_LEADER,
        display_name="Analytics Leader",
        title="Executive Strategic Analytics Perspective",
        summary_template="Executive overview for {project_name}",
        technical_depth=TechnicalDepth.EXECUTIVE,
        focus_areas=[LensFocus.STRATEGIC_ALIGNMENT, LensFocus.BUSINESS_VALUE],
        visible_object_types=["FACT", "KPI"],
        aliases=["executive", "cdo", "head_of_data"]
    )
    assert definition.role == PersonaRole.ANALYTICS_LEADER
    assert definition.technical_depth == TechnicalDepth.EXECUTIVE

    projection = PersonaProjection(
        persona_id="analytics_leader",
        role=PersonaRole.ANALYTICS_LEADER,
        title="Executive Summary View",
        summary="High-level business perspective",
        technical_depth=TechnicalDepth.EXECUTIVE,
        focus_areas=[LensFocus.STRATEGIC_ALIGNMENT],
        primary_entities=["fact_orders"],
        certified_metrics=["Total Revenue"],
        recommendations=[
            PersonaRecommendation(
                id="REC-001",
                title="Certify Dim Customer",
                description="Ensure customer dimension has verified owners",
                priority=RecommendationPriority.HIGH,
                impact="Improves audit compliance",
                effort="Low"
            )
        ],
        responsibilities=[
            ResponsibilityAssignment(
                task_or_artifact="Data Strategy Roadmap",
                role=RaciRole.ACCOUNTABLE,
                description="Approves cross-domain KPI definitions"
            )
        ],
        interactions=[
            TeamInteraction(
                target_persona=PersonaRole.DATA_PRODUCT_MANAGER,
                interaction_type="approval",
                frequency="Sprint",
                interface_artifact="Product KPI Roadmap"
            )
        ],
        maturity_assessment=PersonaMaturityAssessment(
            overall_score=85.0,
            maturity_level="Quantitatively Managed",
            dimensions=[
                MaturityDimension(dimension_name="Governance", score=90.0, level="Optimizing"),
                MaturityDimension(dimension_name="Modeling", score=80.0, level="Defined")
            ]
        )
    )

    assert len(projection.recommendations) == 1
    assert projection.responsibilities[0].role == RaciRole.ACCOUNTABLE
    assert projection.maturity_assessment.overall_score == 85.0

    # Test JSON serialization roundtrip
    json_str = projection.model_dump_json()
    reloaded = PersonaProjection.model_validate_json(json_str)
    assert reloaded.persona_id == projection.persona_id
    assert reloaded.maturity_assessment.overall_score == 85.0


def test_leadership_cockpit_contract():
    """Verify LeadershipCockpit model instantiation and telemetry aggregation."""
    cockpit = LeadershipCockpit(
        project_id="proj_enterprise",
        project_name="Enterprise Data Platform",
        generated_at="2026-09-14T17:00:00Z",
        executive_summary="Executive Cockpit for Enterprise Data Platform",
        governance_overview={"certified_kpi_count": 12, "compliance_rate_pct": 98.5},
        maturity_radar={"ANALYTICS_LEADER": 88.0, "DATA_GOVERNANCE_OFFICER": 92.0},
        cross_functional_alignment={"raci_coverage_pct": 100.0, "cross_persona_handoffs": 15},
        priority_action_matrix=[]
    )
    assert cockpit.project_name == "Enterprise Data Platform"
    assert cockpit.maturity_radar["DATA_GOVERNANCE_OFFICER"] == 92.0


class DummyConcreteLens(PersonaLens):
    """Concrete implementation of PersonaLens for contract testing."""
    @property
    def role(self) -> PersonaRole:
        return PersonaRole.ANALYTICS_LEADER

    @property
    def definition(self) -> PersonaDefinition:
        return PersonaDefinition(
            persona_id="analytics_leader",
            role=PersonaRole.ANALYTICS_LEADER,
            display_name="Analytics Leader",
            title="Executive Perspective",
            summary_template="Executive overview",
            technical_depth=TechnicalDepth.EXECUTIVE,
        )

    def project(self, project: CanonicalSemanticProject, config=None) -> PersonaProjection:
        return PersonaProjection(
            persona_id="analytics_leader",
            role=PersonaRole.ANALYTICS_LEADER,
            title=self.definition.title,
            summary="Executive lens projection",
            technical_depth=self.definition.technical_depth,
            primary_entities=[e.name for e in project.entities if e.role.value == "FACT"],
        )


def test_override_safety_classifier():
    """Verify classification of overrides as SAFE, REVIEW_REQUIRED, or PROHIBITED."""
    lens = DummyConcreteLens()

    # SAFE overrides
    res_safe = lens.validate_override("display_name", "Senior Analytics Leader")
    assert res_safe.safety_level == OverrideSafetyLevel.SAFE
    assert res_safe.is_allowed is True

    res_safe_alias = lens.validate_override("aliases", ["chief_analytics_officer"])
    assert res_safe_alias.safety_level == OverrideSafetyLevel.SAFE
    assert res_safe_alias.is_allowed is True

    # REVIEW_REQUIRED overrides
    res_review = lens.validate_override("technical_depth", TechnicalDepth.EXHAUSTIVE)
    assert res_review.safety_level == OverrideSafetyLevel.REVIEW_REQUIRED
    assert res_review.is_allowed is True

    res_review_vis = lens.validate_override("visible_object_types", ["ALL"])
    assert res_review_vis.safety_level == OverrideSafetyLevel.REVIEW_REQUIRED
    assert res_review_vis.is_allowed is True

    # PROHIBITED overrides
    res_prohib = lens.validate_override("persona_id", "hacked_id")
    assert res_prohib.safety_level == OverrideSafetyLevel.PROHIBITED
    assert res_prohib.is_allowed is False

    res_prohib_role = lens.validate_override("role", PersonaRole.DATA_ENGINEER)
    assert res_prohib_role.safety_level == OverrideSafetyLevel.PROHIBITED
    assert res_prohib_role.is_allowed is False


def test_enterprise_fixture_completeness(enterprise_project):
    """Verify enterprise fixture contains complete entities, relationships, and governance."""
    assert enterprise_project.name == "EnterpriseRetailPlatform"
    assert enterprise_project.governance is not None
    assert enterprise_project.governance.classification == "Confidential"
    assert len(enterprise_project.entities) == 5
    assert len(enterprise_project.relationships) == 3

    fact_orders = enterprise_project.get_entity("fact_orders")
    assert fact_orders is not None
    assert len(fact_orders.metrics) == 3

    dim_cust = enterprise_project.get_entity("dim_customers")
    assert dim_cust is not None
    pii_attrs = [a for a in dim_cust.attributes if a.governance.is_pii]
    assert len(pii_attrs) == 2


def test_metro_santiago_regression(metro_canonical_project):
    """Verify Metro Santiago project continues to load seamlessly without project governance."""
    assert metro_canonical_project.name is not None
    assert len(metro_canonical_project.entities) > 0
    # Metro Santiago initially has governance=None
    assert metro_canonical_project.governance is None
    # resolve_asset_governance should work safely with None
    entity = metro_canonical_project.entities[0]
    res_gov = metro_canonical_project.resolve_asset_governance(entity)
    assert res_gov is not None
