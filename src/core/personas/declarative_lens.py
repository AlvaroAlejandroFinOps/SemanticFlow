"""
Declarative Domain Lens implementation for company-specific custom lenses.
Enables YAML-defined domain lenses without requiring modification of core Python codebase.
"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.ast.canonical.models import CanonicalSemanticProject, EntityRole
from src.core.personas.interfaces import PersonaLens
from src.core.personas.models import (
    LensFocus,
    PersonaDefinition,
    PersonaProjection,
    PersonaRecommendation,
    PersonaRole,
    RecommendationPriority,
    TechnicalDepth,
)


def _resolve_role(raw_role: Any) -> PersonaRole:
    if isinstance(raw_role, PersonaRole):
        return raw_role
    if not raw_role:
        return PersonaRole.CUSTOM
    val = str(raw_role).strip().upper()
    try:
        return PersonaRole(val)
    except ValueError:
        # Check standard mappings
        role_map = {
            "OPERATIONAL": PersonaRole.CUSTOM,
            "MANAGEMENT": PersonaRole.DOMAIN_OWNER,
            "GOVERNANCE": PersonaRole.DATA_GOVERNANCE_OFFICER,
            "AUDIT": PersonaRole.COMPLIANCE_AUDITOR,
            "TECHNICAL": PersonaRole.DATA_ENGINEER,
            "EXECUTIVE": PersonaRole.ANALYTICS_LEADER,
        }
        return role_map.get(val, PersonaRole.CUSTOM)


def _resolve_depth(raw_depth: Any) -> TechnicalDepth:
    if isinstance(raw_depth, TechnicalDepth):
        return raw_depth
    if not raw_depth:
        return TechnicalDepth.SUMMARY
    val = str(raw_depth).strip().upper()
    depth_map = {
        "C_LEVEL": TechnicalDepth.EXECUTIVE,
        "STRATEGIC": TechnicalDepth.EXECUTIVE,
        "OPERATIONAL": TechnicalDepth.SUMMARY,
        "DEEP_TECHNICAL": TechnicalDepth.EXHAUSTIVE,
        "TECHNICAL": TechnicalDepth.TECHNICAL,
        "EXHAUSTIVE": TechnicalDepth.EXHAUSTIVE,
        "EXECUTIVE": TechnicalDepth.EXECUTIVE,
        "SUMMARY": TechnicalDepth.SUMMARY,
    }
    return depth_map.get(val, TechnicalDepth.SUMMARY)


class DeclarativeDomainLens(PersonaLens):
    """
    A Persona Lens driven dynamically by a declarative YAML definition file.
    Supports company custom roles (e.g. Jefe de Obra y Control de Obras).
    """

    def __init__(self, raw_definition: Dict[str, Any], filepath: Optional[Path] = None):
        self._raw = dict(raw_definition)
        self._filepath = filepath

        self._persona_id = str(self._raw.get("persona_id", "")).strip().lower()
        if not self._persona_id:
            raise ValueError("Declarative lens definition requires a non-empty 'persona_id'.")

        self._role = _resolve_role(self._raw.get("role"))
        self._depth = _resolve_depth(self._raw.get("technical_depth"))

        display_name = (
            self._raw.get("display_name")
            or self._raw.get("name")
            or self._persona_id.replace("_", " ").title()
        )
        title = self._raw.get("title") or f"{display_name} Perspective"
        summary_template = (
            self._raw.get("summary_template")
            or f"Tailored operational perspective for {display_name} on {{project_name}}."
        )

        aliases = [str(a).strip().lower() for a in self._raw.get("aliases", []) if a]
        if self._persona_id not in aliases:
            aliases.append(self._persona_id)

        focus_areas: List[LensFocus] = []
        for fa in self._raw.get("focus_areas", []):
            try:
                focus_areas.append(LensFocus(str(fa).strip().upper()))
            except ValueError:
                pass
        if not focus_areas:
            focus_areas = [LensFocus.BUSINESS_VALUE, LensFocus.MODELING_QUALITY]

        self._definition = PersonaDefinition(
            persona_id=self._persona_id,
            role=self._role,
            display_name=display_name,
            title=title,
            summary_template=summary_template,
            technical_depth=self._depth,
            focus_areas=focus_areas,
            visible_object_types=self._raw.get("visible_object_types", ["TABLE", "COLUMN", "METRIC"]),
            aliases=sorted(list(set(aliases))),
            custom_properties={
                "scope": self._raw.get("scope", "company"),
                "company_id": self._raw.get("company_id"),
                "target_entities": self._raw.get("target_entities", []),
                "focus_metrics": self._raw.get("focus_metrics", []),
                "domain_kpis": self._raw.get("domain_kpis", []),
                "operational_guidelines": self._raw.get("operational_guidelines", []),
                "quality_gate_rules": self._raw.get("quality_gate_rules", []),
            },
        )

    @property
    def role(self) -> PersonaRole:
        return self._role

    @property
    def definition(self) -> PersonaDefinition:
        return self._definition

    @property
    def filepath(self) -> Optional[Path]:
        return self._filepath

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self._persona_id == other.strip().lower()
        if isinstance(other, DeclarativeDomainLens):
            return self._persona_id == other._persona_id
        return False

    def project(
        self,
        project: CanonicalSemanticProject,
        config: Optional[Dict[str, Any]] = None,
    ) -> PersonaProjection:
        """
        Projects CanonicalSemanticProject deterministically through this domain lens.
        Guarantees Zero-Diff reproducibility with deterministic sorting and null rendered_at.
        """
        cfg = config or {}
        target_entities_spec = [str(e).strip() for e in self._raw.get("target_entities", [])]
        focus_metrics_spec = [str(m).strip().lower() for m in self._raw.get("focus_metrics", [])]

        primary_entities: List[str] = []
        secondary_entities: List[str] = []

        target_set = {t.lower() for t in target_entities_spec}
        roles_filter = {t.upper() for t in target_entities_spec if t.upper() in ("FACT", "DIMENSION", "BRIDGE")}

        for entity in sorted(project.entities, key=lambda e: (e.name.lower(), e.name)):
            is_primary = False
            if entity.name.lower() in target_set:
                is_primary = True
            elif entity.role and entity.role.value.upper() in roles_filter:
                is_primary = True
            elif not target_entities_spec and entity.role == EntityRole.FACT:
                is_primary = True

            if is_primary:
                primary_entities.append(entity.name)
            else:
                secondary_entities.append(entity.name)

        # Certified & secondary metrics
        all_metrics = []
        for entity in project.entities:
            for m in entity.metrics:
                all_metrics.append(m.name)

        certified_metrics: List[str] = []
        secondary_metrics: List[str] = []

        for m_name in sorted(all_metrics, key=lambda x: (x.lower(), x)):
            if focus_metrics_spec:
                if m_name.lower() in focus_metrics_spec:
                    certified_metrics.append(m_name)
                else:
                    secondary_metrics.append(m_name)
            else:
                certified_metrics.append(m_name)

        # Add domain KPIs if defined in custom lens and check model coverage
        all_metrics_lower = {m.lower() for m in all_metrics}
        missing_domain_kpis: List[Dict[str, Any]] = []
        for kpi in self._raw.get("domain_kpis", []):
            if isinstance(kpi, dict) and "name" in kpi:
                k_name = kpi["name"]
                if k_name not in certified_metrics:
                    certified_metrics.append(k_name)
                if k_name.lower() not in all_metrics_lower:
                    missing_domain_kpis.append(kpi)

        # Relationships count
        primary_set = {e.lower() for e in primary_entities}
        active_rels = []
        for rel in sorted(project.relationships, key=lambda r: (r.from_entity_id.lower(), r.to_entity_id.lower())):
            from_e = rel.from_entity_id.lower()
            to_e = rel.to_entity_id.lower()
            if from_e in primary_set or to_e in primary_set or not primary_set:
                active_rels.append({
                    "name": rel.name,
                    "from_entity": rel.from_entity_id,
                    "from_attribute": rel.from_attribute_id,
                    "to_entity": rel.to_entity_id,
                    "to_attribute": rel.to_attribute_id,
                    "cardinality": str(rel.cardinality),
                })

        # Recommendations from guidelines, quality rules, and explicit recommendations
        recommendations: List[PersonaRecommendation] = []
        rec_idx = 1

        for guide in self._raw.get("operational_guidelines", []):
            recommendations.append(
                PersonaRecommendation(
                    id=f"{self._persona_id.upper()}-REC-{rec_idx:03d}",
                    title=f"Guía Operativa: {str(guide)[:60]}",
                    description=str(guide),
                    priority=RecommendationPriority.MEDIUM,
                    impact="Optimización de control de gestión y toma de decisiones operativas",
                    effort="Medio",
                    target_objects=primary_entities[:3],
                    suggested_action="Incorporar en el tablero de control del rol",
                )
            )
            rec_idx += 1

        for rule in self._raw.get("quality_gate_rules", []):
            if isinstance(rule, dict):
                r_id = rule.get("rule_id", f"{self._persona_id.upper()}-QG-{rec_idx:03d}")
                recommendations.append(
                    PersonaRecommendation(
                        id=str(r_id),
                        title=str(rule.get("title", f"Regla de Calidad de Dominio: {r_id}")),
                        description=str(rule.get("description", "Validación de integridad del dominio")),
                        priority=RecommendationPriority.HIGH if rule.get("blocking") else RecommendationPriority.MEDIUM,
                        impact="Gobernanza y confiabilidad del modelo de datos",
                        effort="Bajo",
                        target_objects=primary_entities[:2],
                        suggested_action="Verificar en auditoría cQS",
                        rule_id=str(r_id),
                    )
                )
                rec_idx += 1

        for rec_dict in self._raw.get("recommendations", []):
            if isinstance(rec_dict, dict) and "title" in rec_dict:
                recommendations.append(
                    PersonaRecommendation(
                        id=rec_dict.get("id", f"{self._persona_id.upper()}-REC-{rec_idx:03d}"),
                        title=str(rec_dict.get("title")),
                        description=str(rec_dict.get("description", "")),
                        priority=RecommendationPriority(rec_dict.get("priority", "MEDIUM").upper()),
                        impact=str(rec_dict.get("impact", "Impacto Operativo")),
                        effort=str(rec_dict.get("effort", "Medio")),
                        target_objects=rec_dict.get("target_objects", []),
                        suggested_action=rec_dict.get("suggested_action"),
                    )
                )
                rec_idx += 1

        for kpi_gap in missing_domain_kpis:
            k_name = str(kpi_gap.get("name", "KPI"))
            k_formula = kpi_gap.get("formula") or kpi_gap.get("dax_hint") or "Definir medida DAX"
            recommendations.append(
                PersonaRecommendation(
                    id=f"{self._persona_id.upper()}-KPI-GAP-{rec_idx:03d}",
                    title=f"Implementar KPI de Dominio en Esquema: {k_name}",
                    description=str(kpi_gap.get("description", f"El KPI '{k_name}' requerido por la lente aún no está declarado como medida explícita en el esquema.")),
                    priority=RecommendationPriority.MEDIUM,
                    impact=str(kpi_gap.get("business_impact", "Cobertura completa del tablero de control de dominio")),
                    effort="Bajo",
                    target_objects=primary_entities[:2],
                    suggested_action=f"Declarar medida DAX: {k_formula}",
                )
            )
            rec_idx += 1

        # Rendered projection
        summary = (
            f"Perspectiva Operativa para {self._definition.display_name} en '{project.name}'. "
            f"Monitoreo de {len(primary_entities)} entidades primarias, "
            f"{len(certified_metrics)} KPIs foco y {len(active_rels)} relaciones operativas."
        )

        return PersonaProjection(
            persona_id=self._persona_id,
            role=self._role,
            title=self._definition.title,
            summary=summary,
            technical_depth=self._depth,
            focus_areas=self._definition.focus_areas,
            primary_entities=sorted(primary_entities),
            secondary_entities=sorted(secondary_entities),
            certified_metrics=sorted(certified_metrics),
            secondary_metrics=sorted(secondary_metrics),
            relationships_count=len(active_rels),
            active_relationships=active_rels,
            recommendations=sorted(recommendations, key=lambda r: (r.id, r.title)),
            rendered_at=cfg.get("rendered_at", None),  # None ensures deterministic SHA-256
        )
