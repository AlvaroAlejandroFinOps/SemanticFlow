"""
Governance Policy Loader with Floor Guardrails enforcement.
Loads corporate baseline policies and merges company-specific overrides without weakening floor guardrails.
"""
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from src.core.security.sanitize import resolve_within
from src.core.security.secret_scanner import scan_file_for_secrets

FLOOR_GUARDRAILS = {
    "min_score": 60.0,
    "require_primary_keys": True,
    "block_cyclic_dependencies": True,
    "disallow_unidirectional_m2m": True,
}

MANDATORY_SECURITY_RULES = ("GOV_PII_001", "D-011", "D-012")


class GovernancePolicyLoader:
    """Loads and validates Policy-as-Code governance policies with Floor Guardrail enforcement."""

    MANDATORY_SECURITY_RULES = MANDATORY_SECURITY_RULES
    FLOOR_MIN_CQS_SCORE: float = 60.0
    DEFAULT_BASELINE_PATH: Path = Path("config/governance/baseline_policy.yaml")

    @classmethod
    def load_effective_policy(
        cls,
        company_dir: Optional[Path] = None,
        baseline_path: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """
        Loads baseline_policy.yaml and applies company_dir/governance_policy.yaml (or direct file) if present.
        Enforces Floor Guardrails: mandatory security/PII rules cannot be disabled and
        minimum security thresholds cannot be lowered below corporate floor.
        """
        company_policy_path: Optional[Path] = None
        if company_dir is not None:
            candidate = Path(company_dir)
            if candidate.is_dir():
                base_dir = candidate.resolve()
                for fname in ("governance_policy.yaml", "governance_policy.yml"):
                    fpath = base_dir / fname
                    if fpath.exists():
                        company_policy_path = resolve_within(base_dir, fpath)
                        break
            elif candidate.exists():
                parent_resolved = candidate.parent.resolve()
                company_policy_path = resolve_within(parent_resolved, candidate.resolve())

        return cls.load_policy(company_policy_path=company_policy_path, baseline_path=baseline_path)

    @classmethod
    def load_policy(
        cls,
        company_policy_path: Optional[Path] = None,
        baseline_path: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """
        Carga y fusiona la política de gobernanza local sobre la política corporativa base.
        Valida que ningún umbral local viole los Floor Guardrails corporativos mínimos
        (ej. min_score >= 60.0, block_cyclic_dependencies == True, mandatory_rules intactas).
        """
        if baseline_path is None:
            baseline_path = cls.DEFAULT_BASELINE_PATH

        policy: Dict[str, Any] = {
            "version": "1.0",
            "policy_id": "corporate_baseline",
            "min_cqs_score": 75.0,
            "min_operational_score": 45.0,
            "mandatory_rules": list(MANDATORY_SECURITY_RULES),
            "quality_thresholds": dict(FLOOR_GUARDRAILS),
            "local_rules": {},
        }

        if baseline_path.exists():
            with open(baseline_path, "r", encoding="utf-8") as bf:
                raw_base = yaml.safe_load(bf)
                if isinstance(raw_base, dict):
                    policy.update(raw_base)

        if company_policy_path and Path(company_policy_path).exists():
            comp_raw = Path(company_policy_path)
            comp_path = resolve_within(comp_raw.parent.resolve(), comp_raw.resolve())
            findings = scan_file_for_secrets(comp_path)
            if findings:
                raise PermissionError(
                    f"Violación de seguridad: secretos detectados en política de gobernanza '{comp_path.name}': "
                    f"{[f.rule_id for f in findings]}"
                )

            with open(comp_path, "r", encoding="utf-8") as cf:
                company_data = yaml.safe_load(cf)

            if isinstance(company_data, dict):
                disabled_rules = company_data.get("disabled_rules", [])
                if isinstance(disabled_rules, list):
                    for m_rule in MANDATORY_SECURITY_RULES:
                        if m_rule in disabled_rules:
                            raise ValueError(
                                f"Violación de Floor Guardrail: la regla obligatoria '{m_rule}' no puede ser deshabilitada."
                            )

                if "mandatory_rules" in company_data and isinstance(company_data["mandatory_rules"], list):
                    for m_rule in MANDATORY_SECURITY_RULES:
                        if m_rule not in company_data["mandatory_rules"]:
                            raise ValueError(
                                f"Violación de Floor Guardrail: 'mandatory_rules' debe conservar la regla obligatoria '{m_rule}'."
                            )

                for k, v in company_data.items():
                    if isinstance(v, dict) and isinstance(policy.get(k), dict):
                        policy[k].update(v)
                    else:
                        policy[k] = v

        # Enforce Floor Guardrails
        thresholds = policy.get("quality_thresholds", {})
        min_score = float(thresholds.get("min_score", 60.0))
        if min_score < FLOOR_GUARDRAILS["min_score"]:
            raise ValueError(
                f"Violación de Floor Guardrail: min_score no puede ser inferior a "
                f"{FLOOR_GUARDRAILS['min_score']} (recibido: {min_score})."
            )

        if thresholds.get("require_primary_keys") is False:
            raise ValueError("Violación de Floor Guardrail: require_primary_keys es obligatorio en True.")

        if thresholds.get("block_cyclic_dependencies") is False:
            raise ValueError("Violación de Floor Guardrail: block_cyclic_dependencies es obligatorio en True.")

        if thresholds.get("disallow_unidirectional_m2m") is False:
            raise ValueError("Violación de Floor Guardrail: disallow_unidirectional_m2m es obligatorio en True.")

        # Guarantee mandatory rules remain present in effective policy
        eff_mandatory = list(policy.get("mandatory_rules", []))
        for m_rule in MANDATORY_SECURITY_RULES:
            if m_rule not in eff_mandatory:
                eff_mandatory.append(m_rule)
        policy["mandatory_rules"] = eff_mandatory

        return policy
