# 07. AUDITORÍA DE SEGURIDAD Y SEGURIDAD DE SALIDAS (SECURITY & OUTPUT SAFETY)

**Proyecto:** SemanticFlow  
**Fecha de Auditoría:** 2026-09-19  
**Commit:** `59f3c929b3e7a2d52ceb3553b9285388a52eee52`  

---

## 1. EVALUACIÓN DEL CHECKLIST DE SEGURIDAD

| Control de Seguridad | Estado | Evidencia / Ubicación | Diagnóstico y Riesgo |
|---|---|---|---|
| **1. Uso universal de `yaml.safe_load`** | ✅ VERIFIED | `src/core/parsers/yaml_parser.py`, `src/core/personas/config_loader.py` | 100% de llamadas utilizan `yaml.safe_load`. Cero riesgo de ejecución arbitraria de código al leer YAML. |
| **2. Cero secretos en fixtures y golden files** | ✅ VERIFIED | `tests/fixtures/`, `tests/golden/` | Inspección de strings: no hay credenciales, tokens, contraseñas ni cadenas de conexión hardcodeadas. |
| **3. Política de visibilidad PII por Persona** | ✅ VERIFIED | `src/core/personas/renderers.py`, `lenses/` | Roles de consumo (`DATA_ANALYST`, `BUSINESS_CONSUMER`) no tienen visibilidad de atributos marcados con PII o clasificados como confidenciales. |
| **4. Telemetría desactivada por defecto** | ✅ VERIFIED | Todo el codebase | El compilador es 100% local, offline, in-memory; no envía telemetría de red ni realiza llamadas HTTP. |
| **5. Prohibición de puntuación individual (HR Safety)**| ✅ VERIFIED | `src/core/personas/projector.py` | Las matrices RACI y recomendaciones organizacionales solo asignan roles a artefactos, sin evaluar personas individuales. |
| **6. Tests de Path Traversal (`../`)** | ❌ NOT_IMPLEMENTED (P0) | Ausente | El CLI y los writers (`pbip_writer.py`, `cockpit.py`) no validan explícitamente si un `--output` malicioso intenta escribir fuera del árbol permitido. |
| **7. Tests de Symlink Escape** | ❌ NOT_IMPLEMENTED (P0) | Ausente | No hay validación contra enlaces simbólicos que apunten a ubicaciones críticas del sistema de archivos. |
| **8. Contención de salida (Output Containment)** | ❌ NOT_IMPLEMENTED (P0) | Ausente | No existe suite de pruebas dedicada `tests/test_output_safety.py`. |
| **9. Reemplazo atómico y staging temporal** | ⚠️ PARTIAL | `src/core/emitter/pbip_writer.py` | Escribe directamente en el directorio destino con `mkdir(parents=True, exist_ok=True)`. Si el proceso se interrumpe, puede dejar un estado corrupto parcial. |
| **10. Protección de raíz del repositorio** | ⚠️ PARTIAL | CLI options | Se debe forzar que el compilador rechace explícitamente escribir sobre la raíz del repositorio (`.` o `/`). |

---

## 2. ESPECIFICACIÓN DEL REQUISITO CRÍTICO: `tests/test_output_safety.py`

Para superar el Gate P0 de seguridad, se debe implementar `tests/test_output_safety.py` cubriendo los siguientes casos de prueba:

1. **`test_path_traversal_prevention()`**:
   - Pasar rutas de salida con `../../` o rutas absolutas prohibidas fuera del workspace.
   - Debe lanzar una excepción de validación y detener la ejecución sin crear archivos.
2. **`test_atomic_write_preserves_previous_build_on_failure()`**:
   - Simular un fallo forzado durante la generación de TMDL a mitad de proceso.
   - El directorio previo debe permanecer intacto mediante el uso de un directorio temporal (`.tmp_build_staging`) y reemplazo atómico (`os.replace` o `shutil.move`).
3. **`test_output_root_protection()`**:
   - Intentar compilar pasando `--output .` o `--output /`.
   - Debe ser rechazado con un código de error de seguridad.
4. **`test_pii_attribute_masking_in_consumer_lenses()`**:
   - Crear un proyecto con atributos gobernados etiquetados `PII=True` o `Confidential`.
   - Verificar que `DATA_ANALYST` y `BUSINESS_CONSUMER` nunca emiten el nombre real del campo sin enmascaramiento.
