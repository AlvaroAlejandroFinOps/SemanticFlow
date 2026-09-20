"""
Audit & Risk Persona Lens.
Tailored for Regulatory Compliance, Exception Tracking, Provenance Auditing, and Risk Management.
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


class AuditRiskLens(PersonaLens):
    """Compliance and risk lens focusing on regulatory audit trails, provenance, and exceptions."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="audit_risk",
            role=PersonaRole.AUDIT_RISK,
            display_name="Audit & Risk Officer",
            title="Regulatory Compliance, Audit Provenance & Risk Lens",
            summary_template="Regulatory compliance (GDPR/SOX), provenance audit trail, and risk exceptions for {project_name}.",
            technical_depth=TechnicalDepth.EXHAUSTIVE,
            focus_areas=[LensFocus.AUDIT_TRACEABILITY, LensFocus.GOVERNANCE_COMPLIANCE],
            visible_object_types=["FACT", "DIMENSION", "CLASSIFICATION", "PROVENANCE", "EXCEPTION"],
            icon="shield",
            color_theme="#C53030",
            aliases=["risk_officer", "compliance_officer", "auditor"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.AUDIT_RISK

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
                id="REC-RISK-001",
                rule_id="RULE_PROVENANCE_AUDIT",
                title="Verify Complete End-to-End Transformation Provenance",
                description="Verify end-to-end transformation provenance logs to support statutory audits and compliance checks.",
                impact="Guarantees full audit defense and regulatory compliance for financial metrics.",
                effort="Medium",
                suggested_action="Ensure all calculated metrics retain provenance records to source columns.",
                priority=RecommendationPriority.HIGH,
                target_objects=primary_entities,
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Regulatory Audit Traceability & Risk Exception Governance",
                role=RaciRole.ACCOUNTABLE,
                description="Governs regulatory compliance (GDPR, SOX), provenance logs, and risk exceptions.",
                collaborator_roles=[PersonaRole.DATA_GOVERNANCE_OFFICER, PersonaRole.DATA_ARCHITECT],
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.DATA_GOVERNANCE_OFFICER,
                interaction_type="approval",
                frequency="Milestone",
                interface_artifact="Regulatory Compliance Audit Package",
                sla_or_expectation="Sign-off prior to major production release",
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=94.0,
            maturity_level="Optimizing",
            dimensions=[MaturityDimension(dimension_name="Audit Traceability", score=94.0, level="Optimizing", findings=["Full provenance log maintained"])],
            strengths=["Complete rule provenance records", "Strict PII boundary enforcement"],
            gaps=["Automated compliance change logging"],
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
