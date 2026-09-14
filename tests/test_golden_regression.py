"""
Regression tests verifying compiler output against deterministic golden files.
"""
from pathlib import Path
import re
import pytest
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.personas.cockpit import DataLeadershipCockpitEngine
from tests.fixtures.enterprise_fixture import create_enterprise_project


def normalize_content(content: str) -> str:
    """Replaces dynamic ISO timestamps with a fixed deterministic timestamp string."""
    return re.sub(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?",
        "2026-09-14T17:00:00Z",
        content,
    )


def test_golden_regression_metro_santiago(tmp_path):
    """Verify Metro Santiago cockpit and lenses match golden master files."""
    schema_path = Path("docs/architecture/esquema_relacional.md")
    parser = MarkdownSchemaParser()
    raw_metro = parser.parse(schema_path)
    metro_proj = raw_to_canonical(raw_metro)

    engine = DataLeadershipCockpitEngine(metro_proj)
    generated = engine.export_all(tmp_path, include_individual_lenses=True, formats=["md", "json"])

    golden_dir = Path("tests/golden/metro_santiago")
    assert golden_dir.exists(), "Metro Santiago golden directory missing"

    # Compare Cockpit Markdown
    gen_cockpit_md = normalize_content((tmp_path / "data_leadership_cockpit.md").read_text(encoding="utf-8"))
    gold_cockpit_md = (golden_dir / "data_leadership_cockpit.md").read_text(encoding="utf-8")
    assert gen_cockpit_md == gold_cockpit_md

    # Compare Cockpit JSON
    gen_cockpit_json = normalize_content((tmp_path / "data_leadership_cockpit.json").read_text(encoding="utf-8"))
    gold_cockpit_json = (golden_dir / "data_leadership_cockpit.json").read_text(encoding="utf-8")
    assert gen_cockpit_json == gold_cockpit_json

    # Compare 10 Individual Lens Markdown Files
    for lens_gold_file in (golden_dir / "lenses").glob("*.md"):
        gen_file = tmp_path / "lenses" / lens_gold_file.name
        assert gen_file.exists(), f"Generated file {gen_file.name} missing"
        gen_text = normalize_content(gen_file.read_text(encoding="utf-8"))
        gold_text = lens_gold_file.read_text(encoding="utf-8")
        assert gen_text == gold_text, f"Drift detected in golden file {lens_gold_file.name}"


def test_golden_regression_enterprise(tmp_path):
    """Verify Enterprise Retail Platform cockpit and lenses match golden master files."""
    ent_proj = create_enterprise_project()
    engine = DataLeadershipCockpitEngine(ent_proj)
    engine.export_all(tmp_path, include_individual_lenses=True, formats=["md", "json"])

    golden_dir = Path("tests/golden/enterprise")
    assert golden_dir.exists(), "Enterprise golden directory missing"

    # Compare Cockpit Markdown
    gen_cockpit_md = normalize_content((tmp_path / "data_leadership_cockpit.md").read_text(encoding="utf-8"))
    gold_cockpit_md = (golden_dir / "data_leadership_cockpit.md").read_text(encoding="utf-8")
    assert gen_cockpit_md == gold_cockpit_md

    # Compare 10 Individual Lens Markdown Files
    for lens_gold_file in (golden_dir / "lenses").glob("*.md"):
        gen_file = tmp_path / "lenses" / lens_gold_file.name
        assert gen_file.exists(), f"Generated file {gen_file.name} missing"
        gen_text = normalize_content(gen_file.read_text(encoding="utf-8"))
        gold_text = lens_gold_file.read_text(encoding="utf-8")
        assert gen_text == gold_text, f"Drift detected in golden file {lens_gold_file.name}"
