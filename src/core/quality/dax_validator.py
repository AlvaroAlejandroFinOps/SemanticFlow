"""
DAX Lexical Validator and Semantic Injection Defense.
Valida sintaxis básica, balanceo de delimitadores y bloquea inyecciones de escape administrativo en DAX.
"""
import re
from typing import List, Optional

from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    Diagnostic,
    DiagnosticCategory,
    DiagnosticSeverity,
)

# Palabras clave administrativas no operativas en medidas tabulares o de escape
_DISALLOWED_DAX_KEYWORDS = [
    r"\bEVALUATE\b",
    r"\bDEFINE\b",
    r"\bORDER\s+BY\b",
    r"\bSTART\s+AT\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bSELECT\s+.+\s+FROM\b",
]

_DISALLOWED_RE = re.compile("|".join(_DISALLOWED_DAX_KEYWORDS), re.IGNORECASE)


def validate_dax_expression(expression: str, object_id: Optional[str] = None) -> List[Diagnostic]:
    """
    Realiza validación léxica de una expresión DAX:
    1. Balanceo de paréntesis (), corchetes [] y llaves {}.
    2. Bloqueo de sentencias administrativas o de escape (EVALUATE, DEFINE, DROP, etc.).
    3. Balanceo de bloques VAR ... RETURN.
    """
    diagnostics: List[Diagnostic] = []

    if not expression or not expression.strip():
        diagnostics.append(
            Diagnostic(
                code="DAX_EMPTY_001",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SEMANTIC,
                message="La expresión DAX no puede estar vacía.",
                object_id=object_id,
                suggested_action="Definir una fórmula DAX válida (ej. SUM('Tabla'[Columna])).",
            )
        )
        return diagnostics

    # 1. Quitar strings entre comillas dobles para análisis sintáctico seguro
    # En DAX las comillas dobles se escapan como ""
    in_string = False
    clean_chars = []
    i = 0
    n = len(expression)
    while i < n:
        char = expression[i]
        if char == '"':
            if in_string and i + 1 < n and expression[i + 1] == '"':
                i += 2  # comilla doble escapada
                continue
            in_string = not in_string
            clean_chars.append(" ")
            i += 1
            continue
        if in_string:
            clean_chars.append(" ")
        else:
            clean_chars.append(char)
        i += 1

    if in_string:
        diagnostics.append(
            Diagnostic(
                code="DAX_STR_001",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SEMANTIC,
                message="Cadena literal de texto no cerrada en expresión DAX (falta comilla doble de cierre).",
                object_id=object_id,
                suggested_action="Cerrar las comillas dobles en la cadena de texto de la fórmula DAX.",
            )
        )
        return diagnostics

    parsed_text = "".join(clean_chars)

    # 2. Bloqueo de inyecciones administrativas y palabras prohibidas
    match = _DISALLOWED_RE.search(parsed_text)
    if match:
        disallowed_word = match.group(0).strip()
        diagnostics.append(
            Diagnostic(
                code="DAX_INJECTION_001",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SEMANTIC,
                message=(
                    f"Comando o directiva no permitida en medida DAX: '{disallowed_word}'. "
                    "Las medidas tabulares no admiten sentencias de consulta administrativas."
                ),
                object_id=object_id,
                suggested_action="Eliminar palabras de consulta administrativas (EVALUATE, DEFINE, SQL).",
            )
        )

    # 3. Balanceo de delimitadores: (), [], {}
    # Nota: Dentro de nombres de tabla '...' los corchetes o paréntesis pueden aparecer, por lo que ignoramos '...'
    tokens_text = re.sub(r"'(?:''|[^'])*'", " 'table' ", parsed_text)

    stack = []
    matching = {")": "(", "]": "[", "}": "{"}
    pair_names = {")": "paréntesis", "]": "corchetes", "}": "llaves"}

    for idx, c in enumerate(tokens_text):
        if c in "([{":
            stack.append((c, idx))
        elif c in ")]}":
            if not stack:
                diagnostics.append(
                    Diagnostic(
                        code="DAX_UNBALANCED_001",
                        severity=DiagnosticSeverity.ERROR,
                        category=DiagnosticCategory.SEMANTIC,
                        message=f"Delimitador de cierre '{c}' ({pair_names[c]}) sin apertura correspondiente.",
                        object_id=object_id,
                        suggested_action="Verificar y balancear los delimitadores en la fórmula DAX.",
                    )
                )
                break
            top, _ = stack.pop()
            if top != matching[c]:
                diagnostics.append(
                    Diagnostic(
                        code="DAX_MISMATCH_001",
                        severity=DiagnosticSeverity.ERROR,
                        category=DiagnosticCategory.SEMANTIC,
                        message=f"Delimitador cruzado o inconsistente: se esperaba cierre de '{top}', pero se encontró '{c}'.",
                        object_id=object_id,
                        suggested_action="Revisar anidamiento de paréntesis y corchetes.",
                    )
                )
                break

    if stack and not any(d.code.startswith("DAX_") and d.code != "DAX_INJECTION_001" for d in diagnostics):
        unclosed, _ = stack[-1]
        diagnostics.append(
            Diagnostic(
                code="DAX_UNCLOSED_001",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SEMANTIC,
                message=f"Delimitador '{unclosed}' no cerrado en la expresión DAX.",
                object_id=object_id,
                suggested_action="Añadir el delimitador de cierre correspondiente.",
            )
        )

    # 4. Chequeo de variables VAR ... RETURN
    var_count = len(re.findall(r"\bVAR\b", parsed_text, re.IGNORECASE))
    return_count = len(re.findall(r"\bRETURN\b", parsed_text, re.IGNORECASE))
    if var_count > 0 and return_count == 0:
        diagnostics.append(
            Diagnostic(
                code="DAX_VAR_RETURN_001",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.SEMANTIC,
                message="Se declaró una o más variables 'VAR' sin su sentencia 'RETURN' correspondiente.",
                object_id=object_id,
                suggested_action="Añadir 'RETURN <expresion>' al bloque de variables DAX.",
            )
        )

    return diagnostics


def validate_project_dax_metrics(project: CanonicalSemanticProject) -> List[Diagnostic]:
    """Valida todas las métricas definidas en el proyecto canónico."""
    diagnostics: List[Diagnostic] = []
    for entity in project.entities:
        for metric in entity.metrics:
            if metric.expression:
                diags = validate_dax_expression(
                    metric.expression, object_id=f"{entity.name}.{metric.name}"
                )
                diagnostics.extend(diags)
    return diagnostics
