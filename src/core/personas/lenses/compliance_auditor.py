"""
Compliance Auditor Persona Lens.
Tailored for Regulatory Compliance Officers, Internal Auditors, and Security Assessors.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from src.core.ast.canonical.models import CanonicalSemanticProject
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


class ComplianceAuditorLens(PersonaLens):
    """Exhaustive Audit & Compliance Lens providing full regulatory traceability."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="compliance_auditor",
            role=PersonaRole.COMPLIANCE_AUDITOR,
            display_name="Compliance Auditor",
            title="Regulatory Compliance, Privacy & Audit Traceability Lens",
            summary_template="Full regulatory audit trace, GDPR/SOX compliance verification, PII lineage, and access boundaries for {project_name}.",
            technical_depth=TechnicalDepth.EXHAUSTIVE,
            focus_areas=[LensFocus.AUDIT_TRACEABILITY, LensFocus.GOVERNANCE_COMPLIANCE],
            visible_object_types=["FACT", "DIMENSION", "BRIDGE", "CALCULATED"],
            icon="file-text",
            color_theme="#4A5568",
            aliases=["auditor", "compliance_officer", "privacy_auditor"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.COMPLIANCE_AUDITOR

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        now_iso = datetime.now(timezone.utc).isoformat()

        # Exhaustive primary entities (all entities in AST)
        primary_entities = [e.name for e in project.entities]

        gov = project.governance
        frameworks = gov.compliance_frameworks if gov else []

        recommendations = [
            PersonaRecommendation(
                id="AUD-01",
                title="Conduct Quarterly SOX/GDPR Re-Certification",
                description=f"Active compliance frameworks: {frameworks or 'None'}. Verify evidence logs and provenance timestamps.",
                priority=RecommendationPriority.HIGH,
                impact="Required to maintain regulatory certifications",
                effort="Medium",
                suggested_action="Export compliance verification bundle with golden file checksums."
            )
        ]

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Regulatory Audit Trace & Provenance Verification",
                role=RaciRole.CONSULTED,
                description="Validates compliance with GDPR, SOX, CCPA, and verifies end-to-end data transformation provenance.",
                collaborator_roles=[PersonaRole.DATA_GOVERNANCE_OFFICER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.DATA_GOVERNANCE_OFFICER,
                interaction_type="approval",
                frequency="Milestone",
                interface_artifact="Full Compliance Audit Package & Provenance Log",
                sla_or_expectation="Sign-off prior to major regulatory submission"
            )
        ]

        maturity = PersonaMaturityAssessment(
            overall_score=94.0,
            maturity_level="Optimizing",
            dimensions=[
                MaturityDimension(dimension_name="Regulatory Traceability", score=96.0, level="Optimizing", findings=[f"{len(frameworks)} compliance frameworks registered"]),
                MaturityDimension(dimension_name="Diagnostic Coverage", score=92.0, level="Optimizing", findings=[f"{len(project.diagnostics)} diagnostic rules evaluated"])
            ],
            strengths=["Complete immutable provenance logs", "Exhaustive AST inspection"],
            gaps=["Continuous automated regulatory change detection"]
        )

        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in project.relationships if r.is_active
        ]

        summary = self.definition.summary_template.format(
            project_name=project.name,
            entities_count=len(primary_entities),
            metrics_count=0,
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
            certified_metrics=[],
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            diagnostics=list(project.diagnostics),
            metadata={"compliance_frameworks": frameworks},
            rendered_at=now_iso,
        )
