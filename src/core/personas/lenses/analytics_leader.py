"""
Analytics Leader Persona Lens.
Tailored for CDOs, VPs of Analytics, and Executive Leadership.
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


class AnalyticsLeaderLens(PersonaLens):
    """Executive Lens focusing on certified KPIs, business value, and strategic alignment."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="analytics_leader",
            role=PersonaRole.ANALYTICS_LEADER,
            display_name="Analytics Leader",
            title="Executive Strategic Analytics & Leadership Cockpit",
            summary_template="Executive portfolio perspective for {project_name} highlighting strategic KPIs and domain maturity.",
            technical_depth=TechnicalDepth.EXECUTIVE,
            focus_areas=[LensFocus.STRATEGIC_ALIGNMENT, LensFocus.BUSINESS_VALUE, LensFocus.PRODUCT_METRICS],
            visible_object_types=["FACT", "KPI"],
            icon="briefcase",
            color_theme="#1A365D",
            aliases=["executive", "cdo", "head_of_data", "vp_analytics"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.ANALYTICS_LEADER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        # Primary entities: Fact tables and calculated aggregates
        primary_entities = [e.name for e in project.entities if e.role in (EntityRole.FACT, EntityRole.CALCULATED)]
        secondary_entities = [e.name for e in project.entities if e.role == EntityRole.DIMENSION]

        # Certified KPIs
        certified_metrics = [
            m.name for e in project.entities for m in e.metrics
            if (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
        ]

        # Recommendations
        recommendations = [
            PersonaRecommendation(
                id="EXEC-01",
                title="Expand Certified Metric Coverage",
                description="Promote draft operational metrics to certified KPI status with governance board approval.",
                priority=RecommendationPriority.HIGH,
                impact="Ensures single source of truth for C-level dashboards",
                effort="Low",
                suggested_action="Review and certify unverified metrics in domain entities."
            )
        ]

        # Responsibilities
        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Enterprise Data & AI Strategy",
                role=RaciRole.ACCOUNTABLE,
                description="Sets data monetization, governance principles, and enterprise KPI taxonomy.",
                collaborator_roles=[PersonaRole.DATA_PRODUCT_MANAGER, PersonaRole.DATA_GOVERNANCE_OFFICER]
            )
        ]

        # Interactions
        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.DATA_PRODUCT_MANAGER,
                interaction_type="approval",
                frequency="Monthly",
                interface_artifact="Data Product KPI Roadmap",
                sla_or_expectation="Review and approval within 3 business days"
            ),
            TeamInteraction(
                target_persona=PersonaRole.DATA_GOVERNANCE_OFFICER,
                interaction_type="review",
                frequency="Quarterly",
                interface_artifact="Executive Compliance & Privacy Audit Report",
                sla_or_expectation="Zero unresolved critical audit findings"
            )
        ]

        # Maturity assessment
        kpi_count = len(certified_metrics)
        gov_score = 90.0 if project.governance else 65.0
        score = min(100.0, (gov_score * 0.6) + (min(kpi_count * 10, 40.0)))
        maturity = PersonaMaturityAssessment(
            overall_score=score,
            maturity_level="Optimizing" if score >= 90 else ("Defined" if score >= 75 else "Managed"),
            dimensions=[
                MaturityDimension(dimension_name="Strategic KPI Governance", score=gov_score, level="Defined", findings=[f"{kpi_count} certified KPIs"]),
                MaturityDimension(dimension_name="Domain Ownership", score=85.0, level="Managed", findings=["Project-level governance active"])
            ],
            strengths=["Established strategic focus", "Clear executive ownership"],
            gaps=["Continuous metric certification monitoring"]
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
            metadata={"domain_id": project.governance.domain_id if project.governance else None},
            rendered_at=now_iso,
        )
