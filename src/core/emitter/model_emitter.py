"""
Generador de database.tmdl, model.tmdl y cultures/<culture>.tmdl.
"""
from src.core.ast.semantic import SemanticModel
from src.core.emitter.tmdl_formatter import escape_tmdl_identifier, format_tmdl_string_literal


class ModelEmitter:
    """Emite los archivos de configuración raíz del modelo TMDL."""

    def emit_database(self, model: SemanticModel) -> str:
        db_id = escape_tmdl_identifier(model.name)
        lines: list[str] = []
        if model.description:
            for desc_line in model.description.splitlines():
                lines.append(f"/// {desc_line}")
        lines.extend([
            f"database {db_id}",
            f"\tcompatibilityLevel: {model.compatibility_level}",
        ])
        return "\n".join(lines) + "\n"

    def emit_model(self, model: SemanticModel) -> str:
        lines: list[str] = []
        if model.description:
            for desc_line in model.description.splitlines():
                lines.append(f"/// {desc_line}")
        lines.extend([
            "model Model",
            f"\tculture: {model.culture}",
            "\tdefaultPowerBIDataSourceVersion: powerBI_V3",
            "\tsourceQueryCulture: es-CL",
            "\tdataAccessOptions",
            "\t\tlegacyRedirects",
            "\t\treturnErrorValuesAsNull",
        ])
        if model.tables:
            lines.append("")
            for t in model.tables:
                t_id = escape_tmdl_identifier(t.name)
                lines.append(f"ref table {t_id}")
        return "\n".join(lines) + "\n"

    def emit_culture(self, culture: str) -> str:
        return f"culture {culture}\n"
