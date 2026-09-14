"""
Deep unit tests for each of the 10 concrete Persona Lenses.
"""
import pytest
from src.core.personas.lenses import (
    AiSystemsEngineerLens,
    AnalyticsEngineerLens,
    AnalyticsLeaderLens,
    BiDeveloperLens,
    BusinessConsumerLens,
    ComplianceAuditorLens,
    DataEngineerLens,
    DataGovernanceOfficerLens,
    DataProductManagerLens,
    FinOpsSpecialistLens,
)
from src.core.personas.models import (
    PersonaRole,
    RaciRole,
    TechnicalDepth,
)
from tests.fixtures.enterprise_fixture import create_enterprise_project


@pytest.fixture
def enterprise_project():
    return create_enterprise_project()


def test_analytics_leader_lens(enterprise_project):
    lens = AnalyticsLeaderLens()
    assert lens.role == PersonaRole.ANALYTICS_LEADER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.EXECUTIVE
    assert len(proj.certified_metrics) > 0
    assert len(proj.responsibilities) == 1
    assert proj.responsibilities[0].role == RaciRole.ACCOUNTABLE
    assert proj.maturity_assessment.overall_score >= 80.0


def test_data_engineer_lens(enterprise_project):
    lens = DataEngineerLens()
    assert lens.role == PersonaRole.DATA_ENGINEER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.TECHNICAL
    assert "fact_orders" in proj.primary_entities
    assert "dim_customers" in proj.primary_entities
    assert proj.responsibilities[0].role == RaciRole.RESPONSIBLE


def test_analytics_engineer_lens(enterprise_project):
    lens = AnalyticsEngineerLens()
    assert lens.role == PersonaRole.ANALYTICS_ENGINEER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.TECHNICAL
    assert len(proj.primary_entities) == len(enterprise_project.entities)
    assert len(proj.active_relationships) == 3


def test_bi_developer_lens(enterprise_project):
    lens = BiDeveloperLens()
    assert lens.role == PersonaRole.BI_DEVELOPER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.TECHNICAL
    assert len(proj.certified_metrics) > 0
    assert any(i.target_persona == PersonaRole.BUSINESS_CONSUMER for i in proj.interactions)


def test_data_governance_officer_lens(enterprise_project):
    lens = DataGovernanceOfficerLens()
    assert lens.role == PersonaRole.DATA_GOVERNANCE_OFFICER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.SUMMARY
    assert proj.metadata["pii_attributes_count"] >= 2
    assert any("PII" in r.title for r in proj.recommendations)


def test_data_product_manager_lens(enterprise_project):
    lens = DataProductManagerLens()
    assert lens.role == PersonaRole.DATA_PRODUCT_MANAGER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.SUMMARY
    assert proj.metadata["data_product_status"] == "Certified"
    assert any(i.target_persona == PersonaRole.BUSINESS_CONSUMER for i in proj.interactions)


def test_finops_specialist_lens(enterprise_project):
    lens = FinOpsSpecialistLens()
    assert lens.role == PersonaRole.FINOPS_SPECIALIST
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.SUMMARY
    assert "fact_cloud_consumption" in proj.primary_entities
    assert any(i.target_persona == PersonaRole.DATA_ENGINEER for i in proj.interactions)


def test_ai_systems_engineer_lens(enterprise_project):
    lens = AiSystemsEngineerLens()
    assert lens.role == PersonaRole.AI_SYSTEMS_ENGINEER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.TECHNICAL
    assert "dim_customers" in proj.primary_entities
    assert proj.metadata["ai_features_count"] >= 1


def test_business_consumer_lens(enterprise_project):
    lens = BusinessConsumerLens()
    assert lens.role == PersonaRole.BUSINESS_CONSUMER
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.EXECUTIVE
    assert len(proj.certified_metrics) > 0
    assert proj.responsibilities[0].role == RaciRole.INFORMED


def test_compliance_auditor_lens(enterprise_project):
    lens = ComplianceAuditorLens()
    assert lens.role == PersonaRole.COMPLIANCE_AUDITOR
    proj = lens.project(enterprise_project)
    assert proj.technical_depth == TechnicalDepth.EXHAUSTIVE
    assert len(proj.primary_entities) == len(enterprise_project.entities)
    assert "GDPR" in proj.metadata["compliance_frameworks"]
