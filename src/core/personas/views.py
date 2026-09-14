"""
Persona Views generator contracts and models.
"""
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from src.core.ast.canonical.models import CanonicalSemanticProject, SemanticEntity, SemanticMetric


class PersonaType(str, Enum):
    EXECUTIVE = "EXECUTIVE"
    DATA_GOVERNANCE = "DATA_GOVERNANCE"
    BI_ENGINEER = "BI_ENGINEER"
    ANALYTIC_CONSUMER = "ANALYTIC_CONSUMER"
    FINOPS = "FINOPS"


class PersonaView(BaseModel):
    persona: PersonaType
    title: str
    summary: str
    primary_entities: List[str]
    certified_metrics: List[str]
    metadata: Dict[str, Any] = {}


class PersonaViewGenerator:
    """Generates tailored enterprise persona views from the Canonical Model."""

    @staticmethod
    def generate_views(project: CanonicalSemanticProject) -> Dict[PersonaType, PersonaView]:
        views: Dict[PersonaType, PersonaView] = {}

        # 1. Executive Persona View
        exec_metrics = [
            m.name for e in project.entities for m in e.metrics
            if m.governance and m.governance.certified
        ]
        views[PersonaType.EXECUTIVE] = PersonaView(
            persona=PersonaType.EXECUTIVE,
            title="Executive Summary View",
            summary=f"High-level view focusing on {len(exec_metrics)} certified KPI metrics across key business entities.",
            primary_entities=[e.name for e in project.entities if e.role.value == "FACT"],
            certified_metrics=exec_metrics,
        )

        # 2. Data Governance Persona View
        views[PersonaType.DATA_GOVERNANCE] = PersonaView(
            persona=PersonaType.DATA_GOVERNANCE,
            title="Data Governance & Lineage View",
            summary=f"Audit view tracking data ownership, classifications, and lineage across {len(project.entities)} entities.",
            primary_entities=[e.name for e in project.entities],
            certified_metrics=exec_metrics,
            metadata={
                "project_owner": project.governance.owner if getattr(project, 'governance', None) else "Unassigned",
                "classification": project.governance.classification if getattr(project, 'governance', None) else "Internal",
            }
        )

        # 3. BI Engineer Persona View
        views[PersonaType.BI_ENGINEER] = PersonaView(
            persona=PersonaType.BI_ENGINEER,
            title="BI Engineering Technical Model",
            summary=f"Full technical schema containing {len(project.entities)} entities and {len(project.relationships)} relationships.",
            primary_entities=[e.name for e in project.entities],
            certified_metrics=[m.name for e in project.entities for m in e.metrics],
        )

        return views
