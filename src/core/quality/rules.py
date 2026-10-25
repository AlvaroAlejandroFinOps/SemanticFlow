"""
Quality and Validation Rules for Semantic Models.
"""
import re
from typing import List

from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    DataType,
    Diagnostic,
    DiagnosticCategory,
    DiagnosticSeverity,
    EntityRole,
    MetricType,
)


def validate_grain_declaration(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        if entity.role == EntityRole.FACT and not entity.grain:
            diagnostics.append(
                Diagnostic(
                    code="QUAL_GRAIN_001",
                    severity=DiagnosticSeverity.WARNING,
                    category=DiagnosticCategory.QUALITY,
                    message=f"Fact entity '{entity.name}' has no explicit grain declared.",
                    object_id=entity.id,
                    suggested_action="Declare explicit primary key attributes as grain in entity metadata.",
                )
            )
    return diagnostics


def validate_metric_descriptions(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        for metric in entity.metrics:
            if not metric.description:
                diagnostics.append(
                    Diagnostic(
                        code="QUAL_METRIC_001",
                        severity=DiagnosticSeverity.WARNING,
                        category=DiagnosticCategory.METRIC,
                        message=f"Metric '{metric.name}' in entity '{entity.name}' lacks a business description.",
                        object_id=metric.id,
                        suggested_action="Provide a clear business description for the metric.",
                    )
                )
    return diagnostics


def validate_certified_metrics(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        for metric in entity.metrics:
            eff_gov = project.resolve_asset_governance(metric)
            if eff_gov.certification_status == "CERTIFIED":
                if not eff_gov.owner:
                    diagnostics.append(
                        Diagnostic(
                            code="GOV_CERT_001",
                            severity=DiagnosticSeverity.ERROR,
                            category=DiagnosticCategory.GOVERNANCE,
                            message=f"Certified metric '{metric.name}' must have an assigned owner.",
                            object_id=metric.id,
                            suggested_action="Assign a business or technical owner before certifying.",
                        )
                    )
    return diagnostics


def validate_ratio_metrics(project: CanonicalSemanticProject) -> List[Diagnostic]:
    diagnostics = []
    for entity in project.entities:
        for metric in entity.metrics:
            if metric.metric_type == MetricType.RATIO:
                if not metric.numerator_metric_id or not metric.denominator_metric_id:
                    diagnostics.append(
                        Diagnostic(
                            code="METRIC_RATIO_001",
                            severity=DiagnosticSeverity.ERROR,
                            category=DiagnosticCategory.METRIC,
                            message=f"Ratio metric '{metric.name}' must declare numerator_metric_id and denominator_metric_id.",
                            object_id=metric.id,
                            suggested_action="Specify numerator and denominator metric IDs for auditability.",
                        )
                    )
    return diagnostics


def validate_project_governance(project: CanonicalSemanticProject) -> List[Diagnostic]:
    """Validates that the project has explicit domain governance and ownership metadata."""
    diagnostics = []
    if not project.governance or not project.governance.owner:
        diagnostics.append(
            Diagnostic(
                code="GOV_PROJ_001",
                severity=DiagnosticSeverity.RECOMMENDATION,
                category=DiagnosticCategory.GOVERNANCE,
                message=f"Project '{project.name}' has no assigned executive owner.",
                object_id=project.id,
                suggested_action="Declare project-level governance with owner in ProjectGovernance.",
            )
        )
    return diagnostics


def validate_pii_classification(project: CanonicalSemanticProject) -> List[Diagnostic]:
    """Validates that PII attributes are flagged with Restricted or Confidential classification."""
    diagnostics = []
    for entity in project.entities:
        for attr in entity.attributes:
            eff_gov = project.resolve_asset_governance(attr)
            if eff_gov.is_pii:
                if eff_gov.sensitivity_classification not in ("Restricted", "Confidential"):
                    diagnostics.append(
                        Diagnostic(
                            code="GOV_PII_001",
                            severity=DiagnosticSeverity.WARNING,
                            category=DiagnosticCategory.SECURITY,
                            message=f"PII attribute '{entity.name}.{attr.name}' must have 'Restricted' or 'Confidential' classification.",
                            object_id=attr.id,
                            suggested_action="Set sensitivity_classification to Restricted in attribute or project governance.",
                        )
                    )
    return diagnostics


def is_direct_lake_project(project: CanonicalSemanticProject) -> bool:
    """Detecta si el proyecto opera bajo el paradigma Microsoft Fabric Direct Lake."""
    if not project.governance:
        return False
    custom = project.governance.custom_properties or {}
    if custom.get("direct_lake_rules") or custom.get("storage_mode") == "DirectLake":
        return True
    eco = custom.get("technology_ecosystem") or {}
    if isinstance(eco, dict):
        if "direct_lake" in str(eco).lower() or "fabric" in str(eco).lower():
            return True
    tags = [t.lower() for t in project.governance.tags]
    return "direct_lake" in tags or "directlake" in tags


def validate_direct_lake_compatibility(project: CanonicalSemanticProject) -> List[Diagnostic]:
    """
    Regla D-011: Valida compatibilidad con Microsoft Fabric Direct Lake.
    - Rechaza columnas DATETIME no particionadas en hechos (causa fallback a DirectQuery).
    - Rechaza relaciones Many-to-Many (N:N) activas en Direct Lake.
    """
    diagnostics = []
    if not is_direct_lake_project(project):
        return diagnostics

    # 1. Chequeo de columnas DATETIME en tablas de hechos
    for entity in project.entities:
        if entity.role == EntityRole.FACT:
            for attr in entity.attributes:
                if attr.data_type == DataType.DATETIME:
                    diagnostics.append(
                        Diagnostic(
                            code="QUAL_DL_DATETIME_011",
                            severity=DiagnosticSeverity.WARNING,
                            category=DiagnosticCategory.TARGET_COMPATIBILITY,
                            message=(
                                f"La entidad Direct Lake '{entity.name}' tiene el atributo '{attr.name}' con tipo DATETIME. "
                                "En Direct Lake esto degrada V-Order y provoca fallback a DirectQuery."
                            ),
                            object_id=attr.id,
                            suggested_action="Separar en dos atributos discretos: DATE (Fecha) y TIME / INT (Hora).",
                            penalty=10.0,
                        )
                    )

    # 2. Chequeo de relaciones N:N activas
    for rel in project.relationships:
        if rel.is_active and rel.cardinality in ("N:N", "M:N", "MANY_TO_MANY"):
            diagnostics.append(
                Diagnostic(
                    code="QUAL_DL_NN_011",
                    severity=DiagnosticSeverity.WARNING,
                    category=DiagnosticCategory.TARGET_COMPATIBILITY,
                    message=(
                        f"Relación Many-to-Many (N:N) activa '{rel.name}' detectada en Direct Lake. "
                        "Satura el motor de paginación VertiPaq en SKUs F64 o inferiores."
                    ),
                    object_id=rel.id,
                    suggested_action="Desactivar la relación o resolver mediante una tabla puente (Bridge) intermedia 1:N.",
                    penalty=15.0,
                )
            )

    return diagnostics


def validate_vertipaq_performance(project: CanonicalSemanticProject) -> List[Diagnostic]:
    """
    Regla D-012: Detección de antipatrones de rendimiento y FinOps en el motor VertiPaq.
    - Detecta FILTER(ALL('Tabla'), ...) sobre tablas con más de 1M de registros.
    - Detecta filtrado cruzado bidireccional en relaciones que involucran hechos.
    """
    diagnostics = []

    entity_map = {e.id: e for e in project.entities}
    entity_name_map = {e.name.lower(): e for e in project.entities}

    # 0. Cardinalidad no declarada en tablas FACT con métricas o grano (QUAL_CARD_001)
    for entity in project.entities:
        if entity.role == EntityRole.FACT:
            if entity.estimated_rows is None or entity.estimated_rows <= 0:
                if entity.grain or entity.metrics:
                    diagnostics.append(
                        Diagnostic(
                            code="QUAL_CARD_001",
                            severity=DiagnosticSeverity.WARNING,
                            category=DiagnosticCategory.QUALITY,
                            message=(
                                f"La tabla de hechos '{entity.name}' no declara 'estimated_rows'. "
                                "Se asume cardinalidad conservadora (>= 1,000,000) para optimización VertiPaq."
                            ),
                            object_id=entity.id,
                            suggested_action="Declarar 'estimated_rows' en los metadatos de la tabla para afinar el análisis de compresión.",
                            penalty=2.0,
                        )
                    )

    # 1. Antipatrón FILTER(ALL('Tabla'), ...)
    filter_all_re = re.compile(r"FILTER\s*\(\s*ALL\s*\(\s*'?(?P<table>[a-zA-Z0-9_ -]+)'?\s*\)", re.IGNORECASE)

    for entity in project.entities:
        for metric in entity.metrics:
            if not metric.expression:
                continue
            for match in filter_all_re.finditer(metric.expression):
                target_table = match.group("table").strip().lower()
                target_entity = entity_name_map.get(target_table) or entity
                is_high_card = False
                if target_entity.estimated_rows and target_entity.estimated_rows > 1_000_000:
                    is_high_card = True
                elif target_entity.estimated_rows is None and target_entity.role == EntityRole.FACT:
                    is_high_card = True

                if is_high_card:
                    rows_desc = (
                        f"{target_entity.estimated_rows:,} registros"
                        if target_entity.estimated_rows
                        else "cardinalidad no declarada (asumiendo >= 1,000,000)"
                    )
                    diagnostics.append(
                        Diagnostic(
                            code="QUAL_VPAQ_FILTER_012",
                            severity=DiagnosticSeverity.WARNING,
                            category=DiagnosticCategory.QUALITY,
                            message=(
                                f"La métrica '{metric.name}' usa FILTER(ALL('{target_entity.name}')) sobre una tabla "
                                f"con alta cardinalidad estimada ({rows_desc})."
                            ),
                            object_id=metric.id,
                            suggested_action="Reescribir usando KEEPFILTERS o CALCULATETABLE para aprovechar los índices segmentados de VertiPaq.",
                            penalty=5.0,
                        )
                    )

    # 2. Filtrado cruzado bidireccional en relaciones que involucran hechos
    for rel in project.relationships:
        if not rel.is_active:
            continue
        cross_mode = (rel.cross_filtering or "").lower()
        if cross_mode in ("bothdirections", "both", "bidirectional"):
            from_ent = entity_map.get(rel.from_entity_id)
            to_ent = entity_map.get(rel.to_entity_id)
            is_fact_involved = (
                (from_ent and from_ent.role == EntityRole.FACT) or
                (to_ent and to_ent.role == EntityRole.FACT)
            )
            if is_fact_involved:
                diagnostics.append(
                    Diagnostic(
                        code="QUAL_VPAQ_BIDIR_012",
                        severity=DiagnosticSeverity.WARNING,
                        category=DiagnosticCategory.QUALITY,
                        message=(
                            f"Filtrado cruzado bidireccional en la relación '{rel.name}' involucra tablas de hechos. "
                            "Riesgo de bucles de ambigüedad y saturación de memoria VertiPaq."
                        ),
                        object_id=rel.id,
                        suggested_action="Configurar filtrado unidireccional y activar bidireccional solo cuando sea necesario vía CROSSFILTER en DAX.",
                        penalty=5.0,
                    )
                )

    return diagnostics
