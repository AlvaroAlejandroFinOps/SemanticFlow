"""
Tests for Company Custom Declarative Lenses, Registry Loading, and Governance Policy Loader.
Verifies Layer-2 persona architecture and Floor Guardrails enforcement.
"""
from pathlib import Path
import tempfile
import hashlib
import json
import pytest

from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    EntityRole,
    SemanticAttribute,
    SemanticEntity,
    SemanticMetric,
    DataType,
)
from src.core.personas.declarative_lens import DeclarativeDomainLens
from src.core.personas.models import PersonaRole, TechnicalDepth
from src.core.personas.registry import PersonaRegistry
from src.core.quality.policy_loader import GovernancePolicyLoader, FLOOR_GUARDRAILS


@pytest.fixture
def sample_project() -> CanonicalSemanticProject:
    return CanonicalSemanticProject(
        id="sample_test_proj",
        name="SampleProject",
        entities=[
            SemanticEntity(
                id="fact_sales",
                name="Fact_Sales",
                role=EntityRole.FACT,
                attributes=[
                    SemanticAttribute(id="s1", name="sale_id", is_key=True, data_type=DataType.INT64),
                    SemanticAttribute(id="s2", name="amount", data_type=DataType.DECIMAL),
                ],
                metrics=[
                    SemanticMetric(id="m1", name="Total_Sales", expression="SUM('Fact_Sales'[amount])"),
                    SemanticMetric(id="m2", name="Avg_Sale", expression="AVERAGE('Fact_Sales'[amount])"),
                ],
            ),
            SemanticEntity(
                id="dim_customer",
                name="Dim_Customer",
                role=EntityRole.DIMENSION,
                attributes=[
                    SemanticAttribute(id="c1", name="customer_id", is_key=True, data_type=DataType.INT64),
                    SemanticAttribute(id="c2", name="name", data_type=DataType.STRING),
                ],
            ),
        ],
    )


def test_declarative_lens_instantiation_from_dict():
    """Verify DeclarativeDomainLens instantiates correctly with normalized role and depth."""
    raw = {
        "persona_id": "test_lens",
        "display_name": "Test Lens",
        "role": "operational",
        "technical_depth": "operational",
        "target_entities": ["Fact_Sales"],
        "focus_metrics": ["Total_Sales"],
    }
    lens = DeclarativeDomainLens(raw)
    assert lens.definition.persona_id == "test_lens"
    assert lens.definition.display_name == "Test Lens"
    assert lens.definition.technical_depth == TechnicalDepth.SUMMARY
    assert "test_lens" in lens.definition.aliases


def test_declarative_lens_deterministic_projection_zero_diff(sample_project):
    """Verify two consecutive projections produce identical JSON and SHA-256 hashes (Zero-Diff)."""
    raw = {
        "persona_id": "deterministic_lens",
        "display_name": "Deterministic Lens",
        "role": "operational",
        "technical_depth": "operational",
        "target_entities": ["Fact_Sales"],
        "focus_metrics": ["Total_Sales"],
    }
    lens = DeclarativeDomainLens(raw)
    p1 = lens.project(sample_project)
    p2 = lens.project(sample_project)

    json1 = p1.model_dump_json()
    json2 = p2.model_dump_json()
    hash1 = hashlib.sha256(json1.encode("utf-8")).hexdigest()
    hash2 = hashlib.sha256(json2.encode("utf-8")).hexdigest()
    assert hash1 == hash2


def test_declarative_lens_target_entities_filtering(sample_project):
    """Verify DeclarativeDomainLens partitions entities into primary and secondary correctly."""
    raw = {
        "persona_id": "filtering_lens",
        "display_name": "Filtering Lens",
        "role": "custom",
        "technical_depth": "technical",
        "target_entities": ["Dim_Customer"],
    }
    lens = DeclarativeDomainLens(raw)
    projection = lens.project(sample_project)
    assert "Dim_Customer" in projection.primary_entities
    assert "Fact_Sales" in projection.secondary_entities


def test_declarative_lens_focus_metrics_prioritization(sample_project):
    """Verify DeclarativeDomainLens segregates certified focus metrics from secondary metrics."""
    raw = {
        "persona_id": "metrics_lens",
        "display_name": "Metrics Lens",
        "role": "custom",
        "technical_depth": "summary",
        "focus_metrics": ["Total_Sales"],
    }
    lens = DeclarativeDomainLens(raw)
    projection = lens.project(sample_project)
    assert "Total_Sales" in projection.certified_metrics
    assert "Avg_Sale" in projection.secondary_metrics


def test_persona_registry_load_company_lenses_santolaya():
    """Verify PersonaRegistry loads Santolaya's 17_jefe_obra_control lens cleanly and resolves aliases."""
    registry = PersonaRegistry.create_default()
    lenses_dir = Path("artifacts/SemanticFlow/inputs/companies/santolaya/lenses")
    assert lenses_dir.exists(), "Santolaya lenses directory must exist"

    loaded = registry.load_company_lenses(lenses_dir, company_id="santolaya")
    assert len(loaded) >= 1
    assert any(lens == "17_jefe_obra_control" for lens in loaded)

    # Resolution test including aliases
    for alias in ("17_jefe_obra_control", "site_manager", "control_obras", "jefe_obra"):
        resolved_id = registry.resolve_persona_id(alias)
        assert resolved_id == "17_jefe_obra_control"
    retrieved_lens = registry.get_lens("17_jefe_obra_control")
    assert retrieved_lens is not None


