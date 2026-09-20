"""
Health & Maturity module for the Data Leadership Cockpit.
Synthesizes domain maturity scores, semantic quality score (cQS), and diagnostic distributions.
"""
from typing import Dict, List

from pydantic import BaseModel, Field

from src.core.ast.canonical.models import CanonicalSemanticProject, DiagnosticSeverity
from src.core.personas.models import PersonaProjection


class DomainHealthAssessment(BaseModel):
    """Domain-level health and maturity telemetry."""
    domain_name: str
    maturity_score: float
    health_status: str  # Optimal, Satisfactory, Action Required
    blocking_errors: int = 0
    warnings: int = 0


class PortfolioHealthReport(BaseModel):
    """Aggregated portfolio health report across all domains and persona perspectives."""
    overall_health_score: float
    maturity_radar: Dict[str, float] = Field(default_factory=dict)
    domain_assessments: List[DomainHealthAssessment] = Field(default_factory=list)
    total_diagnostics_count: int = 0
    blocking_errors_count: int = 0


class HealthAnalyzer:
    """Computes health telemetry from canonical project diagnostics and persona projections."""

    @staticmethod
    def analyze(
        project: CanonicalSemanticProject,
        projections: Dict[str, PersonaProjection],
    ) -> PortfolioHealthReport:
        maturity_radar: Dict[str, float] = {}
        domain_assessments: List[DomainHealthAssessment] = []

        for pid, proj in projections.items():
            score = proj.maturity_assessment.overall_score if proj.maturity_assessment else 80.0
            maturity_radar[proj.role.value] = score
            status = "Optimal" if score >= 80 else ("Satisfactory" if score >= 65 else "Action Required")
            domain_assessments.append(
                DomainHealthAssessment(
                    domain_name=proj.role.value,
                    maturity_score=score,
                    health_status=status,
                )
            )

        blocking = sum(1 for d in project.diagnostics if d.severity == DiagnosticSeverity.ERROR)
        overall = sum(maturity_radar.values()) / max(1, len(maturity_radar))

        return PortfolioHealthReport(
            overall_health_score=round(overall, 1),
            maturity_radar=maturity_radar,
            domain_assessments=domain_assessments,
            total_diagnostics_count=len(project.diagnostics),
            blocking_errors_count=blocking,
        )
