"""
Portfolio module for the Data Leadership Cockpit.
Summarizes semantic assets, entity counts, metrics, relationships, and data products.
"""
from typing import Any, Dict

from pydantic import BaseModel, Field

from src.core.ast.canonical.models import CanonicalSemanticProject, EntityRole, MetricType


class PortfolioSummary(BaseModel):
    """C-Level summary of the semantic data portfolio."""
    project_id: str
    project_name: str
    project_version: str
    data_product_status: str
    domain_id: str = "default_domain"
    total_entities: int
    fact_entities_count: int
    dimension_entities_count: int
    total_metrics: int
    certified_kpis_count: int
    total_relationships: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PortfolioAnalyzer:
    """Extracts portfolio telemetry directly from CanonicalSemanticProject."""

    @staticmethod
    def analyze(project: CanonicalSemanticProject) -> PortfolioSummary:
        gov = project.governance
        data_product_status = gov.data_product_status if gov else "Draft"
        domain_id = gov.domain_id if (gov and gov.domain_id) else "default_domain"

        fact_count = sum(1 for e in project.entities if e.role in (EntityRole.FACT, EntityRole.CALCULATED))
        dim_count = sum(1 for e in project.entities if e.role in (EntityRole.DIMENSION, EntityRole.BRIDGE))

        all_metrics = [m for e in project.entities for m in e.metrics]
        certified_kpis = [
            m for m in all_metrics
            if (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
        ]

        return PortfolioSummary(
            project_id=project.id,
            project_name=project.name,
            project_version=project.version,
            data_product_status=data_product_status,
            domain_id=domain_id,
            total_entities=len(project.entities),
            fact_entities_count=fact_count,
            dimension_entities_count=dim_count,
            total_metrics=len(all_metrics),
            certified_kpis_count=len(certified_kpis),
            total_relationships=len(project.relationships),
            metadata={"source_project_id": project.id},
        )
