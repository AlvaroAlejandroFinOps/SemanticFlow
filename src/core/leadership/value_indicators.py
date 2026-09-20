"""
Value Indicators module for the Data Leadership Cockpit.
Tracks business value realization, certified KPIs, and strategic alignment indicators.
"""
from typing import Dict, List

from pydantic import BaseModel, Field

from src.core.ast.canonical.models import CanonicalSemanticProject, MetricType


class ValueIndicator(BaseModel):
    """Business value metric definition."""
    metric_name: str
    entity_name: str
    certification_status: str
    expression: str
    strategic_focus: str


class ValueIndicatorsReport(BaseModel):
    """Aggregate report of strategic business value and certified KPIs."""
    total_value_metrics: int
    certified_kpis: List[ValueIndicator] = Field(default_factory=list)
    strategic_focus_distribution: Dict[str, int] = Field(default_factory=dict)


class ValueIndicatorsAnalyzer:
    """Extracts certified KPIs and business value indicators from the canonical project."""

    @staticmethod
    def analyze(project: CanonicalSemanticProject) -> ValueIndicatorsReport:
        indicators: List[ValueIndicator] = []
        dist: Dict[str, int] = {}

        for e in project.entities:
            for m in e.metrics:
                is_cert = (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
                if is_cert:
                    focus = "Core Business Performance"
                    indicators.append(
                        ValueIndicator(
                            metric_name=m.name,
                            entity_name=e.name,
                            certification_status=m.governance.certification_status if m.governance else "Draft",
                            expression=m.expression,
                            strategic_focus=focus,
                        )
                    )
                    dist[focus] = dist.get(focus, 0) + 1

        return ValueIndicatorsReport(
            total_value_metrics=len(indicators),
            certified_kpis=indicators,
            strategic_focus_distribution=dist,
        )
