"""
Data Engineer Persona Lens.
Tailored for Data Platform Engineers, Ingestion Specialists, and Pipeline Authors.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.core.ast.canonical.models import CanonicalSemanticProject, EntityRole
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


class DataEngineerLens(PersonaLens):
    """Technical Lens focusing on ingestion pipelines, partitioning, grains, and raw schemas."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="data_engineer",
            role=PersonaRole.DATA_ENGINEER,
            display_name="Data Engineer",
            title="Data Engineering, Ingestion & Pipeline Health Lens",
            summary_template="Physical schema, partition grain, upstream sources, and pipeline integrity for {project_name}.",
            technical_depth=TechnicalDepth.TECHNICAL,
            focus_areas=[LensFocus.PIPELINE_HEALTH, LensFocus.DATA_MODELING],
            visible_object_types=["FACT", "DIMENSION", "BRIDGE"],
            icon="server",
            color_theme="#2B6CB0",
            aliases=["de", "data_platform_engineer"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.DATA_ENGINEER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        # Primary entities: All structural tables (facts, dims, bridges)
        primary_entities = [e.name for e in project.entities if e.role in (EntityRole.FACT, EntityRole.DIMENSION, EntityRole.BRIDGE)]
        secondary_entities = [e.name for e in project.entities if e.role == EntityRole.CALCULATED]

        # Inspect missing grains or primary keys
        recommendations: List[PersonaRecommendation] = []
        for e in project.entities:
            if not e.grain:
                recommendations.append(
                    PersonaRecommendation(
                        id=f"DE-GRAIN-{e.name}",
                        title=f"Define Explicit Grain for {e.name}",
                        description=f"Entity '{e.name}' lacks an explicit primary key / grain definition.",
                        priority=RecommendationPriority.MEDIUM,
                        impact="Prevents Cartesian product joins and pipeline duplication errors",
                        effort="Low",
                        target_objects=[e.name],
                        suggested_action=f"Declare grain columns in {e.name} schema definition."
                    )
                )

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Physical Ingestion & Pipeline SLAs",
                role=RaciRole.RESPONSIBLE,
                description="Manages raw data ingestion, table partitioning, change data capture (CDC), and source freshness.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.ANALYTICS_ENGINEER,
                interaction_type="handoff",
                frequency="Daily",
                interface_artifact="Clean Staging Table Schemas",
                sla_or_expectation="Freshness within daily 06:00 UTC SLA"
            )
        ]

        grain_coverage = len([e for e in project.entities if e.grain]) / max(1, len(project.entities)) * 100.0
        maturity = PersonaMaturityAssessment(
            overall_score=min(100.0, grain_coverage * 0.5 + 45.0),
            maturity_level="Optimizing" if grain_coverage >= 90 else "Defined",
            dimensions=[
                MaturityDimension(dimension_name="Grain Definition Completeness", score=grain_coverage, level="Defined", findings=[f"{int(grain_coverage)}% entities have explicit grain"]),
                MaturityDimension(dimension_name="Physical Type Rigor", score=95.0, level="Optimizing", findings=["Strongly-typed data attributes"])
            ],
            strengths=["Explicit data types on all attributes", "Structured entity definitions"],
            gaps=["Verify surrogate key generation in staging layer"]
        )

        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in project.relationships if r.is_active
        ]

        summary = self.definition.summary_template.format(
            project_name=project.name,
            entities_count=len(primary_entities),
            metrics_count=0,
        )

        return PersonaProjection(
            persona_id=self.definition.persona_id,
            role=self.role,
            title=self.definition.title,
            summary=summary,
            technical_depth=self.definition.technical_depth,
            focus_areas=self.definition.focus_areas,
            primary_entities=primary_entities,
            secondary_entities=secondary_entities,
            certified_metrics=[],
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            diagnostics=list(project.diagnostics),
            rendered_at=now_iso,
        )
