"""
Core domain contracts and data models for the Persona Lens Framework and Data Leadership Cockpit.
"""
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from src.core.ast.canonical.models import Diagnostic, ProjectGovernance


class PersonaRole(str, Enum):
    """The 10 Standard Organizational Personas plus legacy/custom extensions."""
    ANALYTICS_LEADER = "ANALYTICS_LEADER"
    DATA_ENGINEER = "DATA_ENGINEER"
    ANALYTICS_ENGINEER = "ANALYTICS_ENGINEER"
    BI_DEVELOPER = "BI_DEVELOPER"
    DATA_GOVERNANCE_OFFICER = "DATA_GOVERNANCE_OFFICER"
    DATA_PRODUCT_MANAGER = "DATA_PRODUCT_MANAGER"
    FINOPS_SPECIALIST = "FINOPS_SPECIALIST"
    AI_SYSTEMS_ENGINEER = "AI_SYSTEMS_ENGINEER"
    BUSINESS_CONSUMER = "BUSINESS_CONSUMER"
    COMPLIANCE_AUDITOR = "COMPLIANCE_AUDITOR"
    
    # Backward compatibility and custom roles
    EXECUTIVE = "EXECUTIVE"
    ANALYTIC_CONSUMER = "ANALYTIC_CONSUMER"
    FINOPS = "FINOPS"
    CUSTOM = "CUSTOM"


class TechnicalDepth(str, Enum):
    """Level of technical detail exposed in persona projections."""
    EXECUTIVE = "EXECUTIVE"      # High-level KPIs, strategic value, zero technical jargon
    SUMMARY = "SUMMARY"          # Domain-level aggregations, data product health, key metrics
    TECHNICAL = "TECHNICAL"      # Granular entities, SQL/DAX/TMDL logic, data types, physical attributes
    EXHAUSTIVE = "EXHAUSTIVE"    # Complete AST introspection, lineage graphs, full diagnostic trace


class LensFocus(str, Enum):
    """Core focus areas for persona lenses."""
    STRATEGIC_ALIGNMENT = "STRATEGIC_ALIGNMENT"
    BUSINESS_VALUE = "BUSINESS_VALUE"
    PIPELINE_HEALTH = "PIPELINE_HEALTH"
    DATA_MODELING = "DATA_MODELING"
    MODELING_QUALITY = "MODELING_QUALITY"
    VISUALIZATION_EFFICIENCY = "VISUALIZATION_EFFICIENCY"
    GOVERNANCE_COMPLIANCE = "GOVERNANCE_COMPLIANCE"
    PRODUCT_LIFECYCLE = "PRODUCT_LIFECYCLE"
    PRODUCT_METRICS = "PRODUCT_METRICS"
    COST_CAPACITY = "COST_CAPACITY"
    AI_READINESS = "AI_READINESS"
    CONSUMPTION_SIMPLICITY = "CONSUMPTION_SIMPLICITY"
    AUDIT_TRACEABILITY = "AUDIT_TRACEABILITY"


class OverrideSafetyLevel(str, Enum):
    """Safety classification for configuration overrides."""
    SAFE = "SAFE"                          # Display names, descriptions, titles, aliases
    REVIEW_REQUIRED = "REVIEW_REQUIRED"    # Technical depth adjustments, visibility filtering
    PROHIBITED = "PROHIBITED"              # Invariant alterations (persona_id, security rules)


class RaciRole(str, Enum):
    """RACI matrix designation."""
    RESPONSIBLE = "RESPONSIBLE"
    ACCOUNTABLE = "ACCOUNTABLE"
    CONSULTED = "CONSULTED"
    INFORMED = "INFORMED"


class RecommendationPriority(str, Enum):
    """Priority level for recommendations."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ResponsibilityAssignment(BaseModel):
    """Mapping of a persona to a governance/modeling task or artifact."""
    task_or_artifact: str
    role: RaciRole
    description: Optional[str] = None
    collaborator_roles: List[PersonaRole] = Field(default_factory=list)


class TeamInteraction(BaseModel):
    """Contractual interaction between two personas across the data lifecycle."""
    target_persona: PersonaRole
    interaction_type: str  # e.g., "handoff", "review", "consultation", "approval", "service"
    frequency: str         # e.g., "Daily", "Sprint", "On-Demand", "Milestone"
    interface_artifact: str  # e.g., "Canonical Contract", "Certified KPI", "TMDL Model"
    sla_or_expectation: Optional[str] = None


class PersonaRecommendation(BaseModel):
    """Tailored actionable recommendation for a specific persona."""
    id: str
    title: str
    description: str
    priority: RecommendationPriority = RecommendationPriority.MEDIUM
    impact: str
    effort: str
    target_objects: List[str] = Field(default_factory=list)
    suggested_action: Optional[str] = None
    rule_id: Optional[str] = None


class MaturityDimension(BaseModel):
    """Individual maturity score along a specific governance or architectural vector."""
    dimension_name: str
    score: float = Field(ge=0.0, le=100.0)
    level: str  # "Initial", "Managed", "Defined", "Quantitatively Managed", "Optimizing"
    findings: List[str] = Field(default_factory=list)


class PersonaMaturityAssessment(BaseModel):
    """Aggregate maturity evaluation tailored to a persona's domain."""
    overall_score: float = Field(ge=0.0, le=100.0)
    maturity_level: str
    dimensions: List[MaturityDimension] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)


class OverrideValidationResult(BaseModel):
    """Result of classifying a configuration override against security guardrails."""
    field_name: str
    safety_level: OverrideSafetyLevel
    is_allowed: bool
    message: str
    original_value: Any = None
    proposed_value: Any = None


class PersonaDefinition(BaseModel):
    """Static and configurable definition of a Persona Lens."""
    persona_id: str
    role: PersonaRole
    display_name: str
    title: str
    summary_template: str
    technical_depth: TechnicalDepth
    focus_areas: List[LensFocus] = Field(default_factory=list)
    visible_object_types: List[str] = Field(default_factory=list)
    icon: Optional[str] = None
    color_theme: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    custom_properties: Dict[str, Any] = Field(default_factory=dict)


class PersonaProjection(BaseModel):
    """Rendered projection of the canonical semantic project through a specific Persona Lens."""
    persona_id: str
    role: PersonaRole
    title: str
    summary: str
    technical_depth: TechnicalDepth
    focus_areas: List[LensFocus] = Field(default_factory=list)
    primary_entities: List[str] = Field(default_factory=list)
    secondary_entities: List[str] = Field(default_factory=list)
    certified_metrics: List[str] = Field(default_factory=list)
    secondary_metrics: List[str] = Field(default_factory=list)
    relationships_count: int = 0
    active_relationships: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[PersonaRecommendation] = Field(default_factory=list)
    responsibilities: List[ResponsibilityAssignment] = Field(default_factory=list)
    interactions: List[TeamInteraction] = Field(default_factory=list)
    maturity_assessment: Optional[PersonaMaturityAssessment] = None
    diagnostics: List[Diagnostic] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    rendered_at: Optional[str] = None


class LeadershipCockpit(BaseModel):
    """Executive and Data Leadership Cockpit synthesizing all persona projections."""
    project_id: str
    project_name: str
    project_version: str = "1.0.0"
    generated_at: str
    executive_summary: str
    governance_overview: Dict[str, Any] = Field(default_factory=dict)
    maturity_radar: Dict[str, float] = Field(default_factory=dict)
    cross_functional_alignment: Dict[str, Any] = Field(default_factory=dict)
    priority_action_matrix: List[PersonaRecommendation] = Field(default_factory=list)
    lens_projections: Dict[str, PersonaProjection] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
