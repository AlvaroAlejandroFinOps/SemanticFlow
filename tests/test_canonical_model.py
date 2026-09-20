"""
Tests for Canonical Semantic Model, Mappers, and Explainer.
"""
from pathlib import Path

from src.core.ast.canonical.models import EntityRole
from src.core.engine.explainer import SemanticExplainer
from src.core.mappers.canonical_to_pbi import canonical_to_pbi
from src.core.mappers.raw_to_canonical import raw_to_canonical
from src.core.parsers.markdown_parser import MarkdownSchemaParser


def test_raw_to_canonical_mapping():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(schema_path)
    canonical = raw_to_canonical(raw_schema)

    assert canonical.name == "esquema_relacional"
    assert len(canonical.entities) == 20
    assert len(canonical.relationships) == 24

    dim_linea = canonical.get_entity("Dim_Linea")
    assert dim_linea is not None
    assert dim_linea.role == EntityRole.DIMENSION
    assert len(dim_linea.provenance) > 0
    assert dim_linea.provenance[0].rule_id == "RAW_INGESTION_001"


def test_canonical_to_pbi_conversion():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(schema_path)
    canonical = raw_to_canonical(raw_schema)
    pbi_model = canonical_to_pbi(canonical)

    assert pbi_model.name == canonical.name
    assert len(pbi_model.tables) == len(canonical.entities)
    assert len(pbi_model.relationships) == len(canonical.relationships)


def test_semantic_explainer():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(schema_path)
    canonical = raw_to_canonical(raw_schema)
    explainer = SemanticExplainer(canonical)

    expl_dict = explainer.to_dict()
    assert "entities" in expl_dict
    assert len(expl_dict["entities"]) == 20
