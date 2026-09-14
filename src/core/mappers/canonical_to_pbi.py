"""
Mapper: CanonicalSemanticProject -> SemanticModel (Power BI AST)
Bridge for existing TMDL/PBIP emission pipeline.
"""
from src.core.ast.semantic import (
    SemanticModel,
    SemanticTable,
    SemanticColumn,
    SemanticRelationship,
    SemanticMeasure,
    TableRole,
    SummarizeBy,
)
from src.core.ast.types import PbiDataType
from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    EntityRole,
    DataType,
)

CANONICAL_TO_PBI_TYPE = {
    DataType.STRING: PbiDataType.STRING,
    DataType.INT64: PbiDataType.INT64,
    DataType.DOUBLE: PbiDataType.DOUBLE,
    DataType.DECIMAL: PbiDataType.DECIMAL,
    DataType.BOOLEAN: PbiDataType.BOOLEAN,
    DataType.DATETIME: PbiDataType.DATETIME,
    DataType.DATE: PbiDataType.DATETIME,
}

CANONICAL_TO_PBI_ROLE = {
    EntityRole.DIMENSION: TableRole.DIMENSION,
    EntityRole.FACT: TableRole.FACT,
    EntityRole.BRIDGE: TableRole.BRIDGE,
    EntityRole.CALCULATED: TableRole.CALCULATED,
}


class CanonicalToPbiMapper:
    @staticmethod
    def to_pbi_model(canonical_project: CanonicalSemanticProject, culture: str = "es-CL") -> SemanticModel:
        return canonical_to_pbi(canonical_project, culture)


def canonical_to_pbi(canonical_project: CanonicalSemanticProject, culture: str = "es-CL") -> SemanticModel:
    pbi_tables: list[SemanticTable] = []

    for entity in canonical_project.entities:
        columns: list[SemanticColumn] = []
        for attr in entity.attributes:
            pbi_col = SemanticColumn(
                name=attr.name,
                data_type=CANONICAL_TO_PBI_TYPE.get(attr.data_type, PbiDataType.STRING),
                is_hidden=attr.is_hidden,
                summarize_by=SummarizeBy.NONE,
                description=attr.description,
                source_column=attr.source_column or attr.name,
            )
            columns.append(pbi_col)

        measures: list[SemanticMeasure] = []
        for m in entity.metrics:
            pbi_m = SemanticMeasure(
                name=m.name,
                expression=m.expression,
                format_string=m.format_string,
                description=m.description,
                is_hidden=False,
            )
            measures.append(pbi_m)

        table = SemanticTable(
            name=entity.name,
            role=CANONICAL_TO_PBI_ROLE.get(entity.role, TableRole.DIMENSION),
            description=entity.description,
            columns=columns,
            measures=measures,
        )
        pbi_tables.append(table)

    pbi_relationships: list[SemanticRelationship] = []
    for r in canonical_project.relationships:
        pbi_rel = SemanticRelationship(
            name=r.name,
            from_table=r.from_entity_id,
            from_column=r.from_attribute_id.split(".")[-1],
            to_table=r.to_entity_id,
            to_column=r.to_attribute_id.split(".")[-1],
            is_active=r.is_active,
        )
        pbi_relationships.append(pbi_rel)

    return SemanticModel(
        name=canonical_project.name,
        compatibility_level=1567,
        culture=culture,
        tables=pbi_tables,
        relationships=pbi_relationships,
        description=canonical_project.description,
    )
