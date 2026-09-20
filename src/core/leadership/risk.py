"""
Risk & Exceptions module for the Data Leadership Cockpit.
Tracks governance violations, high-priority recommendations, and regulatory risk exposures.
"""
from typing import Dict, List

from pydantic import BaseModel, Field

from src.core.ast.canonical.models import CanonicalSemanticProject, DiagnosticSeverity
from src.core.personas.models import PersonaProjection, PersonaRecommendation, RecommendationPriority


class RiskOverviewReport(BaseModel):
    """Aggregate risk profile and priority actions report."""
    overall_risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    blocking_errors_count: int
    warnings_count: int
    critical_recommendations: List[PersonaRecommendation] = Field(default_factory=list)
    high_recommendations: List[PersonaRecommendation] = Field(default_factory=list)


class RiskAnalyzer:
    """Evaluates risks, diagnostics, and high-priority recommendations across all lenses."""

    @staticmethod
    def analyze(
        project: CanonicalSemanticProject,
        projections: Dict[str, PersonaProjection],
    ) -> RiskOverviewReport:
        critical_recs: List[PersonaRecommendation] = []
        high_recs: List[PersonaRecommendation] = []

        for proj in projections.values():
            for rec in proj.recommendations:
                if rec.priority == RecommendationPriority.CRITICAL:
                    critical_recs.append(rec)
                elif rec.priority == RecommendationPriority.HIGH:
                    high_recs.append(rec)

        blocking = sum(1 for d in project.diagnostics if d.severity == DiagnosticSeverity.ERROR)
        warnings = sum(1 for d in project.diagnostics if d.severity == DiagnosticSeverity.WARNING)

        if blocking > 0 or len(critical_recs) > 0:
            level = "CRITICAL"
        elif warnings > 5 or len(high_recs) > 0:
            level = "HIGH"
        elif warnings > 0:
            level = "MEDIUM"
        else:
            level = "LOW"

        return RiskOverviewReport(
            overall_risk_level=level,
            blocking_errors_count=blocking,
            warnings_count=warnings,
            critical_recommendations=critical_recs,
            high_recommendations=high_recs,
        )
