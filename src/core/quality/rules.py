"""
Quality and Validation Rules for Semantic Models.
"""
from typing import List
from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    Diagnostic,
    DiagnosticSeverity,
    DiagnosticCategory,
    EntityRole,
    MetricType,
)


def validate_grain_declaration(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        if entity.role == EntityRole.FACT and not entity.grain:
            diagnostics.append(
                Diagnostic(
                    code="QUAL_GRAIN_001",
                    severity=DiagnosticSeverity.WARNING,
                    category=DiagnosticCategory.QUALITY,
                    message=f"Fact entity '{entity.name}' has no explicit grain declared.",
                    object_id=entity.id,
                    suggested_action="Declare explicit primary key attributes as grain in entity metadata.",
                )
            )
    return diagnostics


def validate_metric_descriptions(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        for metric in entity.metrics:
            if not metric.description:
                diagnostics.append(
                    Diagnostic(
                        code="QUAL_METRIC_001",
                        severity=DiagnosticSeverity.WARNING,
                        category=DiagnosticCategory.METRIC,
                        message=f"Metric '{metric.name}' in entity '{entity.name}' lacks a business description.",
                        object_id=metric.id,
                        suggested_action="Provide a clear business description for the metric.",
                    )
                )
    return diagnostics


def validate_certified_metrics(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        for metric in entity.metrics:
            eff_gov = project.resolve_asset_governance(metric)
            if eff_gov.certification_status == "CERTIFIED":
                if not eff_gov.owner:
                    diagnostics.append(
                        Diagnostic(
                            code="GOV_CERT_001",
                            severity=DiagnosticSeverity.ERROR,
                            category=DiagnosticCategory.GOVERNANCE,
                            message=f"Certified metric '{metric.name}' must have an assigned owner.",
                            object_id=metric.id,
                            suggested_action="Assign a business or technical owner before certifying.",
                        )
                    )
    return diagnostics


def validate_ratio_metrics(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        for metric in entity.metrics:
            if metric.metric_type == MetricType.RATIO:
                if not metric.numerator_metric_id or not metric.denominator_metric_id:
                    diagnostics.append(
                        Diagnostic(
                            code="METRIC_RATIO_001",
                            severity=DiagnosticSeverity.ERROR, 
                            category=DiagnosticCategory.METRIC,
                            message=f"Ratio metric '{metric.name}' must declare numerator_metric_id and denominator_metric_id.",
                            object_id=metric.id,
                            suggested_action="Specify numerator and denominator metric IDs for auditability.",
                        )
                    )
    return diagnostics


def validate_project_governance(project: CanonicalSemanticProject) -> List[Diagnostic]:
    """Validates that the project has explicit domain governance and ownership metadata."""
    diagnostics = []
    if not project.governance or not project.governance.owner:
        diagnostics.append(
            Diagnostic(
                code="GOV_PROJ_001",
                severity=DiagnosticSeverity.RECOMMENDATION,
                category=DiagnosticCategory.GOVERNANCE,
                message=f"Project '{project.name}' has no assigned executive owner.",
                object_id=project.id,
                suggested_action="Declare project-level governance with owner in ProjectGovernance.",
            )
        )
    return diagnostics


def validate_pii_classification(project: CanonicalSemanticProject) -> List[Diagnostic]:
    """Validates that PII attributes are flagged with Restricted or Confidential classification."""
    diagnostics = []
    for entity in project.entities:
        for attr in entity.attributes:
            eff_gov = project.resolve_asset_governance(attr)
            if eff_gov.is_pii:
                if eff_gov.sensitivity_classification not in ("Restricted", "Confidential"):
                    diagnostics.append(
                        Diagnostic(
                            code="GOV_PII_001",
                            severity=DiagnosticSeverity.WARNING,
                            category=DiagnosticCategory.SECURITY,
                            message=f"PII attribute '{entity.name}.{attr.name}' must have 'Restricted' or 'Confidential' classification.",
                            object_id=attr.id,
                            suggested_action="Set sensitivity_classification to Restricted in attribute or project governance.",
                        )
                    )
    return diagnostics
