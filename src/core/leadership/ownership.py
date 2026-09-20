"""
Ownership & Stewardship module for the Data Leadership Cockpit.
Tracks assignment of business owners, technical stewards, and unassigned governance gaps.
"""
from typing import Dict, List

from pydantic import BaseModel, Field

from src.core.ast.canonical.models import CanonicalSemanticProject


class OwnershipCoverageReport(BaseModel):
    """Telemetry report on governance ownership and stewardship coverage."""
    executive_owner: str
    total_entities: int
    entities_with_owner: int
    entities_with_steward: int
    unassigned_entities: List[str] = Field(default_factory=list)
    ownership_coverage_pct: float
    stewardship_coverage_pct: float
    owner_distribution: Dict[str, int] = Field(default_factory=dict)


class OwnershipAnalyzer:
    """Calculates ownership and stewardship distribution across the semantic model."""

    @staticmethod
    def analyze(project: CanonicalSemanticProject) -> OwnershipCoverageReport:
        exec_owner = project.governance.owner if (project.governance and project.governance.owner) else "Unassigned"
        total = len(project.entities)

        with_owner = 0
        with_steward = 0
        unassigned: List[str] = []
        dist: Dict[str, int] = {}

        for e in project.entities:
            gov = e.governance
            owner = gov.owner if (gov and gov.owner) else (project.governance.owner if project.governance else None)
            steward = gov.steward if (gov and gov.steward) else (project.governance.steward if project.governance else None)

            if owner and owner != "Unassigned":
                with_owner += 1
                dist[owner] = dist.get(owner, 0) + 1
            else:
                unassigned.append(e.name)

            if steward and steward != "Unassigned":
                with_steward += 1

        owner_pct = (with_owner / total * 100.0) if total > 0 else 0.0
        steward_pct = (with_steward / total * 100.0) if total > 0 else 0.0

        return OwnershipCoverageReport(
            executive_owner=exec_owner,
            total_entities=total,
            entities_with_owner=with_owner,
            entities_with_steward=with_steward,
            unassigned_entities=unassigned,
            ownership_coverage_pct=round(owner_pct, 1),
            stewardship_coverage_pct=round(steward_pct, 1),
            owner_distribution=dist,
        )
