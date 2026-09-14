"""
Mapper: RelationalSchemaRaw -> CanonicalSemanticProject
"""
from src.core.ast.schema import RelationalSchemaRaw, KeyType
from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    SemanticEntity,
    SemanticAttribute,
    SemanticRelationship,
    EntityRole,
    DataType,
    ProvenanceRecord,
)

RAW_TYPE_MAP = {
    "int64": DataType.INT64,
    "integer": DataType.INT64,
    "int": DataType.INT64,
    "bigint": DataType.INT64,
    "double": DataType.DOUBLE,
    "float": DataType.DOUBLE,
    "decimal": DataType.DECIMAL,
    "numeric": DataType.DECIMAL,
    "boolean": DataType.BOOLEAN,
    "bool": DataType.BOOLEAN,
    "datetime": DataType.DATETIME,
    "timestamp": DataType.DATETIME,
    "date": DataType.DATE,
    "string": DataType.STRING,
    "varchar": DataType.STRING,
    "text": DataType.STRING,
}


def map_raw_type_to_canonical(raw_type: str) -> DataType:
    clean_type = raw_type.lower().split("(")[0].strip()
    return RAW_TYPE_MAP.get(clean_type, DataType.STRING)


def raw_to_canonical(raw_schema: RelationalSchemaRaw) -> CanonicalSemanticProject:
    entities: list[SemanticEntity] = []

    for t in raw_schema.tables:
        role = EntityRole.DIMENSION
        if t.name.lower().startswith("fact_"):
            role = EntityRole.FACT
        elif t.name.lower().startswith("bridge_"):
            role = EntityRole.BRIDGE

        attributes: list[SemanticAttribute] = []
        for c in t.columns:
            attr = SemanticAttribute(
                id=f"{t.name}.{c.name}",
                name=c.name,
                display_name=c.name.replace("_", " ").title(),
                description=c.description,
                data_type=map_raw_type_to_canonical(c.raw_type),
                is_key=c.is_primary or c.is_foreign,
                is_hidden=c.is_foreign,
                source_column=c.name,
                provenance=[
                    ProvenanceRecord(
                        rule_id="RAW_INGESTION_001",
                        description="Mapped from Raw AST Column",
                        evidence={"raw_type": c.raw_type, "key_type": c.key_type.value},
                    )
                ],
            )
            attributes.append(attr)

        entity = SemanticEntity(
            id=t.name,
            name=t.name,
            role=role,
            description=t.description,
            attributes=attributes,
            provenance=[
                ProvenanceRecord(
                    rule_id="RAW_INGESTION_001",
                    description="Mapped from Raw AST Table",
                    evidence={"table_name": t.name},
                )
            ],
        )
        entities.append(entity)

    relationships = []
    for r in raw_schema.relationships:
        from_table = r.from_table
        from_col = r.from_column
        to_table = r.to_table
        to_col = r.to_column
        rel = SemanticRelationship(
            id=f"{from_table}.{from_col}->{to_table}.{to_col}",
            name=f"{from_table}_{from_col}_FK",
            from_entity_id=from_table,
            from_attribute_id=f"{from_table}.{from_col}",
            to_entity_id=to_table,
            to_attribute_id=f"{to_table}.{to_col}",
            cardinality="1:N",
            is_active=True,
            provenance=[
                ProvenanceRecord(
                    rule_id="RAW_RELATIONSHIP_001",
                    description="Mapped from Raw AST Relationship",
                    evidence={"from": from_table, "to": to_table},
                )
            ],
        )
        relationships.append(rel)

    return CanonicalSemanticProject(
        id=raw_schema.name,
        name=raw_schema.name,
        description=raw_schema.description,
        entities=entities,
        relationships=relationships,
    )