def test_cross_company_isolation_metro_santiago():
    """Verify metro_santiago does not bleed Santolaya's custom lenses."""
    registry = PersonaRegistry.create_default()
    metro_lenses_dir = Path("artifacts/SemanticFlow/inputs/companies/metro_santiago/lenses")
    loaded = registry.load_company_lenses(metro_lenses_dir, company_id="metro_santiago")
    assert loaded == []
    with pytest.raises(KeyError):
        registry.resolve_persona_id("17_jefe_obra_control")


def test_persona_registry_overrides_application(sample_project):
    """Verify PersonaRegistry applies overrides from Santolaya's overrides.yaml and projects them onto base lenses."""
    from src.core.personas.projector import PersonaProjector

    registry = PersonaRegistry.create_default()
    lenses_dir = Path("artifacts/SemanticFlow/inputs/companies/santolaya/lenses")

    registry.load_company_lenses(lenses_dir, company_id="santolaya")
    analytics_leader_def = registry.get_definition("analytics_leader")
    assert "Santolaya" in analytics_leader_def.display_name or "Operaciones" in analytics_leader_def.display_name

    projector = PersonaProjector(sample_project, registry=registry)
    bi_proj = projector.project_lens("bi_developer")
    assert any("Desviacion_Plazo_Critico_Dias" in m for m in bi_proj.certified_metrics)

    finops_proj = projector.project_lens("finops_specialist")
    assert any("FACT_EVM_AVANCE_OBRA" in e for e in finops_proj.primary_entities)
    assert any("OneLake" in r.description or "D-012" in r.description for r in finops_proj.recommendations)


def test_persona_registry_blocks_sensitive_properties():
    """Verify PersonaRegistry rejects declarative lenses containing sensitive property names."""
    registry = PersonaRegistry.create_default()
    with tempfile.TemporaryDirectory() as tmp_dir:
        bad_lens = Path(tmp_dir) / "bad_lens.yaml"
        bad_lens.write_text(
            "persona_id: bad_lens\n"
            "display_name: Bad Lens\n"
            "role: operational\n"
            "technical_depth: summary\n"
            "api_key_field: header_name\n",
            encoding="utf-8",
        )
        with pytest.raises(PermissionError, match=r"(Violación de seguridad|Propiedad sensible no autorizada)"):
            registry.load_company_lenses(Path(tmp_dir))


def test_persona_registry_blocks_directory_escape():
    """Verify resolve_within blocks directory escape attempts."""
    from src.core.security.sanitize import resolve_within
    base = Path("artifacts/SemanticFlow/inputs")
    escape_target = Path("artifacts/SemanticFlow/inputs/../../etc/passwd")
    with pytest.raises(PermissionError):
        resolve_within(base, escape_target)


def test_governance_policy_loader_baseline():
    """Verify GovernancePolicyLoader loads baseline policy meeting Floor Guardrails."""
    policy = GovernancePolicyLoader.load_policy()
    assert policy is not None
    thresholds = policy["quality_thresholds"]
    assert thresholds["min_score"] >= FLOOR_GUARDRAILS["min_score"]
    assert thresholds["require_primary_keys"] is True
    assert thresholds["block_cyclic_dependencies"] is True


def test_governance_policy_loader_floor_guardrails_violation():
    """Verify GovernancePolicyLoader blocks any company policy attempting to weaken floor guardrails."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 1. min_score below 60.0
        bad_policy_1 = Path(tmp_dir) / "bad_policy_1.yaml"
        bad_policy_1.write_text("quality_thresholds:\n  min_score: 50.0\n", encoding="utf-8")
        with pytest.raises(ValueError, match="Violación de Floor Guardrail: min_score"):
            GovernancePolicyLoader.load_policy(company_policy_path=bad_policy_1)

        # 2. require_primary_keys set to False
        bad_policy_2 = Path(tmp_dir) / "bad_policy_2.yaml"
        bad_policy_2.write_text("quality_thresholds:\n  require_primary_keys: false\n", encoding="utf-8")
        with pytest.raises(ValueError, match="require_primary_keys es obligatorio en True"):
            GovernancePolicyLoader.load_policy(company_policy_path=bad_policy_2)

        # 3. Attempting to disable mandatory_rules via load_effective_policy
        comp_dir = Path(tmp_dir) / "comp_override"
        comp_dir.mkdir(parents=True, exist_ok=True)
        (comp_dir / "governance_policy.yaml").write_text(
            "mandatory_rules:\n  - D-011\n",
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="GOV_PII_001"):
            GovernancePolicyLoader.load_effective_policy(company_dir=comp_dir)
