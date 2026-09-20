"""
Data Analyst Persona Lens.
Tailored for Self-Service Analytics, Business Intelligence Consumption, and Certified KPIs.
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


class DataAnalystLens(PersonaLens):
    """Business and analytics consumption lens focusing on certified KPIs and discoverable dimensions."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="data_analyst",
            role=PersonaRole.DATA_ANALYST,
            display_name="Data Analyst",
            title="Data Analyst & Self-Service Consumption Lens",
            summary_template="Certified KPIs, domain dimensions, and self-service exploration catalog for {project_name}.",
            technical_depth=TechnicalDepth.SUMMARY,
            focus_areas=[LensFocus.CONSUMPTION_SIMPLICITY, LensFocus.BUSINESS_VALUE],
            visible_object_types=["FACT", "DIMENSION", "KPI"],
            icon="bar-chart-2",
            color_theme="#38A169",
            aliases=["analyst", "business_analyst", "bi_analyst"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.DATA_ANALYST

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        # Primary entities: Fact tables and governed dimensions
        primary_entities = [e.name for e in project.entities if e.role in (EntityRole.FACT, EntityRole.CALCULATED)]
        secondary_entities = [e.name for e in project.entities if e.role == EntityRole.DIMENSION]

        # Certified KPIs
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
                id="REC-DA-001",
                rule_id="RULE_KPI_DOCUMENTATION",
                title="Review Business Descriptions for Self-Service Exploration",
                description="Ensure all business metrics and dimensions have human-readable descriptions for self-service analytics.",
                impact="Ensures business consumers understand metric definitions.",
                effort="Low",
                suggested_action="Verify all certified KPIs have business definitions.",
                priority=RecommendationPriority.MEDIUM,
                target_objects=primary_entities,
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Self-Service KPI Consumption & Reporting",
                role=RaciRole.RESPONSIBLE,
                description="Consumes certified dimensions and KPIs to build operational reports.",
                collaborator_roles=[PersonaRole.BI_DEVELOPER, PersonaRole.DOMAIN_OWNER],
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.BI_DEVELOPER,
                interaction_type="consultation",
                frequency="Sprint",
                interface_artifact="Report Requirements & Metric Requests",
                sla_or_expectation="Turnaround < 3 days",
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=88.0,
            maturity_level="Defined",
            dimensions=[MaturityDimension(dimension_name="Consumption Simplicity", score=88.0, level="Defined", findings=["Certified metrics ready"])],
            strengths=["Standardized metric definitions", "Clear dimension conformances"],
            gaps=["Automated glossary integration"],
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
