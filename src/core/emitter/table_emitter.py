"""
Generador del archivo tables/<TableName>.tmdl en sintaxis nativa TMDL.
"""
from pathlib import Path
from typing import Optional

from src.core.ast.semantic import SemanticTable
from src.core.emitter.tmdl_formatter import (
    escape_m_string,
    escape_tmdl_identifier,
    format_tmdl_string_literal,
    sanitize_single_line_tmdl,
)


class TableEmitter:
    """Genera la definición TMDL completa de una tabla, sus columnas, medidas y partición."""

    def emit_table(self, table: SemanticTable, data_file_path: Optional[Path] = None) -> str:
        lines: list[str] = []
        if table.description:
            for desc_line in table.description.splitlines():
                lines.append(f"/// {desc_line}")
        table_id = escape_tmdl_identifier(table.name)
        lines.append(f"table {table_id}")

        # Orden canónico determinista para columnas y medidas
        sorted_columns = sorted(table.columns, key=lambda c: (c.name.lower(), c.name))
        sorted_measures = sorted(table.measures, key=lambda m: (m.name.lower(), m.name))

        # 1. Emisión de Columnas
        for col in sorted_columns:
            lines.append("")
            if col.description:
                for desc_line in col.description.splitlines():
                    lines.append(f"\t/// {desc_line}")
            col_id = escape_tmdl_identifier(col.name)
            lines.append(f"\tcolumn {col_id}")
            lines.append(f"\t\tdataType: {col.data_type.value}")

            if col.is_hidden:
                lines.append("\t\tisHidden")

            if col.format_string:
                lines.append(f"\t\tformatString: {format_tmdl_string_literal(col.format_string)}")

            if col.summarize_by:
                lines.append(f"\t\tsummarizeBy: {col.summarize_by.value}")

            source_col = sanitize_single_line_tmdl(col.source_column or col.name, "sourceColumn")
            lines.append(f"\t\tsourceColumn: {source_col}")

            if col.display_folder:
                lines.append(f"\t\tdisplayFolder: {format_tmdl_string_literal(col.display_folder)}")

        # 2. Emisión de Medidas DAX
        for m in sorted_measures:
            lines.append("")
            if m.description:
                for desc_line in m.description.splitlines():
                    lines.append(f"\t/// {desc_line}")
            m_id = escape_tmdl_identifier(m.name)
            expr = self._format_measure_expression(m.expression)
            lines.append(f"\tmeasure {m_id} = {expr}")

            if m.format_string:
                lines.append(f"\t\tformatString: {format_tmdl_string_literal(m.format_string)}")

            if m.display_folder:
                lines.append(f"\t\tdisplayFolder: {format_tmdl_string_literal(m.display_folder)}")

            if m.is_hidden:
                lines.append("\t\tisHidden")

        # 3. Emisión de Partición M (Import Mode)
        lines.append("")
        part_id = escape_tmdl_identifier(table.name)
        lines.append(f"\tpartition {part_id} = m")
        lines.append("\t\tmode: import")
        lines.append("\t\tsource =")

        # Generar script M sintéticamente tipado o conectado a CSV real
        if data_file_path and data_file_path.exists():
            m_script = self._generate_m_partition_csv(table, data_file_path, sorted_columns)
        else:
            m_script = self._generate_m_partition(table, sorted_columns)

        for m_line in m_script.splitlines():
            lines.append(f"\t\t\t{m_line}")

        return "\n".join(lines) + "\n"

    def _format_measure_expression(self, expr: str) -> str:
        """Formatea la expresión DAX para TMDL preservando indentación segura."""
        clean_expr = expr.strip()
        lines = clean_expr.splitlines()
        if len(lines) <= 1:
            return sanitize_single_line_tmdl(clean_expr, "measure expression")
        
        # Expresión multilínea
        formatted = [lines[0]]
        for l in lines[1:]:
            formatted.append(f"\t\t{l}")
        return "\n".join(formatted)

    def _generate_m_partition_csv(self, table: SemanticTable, csv_path: Path, sorted_columns: list) -> str:
        """Genera script M que carga los datos directamente desde un archivo CSV con rutas y nombres seguros."""
        # Usar el nombre del archivo si es local o normalizar separadores
        clean_csv_name = escape_m_string(csv_path.name)
        type_transforms = []
        for col in sorted_columns:
            m_type = self._map_to_m_transform_type(col.data_type.value)
            safe_col_name = escape_m_string(col.name)
            type_transforms.append(f'{{"{safe_col_name}", {m_type}}}')
        transforms_str = "{" + ", ".join(type_transforms) + "}"
        return (
            f"let\n"
            f'    Source = Csv.Document(File.Contents("{clean_csv_name}"), [Delimiter=",", Columns={len(sorted_columns)}, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
            f'    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n'
            f'    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {transforms_str})\n'
            f"in\n"
            f'    #"Changed Type"'
        )

    def _generate_m_partition(self, table: SemanticTable, sorted_columns: list) -> str:
        """
        Genera un script M funcional de Power Query con #table y Table.TransformColumnTypes
        para que Power BI Desktop cargue el esquema sin requerir conexión a base de datos.
        """
        if not sorted_columns:
            return "let\n    Source = #table({}, {})\nin\n    Source"

        col_names = [f'"{escape_m_string(col.name)}"' for col in sorted_columns]
        col_names_str = "{" + ", ".join(col_names) + "}"

        type_transforms = []
        for col in sorted_columns:
            m_type = self._map_to_m_transform_type(col.data_type.value)
            safe_col_name = escape_m_string(col.name)
            type_transforms.append(f'{{"{safe_col_name}", {m_type}}}')
        transforms_str = "{" + ", ".join(type_transforms) + "}"

        return (
            f"let\n"
            f"    Source = #table({col_names_str}, {{}}),\n"
            f'    #"Changed Type" = Table.TransformColumnTypes(Source, {transforms_str})\n'
            f"in\n"
            f'    #"Changed Type"'
        )

    def _map_to_m_type(self, pbi_type: str) -> str:
        mapping = {
            "int64": "Int64.Type",
            "double": "number",
            "decimal": "Currency.Type",
            "string": "text",
            "dateTime": "datetime",
            "boolean": "logical",
            "binary": "binary",
        }
        return mapping.get(pbi_type, "text")

    def _map_to_m_transform_type(self, pbi_type: str) -> str:
        mapping = {
            "int64": "Int64.Type",
            "double": "type number",
            "decimal": "Currency.Type",
            "string": "type text",
            "dateTime": "type datetime",
            "boolean": "type logical",
            "binary": "type binary",
        }
        return mapping.get(pbi_type, "type text")
