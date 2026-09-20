"""
Abstract interfaces and base contracts for the Persona Lens Framework.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.core.ast.canonical.models import CanonicalSemanticProject
from src.core.personas.models import (
    OverrideSafetyLevel,
    OverrideValidationResult,
    PersonaDefinition,
    PersonaProjection,
    PersonaRole,
)


class PersonaLens(ABC):
    """Abstract Base Class for all Persona Lenses."""

    @property
    @abstractmethod
    def role(self) -> PersonaRole:
        """The specific organizational persona role handled by this lens."""
        pass

    @property
    @abstractmethod
    def definition(self) -> PersonaDefinition:
        """The static definition and metadata for this persona lens."""
        pass

    @abstractmethod
    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        """
        Projects the Canonical Semantic Project through this Persona's unique perspective.
        Must be deterministic, side-effect free, and non-destructive.
        """
        pass

    def validate_override(self, field_name: str, new_value: Any) -> OverrideValidationResult:
        """
        Validates whether a configuration override is SAFE, REVIEW_REQUIRED, or PROHIBITED.
        """
        prohibited_fields = {"persona_id", "role"}
        review_required_fields = {
            "technical_depth",
            "focus_areas",
            "visible_object_types",
            "responsibilities",
            "interactions",
        }
        safe_fields = {"display_name", "title", "summary_template", "icon", "color_theme", "aliases", "custom_properties"}

        if field_name in prohibited_fields:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.PROHIBITED,
                is_allowed=False,
                message=f"Field '{field_name}' is an invariant and cannot be overridden by organizational config.",
                proposed_value=new_value,
            )
        elif field_name in review_required_fields:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.REVIEW_REQUIRED,
                is_allowed=True,
                message=f"Field '{field_name}' alters projection behavior; review required for governance compliance.",
                proposed_value=new_value,
            )
        elif field_name in safe_fields:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.SAFE,
                is_allowed=True,
                message=f"Field '{field_name}' is a safe cosmetic or labeling override.",
                proposed_value=new_value,
            )
        else:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.REVIEW_REQUIRED,
                is_allowed=True,
                message=f"Unrecognized field '{field_name}' classified as REVIEW_REQUIRED by default.",
                proposed_value=new_value,
            )
