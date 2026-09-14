"""
Semantic Quality Score (cQA) Engine.
"""
from typing import List, Dict, Any
from pydantic import BaseModel
from src.core.ast.canonical.models import CanonicalSemanticProject, Diagnostic, DiagnosticSeverity
from src.core.quality.rules import (
    validate_grain_declaration,
    validate_metric_descriptions,
    validate_certified_metrics,
    validate_ratio_metrics,
    validate_project_governance,
    validate_pii_classification,
)


class QualityScoreResult(BaseModel):
    score: float
    max_score: float = 100.0
    diagnostics: List[Diagnostic]
    blocking_errors: int
    warnings: int


class SemanticQualityScorer:
    """Calculates a transparent, auditable Semantic Quality Score (0-100)."""

    ACCEPTABLE_WEIGHTS = {
        DiagnosticSeverity.ERROR: 15.0,
        DiagnosticSeverity.WARNING: 5.0,
        DiagnosticSeverity.INFO: 0.0,
        DiagnosticSeverity.RECOMMENDATION: 1.0,
    }

    def __init__(self, project: CanonicalSemanticProject):
        self.project = project

    def evaluate(self) -> QualityScoreResult:
        all_diagnostics: List[Diagnostic] = []
        all_diagnostics.extend(self.project.diagnostics)
        all_diagnostics.extend(validate_grain_declaration(self.project))
        all_diagnostics.extend(validate_metric_descriptions(self.project))
        all_diagnostics.extend(validate_certified_metrics(self.project))
        all_diagnostics.extend(validate_ratio_metrics(self.project))
        all_diagnostics.extend(validate_project_governance(self.project))
        all_diagnostics.extend(validate_pii_classification(self.project))

        deductions = 0.0
        blocking_errors = 0
        warnings = 0

        for d in all_diagnostics:
            deductions += self.ACCEPTABLE_WEIGHTS.get(d.severity, 0.0)
            if d.severity == DiagnosticSeverity.ERROR:
                blocking_errors += 1
            elif d.severity == DiagnosticSeverity.WARNING:
                warnings += 1

        final_score = max(0.0, 100.0 - deductions)

        return QualityScoreResult(
            score=final_score,
            max_score=100.0,
            diagnostics=all_diagnostics,
            blocking_errors=blocking_errors,
            warnings=warnings,
        )
