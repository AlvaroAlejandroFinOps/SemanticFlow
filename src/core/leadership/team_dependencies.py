"""
Team Dependencies & Interaction module for the Data Leadership Cockpit.
Maps organizational handoffs, SLA commitments, and generates Team Topologies diagrams.
"""
from typing import Dict, List

from pydantic import BaseModel, Field

from src.core.personas.models import PersonaProjection, TeamInteraction


class TeamDependenciesReport(BaseModel):
    """Aggregate report of cross-functional team interactions and dependencies."""
    total_handoffs_count: int
    interactions: List[TeamInteraction] = Field(default_factory=list)
    mermaid_topology_diagram: str = ""


class TeamDependenciesAnalyzer:
    """Extracts team interactions across all persona projections and generates Mermaid topologies."""

    @staticmethod
    def analyze(projections: Dict[str, PersonaProjection]) -> TeamDependenciesReport:
        all_interactions: List[TeamInteraction] = []
        for p in projections.values():
            all_interactions.extend(p.interactions)

        # Build Mermaid flowchart
        lines = ["flowchart TD"]
        seen_pairs = set()
        for inter in all_interactions:
            src = inter.target_persona.value if hasattr(inter.target_persona, 'value') else str(inter.target_persona)
            pair_key = (src, inter.interaction_type)
            if pair_key not in seen_pairs:
                seen_pairs.add(pair_key)
                lines.append(f'    {src} -->|"{inter.interaction_type} ({inter.frequency})"| DataLeadership')

        diagram = "\n".join(lines) if len(lines) > 1 else "flowchart TD\n    AllTeams --> DataLeadership"

        return TeamDependenciesReport(
            total_handoffs_count=len(all_interactions),
            interactions=all_interactions,
            mermaid_topology_diagram=diagram,
        )
