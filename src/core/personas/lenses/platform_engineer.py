"""
Platform Engineer Persona Lens.
Tailored for Infrastructure Operations, Compute Capacity, Storage Modes, and SLA Optimization.
"""
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from src.core.ast.canonical.models import CanonicalSemanticProject, EntityRole, MetricType
from src.core.personas.interfaces import PersonaLens
from src.core.personas.models import (
    LensFocus,
    MaturityDimension,
    PersonaDefinition,
    PersonaMaturityAssessment,
    PersonaProjection,
    PersonaRecommendation,
    PersonaRole,
    RaciRole,
    RecommendationPriority,
    ResponsibilityAssignment,
    TeamInteraction,
    TechnicalDepth,
)


class PlatformEngineerLens(PersonaLens):
    """Platform infrastructure lens focusing on compute engine capacity, storage modes, and partitioning."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="platform_engineer",
            role=PersonaRole.PLATFORM_ENGINEER,
            display_name="Platform Engineer",
            title="Data Platform Infrastructure & Storage Capacity Lens",
            summary_template="Engine compute capacity, storage modes (Import/DirectLake), partitions, and refresh SLAs for {project_name}.",
            technical_depth=TechnicalDepth.TECHNICAL,
            focus_areas=[LensFocus.COST_CAPACITY, LensFocus.PIPELINE_HEALTH],
            visible_object_types=["FACT", "DIMENSION", "STORAGE_MODE", "PARTITION"],
            icon="hard-drive",
            color_theme="#DD6B20",
            aliases=["pe", "infrastructure_engineer", "systems_engineer"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.PLATFORM_ENGINEER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        primary_entities = [e.name for e in project.entities if e.role in (EntityRole.FACT, EntityRole.DIMENSION)]
        secondary_entities = [e.name for e in project.entities if e.role not in (EntityRole.FACT, EntityRole.DIMENSION)]

        certified_metrics = [
            m.name for e in project.entities for m in e.metrics
            if (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
        ]
        secondary_metrics = [
            m.name for e in project.entities for m in e.metrics
            if m.name not in certified_metrics
        ]

        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in project.relationships if r.is_active
        ]

        recs = [
            PersonaRecommendation(
                id="REC-PE-001",
                rule_id="RULE_STORAGE_MODE_OPTIMIZATION",
                title="Evaluate VertiPaq / Direct Lake Storage Modes for High-Cardinality Entities",
                description="Optimize storage mode allocation and memory encoding for high-cardinality entities to maximize query throughput.",
                impact="Maximizes memory compression and query performance SLAs in Fabric/Power BI.",
                effort="Medium",
                suggested_action="Review column cardinalities to optimize VertiPaq memory footprint.",
                priority=RecommendationPriority.MEDIUM,
                target_objects=primary_entities,
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Semantic Compute Engine Tuning & Storage Allocation",
                role=RaciRole.RESPONSIBLE,
                description="Manages semantic engine memory capacity, autoscaling limits, and storage modes.",
                collaborator_roles=[PersonaRole.DATA_ENGINEER, PersonaRole.BI_DEVELOPER],
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.DATA_ENGINEER,
                interaction_type="collaboration",
                frequency="Monthly",
                interface_artifact="Engine Capacity & Refresh Performance Report",
                sla_or_expectation="Refresh SLA < 15 min",
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=87.0,
            maturity_level="Defined",
            dimensions=[MaturityDimension(dimension_name="Platform Scalability", score=87.0, level="Defined", findings=["Storage modes mapped"])],
            strengths=["Predictable VertiPaq compression", "Stable relationship evaluation"],
            gaps=["Automated partition optimization"],
        )

        return PersonaProjection(
            persona_id=self._definition.persona_id,
            role=self._definition.role,
            title=self._definition.title,
            summary=self._definition.summary_template.format(project_name=project.name),
            technical_depth=self._definition.technical_depth,
            focus_areas=self._definition.focus_areas,
            primary_entities=primary_entities,
            secondary_entities=secondary_entities,
            certified_metrics=certified_metrics,
            secondary_metrics=secondary_metrics,
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recs,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            diagnostics=list(project.diagnostics),
            metadata={"project_id": project.id, "project_version": project.version},
            rendered_at=now_iso,
        )
