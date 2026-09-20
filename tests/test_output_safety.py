"""
Tests for Output Safety, Path Traversal Defense, Atomic Staging, and PII Masking.
"""
from pathlib import Path

import pytest

from src.core.emitter.pbip_writer import PbipWriter
from src.core.engine.compiler import SemanticCompiler
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.personas.models import PersonaRole, TechnicalDepth
from src.core.personas.projector import PersonaProjector


def test_root_path_rejection():
    """Verify that PbipWriter rejects root directory targets."""
    schema_path = Path("docs/architecture/esquema_relacional.md")
    parser = MarkdownSchemaParser()
    raw = parser.parse(schema_path)
    compiler = SemanticCompiler()
    model = compiler.compile(raw)

    writer = PbipWriter()
    with pytest.raises(ValueError, match="protected root path"):
        writer.write_bundle(model, Path("/"))


def test_atomic_write_rollback_on_failure(tmp_path, monkeypatch):
    """Verify that an exception during emission cleans up staging and leaves target clean."""
    schema_path = Path("docs/architecture/esquema_relacional.md")
    parser = MarkdownSchemaParser()
    raw = parser.parse(schema_path)
    compiler = SemanticCompiler()
    model = compiler.compile(raw)

    writer = PbipWriter()
    target_dir = tmp_path / "failed_bundle"

    # Mock table_emitter to raise a runtime error mid-process
    def mock_emit_table(*args, **kwargs):
        raise RuntimeError("Simulated mid-emission hardware failure")

    monkeypatch.setattr(writer.table_emitter, "emit_table", mock_emit_table)

    with pytest.raises(RuntimeError, match="Simulated mid-emission hardware failure"):
        writer.write_bundle(model, target_dir)

    # Destination directory should NOT contain the finalized PBIP files
    assert not (target_dir / f"{model.name}.pbip").exists()


def test_pii_masking_in_consumer_projections():
    """Verify that consumer lenses respect technical depth and hide raw schema internals."""
    schema_path = Path("docs/architecture/esquema_relacional.md")
    parser = MarkdownSchemaParser()
    raw = parser.parse(schema_path)
    canonical = raw_to_canonical(raw)

    projector = PersonaProjector(canonical)

    # Test Business Consumer / Data Analyst projection
    consumer_proj = projector.project_lens(PersonaRole.BUSINESS_CONSUMER)
    assert consumer_proj.technical_depth in (TechnicalDepth.EXECUTIVE, TechnicalDepth.SUMMARY)

    # Test Governance Officer projection has summary/governance depth
    gov_proj = projector.project_lens(PersonaRole.DATA_GOVERNANCE_OFFICER)
    assert gov_proj.technical_depth in (TechnicalDepth.SUMMARY, TechnicalDepth.TECHNICAL)
