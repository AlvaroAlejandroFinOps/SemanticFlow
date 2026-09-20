"""
Domain Owner Persona Lens.
Tailored for Business Domain Alignment, Data Product Lifecycle, and Value Realization.
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


class DomainOwnerLens(PersonaLens):
    """Business domain lens focusing on data product status, domain KPIs, and stakeholder value."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="domain_owner",
            role=PersonaRole.DOMAIN_OWNER,
            display_name="Domain Owner",
            title="Business Domain Ownership & Data Product Lifecycle Lens",
            summary_template="Domain data products, certified KPIs, business ownership, and strategic alignment for {project_name}.",
            technical_depth=TechnicalDepth.SUMMARY,
            focus_areas=[LensFocus.BUSINESS_VALUE, LensFocus.PRODUCT_LIFECYCLE],
            visible_object_types=["FACT", "KPI", "DATA_PRODUCT"],
            icon="briefcase",
            color_theme="#2C5282",
            aliases=["business_owner", "domain_lead", "product_owner"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.DOMAIN_OWNER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        primary_entities = [e.name for e in project.entities if e.role in (EntityRole.FACT, EntityRole.CALCULATED)]
        secondary_entities = [e.name for e in project.entities if e.role == EntityRole.DIMENSION]

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
                id="REC-DO-001",
                rule_id="RULE_DOMAIN_CERTIFICATION",
                title="Promote Certified Domain Metrics to Production Status",
                description="Promote verified domain-level metrics and entities to official certified status for organizational reuse.",
                impact="Increases data product trust and executive adoption.",
                effort="Low",
                suggested_action="Review domain KPIs with data governance officer for formal sign-off.",
                priority=RecommendationPriority.HIGH,
                target_objects=primary_entities,
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Domain Data Product Accountability & Business Sign-Off",
                role=RaciRole.ACCOUNTABLE,
                description="Approves semantic data product definitions and certified business KPIs.",
                collaborator_roles=[PersonaRole.DATA_ANALYST, PersonaRole.DATA_GOVERNANCE_OFFICER],
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.DATA_ANALYST,
                interaction_type="consultation",
                frequency="Sprint",
                interface_artifact="Domain Data Product Backlog",
                sla_or_expectation="Bi-weekly review",
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=89.0,
            maturity_level="Defined",
            dimensions=[MaturityDimension(dimension_name="Domain Ownership", score=89.0, level="Defined", findings=["Domain owner assigned"])],
            strengths=["Clear business accountability", "Certified core KPIs"],
            gaps=["Continuous consumer feedback telemetry"],
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
