"""
Tests for DataLeadershipCockpitEngine and multi-format export capabilities.
"""
import json
from pathlib import Path

import pytest

from src.core.personas.cockpit import DataLeadershipCockpitEngine
from tests.fixtures.enterprise_fixture import create_enterprise_project


@pytest.fixture
def enterprise_project():
    return create_enterprise_project()


def test_cockpit_engine_generation(enterprise_project):
    """Verify DataLeadershipCockpitEngine synthesizes all domain telemetry."""
    engine = DataLeadershipCockpitEngine(enterprise_project)
    cockpit = engine.generate_cockpit()

    assert cockpit.project_name == "EnterpriseRetailPlatform"
    assert cockpit.governance_overview["data_product_status"] == "Certified"
    assert cockpit.governance_overview["classification"] == "Confidential"
    assert cockpit.governance_overview["entities_governed"] == 5

    # Check Radar
    assert len(cockpit.maturity_radar) >= 10
    for role_name, score in cockpit.maturity_radar.items():
        assert 0.0 <= score <= 100.0

    # Check alignment
    assert cockpit.cross_functional_alignment["registered_personas"] >= 10
    assert cockpit.cross_functional_alignment["total_responsibilities"] > 0


def test_cockpit_engine_export_all(enterprise_project, tmp_path):
    """Verify export_all writes cockpit and all 10 lenses in Markdown and JSON formats."""
    engine = DataLeadershipCockpitEngine(enterprise_project)
    output_dir = tmp_path / "cockpit_export"

    exported = engine.export_all(output_dir, include_individual_lenses=True, formats=["md", "json"])

    # Verify cockpit files
    assert "cockpit_markdown" in exported
    assert "cockpit_json" in exported
    assert Path(exported["cockpit_markdown"]).exists()
    assert Path(exported["cockpit_json"]).exists()

    # Verify Markdown content
    with open(exported["cockpit_markdown"], "r", encoding="utf-8") as f:
        md_text = f.read()
    assert "# Data Leadership Cockpit: EnterpriseRetailPlatform" in md_text
    assert "## Executive Overview" in md_text
    assert "## Domain Maturity Radar" in md_text

    # Verify JSON content
    with open(exported["cockpit_json"], "r", encoding="utf-8") as f:
        json_data = json.load(f)
    assert json_data["project_name"] == "EnterpriseRetailPlatform"
    assert "maturity_radar" in json_data

    # Verify individual lenses
    lenses_dir = output_dir / "lenses"
    assert lenses_dir.exists()
    lens_files = list(lenses_dir.glob("*.md"))
    assert len(lens_files) >= 10

    # Spot check one lens file
    leader_md = lenses_dir / "analytics_leader_lens.md"
    assert leader_md.exists()
    with open(leader_md, "r", encoding="utf-8") as f:
        leader_content = f.read()
    assert "ANALYTICS_LEADER" in leader_content
    assert "EXECUTIVE" in leader_content
    assert "Executive Strategic Analytics" in leader_content
