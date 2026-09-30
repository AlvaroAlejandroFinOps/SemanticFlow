"""
Tests for dbt Semantic Layer emitter.
"""
from pathlib import Path
import yaml
import pytest

from src.core.emitter.dbt_emitter import DbtSemanticEmitter
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.parsers.markdown_parser import MarkdownSchemaParser


def test_dbt_semantic_emitter(tmp_path: Path):
    schema_path = Path("docs/architecture/esquema_relacional.md")
    assert schema_path.exists()

    parser = MarkdownSchemaParser()
    raw = parser.parse(schema_path)
    canonical = raw_to_canonical(raw)

    emitter = DbtSemanticEmitter(canonical)
    spec = emitter.generate_spec()

    assert spec["version"] == 2
    assert "semantic_models" in spec
    assert len(spec["semantic_models"]) == len(canonical.entities)

    first_model = spec["semantic_models"][0]
    assert "name" in first_model
    assert "entities" in first_model
    assert "dimensions" in first_model
    assert "measures" in first_model

    # Test file writing
    out_file = tmp_path / "semantic_models.yml"
    emitter.write_to_file(str(out_file))
    assert out_file.exists()

    # Verify YAML is valid
    parsed_yaml = yaml.safe_load(out_file.read_text(encoding="utf-8"))
    assert parsed_yaml["version"] == 2
    assert len(parsed_yaml["semantic_models"]) > 0
