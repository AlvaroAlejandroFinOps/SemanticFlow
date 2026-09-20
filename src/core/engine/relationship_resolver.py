"""
Resolución de relaciones analíticas 1:N unidireccionales para Power BI.
Evita caminos ambiguos (PFE_XL_USERELATIONSHIP_AMBIGUOUS_PATH) en el motor VertiPaq.
"""
import networkx as nx

from src.core.ast.schema import RelationalSchemaRaw
from src.core.ast.semantic import (
    CrossFilteringBehavior,
    SemanticRelationship,
    TableRole,
)


class RelationshipResolver:
    """Resuelve y valida relaciones 1:N unidireccionales para TMDL."""

    def resolve_relationships(
        self,
        raw_schema: RelationalSchemaRaw,
        table_roles: dict[str, TableRole],
    ) -> list[SemanticRelationship]:
        resolved: list[SemanticRelationship] = []
        seen_pairs: set[tuple[str, str, str, str]] = set()

        table_cols = {t.name: {c.name for c in t.columns} for t in raw_schema.tables}
        table_pks = {t.name: (t.primary_keys[0].name if t.primary_keys else None) for t in raw_schema.tables}

        # Grafo no dirigido para rastrear caminos activos y prevenir ciclos / caminos ambiguos en VertiPaq
        active_graph = nx.Graph()
        for t in raw_schema.tables:
            active_graph.add_node(t.name)

        for rel in raw_schema.relationships:
            from_t = rel.from_table
            from_c = rel.from_column
            to_t = rel.to_table
            to_c = rel.to_column

            # Validar existencia de tablas
            if from_t not in table_cols or to_t not in table_cols:
                continue

            # Validar/reparar to_column si no existe en la tabla de destino
            if to_c not in table_cols[to_t]:
                if from_c in table_cols[to_t]:
                    to_c = from_c
                else:
                    target_pk = table_pks.get(to_t)
                    if target_pk is not None and target_pk in table_cols[to_t]:
                        to_c = target_pk
                    else:
                        continue

            # Validar from_column
            if from_c not in table_cols[from_t]:
                continue

            # Asegurar orden canónico de Star Schema: From Fact (Many) -> To Dim (One)
            from_role = table_roles.get(from_t, TableRole.DIMENSION)
            to_role = table_roles.get(to_t, TableRole.DIMENSION)

            # Si está invertido (From Dim -> To Fact), invertir para que coincida con TMDL standard
            if from_role == TableRole.DIMENSION and to_role == TableRole.FACT:
                from_t, to_t = to_t, from_t
                from_c, to_c = to_c, from_c

            pair_key = (from_t.lower(), from_c.lower(), to_t.lower(), to_c.lower())
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)

            rel_name = f"AutoRel_{from_t}_{from_c}_{to_t}_{to_c}"

            # Evaluar si la relación debe ser activa o inactiva para evitar caminos ambiguos (PFE_XL_USERELATIONSHIP_AMBIGUOUS_PATH)
            is_active = True
            if nx.has_path(active_graph, from_t, to_t):
                is_active = False
            else:
                active_graph.add_edge(from_t, to_t)

            resolved.append(
                SemanticRelationship(
                    name=rel_name,
                    from_table=from_t,
                    from_column=from_c,
                    to_table=to_t,
                    to_column=to_c,
                    cross_filtering_behavior=CrossFilteringBehavior.ONE_DIRECTION,
                    is_active=is_active,
                    security_filtering_behavior="oneDirection",
                )
            )

        return resolved

