from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class EntityRole(str, Enum):
    DIMENSION = 'DIMENSION'
    FACT = 'FACT'
    BRIDGE = 'BRIDGE'
    CALCULATED = 'CALCULATED'

class DataType(str, Enum):
    STRING = 'STRING'
    INT64 = 'INT64'
    DOUBLE = 'DOUBLE'
    DECIMAL = 'DECIMAL'
    BOOLEAN = 'BOOLEAN'
    DATETIME = 'DATETIME'
    DATE = 'DATE'

class MetricType(str, Enum):
    BASE = 'BASE'
    DERIVED = 'DERIVED'
    RATIO = 'RATIO'
    CUMULATIVE = 'CUMULATIVE'
    SNAPSHOT = 'SNAPSHOT'
    KPI = 'KPI'

class MetricAdditivity(str, Enum):
    ADDITIVE = 'ADDITIVE'
    SEMI_ADDITIVE = 'SEMI_ADDITIVE'
    NON_ADDITIVE = 'NON_ADDITIVE'

class DiagnosticSeverity(str, Enum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    RECOMMENDATION = 'RECOMMENDATION'

class DiagnosticCategory(str, Enum):
    PARSE = 'PARSE'
    CONTRACT = 'CONTRACT'
    SEMANTIC = 'SEMANTIC'
    METRIC = 'METRIC'
    GOVERNANCE = 'GOVERNANCE'
    SECURITY = 'SECURITY'
    QUALITY = 'QUALITY'
    TARGET_COMPATIBILITY = 'TARGET_COMPATIBILITY'
    EMISSION = 'EMISSION'

class ProvenanceRecord(BaseModel):
    rule_id: str
    description: str
    evidence: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    override_applied: bool = False

class Diagnostic(BaseModel):
    code: str
    severity: DiagnosticSeverity
    category: DiagnosticCategory
    message: str
    object_id: Optional[str] = None
    suggested_action: Optional[str] = None
    target: Optional[str] = None

class GovernanceMetadata(BaseModel):
    owner: Optional[str] = None
    steward: Optional[str] = None
    sensitivity_classification: Optional[str] = None
    is_pii: bool = False
    certification_status: str = 'DRAFT'
    tags: List[str] = Field(default_factory=list)

class SemanticAttribute(BaseModel):
    id: str
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    data_type: DataType = DataType.STRING
    is_hidden: bool = False
    is_key: bool = False
    source_column: Optional[str] = None
    governance: GovernanceMetadata = Field(default_factory=GovernanceMetadata)
    provenance: List[ProvenanceRecord] = Field(default_factory=list)

class SemanticMetric(BaseModel):
    id: str
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    metric_type: MetricType = MetricType.BASE
    additivity: MetricAdditivity = MetricAdditivity.ADDITIVE
    expression: str
    format_string: Optional[str] = None
    unit: Optional[str] = None
    numerator_metric_id: Optional[str] = None
    denominator_metric_id: Optional[str] = None
    governance: GovernanceMetadata = Field(default_factory=GovernanceMetadata)
    target_expressions: Dict[str, str] = Field(default_factory=dict)
    provenance: List[ProvenanceRecord] = Field(default_factory=list)

class SemanticEntity(BaseModel):
    id: str
    name: str
    role: EntityRole = EntityRole.DIMENSION
    description: Optional[str] = None
    grain: Optional[List[str]] = None
    attributes: List[SemanticAttribute] = Field(default_factory=list)
    metrics: List[SemanticMetric] = Field(default_factory=list)
    governance: GovernanceMetadata = Field(default_factory=GovernanceMetadata)
    provenance: List[ProvenanceRecord] = Field(default_factory=list)

    def get_attribute(self, attr_name: str) -> Optional[SemanticAttribute]:
        for a in self.attributes:
            if a.name.lower() == attr_name.lower():
                return a
        return None

class SemanticRelationship(BaseModel):
    id: str
    name: str
    from_entity_id: str
    from_attribute_id: str
    to_entity_id: str
    to_attribute_id: str
    cardinality: str = '1:N'
    is_active: bool = True
    provenance: List[ProvenanceRecord] = Field(default_factory=list)

class ProjectGovernance(BaseModel):
    domain_id: Optional[str] = None
    domain_name: Optional[str] = None
    classification: str = 'Internal'
    data_product_status: str = 'Draft'
    owner: Optional[str] = None
    steward: Optional[str] = None
    criticality: str = 'Medium'
    sla: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    compliance_frameworks: List[str] = Field(default_factory=list)
    asset_override_policy: str = 'ALLOW_INHERITANCE_WITH_OVERRIDES'
    custom_properties: Dict[str, Any] = Field(default_factory=dict)

class CanonicalSemanticProject(BaseModel):
    id: str
    name: str
    version: str = '1.0.0'
    description: Optional[str] = None
    governance: Optional[ProjectGovernance] = None
    entities: List[SemanticEntity] = Field(default_factory=list)
    relationships: List[SemanticRelationship] = Field(default_factory=list)
    diagnostics: List[Diagnostic] = Field(default_factory=list)
    target_extensions: Dict[str, Any] = Field(default_factory=dict)

    def get_entity(self, entity_name: str) -> Optional[SemanticEntity]:
        for e in self.entities:
            if e.name.lower() == entity_name.lower():
                return e
        return None

    def resolve_asset_governance(self, asset: Any) -> GovernanceMetadata:
        """Resolves asset governance by applying project-level defaults to unset fields."""
        asset_gov = getattr(asset, 'governance', None)
        if asset_gov is None:
            asset_gov = GovernanceMetadata()
        else:
            # Create a shallow copy to avoid mutating source model
            asset_gov = asset_gov.model_copy()

        if self.governance:
            if not asset_gov.owner and self.governance.owner:
                asset_gov.owner = self.governance.owner
            if not asset_gov.steward and self.governance.steward:
                asset_gov.steward = self.governance.steward
            if not asset_gov.sensitivity_classification and self.governance.classification:
                asset_gov.sensitivity_classification = self.governance.classification
            if self.governance.tags:
                merged_tags = list(dict.fromkeys(asset_gov.tags + self.governance.tags))
                asset_gov.tags = merged_tags

        return asset_gov
