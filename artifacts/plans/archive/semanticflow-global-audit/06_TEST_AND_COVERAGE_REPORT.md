# 06. REPORTE EXHAUSTIVO DE PRUEBAS Y COBERTURA (TEST & COVERAGE)

**Proyecto:** SemanticFlow  
**Fecha de Ejecución:** 2026-09-19  
**Commit:** `59f3c929b3e7a2d52ceb3553b9285388a52eee52`  
**Entorno:** Python 3.12.10 | pytest 9.1.1 | pytest-cov 7.1.0 | Coverage 7.16.0  

---

## 1. RESUMEN GLOBAL DE LA SUITE DE PRUEBAS

```
============================= 71 passed in 33.01s =============================
- Tests Unitarios e Integración Básica: 61 tests
- Tests de Estrés Masivo (Tier 1, 2, 3 y v2): 10 tests
- Total Statements: 2,461 | Statements Missing: 296
- Total Branches: 652 | Partial Branches: 91
- Cobertura Total de Líneas y Ramas: 85%
```

---

## 2. TABLA DETALLADA DE COBERTURA POR MÓDULO (`pytest --cov=src --cov-branch`)

| Módulo / Archivo Fuente | Sentencias (Stmts) | Perdidas (Miss) | Ramas (Branch) | Ramas Parciales (BrPart) | Cobertura Total | Líneas No Cubiertas / Brecha |
|---|---|---|---|---|---|---|
| `src/__init__.py` | 1 | 0 | 0 | 0 | **100%** | Ninguna |
| `src/cli.py` | 184 | 42 | 42 | 8 | **73%** | 31-35, 250-254, 439-487 (subcomandos interactivos) |
| `src/core/ast/canonical/models.py` | 158 | 6 | 20 | 3 | **93%** | 114-117, 159, 165 (validadores defensivos) |
| `src/core/ast/schema.py` | 56 | 1 | 8 | 1 | **97%** | 76 |
| `src/core/ast/semantic.py` | 70 | 2 | 8 | 2 | **95%** | 65, 91 |
| `src/core/ast/types.py` | 15 | 1 | 2 | 1 | **88%** | 64 |
| `src/core/capabilities/planner.py` | 33 | 0 | 4 | 0 | **100%** | Ninguna |
| `src/core/docs/emitter.py` | 62 | 8 | 18 | 4 | **82%** | 46-53 (filtros de diagramas ERD) |
| `src/core/emitter/model_emitter.py` | 25 | 0 | 12 | 3 | **92%** | Ramas de propiedades opcionales |
| `src/core/emitter/pbip_writer.py` | 67 | 1 | 10 | 2 | **96%** | 111 |
| `src/core/emitter/relationship_emitter.py` | 18 | 1 | 6 | 1 | **92%** | 26 |
| `src/core/emitter/table_emitter.py` | 79 | 4 | 40 | 8 | **90%** | 125-134 (carpetas de visualización anidadas) |
| `src/core/emitter/tmdl_formatter.py` | 9 | 0 | 2 | 0 | **100%** | Ninguna |
| `src/core/engine/compiler.py` | 25 | 0 | 2 | 0 | **100%** | Ninguna |
| `src/core/engine/dax_generator.py` | 37 | 1 | 22 | 1 | **97%** | 111 |
| `src/core/engine/explainer.py` | 27 | 16 | 2 | 0 | **38%** | 18-46 (explicación interactiva por consola) |
| `src/core/engine/governance.py` | 62 | 0 | 42 | 0 | **100%** | Ninguna |
| `src/core/engine/graph.py` | 23 | 7 | 4 | 0 | **74%** | 48-51 (métodos auxiliares de ciclo) |
| `src/core/engine/inference.py` | 21 | 21 | 10 | 0 | **0%** | 4-64 (**Archivo legacy redundante - P1**) |
| `src/core/engine/relationship_resolver.py` | 43 | 10 | 20 | 5 | **70%** | 45-50, 62-63 (resolución de cardinalidad ambigua) |
| `src/core/engine/role_inferer.py` | 21 | 9 | 10 | 1 | **48%** | 24-39 (fallbacks a roles desconocidos) |
| `src/core/mappers/canonical_to_pbi.py` | 27 | 2 | 8 | 1 | **91%** | 63-70 |
| `src/core/mappers/raw_to_canonical.py` | 29 | 1 | 10 | 1 | **95%** | 48 |
| `src/core/parsers/markdown_parser.py` | 103 | 11 | 44 | 7 | **86%** | 25-31, 75, 96, 162 |
| `src/core/parsers/yaml_parser.py` | 34 | 7 | 10 | 2 | **80%** | 22-27, 43-44 |
| `src/core/personas/cockpit.py` | 53 | 2 | 14 | 5 | **90%** | 37, 57 |
| `src/core/personas/config_loader.py` | 73 | 5 | 36 | 8 | **88%** | 56, 62, 112, 154 |
| `src/core/personas/interfaces.py` | 27 | 4 | 6 | 1 | **85%** | 27, 33, 45, 86 |
| `src/core/personas/legacy_adapter.py` | 22 | 4 | 2 | 1 | **79%** | 31-38, 45 |
| `src/core/personas/lenses/*.py` (10 lenses) | 314 | 1 | 42 | 1 | **99%** | Cobertura casi total en los 10 archivos de lentes |
| `src/core/personas/models.py` | 136 | 0 | 0 | 0 | **100%** | Ninguna (Contratos Pydantic 100% cubiertos) |
| `src/core/personas/projector.py` | 156 | 109 | 60 | 2 | **27%** | Ramas secundarias de proyección |
| `src/core/personas/registry.py` | 77 | 10 | 20 | 4 | **84%** | 138-160 (métodos de carga dinámica) |
| `src/core/personas/renderers.py` | 178 | 6 | 74 | 16 | **90%** | 93-96, 134-142 |
| `src/core/personas/views.py` | 26 | 0 | 0 | 0 | **100%** | Ninguna |
| `src/core/quality/rules.py` | 46 | 1 | 36 | 2 | **96%** | 76 |
| `src/core/quality/scorer.py` | 34 | 0 | 6 | 0 | **100%** | Ninguna |
| `src/core/targets/powerbi/adapter.py` | 16 | 0 | 0 | 0 | **100%** | Ninguna |
| **TOTAL CONSOLIDADO** | **2,461** | **296** | **652** | **91** | **85%** | **Estado General: SALUDABLE** |

