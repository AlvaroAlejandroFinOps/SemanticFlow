"""
Analytics Engineer Persona Lens.
Tailored for Dimensional Modelers, dbt Developers, and Semantic Metric Authors.
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


class AnalyticsEngineerLens(PersonaLens):
    """Technical Lens focusing on star schema topology, semantic metric logic, and relationships."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="analytics_engineer",
            role=PersonaRole.ANALYTICS_ENGINEER,
            display_name="Analytics Engineer",
            title="Analytics Engineering, Dimensional Modeling & Transformation Lens",
            summary_template="Star-schema topology, semantic metrics, SQL transformations, and grain definitions for {project_name}.",
            technical_depth=TechnicalDepth.TECHNICAL,
            focus_areas=[LensFocus.DATA_MODELING, LensFocus.MODELING_QUALITY],
            visible_object_types=["FACT", "DIMENSION", "BRIDGE", "CALCULATED"],
            icon="code",
            color_theme="#319795",
            aliases=["ae", "dbt_developer", "semantic_modeler"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.ANALYTICS_ENGINEER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        primary_entities = [e.name for e in project.entities]
        
        all_metrics = [m.name for e in project.entities for m in e.metrics]
        certified_metrics = [
            m.name for e in project.entities for m in e.metrics
            if (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
        ]
        secondary_metrics = [m for m in all_metrics if m not in certified_metrics]

        # Recommendations on metric expressions and target dialect coverage
        recommendations: List[PersonaRecommendation] = []
        for e in project.entities:
            for m in e.metrics:
                if not m.target_expressions or "dax" not in m.target_expressions:
                    recommendations.append(
                        PersonaRecommendation(
                            id=f"AE-TGT-{m.id}",
                            title=f"Add Native Target Expression for {m.name}",
                            description=f"Metric '{m.name}' has generic formula but lacks compiled DAX target expression.",
                            priority=RecommendationPriority.LOW,
                            impact="Accelerates Power BI compilation and prevents runtime translation fallback",
                            effort="Low",
                            target_objects=[m.name]
                        )
                    )

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Dimensional Modeling & Semantic Metrics",
                role=RaciRole.RESPONSIBLE,
                description="Authors clean star schemas, conformed dimensions, metric formulas, and grain invariants.",
                collaborator_roles=[PersonaRole.DATA_ENGINEER, PersonaRole.BI_DEVELOPER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.BI_DEVELOPER,
                interaction_type="review",
                frequency="Sprint",
                interface_artifact="TMDL Semantic Data Model Definition",
                sla_or_expectation="Review and validate DAX measures before report deployment"
            )
        ]

        metric_coverage = 92.0 if all_metrics else 70.0
        rel_coverage = 90.0 if project.relationships else 60.0
        overall = (metric_coverage + rel_coverage) / 2.0

        maturity = PersonaMaturityAssessment(
            overall_score=overall,
            maturity_level="Optimizing" if overall >= 90 else "Defined",
            dimensions=[
                MaturityDimension(dimension_name="Star Schema Conformance", score=rel_coverage, level="Defined", findings=[f"{len(project.relationships)} active relationships"]),
                MaturityDimension(dimension_name="Metric Formalization", score=metric_coverage, level="Optimizing", findings=[f"{len(all_metrics)} metrics defined"])
            ],
            strengths=["Explicit relationships between fact and dimensions", "Multi-dialect metric support"],
            gaps=["Document complex ratio metric calculations in markdown schema"]
        )

        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in project.relationships if r.is_active
        ]

        summary = self.definition.summary_template.format(
            project_name=project.name,
            entities_count=len(primary_entities),
            metrics_count=len(all_metrics),
        )

        return PersonaProjection(
            persona_id=self.definition.persona_id,
            role=self.role,
            title=self.definition.title,
            summary=summary,
            technical_depth=self.definition.technical_depth,
            focus_areas=self.definition.focus_areas,
            primary_entities=primary_entities,
            secondary_entities=[],
            certified_metrics=certified_metrics,
            secondary_metrics=secondary_metrics,
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            diagnostics=list(project.diagnostics),
            rendered_at=now_iso,
        )
