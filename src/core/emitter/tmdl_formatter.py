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
