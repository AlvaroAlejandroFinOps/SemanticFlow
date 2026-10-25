"""
Persona Registry managing built-in and customized Persona Lenses.
"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from src.core.personas.config_loader import PersonaConfigLoader
from src.core.personas.interfaces import PersonaLens
from src.core.personas.models import (
    OverrideValidationResult,
    PersonaDefinition,
    PersonaRole,
    TechnicalDepth,
)


class PersonaNotFoundError(KeyError):
    """Raised when an unrecognized persona ID, role, or alias is requested."""
    pass


class PersonaRegistry:
    """Central registry of all available Persona Lenses with alias resolution."""

    def __init__(self):
        self._lenses: Dict[str, PersonaLens] = {}
        self._definitions: Dict[str, PersonaDefinition] = {}
        self._alias_map: Dict[str, str] = {}
        self._override_audit_trail: List[OverrideValidationResult] = []

    def register_definition(self, definition: PersonaDefinition) -> None:
        """Registers a PersonaDefinition and maps all its aliases."""
        pid = definition.persona_id.lower()
        self._definitions[pid] = definition

        # Map role name and ID
        self._alias_map[pid] = pid
        self._alias_map[definition.role.value.lower()] = pid

        # Map explicit aliases
        for alias in definition.aliases:
            self._alias_map[alias.lower()] = pid

    def register_lens(self, lens: PersonaLens) -> None:
        """Registers a concrete PersonaLens instance."""
        pid = lens.definition.persona_id.lower()
        self._lenses[pid] = lens
        self.register_definition(lens.definition)

    def resolve_persona_id(self, key: Union[str, PersonaRole]) -> str:
        """Resolves an alias, role string, or PersonaRole enum to its canonical persona_id."""
        if isinstance(key, PersonaRole):
            key_str = key.value.lower()
        else:
            key_str = str(key).strip().lower()

        if key_str in self._alias_map:
            return self._alias_map[key_str]

        # Check if directly in definitions
        if key_str in self._definitions:
            return key_str

        raise PersonaNotFoundError(f"No persona found matching key, role or alias: '{key}'")

    def get_definition(self, key: Union[str, PersonaRole]) -> PersonaDefinition:
        """Retrieves the PersonaDefinition for a given key or alias."""
        pid = self.resolve_persona_id(key)
        return self._definitions[pid]

    def get_lens(self, key: Union[str, PersonaRole]) -> Optional[PersonaLens]:
        """Retrieves the registered PersonaLens instance if registered."""
        pid = self.resolve_persona_id(key)
        return self._lenses.get(pid)

    def list_persona_ids(self) -> List[str]:
        """Returns a sorted list of all canonical persona IDs."""
        return sorted(list(self._definitions.keys()))

    def list_definitions(self) -> List[PersonaDefinition]:
        """Returns all registered PersonaDefinition objects."""
        return [self._definitions[pid] for pid in self.list_persona_ids()]

    def list_aliases(self) -> Dict[str, str]:
        """Returns the full alias mapping dictionary."""
        return dict(self._alias_map)

    def load_overrides(self, overrides: Union[Dict[str, Any], str, Path]) -> List[OverrideValidationResult]:
        """
        Loads and applies configuration overrides.
        Validates safety levels (SAFE, REVIEW_REQUIRED, PROHIBITED).
        """
        if isinstance(overrides, (str, Path)):
            import yaml
            with open(overrides, "r", encoding="utf-8") as f:
                overrides_data = yaml.safe_load(f)
        else:
            overrides_data = overrides

        updated_defs, audit_log = PersonaConfigLoader.apply_overrides(
            self._definitions, overrides_data
        )

        for definition in updated_defs.values():
            self.register_definition(definition)

        self._override_audit_trail.extend(audit_log)
        return audit_log

    def load_company_lenses(
        self, lenses_dir: Path, company_id: Optional[str] = None
    ) -> List[Any]:
        """
        Loads company-specific declarative lenses and overrides from a directory.
        Performs boundary isolation, secret scanning, and schema validation.
        """
        import json
        import jsonschema
        import yaml
        from src.core.personas.declarative_lens import DeclarativeDomainLens
        from src.core.security.sanitize import resolve_within, safe_filename
        from src.core.security.secret_scanner import scan_file_for_secrets

        if not lenses_dir or not Path(lenses_dir).exists() or not Path(lenses_dir).is_dir():
            return []

        lenses_path = Path(lenses_dir)
        loaded_lenses: List[DeclarativeDomainLens] = []

        schema_path = Path("schemas/persona_definition.schema.json")
        schema_data = None
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as sf:
                schema_data = json.load(sf)

        candidate_files = sorted(
            list(lenses_path.glob("*.yaml")) + list(lenses_path.glob("*.yml")),
            key=lambda p: p.name.lower()
        )

        banned_property_substrings = ("password", "secret", "token", "credential", "api_key")

        for c_file in candidate_files:
            safe_file = resolve_within(lenses_path, c_file)
            _ = safe_filename(safe_file.name)

            if safe_file.name.lower() in ("overrides.yaml", "overrides.yml"):
                continue

            findings = scan_file_for_secrets(safe_file)
            if findings:
                raise PermissionError(
                    f"Violación de seguridad: secretos detectados en archivo de lente '{safe_file.name}': "
                    f"{[f.rule_id for f in findings]}"
                )

            with open(safe_file, "r", encoding="utf-8") as lf:
                lens_data = yaml.safe_load(lf)

            if not isinstance(lens_data, dict):
                continue

            for key in lens_data.keys():
                low_key = key.lower()
                if any(banned in low_key for banned in banned_property_substrings):
                    raise PermissionError(
                        f"Propiedad sensible no autorizada '{key}' detectada en lente '{safe_file.name}'."
                    )

            if schema_data and "persona_id" in lens_data:
                validation_copy = dict(lens_data)
                if "role" not in validation_copy:
                    validation_copy["role"] = "CUSTOM"
                if "display_name" not in validation_copy:
                    validation_copy["display_name"] = validation_copy.get(
                        "name", str(validation_copy["persona_id"]).replace("_", " ").title()
                    )
                if "title" not in validation_copy:
                    validation_copy["title"] = f"{validation_copy['display_name']} Perspective"
                if "technical_depth" not in validation_copy:
                    validation_copy["technical_depth"] = "SUMMARY"
                jsonschema.validate(instance=validation_copy, schema=schema_data)

            if company_id:
                lens_data["company_id"] = company_id
            if "scope" not in lens_data:
                lens_data["scope"] = "company_custom"

            lens = DeclarativeDomainLens(lens_data, filepath=safe_file)
            self.register_lens(lens)
            loaded_lenses.append(lens)

        for ov_name in ("overrides.yaml", "overrides.yml"):
            ov_path = lenses_path / ov_name
            if ov_path.exists():
                safe_ov = resolve_within(lenses_path, ov_path)
                findings = scan_file_for_secrets(safe_ov)
                if findings:
                    raise PermissionError(
                        f"Violación de seguridad: secretos detectados en '{safe_ov.name}': "
                        f"{[f.rule_id for f in findings]}"
                    )
                self.load_overrides(safe_ov)

        return loaded_lenses

    @property
    def override_audit_trail(self) -> List[OverrideValidationResult]:
        """Returns all overrides validated and applied during the registry's lifecycle."""
        return list(self._override_audit_trail)

    @classmethod
    def create_default(cls, default_yaml_path: Optional[Union[str, Path]] = None) -> "PersonaRegistry":
        """Factory creating a registry pre-loaded with standard 10 Persona definitions and lenses."""
        registry = cls()

        # 1. Register concrete lenses
        from src.core.personas.lenses import register_all_lenses
        register_all_lenses(registry)

        # 2. Load YAML configuration if provided or present
        if default_yaml_path is None:
            default_yaml_path = Path("config/personas/default_personas.yaml")

        path = Path(default_yaml_path)
        if path.exists():
            definitions = PersonaConfigLoader.load_from_yaml(path)
            for definition in definitions.values():
                registry.register_definition(definition)

        return registry

    def _bootstrap_fallback_defaults(self) -> None:
        """Internal fallback providing default definitions programmatically."""
        roles_and_titles = [
            # 10 Core
            (PersonaRole.DATA_ANALYST, "data_analyst", "Data Analyst", TechnicalDepth.SUMMARY, ["analyst", "bi_analyst"]),
            (PersonaRole.ANALYTICS_ENGINEER, "analytics_engineer", "Analytics Engineer", TechnicalDepth.TECHNICAL, ["ae", "dbt_developer"]),
            (PersonaRole.DATA_ENGINEER, "data_engineer", "Data Engineer", TechnicalDepth.TECHNICAL, ["de"]),
            (PersonaRole.DATA_SCIENTIST, "data_scientist", "Data Scientist", TechnicalDepth.TECHNICAL, ["ds", "ml_scientist"]),
            (PersonaRole.BI_DEVELOPER, "bi_developer", "BI Developer", TechnicalDepth.TECHNICAL, ["bi_engineer", "powerbi_developer"]),
            (PersonaRole.DATA_ARCHITECT, "data_architect", "Data Architect", TechnicalDepth.EXHAUSTIVE, ["architect", "enterprise_architect"]),
            (PersonaRole.DATA_GOVERNANCE_OFFICER, "data_governance_officer", "Data Governance Officer", TechnicalDepth.SUMMARY, ["governance", "steward"]),
            (PersonaRole.PLATFORM_ENGINEER, "platform_engineer", "Platform Engineer", TechnicalDepth.TECHNICAL, ["pe", "infrastructure_engineer"]),
            (PersonaRole.DOMAIN_OWNER, "domain_owner", "Domain Owner", TechnicalDepth.SUMMARY, ["business_owner", "domain_lead"]),
            (PersonaRole.AUDIT_RISK, "audit_risk", "Audit & Risk Officer", TechnicalDepth.EXHAUSTIVE, ["risk_officer", "compliance_officer"]),
            # 6 Extensions
            (PersonaRole.ANALYTICS_LEADER, "analytics_leader", "Analytics Leader", TechnicalDepth.EXECUTIVE, ["executive", "cdo"]),
            (PersonaRole.DATA_PRODUCT_MANAGER, "data_product_manager", "Data Product Manager", TechnicalDepth.SUMMARY, ["dpm", "data_pm"]),
            (PersonaRole.FINOPS_SPECIALIST, "finops_specialist", "FinOps Specialist", TechnicalDepth.SUMMARY, ["finops"]),
            (PersonaRole.AI_SYSTEMS_ENGINEER, "ai_systems_engineer", "AI Systems Engineer", TechnicalDepth.TECHNICAL, ["mle", "ai_engineer"]),
            (PersonaRole.BUSINESS_CONSUMER, "business_consumer", "Business Consumer", TechnicalDepth.SUMMARY, ["consumer", "business_user"]),
            (PersonaRole.COMPLIANCE_AUDITOR, "compliance_auditor", "Compliance Auditor", TechnicalDepth.EXHAUSTIVE, ["auditor_external"]),
        ]
        for role, pid, dname, depth, aliases in roles_and_titles:
            defn = PersonaDefinition(
                persona_id=pid,
                role=role,
                display_name=dname,
                title=f"{dname} Perspective",
                summary_template=f"Tailored perspective for {dname} on {{project_name}}",
                technical_depth=depth,
                aliases=aliases,
            )
            self.register_definition(defn)
