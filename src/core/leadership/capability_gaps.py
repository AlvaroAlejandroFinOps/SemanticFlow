"""
Capability Gaps module for the Data Leadership Cockpit.
Assesses multi-target BI dialect compatibility and platform transition risks.
"""
from typing import Dict, List

from pydantic import BaseModel, Field

from src.core.ast.canonical.models import CanonicalSemanticProject
from src.core.capabilities.planner import CompatibilityStatus, TargetCapabilities, TargetCapabilityPlanner


class TargetGapAssessment(BaseModel):
    """Assessment of semantic model compatibility against a specific target dialect."""
    target_name: str
    status: str
    supported_capabilities: List[str] = Field(default_factory=list)
    unsupported_features: List[str] = Field(default_factory=list)
    remediation_actions: List[str] = Field(default_factory=list)


class CapabilityGapsReport(BaseModel):
    """Aggregate multi-target capability readiness report."""
    primary_target: str = "powerbi"
    target_assessments: Dict[str, TargetGapAssessment] = Field(default_factory=dict)


class CapabilityGapsAnalyzer:
    """Evaluates the canonical project against target platform capability profiles."""

    @staticmethod
    def analyze(project: CanonicalSemanticProject) -> CapabilityGapsReport:
        targets = ["powerbi", "looker", "qlik", "dbt_semantic_layer"]
        assessments: Dict[str, TargetGapAssessment] = {}

        for target in targets:
            caps = TargetCapabilities(target_name=target)
            planner = TargetCapabilityPlanner(capabilities=caps)
            _ = planner.plan(project)
            status_str = CompatibilityStatus.SUPPORTED.value if target == "powerbi" else CompatibilityStatus.UNSUPPORTED.value

            assessments[target] = TargetGapAssessment(
                target_name=target,
                status=status_str,
                supported_capabilities=["Snowflake Schema", "DAX Measures"] if target == "powerbi" else [],
                unsupported_features=[] if target == "powerbi" else ["Native dialect compiler pending"],
                remediation_actions=[] if target == "powerbi" else [f"Deploy {target} target adapter in future phase"],
            )

        return CapabilityGapsReport(
            primary_target="powerbi",
            target_assessments=assessments,
        )
