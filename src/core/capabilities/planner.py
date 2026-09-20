"""
Target Capability Planner and Adapter Interfaces.
"""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from src.core.ast.canonical.models import CanonicalSemanticProject


class CompatibilityStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    SUPPORTED_WITH_TRANSFORMATION = "SUPPORTED_WITH_TRANSFORMATION"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    REQUIRES_MANUAL_REVIEW = "REQUIRES_MANUAL_REVIEW"


class ObjectCompatibilityReport(BaseModel):
    object_id: str
    object_type: str
    status: CompatibilityStatus
    details: Optional[str] = None


class TargetCapabilities(BaseModel):
    target_name: str
    supports_ratio_metrics: bool = True
    supports_rls: bool = True
    supports_ols: bool = True
    supports_calculation_groups: bool = True
    supports_perspectives: bool = True


class TargetCapabilityPlanner:
    """Evaluates canonical model compatibility against a target BI platform."""

    def __init__(self, capabilities: TargetCapabilities):
        self.capabilities = capabilities

    def plan(self, project: CanonicalSemanticProject) -> List[ObjectCompatibilityReport]:
        reports: List[ObjectCompatibilityReport] = []

        for entity in project.entities:
            role_val = entity.role.value if hasattr(entity, 'role') else 'Entity'
            reports.append(
                ObjectCompatibilityReport(
                    object_id=entity.id,
                    object_type="Entity",
                    status=CompatibilityStatus.SUPPORTED,
                    details=f"Known support for {role_val} in {self.capabilities.target_name}.",
                )
            )

        for r in project.relationships:
            reports.append(
                ObjectCompatibilityReport(
                    object_id=r.id,
                    object_type="Relationship",
                    status=CompatibilityStatus.SUPPORTED,
                    details=f"1:N Relationship supported in {self.capabilities.target_name}.",
                )
            )

        return reports
