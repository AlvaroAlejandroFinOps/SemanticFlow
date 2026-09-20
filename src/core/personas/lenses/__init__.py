"""
Collection of Core and Extension Persona Lenses for SemanticFlow Enterprise.
"""
from typing import TYPE_CHECKING

# 6 Extension Lenses
from src.core.personas.lenses.ai_systems_engineer import AiSystemsEngineerLens
from src.core.personas.lenses.analytics_engineer import AnalyticsEngineerLens
from src.core.personas.lenses.analytics_leader import AnalyticsLeaderLens
from src.core.personas.lenses.audit_risk import AuditRiskLens
from src.core.personas.lenses.bi_developer import BiDeveloperLens
from src.core.personas.lenses.business_consumer import BusinessConsumerLens
from src.core.personas.lenses.compliance_auditor import ComplianceAuditorLens

# 10 Core Canonical Lenses
from src.core.personas.lenses.data_analyst import DataAnalystLens
from src.core.personas.lenses.data_architect import DataArchitectLens
from src.core.personas.lenses.data_engineer import DataEngineerLens
from src.core.personas.lenses.data_governance_officer import DataGovernanceOfficerLens
from src.core.personas.lenses.data_product_manager import DataProductManagerLens
from src.core.personas.lenses.data_scientist import DataScientistLens
from src.core.personas.lenses.domain_owner import DomainOwnerLens
from src.core.personas.lenses.finops_specialist import FinOpsSpecialistLens
from src.core.personas.lenses.platform_engineer import PlatformEngineerLens

if TYPE_CHECKING:
    from src.core.personas.registry import PersonaRegistry


def register_all_lenses(registry: "PersonaRegistry") -> None:
    """Registers instances of all 10 Core Canonical Lenses + 6 Extension Lenses into a PersonaRegistry."""
    # Register 10 Core Lenses
    registry.register_lens(DataAnalystLens())
    registry.register_lens(AnalyticsEngineerLens())
    registry.register_lens(DataEngineerLens())
    registry.register_lens(DataScientistLens())
    registry.register_lens(BiDeveloperLens())
    registry.register_lens(DataArchitectLens())
    registry.register_lens(DataGovernanceOfficerLens())
    registry.register_lens(PlatformEngineerLens())
    registry.register_lens(DomainOwnerLens())
    registry.register_lens(AuditRiskLens())

    # Register 6 Extension Lenses
    registry.register_lens(AiSystemsEngineerLens())
    registry.register_lens(AnalyticsLeaderLens())
    registry.register_lens(BusinessConsumerLens())
    registry.register_lens(ComplianceAuditorLens())
    registry.register_lens(DataProductManagerLens())
    registry.register_lens(FinOpsSpecialistLens())


__all__ = [
    # 10 Core
    "DataAnalystLens",
    "AnalyticsEngineerLens",
    "DataEngineerLens",
    "DataScientistLens",
    "BiDeveloperLens",
    "DataArchitectLens",
    "DataGovernanceOfficerLens",
    "PlatformEngineerLens",
    "DomainOwnerLens",
    "AuditRiskLens",
    # 6 Extensions
    "AiSystemsEngineerLens",
    "AnalyticsLeaderLens",
    "BusinessConsumerLens",
    "ComplianceAuditorLens",
    "DataProductManagerLens",
    "FinOpsSpecialistLens",
    "register_all_lenses",
]
