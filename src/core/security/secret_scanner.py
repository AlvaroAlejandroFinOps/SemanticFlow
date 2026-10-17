"""
Secret Scanner and Credential Leak Defense for SemanticFlow.
"""
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class SecretFinding:
    filename: str
    line_number: int
    rule_id: str
    description: str

    def format_diagnostic(self) -> str:
        return f"[{self.rule_id}] En {self.filename}:{self.line_number} - {self.description}"


# Reglas de detección sin emitir el valor real del secreto
# 1. Bearer Token JWT (Bearer eyJ...)
_BEARER_TOKEN_RE = re.compile(r"(?i)\bBearer\s+(eyJ[a-zA-Z0-9_\-\.]{15,})")

# 2. Azure / AWS / Cloud API keys o Client Secrets asociados a claves explícitas
_ASSIGNED_SECRET_RE = re.compile(
    r"(?i)(client_secret|api_key|private_key|secret_key|auth_token|password|access_token)"
    r"\s*[:=]\s*['\"]?([a-zA-Z0-9~._\-/+=]{16,})['\"]?"
)

# 3. Encabezados de Claves Privadas PEM
_PEM_PRIVATE_KEY_RE = re.compile(r"-----BEGIN\s+([A-Z\s]+)?PRIVATE\s+KEY-----")

# 4. Detección de claves de diccionario sensibles con valores no triviales
_SENSITIVE_KEY_RE = re.compile(
    r"(?i)^\s*([a-zA-Z0-9_-]*(?:secret|token|password|bearer|api_key|private_key)[a-zA-Z0-9_-]*)\s*:\s*(.+)$"
)


def scan_text_for_secrets(content: str, filename: str = "<input>") -> List[SecretFinding]:
    """
    Escanea texto en busca de credenciales, tokens o secretos hardcodeados.
    NUNCA incluye el valor descubierto en el resultado para evitar fugas en logs o en el contexto del LLM.
    """
    findings: List[SecretFinding] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # 1. Chequeo Bearer Token
        if _BEARER_TOKEN_RE.search(line):
            findings.append(
                SecretFinding(
                    filename=filename,
                    line_number=idx,
                    rule_id="SEC_LEAK_001",
                    description="Se detectó un token de autorización Bearer en texto plano.",
                )
            )

        # 2. Chequeo PEM Private Key
        if _PEM_PRIVATE_KEY_RE.search(line):
            findings.append(
                SecretFinding(
                    filename=filename,
                    line_number=idx,
                    rule_id="SEC_LEAK_002",
                    description="Se detectó un bloque de clave privada PEM.",
                )
            )

        # 3. Chequeo de asignación de credencial o secreto explícito
        secret_match = _ASSIGNED_SECRET_RE.search(line)
        if secret_match:
            findings.append(
                SecretFinding(
                    filename=filename,
                    line_number=idx,
                    rule_id="SEC_LEAK_003",
                    description=f"Se detectó un secreto o clave asignada a '{secret_match.group(1)}'.",
                )
            )
            continue

        # 4. Chequeo de claves YAML sensibles
        yaml_match = _SENSITIVE_KEY_RE.search(line)
        if yaml_match:
            val = yaml_match.group(2).strip().strip("'\"")
            # Ignorar si es un placeholder o variable de entorno tipo ${ENV} o null / vacio
            if val and not (val.startswith("${") or val in ("null", "~", "None", "") or val.startswith("<")):
                findings.append(
                    SecretFinding(
                        filename=filename,
                        line_number=idx,
                        rule_id="SEC_LEAK_004",
                        description=f"Clave sensible sospechosa detectada en estructura de datos: '{yaml_match.group(1)}'.",
                    )
                )

    return findings


def scan_file_for_secrets(file_path: Path) -> List[SecretFinding]:
    """
    Escanea un archivo en el sistema de archivos buscando secretos.
    """
    if not file_path.exists() or not file_path.is_file():
        return []
    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        return scan_text_for_secrets(content, filename=str(file_path))
    except Exception as e:
        return [
            SecretFinding(
                filename=str(file_path),
                line_number=0,
                rule_id="SEC_IO_ERROR",
                description=f"Error leyendo archivo para escaneo de seguridad: {e}",
            )
        ]
