"""
Data Governance Officer Persona Lens.
Tailored for Data Stewards, Privacy Leads, and CISO Data Governance Officers.
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


class DataGovernanceOfficerLens(PersonaLens):
    """Governance & Audit Lens tracking data stewardship, PII classifications, and compliance."""

    def __init__(self, definition: Optional[PersonaDefinition] = None):
        self._definition = definition or PersonaDefinition(
            persona_id="data_governance_officer",
            role=PersonaRole.DATA_GOVERNANCE_OFFICER,
            display_name="Data Governance Officer",
            title="Data Governance, Quality & Ownership Lens",
            summary_template="Asset ownership, PII privacy boundaries, certification lifecycle, and quality scores for {project_name}.",
            technical_depth=TechnicalDepth.SUMMARY,
            focus_areas=[LensFocus.GOVERNANCE_COMPLIANCE, LensFocus.MODELING_QUALITY],
            visible_object_types=["FACT", "DIMENSION", "BRIDGE"],
            icon="shield",
            color_theme="#805AD5",
            aliases=["data_governance", "data_steward", "ciso_data_lead"],
        )

    @property
    def role(self) -> PersonaRole:
        return PersonaRole.DATA_GOVERNANCE_OFFICER

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

        # Audit PII attributes and missing owners
        pii_attrs: List[str] = []
        unassigned_entities: List[str] = []
        recommendations: List[PersonaRecommendation] = []

        for e in project.entities:
            eff_gov = project.resolve_asset_governance(e)
            if not eff_gov.owner:
                unassigned_entities.append(e.name)
            for a in e.attributes:
                eff_attr_gov = project.resolve_asset_governance(a)
                if eff_attr_gov.is_pii:
                    pii_attrs.append(f"{e.name}.{a.name}")

        if unassigned_entities:
            recommendations.append(
                PersonaRecommendation(
                    id="GOV-OWNER-01",
                    title="Assign Explicit Asset Owners",
                    description=f"Entities {unassigned_entities} lack explicit owner metadata.",
                    priority=RecommendationPriority.HIGH,
                    impact="Enables data steward accountability and escalations",
                    effort="Low",
                    target_objects=unassigned_entities,
                    suggested_action="Assign business owner email/name in project or entity governance metadata."
                )
            )
        else:
            recommendations.append(
                PersonaRecommendation(
                    id="GOV-REV-01",
                    title="Conduct Asset Ownership Re-Certification",
                    description="All primary entities have verified ownership. Conduct scheduled periodic steward reviews.",
                    priority=RecommendationPriority.LOW,
                    impact="Maintains active data stewardship and lineage validity",
                    effort="Low",
                    suggested_action="Schedule quarterly review with domain stewards."
                )
            )

        if pii_attrs:
            recommendations.append(
                PersonaRecommendation(
                    id="GOV-PII-01",
                    title="Enforce PII Masking Policies",
                    description=f"Found {len(pii_attrs)} PII fields ({', '.join(pii_attrs[:3])}...).",
                    priority=RecommendationPriority.CRITICAL,
                    impact="Mandatory for GDPR, CCPA, and ISO-27001 regulatory compliance",
                    effort="Medium",
                    target_objects=pii_attrs,
                    suggested_action="Verify column-level encryption or dynamic masking in Power BI TMDL."
                )
            )

        responsibilities = [
            ResponsibilityAssignment(
                task_or_artifact="Enterprise Data Governance & PII Classification",
                role=RaciRole.ACCOUNTABLE,
                description="Audits data sensitivity, enforces privacy tagging, approves domain certifications, and manages glossary.",
                collaborator_roles=[PersonaRole.COMPLIANCE_AUDITOR, PersonaRole.ANALYTICS_ENGINEER]
            )
        ]

        interactions = [
            TeamInteraction(
                target_persona=PersonaRole.COMPLIANCE_AUDITOR,
                interaction_type="approval",
                frequency="Milestone",
                interface_artifact="Enterprise Data Protection Audit Artifact",
                sla_or_expectation="Zero unauthorized PII exposures in production semantic datasets"
            )
        ]

        stewardship_score = 95.0 if not unassigned_entities else 70.0
        pii_score = 90.0
        overall = (stewardship_score + pii_score) / 2.0

        maturity = PersonaMaturityAssessment(
            overall_score=overall,
            maturity_level="Optimizing" if overall >= 90 else "Defined",
            dimensions=[
                MaturityDimension(dimension_name="PII & Privacy Protection", score=pii_score, level="Optimizing", findings=[f"{len(pii_attrs)} PII attributes mapped"]),
                MaturityDimension(dimension_name="Stewardship & Ownership", score=stewardship_score, level="Defined" if unassigned_entities else "Optimizing", findings=[f"{len(project.entities) - len(unassigned_entities)}/{len(project.entities)} entities owned"])
            ],
            strengths=["Two-level cascading governance model", "Automated PII detection"],
            gaps=["Continuous policy compliance verification"]
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
            metadata={
                "project_owner": project.governance.owner if project.governance else "Unassigned",
                "classification": project.governance.classification if project.governance else "Internal",
                "pii_attributes_count": len(pii_attrs),
            },
            rendered_at=now_iso,
        )
