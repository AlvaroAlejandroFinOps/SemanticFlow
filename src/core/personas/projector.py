"""
Deterministic, Non-Destructive Persona Projection Engine.
"""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    EntityRole,
    MetricType,
)
from src.core.personas.models import (
    LeadershipCockpit,
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
)
from src.core.personas.registry import PersonaRegistry


class PersonaProjector:
    """Projects CanonicalSemanticProject through specialized Persona Lenses deterministically."""

    def __init__(self, project: CanonicalSemanticProject, registry: Optional[PersonaRegistry] = None):
        self._project = project  # Read-only reference
        self._registry = registry or PersonaRegistry.create_default()

    @property
    def project(self) -> CanonicalSemanticProject:
        """Read-only access to the source canonical project."""
        return self._project

    @property
    def registry(self) -> PersonaRegistry:
        """Access to the persona registry."""
        return self._registry

    def project_lens(
        self,
        persona_key: Union[str, PersonaRole],
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        """Projects a single persona perspective by ID, role, or alias."""
        pid = self._registry.resolve_persona_id(persona_key)
        lens = self._registry.get_lens(pid)

        # If a custom PersonaLens class is registered, use its custom projection logic
        if lens:
            return lens.project(self._project, config=config)

        # Otherwise, run the built-in deterministic projection algorithm
        definition = self._registry.get_definition(pid)
        return self._build_deterministic_projection(definition, config)

    def project_all(self) -> Dict[str, PersonaProjection]:
        """Projects all registered personas in the registry."""
        projections: Dict[str, PersonaProjection] = {}
        for pid in self._registry.list_persona_ids():
            projections[pid] = self.project_lens(pid)
        return projections

    def build_leadership_cockpit(self) -> LeadershipCockpit:
        """Synthesizes all persona projections into an aggregate C-Level Leadership Cockpit."""
        all_projections = self.project_all()
        now_iso = datetime.now(timezone.utc).isoformat()

        # Aggregate governance overview
        total_entities = len(self._project.entities)
        total_relationships = len(self._project.relationships)

        gov = self._project.governance
        classification = gov.classification if gov else "Internal"
        data_product_status = gov.data_product_status if gov else "Draft"
        owner = gov.owner if gov else "Unassigned"

        gov_overview = {
            "data_product_status": data_product_status,
            "classification": classification,
            "executive_owner": owner,
            "entities_governed": total_entities,
            "active_relationships": total_relationships,
            "certified_kpis_count": len([
                m for e in self._project.entities for m in e.metrics
                if (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
            ]),
            "diagnostics_count": len(self._project.diagnostics),
        }

        # Aggregate maturity radar
        maturity_radar: Dict[str, float] = {}
        for pid, proj in all_projections.items():
            if proj.maturity_assessment:
                maturity_radar[proj.role.value] = proj.maturity_assessment.overall_score
            else:
                maturity_radar[proj.role.value] = 80.0

        # Aggregate priority actions
        priority_actions: List[PersonaRecommendation] = []
        for proj in all_projections.values():
            for rec in proj.recommendations:
                if rec.priority in (RecommendationPriority.CRITICAL, RecommendationPriority.HIGH):
                    priority_actions.append(rec)

        executive_summary = (
            f"Leadership Cockpit for '{self._project.name}' (v{self._project.version}). "
            f"Data Product Status: {data_product_status} ({classification}). "
            f"Encompassing {total_entities} entities, {total_relationships} relationships, "
            f"and {gov_overview['certified_kpis_count']} certified metrics across 10 active organizational domains."
        )

        return LeadershipCockpit(
            project_id=self._project.id,
            project_name=self._project.name,
            project_version=self._project.version,
            generated_at=now_iso,
            executive_summary=executive_summary,
            governance_overview=gov_overview,
            maturity_radar=maturity_radar,
            cross_functional_alignment={
                "registered_personas": len(all_projections),
                "total_responsibilities": sum(len(p.responsibilities) for p in all_projections.values()),
                "cross_domain_handoffs": sum(len(p.interactions) for p in all_projections.values()),
            },
            priority_action_matrix=priority_actions,
            lens_projections=all_projections,
            metadata={"source_project_id": self._project.id},
        )

    def _build_deterministic_projection(
        self,
        definition: PersonaDefinition,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        """Internal deterministic projector generating tailored outputs based on role and depth."""
        role = definition.role
        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Entity classification
        primary_entities: List[str] = []
        secondary_entities: List[str] = []

        if role in (PersonaRole.ANALYTICS_LEADER, PersonaRole.EXECUTIVE):
            primary_entities = [e.name for e in self._project.entities if e.role in (EntityRole.FACT, EntityRole.CALCULATED)]
            secondary_entities = [e.name for e in self._project.entities if e.role == EntityRole.DIMENSION]
        elif role == PersonaRole.DATA_ENGINEER:
            primary_entities = [e.name for e in self._project.entities if e.role in (EntityRole.FACT, EntityRole.DIMENSION, EntityRole.BRIDGE)]
        elif role == PersonaRole.ANALYTICS_ENGINEER:
            primary_entities = [e.name for e in self._project.entities]
        elif role == PersonaRole.BI_DEVELOPER:
            primary_entities = [e.name for e in self._project.entities if e.metrics or e.role == EntityRole.FACT]
            secondary_entities = [e.name for e in self._project.entities if not e.metrics]
        elif role in (PersonaRole.DATA_GOVERNANCE_OFFICER, PersonaRole.COMPLIANCE_AUDITOR):
            primary_entities = [e.name for e in self._project.entities]
        elif role == PersonaRole.DATA_PRODUCT_MANAGER:
            primary_entities = [e.name for e in self._project.entities if e.role == EntityRole.FACT]
            secondary_entities = [e.name for e in self._project.entities if e.role != EntityRole.FACT]
        elif role in (PersonaRole.FINOPS_SPECIALIST, PersonaRole.FINOPS):
            primary_entities = [
                e.name for e in self._project.entities
                if "finops" in e.name.lower() or "cost" in e.name.lower() or (e.governance and "finops" in e.governance.tags)
            ]
            if not primary_entities:
                primary_entities = [e.name for e in self._project.entities if e.role == EntityRole.FACT]
        elif role == PersonaRole.AI_SYSTEMS_ENGINEER:
            primary_entities = [
                e.name for e in self._project.entities
                if any("ai" in a.name.lower() or "score" in a.name.lower() or (a.governance and "ai_feature" in a.governance.tags) for a in e.attributes)
            ]
            if not primary_entities:
                primary_entities = [e.name for e in self._project.entities if e.role in (EntityRole.FACT, EntityRole.DIMENSION)]
        else:  # BUSINESS_CONSUMER / ANALYTIC_CONSUMER / CUSTOM
            primary_entities = [e.name for e in self._project.entities if e.role == EntityRole.FACT]
            secondary_entities = [e.name for e in self._project.entities if e.role == EntityRole.DIMENSION]

        # 2. Metric classification
        certified_metrics: List[str] = []
        secondary_metrics: List[str] = []

        for e in self._project.entities:
            for m in e.metrics:
                is_cert = (m.governance and m.governance.certification_status == "CERTIFIED") or m.metric_type == MetricType.KPI
                if is_cert:
                    certified_metrics.append(m.name)
                else:
                    secondary_metrics.append(m.name)

        # 3. Recommendations & RACI assignments tailored to role
        recommendations, responsibilities, interactions, maturity = self._build_role_artifacts(role, primary_entities, certified_metrics)

        # 4. Filter active relationships
        active_rels = [
            {"name": r.name, "from": r.from_entity_id, "to": r.to_entity_id, "cardinality": r.cardinality}
            for r in self._project.relationships if r.is_active
        ]

        summary_text = definition.summary_template.format(
            project_name=self._project.name,
            entities_count=len(primary_entities),
            metrics_count=len(certified_metrics),
        )

        return PersonaProjection(
            persona_id=definition.persona_id,
            role=definition.role,
            title=definition.title,
            summary=summary_text,
            technical_depth=definition.technical_depth,
            focus_areas=definition.focus_areas,
            primary_entities=primary_entities,
            secondary_entities=secondary_entities,
            certified_metrics=certified_metrics,
            secondary_metrics=secondary_metrics,
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=recommendations,
            responsibilities=responsibilities,
            interactions=interactions,
            maturity_assessment=maturity,
            diagnostics=list(self._project.diagnostics),
            metadata={
                "project_id": self._project.id,
                "project_version": self._project.version,
                "domain_id": self._project.governance.domain_id if self._project.governance else None,
            },
            rendered_at=now_iso,
        )

    def _build_role_artifacts(
        self,
        role: PersonaRole,
        primary_entities: List[str],
        certified_metrics: List[str],
    ) -> Tuple[List[PersonaRecommendation], List[ResponsibilityAssignment], List[TeamInteraction], PersonaMaturityAssessment]:
        """Generates tailored RACI, recommendations, interactions, and maturity assessments per persona role."""
        recs: List[PersonaRecommendation] = []
        resp: List[ResponsibilityAssignment] = []
        inter: List[TeamInteraction] = []
        dimensions: List[MaturityDimension] = []

        if role in (PersonaRole.ANALYTICS_LEADER, PersonaRole.EXECUTIVE):
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Enterprise Data & AI Strategy",
                role=RaciRole.ACCOUNTABLE,
                description="Aligns semantic definitions with C-level corporate objectives.",
                collaborator_roles=[PersonaRole.DATA_PRODUCT_MANAGER, PersonaRole.DATA_GOVERNANCE_OFFICER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.DATA_PRODUCT_MANAGER,
                interaction_type="approval",
                frequency="Monthly",
                interface_artifact="Data Product Portfolio KPI Review",
                sla_or_expectation="Sign-off within 3 business days"
            ))
            dimensions.append(MaturityDimension(dimension_name="Strategic KPI Coverage", score=90.0, level="Defined", findings=["Certified KPIs established"]))
            dimensions.append(MaturityDimension(dimension_name="Executive Alignment", score=85.0, level="Managed", findings=["Clear portfolio scope"]))
            score = 87.5

        elif role == PersonaRole.DATA_GOVERNANCE_OFFICER:
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Data Classification & Privacy Policy",
                role=RaciRole.ACCOUNTABLE,
                description="Enforces PII protection, sensitivity tags, and ownership audits.",
                collaborator_roles=[PersonaRole.COMPLIANCE_AUDITOR, PersonaRole.DATA_ENGINEER]
            ))
            recs.append(PersonaRecommendation(
                id="GOV-01",
                title="Verify Entity Ownership & Stewards",
                description="Ensure every primary entity has an assigned technical steward and business owner.",
                priority=RecommendationPriority.HIGH,
                impact="Strengthens audit readiness and data catalog accuracy",
                effort="Low",
                suggested_action="Assign stewards to unassigned entities in semantic metadata."
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.ANALYTICS_ENGINEER,
                interaction_type="review",
                frequency="Sprint",
                interface_artifact="PII and Governance Tagging Audit",
                sla_or_expectation="Tagging verified prior to production deployment"
            ))
            dimensions.append(MaturityDimension(dimension_name="Lineage & Classification", score=92.0, level="Optimizing", findings=["PII tags actively monitored"]))
            dimensions.append(MaturityDimension(dimension_name="Data Stewardship Coverage", score=88.0, level="Defined", findings=["Governance board active"]))
            score = 90.0

        elif role == PersonaRole.DATA_ENGINEER:
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Physical Ingestion & Pipeline SLAs",
                role=RaciRole.RESPONSIBLE,
                description="Guarantees upstream ingestion timeliness, partitioning, and raw data types.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.ANALYTICS_ENGINEER,
                interaction_type="handoff",
                frequency="Daily",
                interface_artifact="Clean Ingestion Staging Tables",
                sla_or_expectation="Data freshness SLA 99.9%"
            ))
            dimensions.append(MaturityDimension(dimension_name="Pipeline Health & Freshness", score=95.0, level="Optimizing", findings=["Automated ingestion"]))
            score = 95.0

        elif role == PersonaRole.ANALYTICS_ENGINEER:
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Dimensional Modeling & Semantic Metric Engine",
                role=RaciRole.RESPONSIBLE,
                description="Builds Kimball star-schemas, surrogate keys, and additive/non-additive metrics.",
                collaborator_roles=[PersonaRole.BI_DEVELOPER, PersonaRole.DATA_ENGINEER]
            ))
            recs.append(PersonaRecommendation(
                id="MOD-01",
                title="Optimize Conformed Dimensions",
                description="Verify conformed dimension grains across fact relationships.",
                priority=RecommendationPriority.MEDIUM,
                impact="Eliminates fan-out join traps and chasm traps",
                effort="Medium"
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.BI_DEVELOPER,
                interaction_type="review",
                frequency="Sprint",
                interface_artifact="TMDL Semantic Model Definition",
                sla_or_expectation="Schema validation passing before report authoring"
            ))
            dimensions.append(MaturityDimension(dimension_name="Dimensional Modeling Rigor", score=88.0, level="Defined", findings=["Kimball star schema applied"]))
            score = 88.0

        elif role == PersonaRole.BI_DEVELOPER:
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Power BI / TMDL Model & DAX Efficiency",
                role=RaciRole.RESPONSIBLE,
                description="Implements DAX measures, display folders, relationship direction, and reporting performance.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER, PersonaRole.BUSINESS_CONSUMER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.BUSINESS_CONSUMER,
                interaction_type="service",
                frequency="Sprint",
                interface_artifact="Self-Service Semantic Model & Reports",
                sla_or_expectation="Query response time < 1.5s"
            ))
            dimensions.append(MaturityDimension(dimension_name="Reporting Performance", score=91.0, level="Optimizing", findings=["Optimized DAX formulas"]))
            score = 91.0

        elif role == PersonaRole.DATA_PRODUCT_MANAGER:
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Data Product Lifecycle & Consumer Adoption",
                role=RaciRole.ACCOUNTABLE,
                description="Monitors semantic data product SLA, release cadence, and cross-team adoption metrics.",
                collaborator_roles=[PersonaRole.ANALYTICS_LEADER, PersonaRole.BUSINESS_CONSUMER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.BUSINESS_CONSUMER,
                interaction_type="consultation",
                frequency="Bi-Weekly",
                interface_artifact="Data Product Feature Backlog",
                sla_or_expectation="Consumer feedback loop established"
            ))
            dimensions.append(MaturityDimension(dimension_name="Product Maturity", score=84.0, level="Defined", findings=["Contract certified"]))
            score = 84.0

        elif role in (PersonaRole.FINOPS_SPECIALIST, PersonaRole.FINOPS):
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Semantic Query Cost & Cloud Capacity Attribution",
                role=RaciRole.RESPONSIBLE,
                description="Monitors query compute consumption, autoscaling thresholds, and cost per query.",
                collaborator_roles=[PersonaRole.DATA_ENGINEER, PersonaRole.ANALYTICS_LEADER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.DATA_ENGINEER,
                interaction_type="consultation",
                frequency="Monthly",
                interface_artifact="Cloud Cost & Capacity Telemetry Report",
                sla_or_expectation="Cost run-rate within quarterly budget"
            ))
            dimensions.append(MaturityDimension(dimension_name="Cost Efficiency & Unit Economics", score=86.0, level="Defined", findings=["Query cost tracking active"]))
            score = 86.0

        elif role == PersonaRole.AI_SYSTEMS_ENGINEER:
            resp.append(ResponsibilityAssignment(
                task_or_artifact="ML Feature Store & Training Data Provenance",
                role=RaciRole.RESPONSIBLE,
                description="Provides standardized entity features, embedding dimensions, and low-latency inference attributes.",
                collaborator_roles=[PersonaRole.ANALYTICS_ENGINEER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.ANALYTICS_ENGINEER,
                interaction_type="review",
                frequency="Sprint",
                interface_artifact="Feature Store Schema Contract",
                sla_or_expectation="Feature freshness < 1 hour"
            ))
            dimensions.append(MaturityDimension(dimension_name="AI/ML Readiness", score=82.0, level="Managed", findings=["Feature attributes tagged"]))
            score = 82.0

        elif role in (PersonaRole.BUSINESS_CONSUMER, PersonaRole.ANALYTIC_CONSUMER):
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Self-Service Business Exploration",
                role=RaciRole.INFORMED,
                description="Consumes certified KPIs and semantic dimensions to drive operational decisions.",
                collaborator_roles=[PersonaRole.BI_DEVELOPER, PersonaRole.DATA_PRODUCT_MANAGER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.BI_DEVELOPER,
                interaction_type="consultation",
                frequency="On-Demand",
                interface_artifact="Certified KPI Glossary & Dashboards"
            ))
            dimensions.append(MaturityDimension(dimension_name="Self-Service Simplicity", score=89.0, level="Optimizing", findings=["Intuitive business taxonomy"]))
            score = 89.0

        elif role == PersonaRole.COMPLIANCE_AUDITOR:
            resp.append(ResponsibilityAssignment(
                task_or_artifact="Regulatory Audit Trace & Provenance Verification",
                role=RaciRole.CONSULTED,
                description="Validates compliance with GDPR, SOX, CCPA, and verifies end-to-end data transformation provenance.",
                collaborator_roles=[PersonaRole.DATA_GOVERNANCE_OFFICER]
            ))
            inter.append(TeamInteraction(
                target_persona=PersonaRole.DATA_GOVERNANCE_OFFICER,
                interaction_type="approval",
                frequency="Milestone",
                interface_artifact="Full Compliance Audit Package & Provenance Log",
                sla_or_expectation="Audit sign-off prior to major regulatory filing"
            ))
            dimensions.append(MaturityDimension(dimension_name="Audit Traceability", score=96.0, level="Optimizing", findings=["Full provenance log maintained"]))
            score = 96.0

        else:
            score = 80.0
            dimensions.append(MaturityDimension(dimension_name="General Governance", score=80.0, level="Defined", findings=["Standard model"]))

        level = "Optimizing" if score >= 90 else ("Defined" if score >= 80 else "Managed")
        maturity = PersonaMaturityAssessment(
            overall_score=score,
            maturity_level=level,
            dimensions=dimensions,
            strengths=["Consistent semantic definitions", "Clear organizational roles"],
            gaps=["Continuous automated testing in production"]
        )

        return recs, resp, inter, maturity
