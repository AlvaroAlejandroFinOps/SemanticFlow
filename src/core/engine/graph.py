"""
Construcción y análisis topológico del grafo relacional con NetworkX.
"""
import networkx as nx
from src.core.ast.schema import RelationalSchemaRaw


class RelationalGraph:
    """Representa el grafo de dependencias relacionales entre tablas."""

    def __init__(self, raw_schema: RelationalSchemaRaw):
        self.raw_schema = raw_schema
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        for table in self.raw_schema.tables:
            self.graph.add_node(
                table.name,
                table=table,
                num_columns=len(table.columns),
                num_pks=len(table.primary_keys),
                num_fks=len(table.foreign_keys),
            )

        for rel in self.raw_schema.relationships:
            self.graph.add_edge(
                rel.from_table,
                rel.to_table,
                from_col=rel.from_column,
                to_col=rel.to_column,
                description=rel.description,
            )

    def get_in_degree(self, table_name: str) -> int:
        """Número de tablas que referencian a esta tabla (típico de Dimensiones)."""
        return self.graph.in_degree(table_name) if table_name in self.graph else 0

    def get_out_degree(self, table_name: str) -> int:
        """Número de tablas foráneas referenciadas por esta tabla (típico de Facts)."""
        return self.graph.out_degree(table_name) if table_name in self.graph else 0

    def get_neighbors(self, table_name: str) -> list[str]:
        return list(self.graph.neighbors(table_name)) if table_name in self.graph else []

    def has_cycle(self) -> bool:
        """Determina si hay ciclos de dependencia en el modelo."""
        try:
            return not nx.is_directed_acyclic_graph(self.graph)
        except Exception:
            return False
