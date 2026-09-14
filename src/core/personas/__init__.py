"""
SemanticFlow Persona Lens Framework and Data Leadership Cockpit.
"""
from src.core.personas.models import (
    PersonaRole,
    TechnicalDepth,
    LensFocus,
    OverrideSafetyLevel,
    RaciRole,
    RecommendationPriority,
    ResponsibilityAssignment,
    TeamInteraction,
    PersonaRecommendation,
    MaturityDimension,
    PersonaMaturityAssessment,
    OverrideValidationResult,
    PersonaDefinition,
    PersonaProjection,
    LeadershipCockpit,
)
from src.core.personas.interfaces import PersonaLens
from src.core.personas.config_loader import (
    PersonaConfigLoader,
    ConfigurationValidationError,
)
from src.core.personas.registry import (
    PersonaRegistry,
    PersonaNotFoundError,
)
from src.core.personas.projector import PersonaProjector
from src.core.personas.cockpit import DataLeadershipCockpitEngine
from src.core.personas.renderers import (
    MarkdownPersonaRenderer,
    JsonPersonaRenderer,
    MermaidPersonaRenderer,
    LeadershipCockpitRenderer,
)
from src.core.personas.lenses import (
    AnalyticsLeaderLens,
    DataEngineerLens,
    AnalyticsEngineerLens,
    BiDeveloperLens,
    DataGovernanceOfficerLens,
    DataProductManagerLens,
    FinOpsSpecialistLens,
    AiSystemsEngineerLens,
    BusinessConsumerLens,
    ComplianceAuditorLens,
    register_all_lenses,
)
from src.core.personas.legacy_adapter import LegacyPersonaAdapter
from src.core.personas.views import (
    PersonaType,
    PersonaView,
    PersonaViewGenerator,
)

__all__ = [
    # Modern Domain Enums & Models
    "PersonaRole",
    "TechnicalDepth",
    "LensFocus",
    "OverrideSafetyLevel",
    "RaciRole",
    "RecommendationPriority",
    "ResponsibilityAssignment",
    "TeamInteraction",
    "PersonaRecommendation",
    "MaturityDimension",
    "PersonaMaturityAssessment",
    "OverrideValidationResult",
    "PersonaDefinition",
    "PersonaProjection",
    "LeadershipCockpit",
    # Interfaces
    "PersonaLens",
    # Registry & Config
    "PersonaRegistry",
    "PersonaNotFoundError",
    "PersonaConfigLoader",
    "ConfigurationValidationError",
    # Projector & Cockpit Engine
    "PersonaProjector",
    "DataLeadershipCockpitEngine",
    # Renderers
    "MarkdownPersonaRenderer",
    "JsonPersonaRenderer",
    "MermaidPersonaRenderer",
    "LeadershipCockpitRenderer",
    # Concrete Lenses
    "AnalyticsLeaderLens",
    "DataEngineerLens",
    "AnalyticsEngineerLens",
    "BiDeveloperLens",
    "DataGovernanceOfficerLens",
    "DataProductManagerLens",
    "FinOpsSpecialistLens",
    "AiSystemsEngineerLens",
    "BusinessConsumerLens",
    "ComplianceAuditorLens",
    "register_all_lenses",
    # Legacy Adapter & Backward Compatibility
    "LegacyPersonaAdapter",
    "PersonaType",
    "PersonaView",
    "PersonaViewGenerator",
]
