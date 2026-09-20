"""
Tests for CLI commands: explain --persona, personas list, personas export, and cockpit.
"""
import json

from typer.testing import CliRunner

from src.cli import app

runner = CliRunner()
SCHEMA_PATH = "docs/architecture/esquema_relacional.md"


def test_cli_personas_list():
    """Verify 'semanticflow personas list' outputs registered personas table."""
    result = runner.invoke(app, ["personas", "list"])
    assert result.exit_code == 0
    assert "Analytics Leader" in result.stdout
    assert "Data Governance" in result.stdout
    assert "BI Developer" in result.stdout
    assert "FinOps" in result.stdout
    assert "ai_systems" in result.stdout


def test_cli_explain_persona_human():
    """Verify 'semanticflow explain -i <schema> -p executive' prints human report."""
    result = runner.invoke(app, ["explain", "-i", SCHEMA_PATH, "-p", "executive"])
    assert result.exit_code == 0
    assert "Analytics Leader" in result.stdout or "Executive" in result.stdout
    assert "Primary Entities" in result.stdout


def test_cli_explain_persona_json():
    """Verify 'semanticflow explain -i <schema> -p data_governance -f json' returns valid JSON."""
    result = runner.invoke(app, ["explain", "-i", SCHEMA_PATH, "-p", "data_governance", "-f", "json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["persona_id"] == "data_governance_officer"
    assert "primary_entities" in data


def test_cli_explain_persona_markdown():
    """Verify 'semanticflow explain -i <schema> -p bi_engineer -f md' returns Markdown."""
    result = runner.invoke(app, ["explain", "-i", SCHEMA_PATH, "-p", "bi_engineer", "-f", "md"])
    assert result.exit_code == 0
    assert "# BI Developer" in result.stdout
    assert "## Executive Summary" in result.stdout


def test_cli_explain_persona_mermaid():
    """Verify 'semanticflow explain -i <schema> -p finops -f mermaid' returns Mermaid ERD."""
    result = runner.invoke(app, ["explain", "-i", SCHEMA_PATH, "-p", "finops", "-f", "mermaid"])
    assert result.exit_code == 0
    assert "erDiagram" in result.stdout


def test_cli_personas_export(tmp_path):
    """Verify 'semanticflow personas export' exports all 10 lenses and cockpit."""
    out_dir = tmp_path / "cli_personas_out"
    result = runner.invoke(app, ["personas", "export", "-i", SCHEMA_PATH, "-o", str(out_dir)])
    assert result.exit_code == 0
    assert (out_dir / "data_leadership_cockpit.md").exists()
    assert (out_dir / "data_leadership_cockpit.json").exists()
    assert (out_dir / "lenses").exists()
    lenses = list((out_dir / "lenses").glob("*.md"))
    assert len(lenses) >= 10


def test_cli_cockpit_command(tmp_path):
    """Verify 'semanticflow cockpit' generates executive telemetry and exports."""
    # Test human console output
    res_human = runner.invoke(app, ["cockpit", "-i", SCHEMA_PATH])
    assert res_human.exit_code == 0
    assert "Leadership Cockpit" in res_human.stdout
    assert "Radar de Madurez" in res_human.stdout

    # Test export option
    out_dir = tmp_path / "cli_cockpit_out"
    res_export = runner.invoke(app, ["cockpit", "-i", SCHEMA_PATH, "-o", str(out_dir)])
    assert res_export.exit_code == 0
    assert (out_dir / "data_leadership_cockpit.md").exists()
