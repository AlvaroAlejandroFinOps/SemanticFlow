"""
Collection of all 10 specialized Persona Lenses for SemanticFlow.
"""
from src.core.personas.lenses.analytics_leader import AnalyticsLeaderLens
from src.core.personas.lenses.data_engineer import DataEngineerLens
from src.core.personas.lenses.analytics_engineer import AnalyticsEngineerLens
from src.core.personas.lenses.bi_developer import BiDeveloperLens
from src.core.personas.lenses.data_governance_officer import DataGovernanceOfficerLens
from src.core.personas.lenses.data_product_manager import DataProductManagerLens
from src.core.personas.lenses.finops_specialist import FinOpsSpecialistLens
from src.core.personas.lenses.ai_systems_engineer import AiSystemsEngineerLens
from src.core.personas.lenses.business_consumer import BusinessConsumerLens
from src.core.personas.lenses.compliance_auditor import ComplianceAuditorLens
from src.core.personas.registry import PersonaRegistry


def register_all_lenses(registry: PersonaRegistry) -> None:
    """Registers instances of all 10 standard Persona Lenses into a PersonaRegistry."""
    registry.register_lens(AnalyticsLeaderLens())
    registry.register_lens(DataEngineerLens())
    registry.register_lens(AnalyticsEngineerLens())
    registry.register_lens(BiDeveloperLens())
    registry.register_lens(DataGovernanceOfficerLens())
    registry.register_lens(DataProductManagerLens())
    registry.register_lens(FinOpsSpecialistLens())
    registry.register_lens(AiSystemsEngineerLens())
    registry.register_lens(BusinessConsumerLens())
    registry.register_lens(ComplianceAuditorLens())


__all__ = [
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
]
