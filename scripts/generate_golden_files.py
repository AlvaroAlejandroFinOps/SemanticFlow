"""
Script to generate deterministic golden files for regression testing.
"""
import re
from pathlib import Path

from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.personas.cockpit import DataLeadershipCockpitEngine
from tests.fixtures.enterprise_fixture import create_enterprise_project


def normalize_content(content: str) -> str:
    """Replaces dynamic ISO timestamps with a fixed deterministic timestamp string."""
    # Matches ISO 8601 timestamps like 2026-09-14T20:38:01.302728+00:00 or similar
    normalized = re.sub(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?",
        "2026-09-14T17:00:00Z",
        content,
    )
    return normalized


def generate_golden():
    golden_root = Path("tests/golden")
    golden_root.mkdir(parents=True, exist_ok=True)

    # 1. Metro Santiago Project
    metro_schema = Path("docs/architecture/esquema_relacional.md")
    parser = MarkdownSchemaParser()
    raw_metro = parser.parse(metro_schema)
    metro_proj = raw_to_canonical(raw_metro)

    metro_out = golden_root / "metro_santiago"
    engine_metro = DataLeadershipCockpitEngine(metro_proj)
    engine_metro.export_all(metro_out, include_individual_lenses=True, formats=["md", "json"])

    # Normalize timestamps in all generated files in metro_santiago
    for fpath in metro_out.rglob("*.*"):
        if fpath.is_file():
            text = fpath.read_text(encoding="utf-8")
            fpath.write_text(normalize_content(text), encoding="utf-8")

    # 2. Enterprise Retail Project
    ent_proj = create_enterprise_project()
    ent_out = golden_root / "enterprise"
    engine_ent = DataLeadershipCockpitEngine(ent_proj)
    engine_ent.export_all(ent_out, include_individual_lenses=True, formats=["md", "json"])

    # Normalize timestamps in all generated files in enterprise
    for fpath in ent_out.rglob("*.*"):
        if fpath.is_file():
            text = fpath.read_text(encoding="utf-8")
            fpath.write_text(normalize_content(text), encoding="utf-8")

    print(f"Golden files successfully generated in {golden_root.resolve()}")


if __name__ == "__main__":
    generate_golden()
