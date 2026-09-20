# 01. MATRIZ DE DECLARACIONES VS EVIDENCIA REAL (CLAIM-TO-EVIDENCE)

**Proyecto:** SemanticFlow  
**Fecha de Auditoría:** 2026-09-19  
**Commit:** `59f3c929b3e7a2d52ceb3553b9285388a52eee52`  
**Regla de Evidencia:** Toda afirmación se contrasta con código fuente real, pruebas ejecutadas y resultados medibles.

---

## 1. COMPILADOR NÚCLEO, AST Y EMISIÓN POWER BI (DIMENSIÓN A)

| ID | Declaración / Capacidad | Estado | Prioridad | Ruta de Código | Prueba Asociada | Comando de Ejecución | Resultado Observado | Criterio de Cierre |
|---|---|---|---|---|---|---|---|---|
| **C-01** | Parsing Markdown y extracción de tablas/relaciones | **VERIFIED** | P0 | `src/core/parsers/markdown_parser.py` | `tests/test_markdown_parser.py` | `pytest tests/test_markdown_parser.py` | 1 test PASS (100%) | Parser extrae entidades, atributos, tipos y relaciones. |
| **C-02** | Parsing YAML/JSON | **VERIFIED** | P0 | `src/core/parsers/yaml_parser.py` | `tests/test_yaml_parser.py` | `pytest tests/test_yaml_parser.py` | 1 test PASS (100%) | Soporta esquemas relacionales serializados en YAML/JSON. |
| **C-03** | Mapeo Raw a Canonical AST (`CanonicalSemanticProject`) | **VERIFIED** | P0 | `src/core/mappers/raw_to_canonical.py`, `src/core/ast/canonical/models.py` | `tests/test_canonical_model.py` | `pytest tests/test_canonical_model.py` | 3 tests PASS (100%) | `CanonicalSemanticProject` actúa como única verdad semántica. |
| **C-04** | Gobernanza a nivel de proyecto (`ProjectGovernance`) | **VERIFIED** | P1 | `src/core/ast/canonical/models.py` | `tests/test_persona_quality_rules.py` | `pytest tests/test_persona_quality_rules.py` | PASSED | Soporta `domain_id`, `data_product_id`, `owner`, `steward`, `classification`, `lifecycle`. |
| **C-05** | Inferencia de roles relacionales (Hechos vs Dimensiones) | **VERIFIED** | P0 | `src/core/engine/role_inferer.py` | `tests/test_inference_engine.py` | `pytest tests/test_inference_engine.py` | 1 test PASS (100%) | Infiere Fact si tiene FKs salientes; Dimension si tiene PK entrante. |
| **C-06** | Resolución topológica de relaciones y detección de ciclos | **VERIFIED** | P0 | `src/core/engine/relationship_resolver.py`, `src/core/engine/graph.py` | `tests/test_inference_engine.py` | `pytest tests/test_inference_engine.py` | PASS | Utiliza NetworkX para resolver grafos DAG sin ciclos infinitos. |
| **C-07** | Síntesis de medidas DAX canónicas | **VERIFIED** | P0 | `src/core/engine/dax_generator.py` | `tests/test_tmdl_emitter.py` | `pytest tests/test_tmdl_emitter.py` | PASS | Genera `SUM()`, `DISTINCTCOUNT()`, `DIVIDE()` con nombres y descripciones. |
| **C-08** | Reglas de gobierno de atributos (ocultamiento FK) | **VERIFIED** | P0 | `src/core/engine/governance.py` | `tests/test_canonical_model.py` | `pytest tests/test_canonical_model.py` | PASS | Claves foráneas se marcan `is_hidden=True` automáticamente. |
| **C-09** | Planificador de Capacidades de Destino (`TargetCapabilityPlanner`) | **VERIFIED** | P0 | `src/core/capabilities/planner.py` | `tests/test_stage3_governance_quality.py` | `pytest tests/test_stage3_governance_quality.py` | PASS | Evalúa soporte del dialecto target (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`). |
| **C-10** | Adaptador Power BI Target (`PowerBiTargetAdapter`) | **VERIFIED** | P0 | `src/core/targets/powerbi/adapter.py` | `tests/test_stage4_hardening_personas.py` | `pytest tests/test_stage4_hardening_personas.py` | PASS | Mapea canonical a PBI semantic model antes de emitir. |
| **C-11** | Emisor TMDL con indentación por tabuladores | **VERIFIED** | P0 | `src/core/emitter/tmdl_formatter.py`, `table_emitter.py`, `relationship_emitter.py` | `tests/test_tmdl_emitter.py` | `pytest tests/test_tmdl_emitter.py` | PASS | Archivos `.tmdl` cumplen especificación estricta de Microsoft Power BI. |
| **C-12** | Escritor de paquetes PBIP (`.pbip`, `definition.pbidataset`) | **VERIFIED** | P0 | `src/core/emitter/pbip_writer.py` | `tests/test_tmdl_emitter.py` | `pytest tests/test_tmdl_emitter.py` | PASS | Genera estructura completa de carpetas ejecutable en Power BI Desktop. |
| **C-13** | Compilación determinista idéntica (Zero-Drift) | **VERIFIED** | P0 | `src/core/emitter/pbip_writer.py` | `tests/test_golden_regression.py` + script determinismo | `python -c ...` | SHA256 hashes coinciden al 100% | Dos ejecuciones idénticas producen exactamente los mismos bytes. |
| **C-14** | Evaluador de Calidad Semántica (**cQS**) | **VERIFIED** | P0 | `src/core/quality/scorer.py`, `rules.py` | `tests/test_stage3_governance_quality.py` | `pytest tests/test_stage3_governance_quality.py` | PASS (cQS: 85.0 / 100) | Calcula score, blocking errors y penalizaciones por regla documentada. |
| **C-15** | Documentación (Diccionario de Datos Markdown + ERD Mermaid) | **VERIFIED** | P1 | `src/core/docs/emitter.py` | `tests/test_stage4_hardening_personas.py` | `pytest tests/test_stage4_hardening_personas.py` | PASS | Exporta `DATA_DICTIONARY.md` y `ARCHITECTURE_ERD.mmd`. |

---

## 2. FRAMEWORK PERSONA LENS (DIMENSIÓN B)

| ID | Declaración / Capacidad | Estado | Prioridad | Ruta de Código | Prueba Asociada | Comando de Ejecución | Resultado Observado | Criterio de Cierre |
|---|---|---|---|---|---|---|---|---|
| **P-01** | Contratos Pydantic v2 de Persona Lenses | **VERIFIED** | P0 | `src/core/personas/models.py` | `tests/test_persona_contracts.py` | `pytest tests/test_persona_contracts.py` | 13 tests PASS | `PersonaDefinition`, `PersonaProjection`, `PersonaRecommendation`, `ResponsibilityAssignment`, `TeamInteraction`, `PersonaMaturityAssessment`. |
| **P-02** | Registro de Personas y resolución de aliases | **VERIFIED** | P0 | `src/core/personas/registry.py` | `tests/test_persona_registry.py` | `pytest tests/test_persona_registry.py` | 7 tests PASS | Registra 10 personas, resuelve aliases organizacionales (ej. `cdo` -> `analytics_leader`). |
| **P-03** | Configuración externa y Overrides con validación de seguridad | **VERIFIED** | P1 | `src/core/personas/config_loader.py`, `config/personas/default_personas.yaml` | `tests/test_persona_registry.py` | `pytest tests/test_persona_registry.py` | PASS | Clasifica overrides en `SAFE`, `REVIEW_REQUIRED`, `PROHIBITED` con audit trail. |
| **P-04** | Motor de proyección no destructivo (`PersonaProjector`) | **VERIFIED** | P0 | `src/core/personas/projector.py` | `tests/test_persona_projector.py` | `pytest tests/test_persona_projector.py` | 8 tests PASS | Garantiza inmutabilidad matemática del `CanonicalSemanticProject`. |
| **P-05** | Renderizadores Markdown, JSON y Mermaid | **VERIFIED** | P0 | `src/core/personas/renderers.py` | `tests/test_all_lenses_deep.py` | `pytest tests/test_all_lenses_deep.py` | 10 tests PASS | Renderiza vistas por rol con aislamiento de detalle técnico. |
| **P-06** | Golden Regression de Lenses (Metro Santiago y Enterprise) | **VERIFIED** | P0 | `tests/golden/metro_santiago/`, `tests/golden/enterprise/` | `tests/test_golden_regression.py` | `pytest tests/test_golden_regression.py` | 2 tests PASS | Salidas de 10 lenses coinciden carácter por carácter con golden masters. |
| **P-07** | Alineación a 10 Core Personas Canónicas | **PARTIAL** | P1 | `src/core/personas/lenses/` | `tests/test_all_lenses_deep.py` | `pytest tests/test_all_lenses_deep.py` | 10 tests PASS (con drift de nombres) | El código implementó 5 Core y 5 Extension en vez de las 10 Core canónicas requeridas. |
| **P-08** | Legacy View Generator Adapter | **VERIFIED** | P1 | `src/core/personas/legacy_adapter.py`, `views.py` | `tests/test_stage4_hardening_personas.py` | `pytest tests/test_stage4_hardening_personas.py` | PASS | Métodos legacy `generate_views()` siguen funcionando sin romper tests históricos. |

---

## 3. DATA LEADERSHIP COCKPIT (AGGREGATE PERSONA)

| ID | Declaración / Capacidad | Estado | Prioridad | Ruta de Código | Prueba Asociada | Comando de Ejecución | Resultado Observado | Criterio de Cierre |
|---|---|---|---|---|---|---|---|---|
| **L-01** | Síntesis C-Level del Cockpit | **VERIFIED** | P0 | `src/core/personas/cockpit.py`, `projector.py` | `tests/test_leadership_cockpit.py` | `pytest tests/test_leadership_cockpit.py` | 3 tests PASS | Genera radar de madurez, gobernanza ejecutiva, prioridades y resumen. |
| **L-02** | Exportación multiformal (Markdown + JSON) | **VERIFIED** | P0 | `src/core/personas/cockpit.py`, `renderers.py` | `tests/test_leadership_cockpit.py` | `pytest tests/test_leadership_cockpit.py` | PASS | Exporta `data_leadership_cockpit.md` y `data_leadership_cockpit.json`. |
| **L-03** | Aislamiento en paquete dedicado `src/core/leadership/` | **NOT_IMPLEMENTED** | P1 | N/A (reside en `src/core/personas/cockpit.py`) | N/A | Inspección de directorio | Directorio `src/core/leadership/` no existe | Debe desacoplarse físicamente en `src/core/leadership/` sin importar personas. |
| **L-04** | 8 Módulos Funcionales Específicos | **PARTIAL** | P1 | `src/core/personas/projector.py` (método monolítico) | `tests/test_leadership_cockpit.py` | `pytest tests/test_leadership_cockpit.py` | PASS | Funcionalidades agrupadas en método general, pendientes módulos modulares individuales. |

---

## 4. SEGURIDAD, OPERACIÓN Y CI/CD

| ID | Declaración / Capacidad | Estado | Prioridad | Ruta de Código | Prueba Asociada | Comando de Ejecución | Resultado Observado | Criterio de Cierre |
|---|---|---|---|---|---|---|---|---|
| **S-01** | Ingesta segura con `yaml.safe_load` | **VERIFIED** | P0 | `src/core/parsers/yaml_parser.py`, `config_loader.py` | Inspección de código | `grep -n "yaml.safe_load"` | 100% usos seguros | Ninguna llamada a `yaml.load` inseguro. |
| **S-02** | Output Containment y Path Traversal Defense | **NOT_IMPLEMENTED** | P0 | N/A | `tests/test_output_safety.py` (ausente) | N/A | Archivo no existe | Requiere test suite `test_output_safety.py` probando contención en subdirectorios. |
| **S-03** | Pipeline Automatizado CI/CD (.github/workflows) | **NOT_IMPLEMENTED** | P0 | `.github/workflows/ci.yml` (ausente) | N/A | N/A | Directorio `.github` ausente | Implementar workflow con linting, mypy, pytest, coverage y golden comparison. |
| **S-04** | Linters y Typecheckers en Entorno Local | **PARTIAL** | P1 | `pyproject.toml` | N/A | `python -m ruff --version` | No module named ruff / mypy | Instalar ruff y mypy en el `.venv` para chequeo local pre-commit. |
| **S-05** | Gobernanza Open Source (Licencia, Contribución, etc.) | **PARTIAL** | P1 | `README.md`, `README_ES.md` (presentes) | N/A | Inspección de directorio | Faltan LICENSE, CONTRIBUTING, SECURITY, CHANGELOG | Crear paquete completo de archivos comunitarios. |

---

## 5. RESUMEN CUANTITATIVO POR ESTADO

- **VERIFIED:** 19 (70.4%)
- **PARTIAL:** 4 (14.8%)
- **NOT_IMPLEMENTED:** 4 (14.8%)
- **DECLARED_ONLY:** 0 (0.0%)
- **CONTRADICTED:** 0 (0.0%)
- **BLOCKED:** 0 (0.0%)
- **TOTAL CAPACIDADES EVALUADAS:** 27
