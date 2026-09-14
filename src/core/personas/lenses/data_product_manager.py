"""
Data Product Manager Persona Lens.
Tailored for Data Product Owners, Value Stream Leads, and Domain Owners.
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


class DataProductManagerLens(PersonaLens):
    """Product & Value Stream Lens tracking data product release lifecycle, SLAs, and consumer value."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="data_product_manager",
            role=PersonaRole.DATA_PRODUCT_MANAGER,
            display_name="Data Product Manager",
            title="Data Product Management, Lifecycle & Consumer Value Lens",
            summary_template="Data product SLA, consumer adoption contracts, release maturity, and product telemetry for {project_name}.",
            technical_depth=TechnicalDepth.SUMMARY,
            focus_areas=[LensFocus.PRODUCT_LIFECYCLE, LensFocus.PRODUCT_METRICS, LensFocus.BUSINESS_VALUE],
            visible_object_types=["FACT", "DIMENSION"],
            icon="layers",
            color_theme="#DD6B20",
            aliases=["dpm", "product_owner_data"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.DATA_PRODUCT_MANAGER

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
        secondary_entities = [e.name for e in project.entities if e.role != EntityRole.FACT]

        certified_metrics = [
            m.name for e in project.entities for m in e.metrics
            if (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
        ]

        gov = project.governance
        product_status = gov.data_product_status if gov else "Draft"
        sla_val = gov.sla if gov else "No SLA committed"

        recommendations = [
            PersonaRecommendation(
                id="DPM-01",
                title="Publish Consumer SLA Contract",
                description=f"Current product status is '{product_status}'. Ensure consumer SLA is documented in data product metadata.",
                priority=RecommendationPriority.MEDIUM,
                impact="Guarantees consumer trust and establishes operational SLOs",
                effort="Low",
                suggested_action="Document query latency and freshness SLAs in project governance."
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Data Product Lifecycle & Consumer SLA",
                role=RaciRole.ACCOUNTABLE,
                description="Defines data product boundary, versioning cadence, consumer contracts, and feature enhancements.",
                collaborator_roles=[PersonaRole.ANALYTICS_LEADER, PersonaRole.BUSINESS_CONSUMER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.BUSINESS_CONSUMER,
                interaction_type="consultation",
                frequency="Bi-Weekly",
                interface_artifact="Data Product Consumer Feedback & Usage Telemetry",
                sla_or_expectation="Incorporate user feedback into quarterly roadmap"
            )
        ]

        status_score = 95.0 if product_status == "Certified" else (80.0 if product_status == "Candidate" else 65.0)
        maturity = PersonaMaturityAssessment(
            overall_score=status_score,
            maturity_level="Optimizing" if status_score >= 90 else "Defined",
            dimensions=[
                MaturityDimension(dimension_name="Product Lifecycle Status", score=status_score, level="Defined", findings=[f"Status: {product_status}"]),
                MaturityDimension(dimension_name="SLA Commitment", score=90.0 if gov and gov.sla else 60.0, level="Defined", findings=[f"SLA: {sla_val}"])
            ],
            strengths=["Data product concept applied", "Explicit domain attribution"],
            gaps=["Automated usage analytics integration"]
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
            metadata={
                "data_product_status": product_status,
                "sla": sla_val,
            },
            rendered_at=now_iso,
        )
