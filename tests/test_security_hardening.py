"""
Tests for Security Hardening, Path Traversal Defenses, Secret Scanning, and Semantic Injection.
"""
from pathlib import Path
import pytest

from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    DiagnosticCategory,
    DiagnosticSeverity,
    EntityRole,
    SemanticAttribute,
    SemanticEntity,
    SemanticMetric,
)
from src.core.ast.semantic import PbiDataType, SemanticColumn, SemanticModel, SemanticTable
from src.core.emitter.pbip_writer import PbipWriter
from src.core.emitter.table_emitter import TableEmitter
from src.core.quality.dax_validator import validate_dax_expression, validate_project_dax_metrics
from src.core.security.sanitize import (
    resolve_within,
    safe_filename,
    sanitize_company_id,
    validate_culture_code,
)
from src.core.security.secret_scanner import scan_text_for_secrets


# ==============================================================================
# 1. Path Traversal & Sanitization Tests
# ==============================================================================

def test_path_traversal_rejection():
    """Verifica que sanitize_company_id rechaza secuencias de path traversal y caracteres peligrosos."""
    malicious_inputs = [
        "../../etc/passwd",
        r"..\..\windows\system32",
        "company/subfolder",
        r"company\subfolder",
        "acme\nmalicious",
        "",
        "   ",
        "company*",
        "company;rm -rf",
        "a" * 65,  # Excede longitud máxima segura
    ]

    for bad in malicious_inputs:
        with pytest.raises(ValueError, match="Identificador de empresa inválido"):
            sanitize_company_id(bad)

    # Casos legítimos permitidos
    assert sanitize_company_id("metro_santiago") == "metro_santiago"
    assert sanitize_company_id("enterprise-retail_01") == "enterprise-retail_01"
    assert sanitize_company_id("Company123") == "Company123"


def test_resolve_within_defense(tmp_path: Path):
    """Verifica que resolve_within bloquea intentos de escapar del directorio base."""
    base_dir = tmp_path / "inputs" / "companies"
    base_dir.mkdir(parents=True, exist_ok=True)

    legit_dir = base_dir / "metro_santiago"
    legit_dir.mkdir()

    # Acceso dentro de la base
    resolved = resolve_within(base_dir, legit_dir)
    assert resolved == legit_dir.resolve()

    # Intento de escape
    escape_target = base_dir / ".." / "unauthorized"
    with pytest.raises(PermissionError, match="intenta escapar del directorio base"):
        resolve_within(base_dir, escape_target)


def test_safe_filename():
    """Verifica que safe_filename elimina caracteres de navegación o peligro."""
    assert safe_filename("../../malicious_table") == "malicious_table"
    assert safe_filename(r"..\..\windows_table") == "windows_table"
    assert safe_filename("table/name") == "table_name"
    assert safe_filename("table\x00null") == "table_null"
    assert safe_filename("") == "unnamed_entity"


def test_validate_culture_code():
    """Verifica validación estricta de códigos de cultura Power BI."""
    assert validate_culture_code("es-CL") == "es-CL"
    assert validate_culture_code("en-US") == "en-US"
    assert validate_culture_code("pt") == "pt"

    with pytest.raises(ValueError, match="Código de cultura inválido"):
        validate_culture_code("../es-CL")
    with pytest.raises(ValueError, match="Código de cultura inválido"):
        validate_culture_code("es-CL; malicious")


# ==============================================================================
# 2. Secret Scanning & Credential Defense Tests
# ==============================================================================

def test_secret_leak_detection():
    """Verifica que se detecten secretos, tokens Bearer y claves privadas."""
    bad_yaml = """
    semantic_governance:
      data_domain: Retail
      client_secret: "superSecretAzureKey34CharactersLongAbcDefGhi"
      authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummyPayload.dummySignature123"
    """
    findings = scan_text_for_secrets(bad_yaml, filename="company_profile.yaml")
    assert len(findings) >= 2
    rule_ids = {f.rule_id for f in findings}
    assert "SEC_LEAK_001" in rule_ids or "SEC_LEAK_003" in rule_ids

    # Bloque PEM
    pem_text = """
    -----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEA0...
    -----END RSA PRIVATE KEY-----
    """
    pem_findings = scan_text_for_secrets(pem_text)
    assert any(f.rule_id == "SEC_LEAK_002" for f in pem_findings)


