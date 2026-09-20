"""
Data Architect Persona Lens.
Tailored for Enterprise Information Architecture, Domain Boundaries, and Multi-Platform Topologies.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.core.ast.canonical.models import CanonicalSemanticProject, MetricType
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


class DataArchitectLens(PersonaLens):
    """Lens for Enterprise Data Architects focusing on data modeling patterns and scalability."""

    def __init__(self) -> None:
        self._definition = PersonaDefinition(
            persona_id="data_architect",
            role=PersonaRole.DATA_ARCHITECT,
            display_name="Data Architect",
            title="Enterprise Data Architecture & Domain Modeling Lens",
            summary_template="Relational graph topology, domain conformances, entity lifecycle, and architectural standards for {project_name}.",
            technical_depth=TechnicalDepth.EXHAUSTIVE,
            focus_areas=[LensFocus.DATA_MODELING, LensFocus.MODELING_QUALITY, LensFocus.STRATEGIC_ALIGNMENT],
            visible_object_types=["entities", "relationships", "governance", "lineage"],
            icon="server-network",
            color_theme="#673AB7",
            aliases=["architect", "enterprise_architect", "solution_architect"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.DATA_ARCHITECT

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        primary_entities: List[str] = [e.name for e in project.entities]
        secondary_entities: List[str] = []

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
                id="REC-ARCH-001",
                rule_id="RULE_CANONICAL_NEUTRALITY",
                title="Maintain Canonical Semantic Model Vendor Neutrality",
                description="Preserve semantic neutrality across entities and relationships to avoid proprietary lock-in.",
                impact="Ensures semantic model remains portable across Power BI, Looker, and dbt.",
                effort="Low",
                suggested_action="Verify no platform-specific DAX logic is embedded into canonical definitions.",
                priority=RecommendationPriority.HIGH,
                target_objects=primary_entities,
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Enterprise Semantic Blueprint & Domain Conformity",
                role=RaciRole.ACCOUNTABLE,
                description="Governs semantic entities, relationships DAG, and cross-domain conformance.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER, PersonaRole.DATA_GOVERNANCE_OFFICER],
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.DATA_GOVERNANCE_OFFICER,
                interaction_type="review",
                frequency="Monthly",
                interface_artifact="Domain Architecture Review Package",
                sla_or_expectation="Zero architecture standard violations",
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=92.0,
            maturity_level="Optimizing",
            dimensions=[MaturityDimension(dimension_name="Architecture Coherence", score=92.0, level="Optimizing", findings=["Canonical model decoupled"])],
            strengths=["Vendor-neutral AST representation", "Strict DAG relationship validation"],
            gaps=["Cross-workspace semantic federation"],
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
