"""
Data Scientist Persona Lens.
Tailored for Feature Engineering, Statistical Analysis, and Machine Learning Model Inputs.
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


class DataScientistLens(PersonaLens):
    """Machine learning and statistical lens focusing on analytical features and data distributions."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="data_scientist",
            role=PersonaRole.DATA_SCIENTIST,
            display_name="Data Scientist",
            title="Data Science, Feature Engineering & Statistical Lens",
            summary_template="Analytical features, continuous variables, entity grains, and training dimensions for {project_name}.",
            technical_depth=TechnicalDepth.TECHNICAL,
            focus_areas=[LensFocus.AI_READINESS, LensFocus.DATA_MODELING],
            visible_object_types=["FACT", "DIMENSION", "FEATURE"],
            icon="activity",
            color_theme="#805AD5",
            aliases=["ds", "ml_scientist", "statistician"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.DATA_SCIENTIST

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        primary_entities = [e.name for e in project.entities if e.role in (EntityRole.FACT, EntityRole.DIMENSION)]
        secondary_entities = [e.name for e in project.entities if e.role == EntityRole.BRIDGE]

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
                id="REC-DS-001",
                rule_id="RULE_FEATURE_DISTRIBUTION",
                title="Verify Feature Cardinality and Numerical Grain",
                description="Verify entity grain definitions and numerical distributions match expected machine learning feature formats.",
                impact="Improves convergence and feature consistency in ML training pipelines.",
                effort="Medium",
                suggested_action="Ensure entity grain definitions match expected feature vector dimensions.",
                priority=RecommendationPriority.MEDIUM,
                target_objects=primary_entities,
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Predictive Feature Formulation & Statistical Verification",
                role=RaciRole.RESPONSIBLE,
                description="Formulates analytical features and evaluates statistical distributions from semantic entities.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER, PersonaRole.DATA_ENGINEER],
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.ANALYTICS_ENGINEER,
                interaction_type="collaboration",
                frequency="Sprint",
                interface_artifact="Feature Definition Contract",
                sla_or_expectation="Feature pipeline alignment",
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=85.0,
            maturity_level="Defined",
            dimensions=[MaturityDimension(dimension_name="Feature Engineering Readiness", score=85.0, level="Defined", findings=["Entities mapped"])],
            strengths=["Consistent grain definitions", "Clean categorical dimensions"],
            gaps=["Automated feature store synchronization"],
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
