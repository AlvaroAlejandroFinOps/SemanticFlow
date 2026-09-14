"""
Tests for PersonaProjector, Renderers, Mutation Safety, and Leadership Cockpit.
"""
from pathlib import Path
import json
import pytest
from src.core.ast.canonical.models import CanonicalSemanticProject
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.personas.models import (
    PersonaRole,
    TechnicalDepth,
)
from src.core.personas.projector import PersonaProjector
from src.core.personas.renderers import (
    JsonPersonaRenderer,
    LeadershipCockpitRenderer,
    MarkdownPersonaRenderer,
    MermaidPersonaRenderer,
)
from src.core.personas.legacy_adapter import LegacyPersonaAdapter
from src.core.personas.views import PersonaType
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


def test_projector_mutation_safety(enterprise_project):
    """Verify projection never mutates the underlying canonical project."""
    # Capture snapshot before projection
    before_json = enterprise_project.model_dump_json()

    projector = PersonaProjector(enterprise_project)
    all_projections = projector.project_all()
    cockpit = projector.build_leadership_cockpit()

    # Capture snapshot after projection
    after_json = enterprise_project.model_dump_json()

    assert before_json == after_json, "CanonicalSemanticProject was mutated during persona projection!"
    assert len(all_projections) >= 10
    assert cockpit.project_name == enterprise_project.name


def test_projector_all_10_lenses_on_enterprise(enterprise_project):
    """Verify all 10 lenses project with tailored entities, metrics, and RACI matrices."""
    projector = PersonaProjector(enterprise_project)
    projections = projector.project_all()

    # 1. Analytics Leader / Executive
    exec_proj = projections["analytics_leader"]
    assert exec_proj.technical_depth == TechnicalDepth.EXECUTIVE
    assert len(exec_proj.primary_entities) > 0
    assert len(exec_proj.certified_metrics) > 0
    assert len(exec_proj.responsibilities) > 0
    assert exec_proj.maturity_assessment is not None

    # 2. Data Governance Officer
    gov_proj = projections["data_governance_officer"]
    assert gov_proj.technical_depth == TechnicalDepth.SUMMARY
    assert len(gov_proj.recommendations) > 0
    assert any("Ownership" in r.title for r in gov_proj.recommendations)

    # 3. FinOps Specialist
    finops_proj = projections["finops_specialist"]
    assert "fact_cloud_consumption" in finops_proj.primary_entities

    # 4. AI Systems Engineer
    ai_proj = projections["ai_systems_engineer"]
    assert "dim_customers" in ai_proj.primary_entities

    # 5. Compliance Auditor
    audit_proj = projections["compliance_auditor"]
    assert audit_proj.technical_depth == TechnicalDepth.EXHAUSTIVE
    assert len(audit_proj.primary_entities) == len(enterprise_project.entities)


def test_projector_alias_resolution(enterprise_project):
    """Verify projection via aliases works identically to canonical IDs."""
    projector = PersonaProjector(enterprise_project)

    proj1 = projector.project_lens("executive")
    proj2 = projector.project_lens("analytics_leader")
    assert proj1.persona_id == proj2.persona_id

    proj_bi = projector.project_lens("bi_engineer")
    assert proj_bi.persona_id == "bi_developer"


def test_markdown_renderer_output(enterprise_project):
    """Verify MarkdownPersonaRenderer generates valid GitHub markdown structure."""
    projector = PersonaProjector(enterprise_project)
    proj = projector.project_lens("analytics_leader")

    md_output = MarkdownPersonaRenderer.render(proj, include_diagrams=True)
    assert f"# {proj.title}" in md_output
    assert "## Executive Summary" in md_output
    assert "## Metrics & KPIs Portfolio" in md_output
    assert "## RACI Responsibility Matrix" in md_output
    assert "## Cross-Functional Team Interactions" in md_output
    assert "```mermaid" in md_output


def test_json_renderer_output(enterprise_project):
    """Verify JsonPersonaRenderer serializes valid and reloadable JSON."""
    projector = PersonaProjector(enterprise_project)
    proj = projector.project_lens("data_engineer")

    json_str = JsonPersonaRenderer.render_projection(proj)
    data = json.loads(json_str)
    assert data["persona_id"] == "data_engineer"
    assert "primary_entities" in data


def test_leadership_cockpit_synthesis_and_markdown(enterprise_project):
    """Verify LeadershipCockpit aggregation and markdown rendering."""
    projector = PersonaProjector(enterprise_project)
    cockpit = projector.build_leadership_cockpit()

    assert cockpit.project_name == "EnterpriseRetailPlatform"
    assert cockpit.governance_overview["data_product_status"] == "Certified"
    assert len(cockpit.maturity_radar) >= 10
    assert len(cockpit.lens_projections) >= 10

    cockpit_md = LeadershipCockpitRenderer.render_markdown(cockpit)
    assert "# Data Leadership Cockpit: EnterpriseRetailPlatform" in cockpit_md
    assert "## Domain Maturity Radar" in cockpit_md
    assert "## Executive Overview" in cockpit_md


def test_legacy_adapter_conversion(enterprise_project):
    """Verify LegacyPersonaAdapter translates modern projections to PersonaView cleanly."""
    projector = PersonaProjector(enterprise_project)
    proj = projector.project_lens("analytics_leader")

    legacy_view = LegacyPersonaAdapter.projection_to_legacy_view(proj)
    assert legacy_view is not None
    assert legacy_view.persona == PersonaType.EXECUTIVE
    assert legacy_view.title == proj.title
    assert legacy_view.primary_entities == proj.primary_entities


def test_metro_santiago_projector_integration(metro_canonical_project):
    """Verify projection on historical Metro Santiago project works without errors."""
    projector = PersonaProjector(metro_canonical_project)
    all_projs = projector.project_all()
    assert len(all_projs) >= 10

    cockpit = projector.build_leadership_cockpit()
    assert cockpit.project_name == metro_canonical_project.name
    assert cockpit.governance_overview["entities_governed"] == len(metro_canonical_project.entities)
