"""
FinOps Specialist Persona Lens.
Tailored for Cloud Economists, Capacity Planners, and Semantic Compute FinOps Leads.
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


class FinOpsSpecialistLens(PersonaLens):
    """Cost & Capacity Lens tracking query consumption, compute costs, and resource efficiency."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="finops_specialist",
            role=PersonaRole.FINOPS_SPECIALIST,
            display_name="FinOps Specialist",
            title="FinOps, Cloud Cost & Capacity Optimization Lens",
            summary_template="Analytical query efficiency, cloud resource consumption, and cost attribution for {project_name}.",
            technical_depth=TechnicalDepth.SUMMARY,
            focus_areas=[LensFocus.COST_CAPACITY, LensFocus.BUSINESS_VALUE],
            visible_object_types=["FACT", "DIMENSION"],
            icon="dollar-sign",
            color_theme="#38A169",
            aliases=["finops", "cloud_economist"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.FINOPS_SPECIALIST

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        # Find FinOps entities / cost facts
        finops_entities = [
            e.name for e in project.entities
            if "finops" in e.name.lower() or "cost" in e.name.lower() or (e.governance and "finops" in e.governance.tags)
        ]
        if not finops_entities:
            finops_entities = [e.name for e in project.entities if e.role == EntityRole.FACT]

        finops_metrics = [
            m.name for e in project.entities for m in e.metrics
            if "cost" in m.name.lower() or "compute" in m.name.lower() or (m.governance and "finops" in m.governance.tags)
        ]

        recommendations = [
            PersonaRecommendation(
                id="FIN-01",
                title="Establish Cost Attribution Tags",
                description="Attach cost_center and business_unit metadata to semantic entities to enable granular FinOps chargeback.",
                priority=RecommendationPriority.MEDIUM,
                impact="Enables showback/chargeback to consuming business departments",
                effort="Low",
                suggested_action="Configure custom_properties with cost_center in project governance."
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Semantic Query Cost & Cloud Attribution",
                role=RaciRole.RESPONSIBLE,
                description="Tracks analytical query costs, identifies expensive Cartesian DAX/SQL queries, and allocates cloud capacity.",
                collaborator_roles=[PersonaRole.DATA_ENGINEER, PersonaRole.ANALYTICS_LEADER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.DATA_ENGINEER,
                interaction_type="consultation",
                frequency="Monthly",
                interface_artifact="Cloud Cost & Capacity Telemetry Report",
                sla_or_expectation="Cost run-rate within quarterly budget limits"
            )
        ]

        cost_tracking_active = bool(finops_metrics)
        score = 88.0 if cost_tracking_active else 72.0
        maturity = PersonaMaturityAssessment(
            overall_score=score,
            maturity_level="Defined" if score >= 80 else "Managed",
            dimensions=[
                MaturityDimension(dimension_name="Cost Transparency", score=score, level="Defined", findings=[f"{len(finops_metrics)} cost telemetry metrics"]),
                MaturityDimension(dimension_name="Capacity Governance", score=85.0, level="Defined", findings=["Resource limits established"])
            ],
            strengths=["Unit economics metrics present", "Cost center alignment"],
            gaps=["Real-time query cost telemetry pipeline"]
        )

        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in project.relationships if r.is_active
        ]

        summary = self.definition.summary_template.format(
            project_name=project.name,
            entities_count=len(finops_entities),
            metrics_count=len(finops_metrics),
        )

        return PersonaProjection(
            persona_id=self.definition.persona_id,
            role=self.role,
            title=self.definition.title,
            summary=summary,
            technical_depth=self.definition.technical_depth,
            focus_areas=self.definition.focus_areas,
            primary_entities=finops_entities,
            secondary_entities=[],
            certified_metrics=finops_metrics,
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            rendered_at=now_iso,
        )
