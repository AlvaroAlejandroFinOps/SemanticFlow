"""
Integration tests for Macro-Stage IV (Target Adapters, Persona Views & Documentation Emitters).
"""
from pathlib import Path

import pytest

from src.core.docs.emitter import DocumentationEmitter
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.personas.views import PersonaType, PersonaViewGenerator
from src.core.targets.powerbi.adapter import PowerBiTargetAdapter


@pytest.fixture
def sample_canonical_project():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    parser = MarkdownSchemaParser()
    raw_schema = parser.parse(schema_path)
    return raw_to_canonical(raw_schema)


def test_powerbi_target_adapter(sample_canonical_project, tmp_path):
    adapter = PowerBiTargetAdapter()
    assert adapter.target_name == "powerbi"

    output_dir = tmp_path / "pbi_export"
    res = adapter.export(sample_canonical_project, str(output_dir))

    assert res["target"] == "powerbi"
    assert res["status"] == "SUCCESS"
    assert res["entities_count"] == len(sample_canonical_project.entities)
    assert Path(res["output_dir"]).exists()


def test_persona_view_generator(sample_canonical_project):
    views = PersonaViewGenerator.generate_views(sample_canonical_project)

    assert PersonaType.EXECUTIVE in views
    assert PersonaType.DATA_GOVERNANCE in views
    assert PersonaType.BI_ENGINEER in views

    exec_view = views[PersonaType.EXECUTIVE]
    assert exec_view.persona == PersonaType.EXECUTIVE
    assert len(exec_view.primary_entities) > 0


def test_documentation_emitter(sample_canonical_project, tmp_path):
    emitter = DocumentationEmitter(sample_canonical_project)

    md_dict = emitter.generate_markdown_dictionary()
    assert "# Data Dictionary:" in md_dict
    assert "| Entity | Role | Attributes Count |" in md_dict

    mermaid_erd = emitter.generate_mermaid_erd()
    assert "erDiagram" in mermaid_erd
    assert "-->" in mermaid_erd or "||--o{" in mermaid_erd

    doc_paths = emitter.export_all(str(tmp_path / "docs"))
    assert Path(doc_paths["dictionary"]).exists()
    assert Path(doc_paths["erd"]).exists()
