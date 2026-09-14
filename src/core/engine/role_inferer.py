"""
Inferencia de roles analíticos (DIMENSION, FACT, BRIDGE).
Combina detección explícita por prefijos con heurísticas topológicas.
"""
from src.core.ast.schema import TableRaw
from src.core.ast.semantic import TableRole
from src.core.engine.graph import RelationalGraph


class RoleInferer:
    """Clasifica las tablas del modelo en sus roles semánticos correspondientes."""

    def __init__(self, graph: RelationalGraph):
        self.graph = graph

    def infer_role(self, table: TableRaw) -> TableRole:
        name_lower = table.name.lower()

        # 1. Regla explícita por prefijo o sufijo convencional
        if name_lower.startswith("dim_") or name_lower.startswith("dim"):
            return TableRole.DIMENSION
        if name_lower.startswith("fact_") or name_lower.startswith("fact"):
            return TableRole.FACT
        if name_lower.startswith("bridge_") or name_lower.startswith("rel_"):
            return TableRole.BRIDGE

        # 2. Heurística topológica (si no tiene prefijos)
        out_degree = self.graph.get_out_degree(table.name)  # Cuántas FKs emite
        in_degree = self.graph.get_in_degree(table.name)    # Cuántas tablas apuntan a ella

        # Si tiene múltiples FKs hacia otras tablas y ninguna o pocas tablas la apuntan a ella
        if out_degree >= 2 and in_degree == 0:
            return TableRole.FACT
        # Si sólo tiene PK y es referenciada por otros
        if in_degree > 0 and out_degree <= 1:
            return TableRole.DIMENSION

        # Default analítico seguro
        return TableRole.DIMENSION
