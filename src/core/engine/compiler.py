"""
Orquestador del motor de inferencia semántica: transforma RelationalSchemaRaw en SemanticModel.
"""
from src.core.ast.schema import RelationalSchemaRaw
from src.core.ast.semantic import (
    SemanticModel,
    SemanticTable,
    TableRole,
)
from src.core.engine.graph import RelationalGraph
from src.core.engine.role_inferer import RoleInferer
from src.core.engine.relationship_resolver import RelationshipResolver
from src.core.engine.governance import AttributeGovernance
from src.core.engine.dax_generator import DaxGenerator


class SemanticCompiler:
    """Compilador de alto nivel del modelo semántico."""

    def __init__(self):
        self.governance = AttributeGovernance()
        self.dax_generator = DaxGenerator()
        self.relationship_resolver = RelationshipResolver()

    def compile(
        self, raw_schema: RelationalSchemaRaw, culture: str = "es-CL"
    ) -> SemanticModel:
        # 1. Construir grafo y resolver roles
        graph = RelationalGraph(raw_schema)
        role_inferer = RoleInferer(graph)

        table_roles: dict[str, TableRole] = {}
        semantic_tables: list[SemanticTable] = []

        for table in raw_schema.tables:
            role = role_inferer.infer_role(table)
            table_roles[table.name] = role

            # 2. Aplicar gobernanza de columnas (ocultar FKs, summarizeBy, formatos)
            semantic_cols = self.governance.govern_columns(table, role)

            # 3. Generar medidas DAX base
            measures = self.dax_generator.generate_measures(table, role)

            semantic_tables.append(
                SemanticTable(
                    name=table.name,
                    role=role,
                    description=table.description,
                    columns=semantic_cols,
                    measures=measures,
                )
            )

        # 4. Resolver relaciones 1:N
        relationships = self.relationship_resolver.resolve_relationships(
            raw_schema, table_roles
        )

        return SemanticModel(
            name=raw_schema.name,
            compatibility_level=1567,
            culture=culture,
            tables=semantic_tables,
            relationships=relationships,
            description=raw_schema.description,
        )