def test_secret_findings_do_not_echo_secret_value():
    """Verifica que el scanner NUNCA expone el secreto en logs o diagnósticos."""
    secret_value = "VERY_CONFIDENTIAL_KEY_9876543210123456"
    text = f"api_key: '{secret_value}'"
    findings = scan_text_for_secrets(text)
    assert len(findings) > 0
    for f in findings:
        diag = f.format_diagnostic()
        assert secret_value not in diag
        assert secret_value not in f.description


def test_secret_scanner_negative_clean_text():
    """Verifica que textos normales sin credenciales no disparen falsos positivos."""
    clean_text = """
    overview:
      company_name: Metro de Santiago
      summary: Red de transporte metropolitano de pasajeros.
    semantic_governance:
      data_domain: Transporte
      owner: Gerencia de Operaciones
    """
    findings = scan_text_for_secrets(clean_text)
    assert len(findings) == 0


# ==============================================================================
# 3. DAX Lexical Validation & Semantic Injection Tests
# ==============================================================================

def test_dax_injection_and_unbalanced_formula():
    """Verifica rechazo de comandos administrativos y balanceo de delimitadores."""
    # 1. Delimitadores desbalanceados
    unbalanced = "CALCULATE(SUM('Fact_Ventas'[Monto])"
    diags = validate_dax_expression(unbalanced)
    assert any(d.code == "DAX_UNCLOSED_001" for d in diags)

    # 2. Delimitador de cierre extra
    extra_close = "SUM('Fact_Ventas'[Monto]))"
    diags2 = validate_dax_expression(extra_close)
    assert any(d.code == "DAX_UNBALANCED_001" for d in diags2)

    # 3. Intento de Semantic Injection administrativa (EVALUATE / DROP)
    injection = "EVALUATE 'Fact_Ventas'"
    diags3 = validate_dax_expression(injection)
    assert any(d.code == "DAX_INJECTION_001" for d in diags3)

    sql_injection = "1; DROP TABLE Fact_Ventas; --"
    diags4 = validate_dax_expression(sql_injection)
    assert any(d.code == "DAX_INJECTION_001" for d in diags4)

    # 4. VAR sin RETURN
    var_no_return = "VAR x = 10"
    diags5 = validate_dax_expression(var_no_return)
    assert any(d.code == "DAX_VAR_RETURN_001" for d in diags5)

    # 5. Caso legítimo válido
    valid_dax = "CALCULATE(SUM('Fact_Ventas'[Monto]), 'Dim_Fecha'[Anio] = 2026)"
    assert len(validate_dax_expression(valid_dax)) == 0


def test_dax_with_parentheses_inside_string():
    """Verifica que caracteres dentro de cadenas de texto DAX no confundan el validador."""
    dax_with_string = 'IF(ISBLANK([Monto]), "N/A (Sin registro)", "OK")'
    diags = validate_dax_expression(dax_with_string)
    assert len(diags) == 0


# ==============================================================================
# 4. Emitter Hardening Tests (V-1, V-3, V-5)
# ==============================================================================

def test_table_name_traversal_in_pbip_writer(tmp_path: Path):
    """Verifica que PbipWriter no permite escapar del directorio de tablas (V-1)."""
    model = SemanticModel(
        name="SecurityTestModel",
        tables=[
            SemanticTable(
                name="../../malicious_table",
                columns=[
                    SemanticColumn(name="ID", data_type=PbiDataType.INT64)
                ]
            )
        ]
    )

    writer = PbipWriter()
    out_dir = tmp_path / "pbip_out"
    pbip_file = writer.write_bundle(model, out_dir)
    assert pbip_file.exists()

    tables_dir = out_dir / "SecurityTestModel.SemanticModel" / "definition" / "tables"
    # El archivo generado debe tener el nombre seguro sin secuencias relativas
    generated_file = tables_dir / "malicious_table.tmdl"
    assert generated_file.exists()
    assert not (out_dir / "malicious_table.tmdl").exists()


def test_m_script_injection_in_column_name():
    """Verifica que TableEmitter escape comillas dobles en nombres de columna en script M (V-3)."""
    table = SemanticTable(
        name="TestTable",
        columns=[
            SemanticColumn(
                name='Injected"Code"Column',
                data_type=PbiDataType.STRING
            )
        ]
    )
    emitter = TableEmitter()
    tmdl = emitter.emit_table(table)
    # En M, la comilla doble debe estar duplicada: ""
    assert 'Injected""Code""Column' in tmdl
    assert 'table TestTable' in tmdl
