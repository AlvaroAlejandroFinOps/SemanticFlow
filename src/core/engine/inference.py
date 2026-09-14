"""
Inference engine with full provenance and explainability tracking.
"""
from src.core.ast.schema import TableRaw, RelationalSchemaRaw
from src.core.ast.canonical.models import (
    EntityRole,
    ProvenanceRecord,
)
from src.core.engine.graph import RelationalGraph


class CanonicalRoleInferer:
    """Infers entity role with full provenance and evidence."""

    def __init__(self, graph: RelationalGraph):
        self.graph = graph

    def infer_role_with_provenance(self, table: TableRaw) -> tuple[org_role: EntityRole, ProvenanceRecord]:
        name_lower = table.name.lower()

        # Rule 1: Explicit Prefix
        if name_lower.startswith("dim_") or name_lower.startswith("dim"):
            return EntityRole.DIMENSION, ProvenanceRecord(
                rule_id="ROLE_PREFIX_001",
                description="Inferred DIMENSION from 'Dim_' or 'Dim' table prefix",
                evidence={"table_name": table.name, "matching_prefix": "dim"},
                confidence=1.0,
            )
        if name_lower.startswith("fact_") or name_lower.startswith("fact"):
            return EntityRole.FACT, ProvenanceRecord(
                rule_id="ROLE_PREFIX_002",
                description="Inferred FACT from 'Fact_' or 'Fact' table prefix",
                evidence={"table_name": table.name, "matching_prefix": "fact"},
                confidence=1.0,
            )
        if name_lower.startswith("bridge_") or name_lower.startswith("rel_"):
            return EntityRole.BRIDGE, ProvenanceRecord(
                rule_id="ROLE_PREFIX_003",
                description="Inferred BRIDGE from 'Bridge_' or 'Rel_' table prefix",
                evidence={"table_name": table.name, "matching_prefix": "bridge"},
                confidence=1.0,
            )

        # Rule 2: Topology heuristics
        out_degree = self.graph.get_out_degree(table.name)
        in_degree = self.graph.get_in_degree(table.name)

        if out_degree >= 2 and in_degree == 0:
            return EntityRole.FACT, ProvenanceRecord(
                rule_id="ROLE_TOPOLOGY_001",
                description="Inferred FACT from network graph topology (out_degree >= 2, in_degree == 0)",
                evidence={"out_degree": out_degree, "in_degree": in_degree},
                confidence=0.85,
            )
        if in_degree > 0 and out_degree <= 1:
            return EntityRole.DIMENSION, ProvenanceRecord(
                rule_id="ROLE_TOPOLOGY_002",
                description="Inferred DIMENSION from network graph topology (in_degree > 0, out_degree <= 1)",
                evidence={"out_degree": out_degree, "in_degree": in_degree},
                confidence=0.85,
            )

        # Fallback default
        return EntityRole.DIMENSION, ProvenanceRecord(
            rule_id="ROLE_DEFAULT_001",
            description="Default DIMENSION assigned as analytical fallback",
            evidence={"table_name": table.name, "out_degree": out_degree, "in_degree": in_degree},
            confidence=0.5,
        )
