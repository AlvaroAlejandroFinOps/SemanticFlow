# 10. BACKLOG DE REMEDIACIÓN PRIORIZADO (REMEDIATION BACKLOG)

**Proyecto:** SemanticFlow  
**Fecha de Auditoría:** 2026-09-19  
**Commit Base:** `59f3c929b3e7a2d52ceb3553b9285388a52eee52`  
**Regla de Ejecución:** No implementar cambios dentro de la auditoría. Este backlog define la secuencia de trabajo autorizable.

---

## BLOQUE P0: BLOQUEANTES DE RELEASE E INTEGRIDAD (RELEASE BLOCKERS) - [COMPLETADO ✅]

### P0-01: Implementación de Suite de Seguridad de Salida (`test_output_safety.py`) - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO Y VERIFICADO (3/3 tests PASS)**
- **Objetivo:** Prevenir vulnerabilidades de Path Traversal (`../../`), Symlink Escapes y escrituras fuera del destino autorizado en el CLI y generadores.
- **Entregables:** `tests/test_output_safety.py`, validaciones en `src/core/emitter/pbip_writer.py` y `src/core/personas/renderers.py`.

### P0-02: Creación del Pipeline Automatizado GitHub Actions CI/CD - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO Y VERIFICADO**
- **Objetivo:** Automatizar la validación de pull requests con linting, mypy, pytest, coverage gate y golden files en Ubuntu, Windows y macOS.
- **Entregables:** `.github/workflows/ci.yml` (multi-OS ubuntu/windows/macos, python 3.10/3.11/3.12, ruff, mypy, pytest, packaging).

### P0-03: Reemplazo Atómico y Staging Temporal en PBIP Writer - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO Y VERIFICADO**
- **Objetivo:** Asegurar que si una compilación falla a mitad de camino, el build previo permanezca íntegro.
- **Entregables:** `src/core/emitter/pbip_writer.py` con `tempfile.TemporaryDirectory` y atomic rename seguro.

---

## BLOQUE P1: BLOQUEANTES DEL ROADMAP ENTERPRISE (ROADMAP BLOCKERS) - [COMPLETADO ✅]

### P1-01: Aislamiento Físico del Paquete `src/core/leadership/` - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO Y VERIFICADO**
- **Objetivo:** Extraer el motor del Cockpit hacia `src/core/leadership/` con sus 8 módulos especializados.
- **Entregables:** `src/core/leadership/` (`portfolio.py`, `health.py`, `ownership.py`, `capability_gaps.py`, `team_dependencies.py`, `delivery_flow.py`, `value_indicators.py`, `risk.py`, `engine.py`, `__init__.py`). Adapter backward-compatible en `src/core/personas/cockpit.py`.

### P1-02: Alineación Canónica de las 10 Core Personas y Coexistencia de Extensiones - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO Y VERIFICADO (16/16 Lenses PASS)**
- **Objetivo:** Implementar explícitamente los 10 lentes canónicos y las 6 Extension Personas.
- **Entregables:** 6 nuevos lentes (`data_analyst.py`, `data_scientist.py`, `data_architect.py`, `platform_engineer.py`, `domain_owner.py`, `audit_risk.py`) + tests en `tests/test_all_lenses_deep.py`.

### P1-03: Remoción de Código Legacy Redundante (`src/core/engine/inference.py`) - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO**
- **Objetivo:** Eliminar archivo legacy sin uso.
- **Entregables:** Eliminación de `src/core/engine/inference.py`.

### P1-04: Instalación y Validación Local de `ruff` y `mypy` - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO Y VERIFICADO (0 errores / 0 warnings)**
- **Objetivo:** Instalar `ruff` y `mypy` en `.venv` y garantizar cumplimiento estricto de tipado y estilo.
- **Entregables:** `ruff check .` (0 errores), `mypy src/` (0 errores).

### P1-05: Incorporación de Gobernanza Open Source - [COMPLETADO ✅]
- **Estado:** ✅ **IMPLEMENTADO**
- **Objetivo:** Crear archivos comunitarios y de gobernanza estándar.
- **Entregables:** `LICENSE` (Apache 2.0), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`, `CHANGELOG.md`.

---

## BLOQUE P2: ENDURECIMIENTO ENTERPRISE (ENTERPRISE HARDENING)

### P2-01: Ingesta Declarativa de SQL DDL (`SqlDdlParser`)
- **Objetivo:** Permitir compilar modelos a partir de archivos `.sql` con sentencias `CREATE TABLE` usando `sqlglot`.
- **Tamaño:** **M** | **Fase Recomendada:** Fase 3.

### P2-02: Modularización de Salidas del Leadership Cockpit en `output/leadership/`
- **Objetivo:** Generar los 9 artefactos individuales JSON/MD/MMD en lugar de un único archivo consolidado.
- **Tamaño:** **M** | **Fase Recomendada:** Fase 3.

### P2-03: Versionado Formal y Registro Histórico (`CHANGELOG.md`)
- **Objetivo:** Documentar la evolución de versiones alineada a SemVer 2.0.0.
- **Tamaño:** **S** | **Fase Recomendada:** Fase 3.

---

## BLOQUE P3: CAPACIDADES FUTURAS (FUTURE ENHANCEMENTS)

### P3-01: Adaptadores de Destino Adicionales (Looker LookML, Qlik, dbt)
- **Objetivo:** Diseñar adaptadores completos para dialectos BI adicionales tras consolidar Power BI.
- **Tamaño:** **XL** | **Fase Recomendada:** Post v1.0.0.
