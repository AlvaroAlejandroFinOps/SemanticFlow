"""
Configuration loader for Persona Lens definitions and organizational overrides.
"""
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import yaml

from src.core.personas.models import (
    LensFocus,
    OverrideSafetyLevel,
    OverrideValidationResult,
    PersonaDefinition,
    PersonaRole,
    TechnicalDepth,
)


class ConfigurationValidationError(Exception):
    """Raised when an invalid or prohibited configuration override is encountered."""
    pass


class PersonaConfigLoader:
    """Loads and validates Persona definitions and organizational overrides."""

    @staticmethod
    def load_from_dict(data: Dict[str, Any]) -> Dict[str, PersonaDefinition]:
        """Parses a dictionary of persona definitions into validated PersonaDefinition models."""
        personas_dict = data.get("personas", data)
        definitions: Dict[str, PersonaDefinition] = {}

        for pid, pdata in personas_dict.items():
            # Ensure persona_id is set
            if "persona_id" not in pdata:
                pdata["persona_id"] = pid

            # Coerce Enums if passed as strings
            if isinstance(pdata.get("role"), str):
                pdata["role"] = PersonaRole(pdata["role"])
            if isinstance(pdata.get("technical_depth"), str):
                pdata["technical_depth"] = TechnicalDepth(pdata["technical_depth"])
            if "focus_areas" in pdata and isinstance(pdata["focus_areas"], list):
                pdata["focus_areas"] = [
                    LensFocus(fa) if isinstance(fa, str) else fa for fa in pdata["focus_areas"]
                ]

            definition = PersonaDefinition(**pdata)
            definitions[definition.persona_id] = definition

        return definitions

    @classmethod
    def load_from_yaml(cls, yaml_path: Union[str, Path]) -> Dict[str, PersonaDefinition]:
        """Loads PersonaDefinitions from a YAML file."""
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Persona configuration file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f)

        if not raw_data or not isinstance(raw_data, dict):
            raise ConfigurationValidationError(f"Invalid YAML structure in {path}")

        return cls.load_from_dict(raw_data)

    @staticmethod
    def classify_override(field_name: str, new_value: Any) -> OverrideValidationResult:
        """Evaluates an override field against safety classifications."""
        prohibited_fields = {"persona_id", "role"}
        review_required_fields = {
            "technical_depth",
            "focus_areas",
            "visible_object_types",
            "responsibilities",
            "interactions",
        }
        safe_fields = {
            "display_name",
            "title",
            "summary_template",
            "icon",
            "color_theme",
            "aliases",
            "custom_properties",
        }

        if field_name in prohibited_fields:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.PROHIBITED,
                is_allowed=False,
                message=f"Attempted prohibited override on immutable invariant field '{field_name}'.",
                proposed_value=new_value,
            )
        elif field_name in review_required_fields:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.REVIEW_REQUIRED,
                is_allowed=True,
                message=f"Override on field '{field_name}' alters projection behavior and requires governance review.",
                proposed_value=new_value,
            )
        elif field_name in safe_fields:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.SAFE,
                is_allowed=True,
                message=f"Override on field '{field_name}' is safe.",
                proposed_value=new_value,
            )
        else:
            return OverrideValidationResult(
                field_name=field_name,
                safety_level=OverrideSafetyLevel.REVIEW_REQUIRED,
                is_allowed=True,
                message=f"Unrecognized field '{field_name}' classified as REVIEW_REQUIRED.",
                proposed_value=new_value,
            )

    @classmethod
    def apply_overrides(
        cls,
        base_definitions: Dict[str, PersonaDefinition],
        overrides_dict: Dict[str, Any],
    ) -> Tuple[Dict[str, PersonaDefinition], List[OverrideValidationResult]]:
        """
        Applies organizational overrides on top of base persona definitions.
        Raises ConfigurationValidationError on PROHIBITED overrides.
        Returns updated definitions and audit log of all applied overrides.
        """
        audit_log: List[OverrideValidationResult] = []
        updated_definitions = {k: v.model_copy(deep=True) for k, v in base_definitions.items()}

        raw_overrides = overrides_dict.get("personas", overrides_dict)

        for pid, p_overrides in raw_overrides.items():
            target_def = updated_definitions.get(pid)
            if not target_def:
                # Could be a new custom persona definition
                if "role" in p_overrides and "display_name" in p_overrides:
                    new_defs = cls.load_from_dict({pid: p_overrides})
                    updated_definitions.update(new_defs)
                    audit_log.append(
                        OverrideValidationResult(
                            field_name="new_custom_persona",
                            safety_level=OverrideSafetyLevel.REVIEW_REQUIRED,
                            is_allowed=True,
                            message=f"Added new custom persona definition: {pid}",
                            proposed_value=pid,
                        )
                    )
                    continue
                else:
                    raise ConfigurationValidationError(
                        f"Cannot override non-existent persona '{pid}' without specifying mandatory fields (role, display_name)."
                    )

            for field_name, new_value in p_overrides.items():
                if field_name == "persona_id":
                    continue

                classification = cls.classify_override(field_name, new_value)
                classification.original_value = getattr(target_def, field_name, None)
                audit_log.append(classification)

                if classification.safety_level == OverrideSafetyLevel.PROHIBITED:
                    raise ConfigurationValidationError(
                        f"PROHIBITED override error for persona '{pid}': {classification.message}"
                    )

                # Coerce values before assigning
                if field_name == "technical_depth" and isinstance(new_value, str):
                    new_value = TechnicalDepth(new_value)
                elif field_name == "focus_areas" and isinstance(new_value, list):
                    new_value = [LensFocus(fa) if isinstance(fa, str) else fa for fa in new_value]

                setattr(target_def, field_name, new_value)

        return updated_definitions, audit_log
