"""
Legacy Adapter providing 100% backward compatibility with PersonaView and PersonaType.
"""
from typing import Dict, Optional
from src.core.ast.canonical.models import CanonicalSemanticProject
from src.core.personas.models import PersonaProjection, PersonaRole
from src.core.personas.views import PersonaType, PersonaView, PersonaViewGenerator


class LegacyPersonaAdapter:
    """Adapts between modern PersonaProjection and legacy PersonaView objects."""

    @staticmethod
    def role_to_legacy_type(role: PersonaRole) -> Optional[PersonaType]:
        """Maps modern PersonaRole to legacy PersonaType enum."""
        mapping = {
            PersonaRole.ANALYTICS_LEADER: PersonaType.EXECUTIVE,
            PersonaRole.EXECUTIVE: PersonaType.EXECUTIVE,
            PersonaRole.DATA_GOVERNANCE_OFFICER: PersonaType.DATA_GOVERNANCE,
            PersonaRole.BI_DEVELOPER: PersonaType.BI_ENGINEER,
            PersonaRole.BUSINESS_CONSUMER: PersonaType.ANALYTIC_CONSUMER,
            PersonaRole.ANALYTIC_CONSUMER: PersonaType.ANALYTIC_CONSUMER,
            PersonaRole.FINOPS_SPECIALIST: PersonaType.FINOPS,
            PersonaRole.FINOPS: PersonaType.FINOPS,
        }
        return mapping.get(role)

    @staticmethod
    def legacy_type_to_role(ptype: PersonaType) -> PersonaRole:
        """Maps legacy PersonaType enum to modern PersonaRole."""
        mapping = {
            PersonaType.EXECUTIVE: PersonaRole.ANALYTICS_LEADER,
            PersonaType.DATA_GOVERNANCE: PersonaRole.DATA_GOVERNANCE_OFFICER,
            PersonaType.BI_ENGINEER: PersonaRole.BI_DEVELOPER,
            PersonaType.ANALYTIC_CONSUMER: PersonaRole.BUSINESS_CONSUMER,
            PersonaType.FINOPS: PersonaRole.FINOPS_SPECIALIST,
        }
        return mapping.get(ptype, PersonaRole.CUSTOM)

    @classmethod
    def projection_to_legacy_view(cls, projection: PersonaProjection) -> Optional[PersonaView]:
        """Converts a modern PersonaProjection into a legacy PersonaView."""
        ptype = cls.role_to_legacy_type(projection.role)
        if not ptype:
            return None

        return PersonaView(
            persona=ptype,
            title=projection.title,
            summary=projection.summary,
            primary_entities=projection.primary_entities,
            certified_metrics=projection.certified_metrics,
            metadata=projection.metadata,
        )

    @classmethod
    def generate_legacy_views(cls, project: CanonicalSemanticProject) -> Dict[PersonaType, PersonaView]:
        """Wrapper delegating to original PersonaViewGenerator."""
        return PersonaViewGenerator.generate_views(project)
