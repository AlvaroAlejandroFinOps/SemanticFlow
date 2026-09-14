"""
Business Consumer Persona Lens.
Tailored for Business Analysts, Operations Managers, and Non-Technical Stakeholders.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
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


class BusinessConsumerLens(PersonaLens):
    """Consumer Lens translating technical semantic artifacts into plain-language business insights."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="business_consumer",
            role=PersonaRole.BUSINESS_CONSUMER,
            display_name="Business Consumer",
            title="Business Consumer & Self-Service Analytics Lens",
            summary_template="Certified business terms, plain-language metric glossary, and intuitive report navigation for {project_name}.",
            technical_depth=TechnicalDepth.EXECUTIVE,
            focus_areas=[LensFocus.CONSUMPTION_SIMPLICITY, LensFocus.BUSINESS_VALUE],
            visible_object_types=["FACT", "DIMENSION"],
            icon="user-check",
            color_theme="#3182CE",
            aliases=["analytic_consumer", "business_analyst", "business_user"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.BUSINESS_CONSUMER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        primary_entities = [e.name for e in project.entities if e.role == EntityRole.FACT]
        secondary_entities = [e.name for e in project.entities if e.role == EntityRole.DIMENSION]

        certified_metrics = [
            m.name for e in project.entities for m in e.metrics
            if (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
        ]

        # Check for missing descriptions
        undescribed = [e.name for e in project.entities if not e.description]
        recommendations: List[PersonaRecommendation] = []
        if undescribed:
            recommendations.append(
                PersonaRecommendation(
                    id="BIZ-DESC-01",
                    title="Add Plain-Language Descriptions",
                    description=f"Entities {undescribed} lack business descriptions.",
                    priority=RecommendationPriority.LOW,
                    impact="Assists self-service business users in identifying appropriate data sets",
                    effort="Low",
                    target_objects=undescribed
                )
            )

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Self-Service Business Exploration",
                role=RaciRole.INFORMED,
                description="Uses certified datasets and dashboards to drive data-informed operational decisions.",
                collaborator_roles=[PersonaRole.BI_DEVELOPER, PersonaRole.DATA_PRODUCT_MANAGER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.BI_DEVELOPER,
                interaction_type="consultation",
                frequency="On-Demand",
                interface_artifact="Certified KPI Business Glossary & Visual Reports"
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=88.0,
            maturity_level="Defined",
            dimensions=[
                MaturityDimension(dimension_name="Business Taxonomy Clarity", score=88.0, level="Defined", findings=[f"{len(certified_metrics)} certified terms available"]),
                MaturityDimension(dimension_name="Self-Service Ease", score=90.0, level="Optimizing", findings=["Simplified executive-level view"])
            ],
            strengths=["Clean non-technical abstraction", "Direct KPI visibility"],
            gaps=["Interactive natural language search over business definitions"]
        )

        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in project.relationships if r.is_active
        ]

        summary = self.definition.summary_template.format(
            project_name=project.name,
            entities_count=len(primary_entities),
            metrics_count=len(certified_metrics),
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
            certified_metrics=certified_metrics,
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            rendered_at=now_iso,
        )
