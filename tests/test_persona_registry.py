"""
Tests for PersonaRegistry, Configuration Loader, and Override Safety Enforcement.
"""
from pathlib import Path
import pytest
from src.core.personas.models import (
    OverrideSafetyLevel,
    PersonaRole,
    TechnicalDepth,
    LensFocus,
)
from src.core.personas.config_loader import (
    ConfigurationValidationError,
    PersonaConfigLoader,
)
from src.core.personas.registry import (
    PersonaNotFoundError,
    PersonaRegistry,
)


def test_registry_create_default_loads_all_10_personas():
    """Verify registry loads all 10 standard personas from YAML config."""
    registry = PersonaRegistry.create_default()
    persona_ids = registry.list_persona_ids()

    expected_ids = [
        "ai_systems_engineer",
        "analytics_engineer",
        "analytics_leader",
        "bi_developer",
        "business_consumer",
        "compliance_auditor",
        "data_engineer",
        "data_governance_officer",
        "data_product_manager",
        "finops_specialist",
    ]
    for exp_id in expected_ids:
        assert exp_id in persona_ids, f"Expected {exp_id} in registry"

    assert len(registry.list_definitions()) >= 10


def test_registry_alias_resolution():
    """Verify alias mapping correctly resolves to canonical persona IDs."""
    registry = PersonaRegistry.create_default()

    # Aliases for Analytics Leader / Executive
    assert registry.resolve_persona_id("executive") == "analytics_leader"
    assert registry.resolve_persona_id("cdo") == "analytics_leader"
    assert registry.resolve_persona_id("head_of_data") == "analytics_leader"
    assert registry.resolve_persona_id(PersonaRole.ANALYTICS_LEADER) == "analytics_leader"

    # Aliases for BI Developer / BI Engineer
    assert registry.resolve_persona_id("bi_engineer") == "bi_developer"
    assert registry.resolve_persona_id("powerbi_developer") == "bi_developer"

    # Aliases for Data Governance
    assert registry.resolve_persona_id("data_governance") == "data_governance_officer"
    assert registry.resolve_persona_id("data_steward") == "data_governance_officer"

    # Aliases for FinOps
    assert registry.resolve_persona_id("finops") == "finops_specialist"
    assert registry.resolve_persona_id("cloud_economist") == "finops_specialist"

    # Aliases for Business Consumer
    assert registry.resolve_persona_id("analytic_consumer") == "business_consumer"
    assert registry.resolve_persona_id("business_analyst") == "business_consumer"

    # Aliases for Analytics Engineer & Data Engineer
    assert registry.resolve_persona_id("ae") == "analytics_engineer"
    assert registry.resolve_persona_id("de") == "data_engineer"

    # Aliases for Auditor & AI
    assert registry.resolve_persona_id("auditor") == "compliance_auditor"
    assert registry.resolve_persona_id("ml_engineer") == "ai_systems_engineer"


def test_registry_unknown_persona_raises_error():
    """Verify requesting an unknown persona raises PersonaNotFoundError."""
    registry = PersonaRegistry.create_default()
    with pytest.raises(PersonaNotFoundError):
        registry.resolve_persona_id("non_existent_persona_xyz")

    with pytest.raises(PersonaNotFoundError):
        registry.get_definition("invalid_role_123")


def test_registry_safe_override():
    """Verify SAFE overrides (display_name, aliases, title) are applied cleanly."""
    registry = PersonaRegistry.create_default()
    
    overrides = {
        "personas": {
            "analytics_leader": {
                "display_name": "Chief Analytics Officer",
                "title": "Global Data Leadership Cockpit",
                "aliases": ["cao", "chief_analytics_officer"]
            }
        }
    }

    audit_trail = registry.load_overrides(overrides)
    assert len(audit_trail) >= 2
    for item in audit_trail:
        assert item.safety_level == OverrideSafetyLevel.SAFE
        assert item.is_allowed is True

    updated_def = registry.get_definition("analytics_leader")
    assert updated_def.display_name == "Chief Analytics Officer"
    assert updated_def.title == "Global Data Leadership Cockpit"
    assert registry.resolve_persona_id("cao") == "analytics_leader"


def test_registry_review_required_override():
    """Verify REVIEW_REQUIRED overrides modify behavior and register in audit trail."""
    registry = PersonaRegistry.create_default()

    overrides = {
        "personas": {
            "data_governance_officer": {
                "technical_depth": "EXHAUSTIVE",
                "focus_areas": ["GOVERNANCE_COMPLIANCE", "AUDIT_TRACEABILITY"]
            }
        }
    }

    audit_trail = registry.load_overrides(overrides)
    review_items = [i for i in audit_trail if i.safety_level == OverrideSafetyLevel.REVIEW_REQUIRED]
    assert len(review_items) >= 1

    updated_def = registry.get_definition("data_governance_officer")
    assert updated_def.technical_depth == TechnicalDepth.EXHAUSTIVE
    assert LensFocus.AUDIT_TRACEABILITY in updated_def.focus_areas


def test_registry_prohibited_override_raises_validation_error():
    """Verify PROHIBITED overrides (e.g. altering persona_id or role) are rejected."""
    registry = PersonaRegistry.create_default()

    # Attempting to override role on existing persona
    overrides = {
        "personas": {
            "data_engineer": {
                "role": "ANALYTICS_LEADER"
            }
        }
    }

    with pytest.raises(ConfigurationValidationError) as exc_info:
        registry.load_overrides(overrides)

    assert "PROHIBITED" in str(exc_info.value)
    assert "role" in str(exc_info.value)


def test_registry_add_custom_persona():
    """Verify adding a brand-new custom persona via overrides."""
    registry = PersonaRegistry.create_default()

    custom_persona = {
        "personas": {
            "sustainability_analyst": {
                "role": "CUSTOM",
                "display_name": "ESG & Sustainability Analyst",
                "title": "Carbon Footprint & ESG Metrics Perspective",
                "summary_template": "Sustainability metrics for {project_name}",
                "technical_depth": "SUMMARY",
                "focus_areas": ["BUSINESS_VALUE"],
                "aliases": ["esg_analyst", "green_ops"]
            }
        }
    }

    audit_trail = registry.load_overrides(custom_persona)
    assert "sustainability_analyst" in registry.list_persona_ids()
    assert registry.resolve_persona_id("green_ops") == "sustainability_analyst"

    esg_def = registry.get_definition("sustainability_analyst")
    assert esg_def.display_name == "ESG & Sustainability Analyst"
