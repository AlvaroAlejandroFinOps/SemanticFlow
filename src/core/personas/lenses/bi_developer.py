"""
BI Developer Persona Lens.
Tailored for Power BI Modelers, DAX Authors, and Semantic Report Designers.
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


class BiDeveloperLens(PersonaLens):
    """Technical Lens focusing on Power BI / TMDL semantic models, DAX measures, and reporting."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="bi_developer",
            role=PersonaRole.BI_DEVELOPER,
            display_name="BI Developer",
            title="BI Developer, TMDL & Semantic Model Consumption Lens",
            summary_template="Power BI / TMDL semantic measures, relationships, DAX formulas, and display folders for {project_name}.",
            technical_depth=TechnicalDepth.TECHNICAL,
            focus_areas=[LensFocus.VISUALIZATION_EFFICIENCY, LensFocus.DATA_MODELING],
            visible_object_types=["FACT", "DIMENSION", "CALCULATED"],
            icon="pie-chart",
            color_theme="#D69E2E",
            aliases=["bi_engineer", "powerbi_developer", "tableau_developer"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.BI_DEVELOPER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        primary_entities = [e.name for e in project.entities if e.metrics or e.role == EntityRole.FACT]
        secondary_entities = [e.name for e in project.entities if not e.metrics and e.role != EntityRole.FACT]

        all_metrics = [m.name for e in project.entities for m in e.metrics]

        # Recommendations on format strings and display folders
        recommendations: List[PersonaRecommendation] = []
        for e in project.entities:
            for m in e.metrics:
                if not m.format_string:
                    recommendations.append(
                        PersonaRecommendation(
                            id=f"BI-FMT-{m.id}",
                            title=f"Specify Format String for Measure {m.name}",
                            description=f"Measure '{m.name}' lacks a format_string (e.g. '$#,##0.00' or '0.0%').",
                            priority=RecommendationPriority.MEDIUM,
                            impact="Ensures uniform formatting in Power BI visual canvases",
                            effort="Low",
                            target_objects=[m.name]
                        )
                    )

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="TMDL Semantic Model & Report Canvases",
                role=RaciRole.RESPONSIBLE,
                description="Generates PBIP/TMDL models, optimizes DAX measures, formats numbers, and maintains visual dashboards.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER, PersonaRole.BUSINESS_CONSUMER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.BUSINESS_CONSUMER,
                interaction_type="service",
                frequency="Sprint",
                interface_artifact="Interactive Power BI Dashboards & Semantic Datasets",
                sla_or_expectation="Sub-second query visual render performance"
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=90.0,
            maturity_level="Optimizing",
            dimensions=[
                MaturityDimension(dimension_name="TMDL/PowerBI Compatibility", score=95.0, level="Optimizing", findings=["Native PBIP target emitter supported"]),
                MaturityDimension(dimension_name="Measure Definition Quality", score=85.0, level="Defined", findings=[f"{len(all_metrics)} measures in model"])
            ],
            strengths=["Clean separation of measures and dimensions", "Deterministic TMDL emission"],
            gaps=["Add automated DAX query performance tests"]
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
            secondary_entities=secondary_entities,
            certified_metrics=all_metrics,
            secondary_metrics=[],
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            diagnostics=list(project.diagnostics),
            rendered_at=now_iso,
        )