---

## 3. DESGLOSE POR SUITES DE PRUEBA

1. **Pruebas de Contratos y Modelos (`test_persona_contracts.py`, `test_canonical_model.py`):** 16 tests pasando.
2. **Pruebas de Registro y Configuración (`test_persona_registry.py`):** 7 tests pasando.
3. **Pruebas de Gobernanza y Calidad cQS (`test_stage3_governance_quality.py`, `test_persona_quality_rules.py`):** 6 tests pasando.
4. **Pruebas de Proyección y Lentes (`test_persona_projector.py`, `test_all_lenses_deep.py`):** 18 tests pasando.
5. **Pruebas de Leadership Cockpit (`test_leadership_cockpit.py`):** 3 tests pasando.
6. **Pruebas de Regresión Golden (`test_golden_regression.py`):** 2 tests pasando.
7. **Pruebas de Parsers y Emisores (`test_markdown_parser.py`, `test_yaml_parser.py`, `test_tmdl_emitter.py`):** 3 tests pasando.
8. **Pruebas de CLI (`test_cli.py`, `test_cli_personas.py`):** 5 tests pasando.
9. **Pruebas de Estrés Masivo (`tests/Massive Stress Test/`, `Massive Data Stress/`):** 10 tests pasando (generación de 100+ tablas y 500+ relaciones).

---

## 4. BRECHAS EN HERRAMENTAL DE CALIDAD LOCAL

1. **Ausencia de `ruff` en `.venv`:**  
   - `pyproject.toml` especifica configuración para `ruff`, pero el ejecutable no está disponible en el entorno virtual.
2. **Ausencia de `mypy` en `.venv`:**  
   - El chequeo de tipos estático estricto no se puede ejecutar en el entorno local actual sin instalar el paquete.
3. **Ausencia de `test_output_safety.py`:**  
   - No existen pruebas de contención de escritura, symlink escape ni path traversal.
