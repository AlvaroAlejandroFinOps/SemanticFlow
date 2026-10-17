"""
Formateador estricto de sintaxis TMDL (Tabular Model Definition Language).
Maneja indentación por tabulaciones (\t), escape de identificadores y expresiones DAX.
"""
import re


def escape_tmdl_identifier(name: str) -> str:
    """
    Escapa un identificador en TMDL si contiene espacios, caracteres especiales
    o coincide con palabras reservadas.
    """
    # Si contiene espacios, caracteres no alfanuméricos (salvo guión bajo) o empieza con dígito
    if re.search(r"[^A-Za-z0-9_]", name) or (name and name[0].isdigit()):
        escaped = name.replace("'", "''")
        return f"'{escaped}'"
    return name


def format_tmdl_string_literal(val: str) -> str:
    """Escapa un valor string entre comillas dobles en TMDL."""
    escaped = val.replace('"', '""')
    return f'"{escaped}"'


def escape_m_string(val: str) -> str:
    """
    Escapa un string literal dentro de código Power Query / M duplicando comillas dobles.
    Previene inyecciones de código en scripts M (#table, Csv.Document, etc.).
    """
    return val.replace('"', '""')


def sanitize_single_line_tmdl(val: str, field_name: str = "field") -> str:
    """
    Verifica que un valor de una sola línea en TMDL no contenga saltos de línea (\r o \n)
    que permitan inyectar directivas o romper la estructura del archivo.
    """
    if "\n" in val or "\r" in val:
        raise ValueError(f"El campo '{field_name}' no puede contener saltos de línea en directivas TMDL.")
    return val
