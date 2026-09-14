"""
Reglas de gobernanza de atributos: ocultamiento de claves, tipos de agregación y formatos.
"""
from src.core.ast.schema import ColumnRaw, TableRaw
from src.core.ast.semantic import (
    SemanticColumn,
    TableRole,
    SummarizeBy,
)
from src.core.ast.types import PbiDataType


class AttributeGovernance:
    """Aplica mejores prácticas de modelado dimensional y gobierno de datos."""

    def govern_columns(
        self, table: TableRaw, role: TableRole
    ) -> list[SemanticColumn]:
        semantic_cols: list[SemanticColumn] = []

        for col in table.columns:
            is_hidden = self._should_hide_column(col, role)
            summarize_by = self._infer_summarize_by(col, role)
            format_string = self._infer_format_string(col)

            semantic_cols.append(
                SemanticColumn(
                    name=col.name,
                    data_type=col.pbi_type,
                    is_hidden=is_hidden,
                    summarize_by=summarize_by,
                    format_string=format_string,
                    description=col.description,
                    display_folder=self._infer_display_folder(col, is_hidden),
                    source_column=col.name,
                )
            )

        return semantic_cols

    def _should_hide_column(self, col: ColumnRaw, role: TableRole) -> bool:
        """
        Oculta claves foráneas en tablas de hechos y claves técnicas
        para forzar el filtrado desde las dimensiones.
        """
        name_lower = col.name.lower()

        # En Facts, todas las claves foráneas (FKey) y surrogate deben ocultarse
        if role == TableRole.FACT:
            if col.is_foreign:
                return True
            if name_lower.startswith("sk_") or name_lower.startswith("id_"):
                return True

        # En Dimensiones, ocultar la surrogate key técnica si no es identificador de negocio
        if role == TableRole.DIMENSION:
            if col.is_foreign:
                return True  # Snowflakes intermedias
            # Si es la Surrogate Key técnica (SK_...) en Dimensión, se oculta
            if name_lower.startswith("sk_"):
                return True

        return False

    def _infer_summarize_by(self, col: ColumnRaw, role: TableRole) -> SummarizeBy:
        """Determina la agregación por defecto en Power BI."""
        name_lower = col.name.lower()

        # Claves, identificadores, códigos, periodos y flags binarios NO deben sumarse
        if col.is_primary or col.is_foreign:
            return SummarizeBy.NONE
        if name_lower.startswith("sk_") or name_lower.startswith("id_") or name_lower.startswith("codigo_"):
            return SummarizeBy.NONE
        if name_lower.startswith("es_") or name_lower.startswith("is_"):
            return SummarizeBy.NONE
        if "segundo_dia" in name_lower or "periodo" in name_lower:
            return SummarizeBy.NONE

        # Si no es numérico, no se agrega
        if col.pbi_type not in (PbiDataType.INT64, PbiDataType.DOUBLE, PbiDataType.DECIMAL):
            return SummarizeBy.NONE

        # En Dimensiones, evitar sumas por defecto de atributos numéricos (ej. año, día, cant_coches)
        if role == TableRole.DIMENSION:
            return SummarizeBy.NONE

        # En Facts numéricos, sumar por defecto
        return SummarizeBy.SUM

    def _infer_format_string(self, col: ColumnRaw) -> str:
        """Infiere formato de presentación visual inicial."""
        name_lower = col.name.lower()
        if "clp" in name_lower:
            return "$#,0;($#,0);$0"
        if "usd" in name_lower:
            return "$#,0.00;($#,0.00);$0.00"
        if "pct" in name_lower or "porcentaje" in name_lower:
            return "0.0%"
        if col.pbi_type == PbiDataType.INT64:
            return "#,0"
        if col.pbi_type in (PbiDataType.DOUBLE, PbiDataType.DECIMAL):
            return "#,0.00"
        return ""

    def _infer_display_folder(self, col: ColumnRaw, is_hidden: bool) -> str:
        """Agrupa atributos en carpetas lógicas en el visor de campos."""
        if is_hidden:
            return "_Claves Técnicas"
        name_lower = col.name.lower()
        if "clp" in name_lower or "usd" in name_lower or "ingreso" in name_lower or "costo" in name_lower:
            return "Finanzas"
        if "temp" in name_lower or "voltaje" in name_lower or "vibracion" in name_lower or "velocidad" in name_lower:
            return "Telemetría & Sensores"
        return "Detalle"
