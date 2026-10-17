"""
Sanitization and path traversal defense primitives.
"""
import re
from pathlib import Path

_COMPANY_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")
_CULTURE_RE = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")


def sanitize_company_id(company_id: str) -> str:
    """
    Sanitiza y valida estrictamente un identificador de empresa / perfil.
    Rechaza path traversal, caracteres especiales, espacios o saltos de línea.
    """
    if not isinstance(company_id, str) or not _COMPANY_RE.fullmatch(company_id):
        raise ValueError(
            f"Identificador de empresa inválido '{company_id}'. "
            "Solo se permiten caracteres alfanuméricos, guiones y guiones bajos (1-64 caracteres)."
        )
    return company_id


def resolve_within(base: Path, candidate: Path) -> Path:
    """
    Resuelve una ruta y garantiza que se encuentre estrictamente dentro de la ruta base permitida.
    Lanza PermissionError en caso de intento de escape de directorio (Path Traversal).
    """
    base_resolved = base.resolve()
    candidate_resolved = candidate.resolve()

    try:
        is_safe = candidate_resolved.is_relative_to(base_resolved)
    except AttributeError:
        # Fallback for older python if ever needed
        try:
            candidate_resolved.relative_to(base_resolved)
            is_safe = True
        except ValueError:
            is_safe = False

    if not is_safe:
        raise PermissionError(
            f"Acceso no autorizado: la ruta '{candidate_resolved}' intenta escapar del directorio base '{base_resolved}'."
        )

    return candidate_resolved


def safe_filename(name: str) -> str:
    """
    Convierte un nombre (e.g. de tabla o modelo) en un nombre de archivo seguro.
    Elimina separadores de ruta (/ o \\), componentes de traversal ('..') y caracteres peligrosos.
    """
    if not name or not isinstance(name, str):
        return "unnamed_entity"
    
    # Reemplazar caracteres no permitidos
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "_", name).strip()
    # Eliminar secuencias relativas
    cleaned = re.sub(r"\.{2,}", "_", cleaned)
    cleaned = cleaned.lstrip("._")
    
    return cleaned or "entity"


def validate_culture_code(culture: str) -> str:
    """
    Valida que un código de cultura (e.g., 'es-CL', 'en-US') tenga formato estándar BCP-47
    y no contenga caracteres que puedan manipular el sistema de archivos.
    """
    if not isinstance(culture, str) or not _CULTURE_RE.fullmatch(culture):
        raise ValueError(f"Código de cultura inválido: '{culture}'. Formato esperado: 'es-CL', 'en-US', etc.")
    return culture
