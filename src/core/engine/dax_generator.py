"""
Síntesis automática de medidas DAX base para tablas de hechos.
"""
from src.core.ast.schema import ColumnRaw, TableRaw
from src.core.ast.semantic import SemanticMeasure, TableRole
from src.core.ast.types import PbiDataType


class DaxGenerator:
    """Genera medidas DAX analíticas estándar (COUNTROWS, SUM, AVERAGE, RATIOS)."""

    def generate_measures(self, table: TableRaw, role: TableRole) -> list[SemanticMeasure]:
        measures: list[SemanticMeasure] = []

        if role != TableRole.FACT:
            return measures

        # 1. Medida base de conteo de transacciones/eventos
        clean_table_name = table.name.replace("Fact_", "").replace("_", " ")
        measures.append(
            SemanticMeasure(
                name=f"# Registros {clean_table_name}",
                expression=f"COUNTROWS('{table.name}')",
                format_string="#,0",
                display_folder="_KPIs Base",
                description=f"Total de registros/eventos en {table.name}",
            )
        )

        # 2. Medidas por columna métrica cuantitativa
        for col in table.columns:
            if not self._is_metric_column(col):
                continue

            col_label = col.name.replace("_", " ")
            name_lower = col.name.lower()

            # Métricas financieras (CLP / USD)
            if "clp" in name_lower:
                measures.append(
                    SemanticMeasure(
                        name=f"Total {col_label}",
                        expression=f"SUM('{table.name}'[{col.name}])",
                        format_string="$#,0;($#,0);$0",
                        display_folder="_Métricas Financieras",
                        description=f"Suma total de {col.name}",
                    )
                )
            elif "usd" in name_lower:
                measures.append(
                    SemanticMeasure(
                        name=f"Total {col_label}",
                        expression=f"SUM('{table.name}'[{col.name}])",
                        format_string="$#,0.00;($#,0.00);$0.00",
                        display_folder="_Métricas Financieras",
                        description=f"Suma total de {col.name}",
                    )
                )
            # Ratios y Porcentajes
            elif "pct" in name_lower or "porcentaje" in name_lower:
                measures.append(
                    SemanticMeasure(
                        name=f"Promedio {col_label}",
                        expression=f"AVERAGE('{table.name}'[{col.name}])",
                        format_string="0.0%",
                        display_folder="_KPIs Calidad & Operación",
                        description=f"Promedio de {col.name}",
                    )
                )
            # NPS y Scores
            elif "nps" in name_lower or "score" in name_lower:
                measures.append(
                    SemanticMeasure(
                        name=f"Promedio {col_label}",
                        expression=f"AVERAGE('{table.name}'[{col.name}])",
                        format_string="#,0.0",
                        display_folder="_KPIs Calidad & Operación",
                        description=f"Promedio de {col.name}",
                    )
                )
            # Métricas físicas y de telemetría continuas
            else:
                measures.append(
                    SemanticMeasure(
                        name=f"Total {col_label}",
                        expression=f"SUM('{table.name}'[{col.name}])",
                        format_string="#,0.00",
                        display_folder="_Operaciones & Sensores",
                        description=f"Suma acumulada de {col.name}",
                    )
                )
                measures.append(
                    SemanticMeasure(
                        name=f"Promedio {col_label}",
                        expression=f"AVERAGE('{table.name}'[{col.name}])",
                        format_string="#,0.00",
                        display_folder="_Operaciones & Sensores",
                        description=f"Promedio de {col.name}",
                    )
                )

        return measures

    def _is_metric_column(self, col: ColumnRaw) -> bool:
        """Determina si una columna es candidata para medidas aditivas/promedios."""
        if col.is_primary or col.is_foreign:
            return False

        name_lower = col.name.lower()
        if name_lower.startswith("sk_") or name_lower.startswith("id_"):
            return False
        if "segundo_dia" in name_lower or "posicion_" in name_lower or "estado_" in name_lower:
            return False
        if col.raw_type.lower() in ("int8", "int16") and name_lower.startswith("es_"):
            return False

        return col.pbi_type in (PbiDataType.INT64, PbiDataType.DOUBLE, PbiDataType.DECIMAL)
