"""
AI Systems Engineer Persona Lens.
Tailored for Machine Learning Engineers, MLOps, and Feature Store Architects.
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


class AiSystemsEngineerLens(PersonaLens):
    """AI/ML Lens focusing on feature store readiness, embedding vectors, and model training provenance."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="ai_systems_engineer",
            role=PersonaRole.AI_SYSTEMS_ENGINEER,
            display_name="AI Systems Engineer",
            title="AI Systems, Feature Engineering & ML Readiness Lens",
            summary_template="Feature readiness, embeddings/ML attributes, training data provenance, and AI inference latency for {project_name}.",
            technical_depth=TechnicalDepth.TECHNICAL,
            focus_areas=[LensFocus.AI_READINESS, LensFocus.DATA_MODELING],
            visible_object_types=["FACT", "DIMENSION"],
            icon="cpu",
            color_theme="#E53E3E",
            aliases=["ml_engineer", "ai_engineer", "feature_store_admin"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.AI_SYSTEMS_ENGINEER

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        # Find entities with AI/ML features, embeddings, or scores
        ai_entities: List[str] = []
        ai_attributes: List[str] = []

        for e in project.entities:
            has_ai_attr = False
            for a in e.attributes:
                if "ai" in a.name.lower() or "score" in a.name.lower() or (a.governance and "ai_feature" in a.governance.tags):
                    ai_attributes.append(f"{e.name}.{a.name}")
                    has_ai_attr = True
            if has_ai_attr:
                ai_entities.append(e.name)

        if not ai_entities:
            ai_entities = [e.name for e in project.entities if e.role in (EntityRole.FACT, EntityRole.DIMENSION)]

        recommendations = [
            PersonaRecommendation(
                id="AI-01",
                title="Register Feature Store Lineage",
                description="Tag AI input features with explicit training data provenance records to support model auditability.",
                priority=RecommendationPriority.MEDIUM,
                impact="Ensures reproducibility and compliance with EU AI Act Article 10 requirements",
                effort="Low",
                target_objects=ai_attributes or ["All ML Features"],
                suggested_action="Add provenance records with confidence and source tags to AI feature attributes."
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="ML Feature Store & Training Data Lineage",
                role=RaciRole.RESPONSIBLE,
                description="Standardizes offline/online feature stores, embedding representations, and AI inference data quality.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER, PersonaRole.DATA_ENGINEER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.ANALYTICS_ENGINEER,
                interaction_type="review",
                frequency="Sprint",
                interface_artifact="Feature Store Schema Contract",
                sla_or_expectation="Feature freshness < 1 hour for real-time inference"
            )
        ]

        score = 88.0 if ai_attributes else 75.0
        maturity = PersonaMaturityAssessment(
            overall_score=score,
            maturity_level="Defined" if score >= 80 else "Managed",
            dimensions=[
                MaturityDimension(dimension_name="Feature Engineering Readiness", score=score, level="Defined", findings=[f"{len(ai_attributes)} AI/ML features mapped"]),
                MaturityDimension(dimension_name="Training Data Lineage", score=85.0, level="Defined", findings=["Provenance tracking available"])
            ],
            strengths=["Feature attributes identified in semantic catalog", "Model inference scores defined"],
            gaps=["Real-time vector database / embedding integration"]
        )

        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in project.relationships if r.is_active
        ]

        summary = self.definition.summary_template.format(
            project_name=project.name,
            entities_count=len(ai_entities),
            metrics_count=0,
        )

        return PersonaProjection(
            persona_id=self.definition.persona_id,
            role=self.role,
            title=self.definition.title,
            summary=summary,
            technical_depth=self.definition.technical_depth,
            focus_areas=self.definition.focus_areas,
            primary_entities=ai_entities,
            secondary_entities=[],
            certified_metrics=[],
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            metadata={"ai_features_count": len(ai_attributes)},
            rendered_at=now_iso,
        )
