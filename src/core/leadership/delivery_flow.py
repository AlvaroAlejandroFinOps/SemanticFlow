"""
Delivery Flow & Lifecycle module for the Data Leadership Cockpit.
Tracks data product lifecycle stages, certification flow, and deployment velocity.
"""
from typing import Any, Dict

from pydantic import BaseModel, Field

from src.core.ast.canonical.models import CanonicalSemanticProject


class DeliveryFlowReport(BaseModel):
    """Telemetry report on data product lifecycle maturity and delivery velocity."""
    lifecycle_phase: str  # Draft, In-Review, Certified, Production, Deprecated
    is_production_ready: bool
    governance_certification: str
    diagnostics_blocking: int
    velocity_metrics: Dict[str, Any] = Field(default_factory=dict)


class DeliveryFlowAnalyzer:
    """Evaluates the deployment readiness and lifecycle flow of the canonical project."""

    @staticmethod
    def analyze(project: CanonicalSemanticProject) -> DeliveryFlowReport:
        gov = project.governance
        phase = gov.data_product_status if (gov and gov.data_product_status) else "Draft"
        cert = gov.certification_status if (gov and hasattr(gov, 'certification_status') and gov.certification_status) else "Draft"
        blocking = sum(1 for d in project.diagnostics if d.severity.value == "ERROR")

        is_ready = (blocking == 0) and (phase.lower() in ("certified", "production", "published"))

        return DeliveryFlowReport(
            lifecycle_phase=phase,
            is_production_ready=is_ready,
            governance_certification=cert,
            diagnostics_blocking=blocking,
            velocity_metrics={
                "project_version": project.version,
                "entities_delivered": len(project.entities),
                "metrics_delivered": sum(len(e.metrics) for e in project.entities),
            },
        )
