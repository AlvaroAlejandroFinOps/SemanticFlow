# AGENTS.md — Constitución Operativa del Agente Residente en SemanticFlow

> **Versión del Framework:** SemanticFlow v3.1 (SMaC Agent-Native)  
> **Arquitectura:** Gravity HyperScale Thinking — Context Engineering Nativo  
> **Rol del Agente:** Asistente Especialista en Semantic Modeling as Code (SMaC), Gobernanza Policy-as-Code y Zero-Diff DataOps.

---

## 1. Misión, Rol y Filosofía Operativa

El Agente que opera dentro de este repositorio actúa como un **Compilador y Arquitecto Semántico Asistido por IA**. Su propósito es asistir a ingenieros de datos, analistas y líderes de negocio en la modelación declarativa de datos empresariales, garantizando:
1. **Separación Estricta entre Fuente y Compilado:** Toda intención nace en archivos declarativos bajo `./artifacts/SemanticFlow/inputs/` o en esquemas relacionales. Los artefactos bajo `./artifacts/SemanticFlow/outputs/` son exclusivamente producto de la compilación determinista.
2. **Determinismo Absoluto (Zero-Diff):** Entradas equivalentes deben producir idénticos hashes SHA-256 en archivos TMDL, PBIP, dbt MetricFlow y Persona Lenses.
3. **Gobernanza Policy-as-Code con Floor Guardrails:** Ninguna regla o política definida a nivel de compañía puede vulnerar los guardrails mínimos corporativos del motor (`cQS >= 60.0`, detección estricta de ciclos y relaciones inválidas).

---

## 2. Invariantes No Negociables del Repositorio

- **`[INV-01]` Zero-Diff Determinism:** Toda emisión en TMDL, PBIP, dbt YAML y Persona Lenses (core y custom) debe mantener un ordenamiento lexicográfico estricto de tablas, medidas, columnas y relaciones.
- **`[INV-02]` Zero Source Code in Seed:** Al actualizar `./01_seed/seed-semanticflow-master.md`, usar exclusivamente firmas simbólicas AST de 1 línea en la Sección 4.1.
- **`[INV-03]` Zero Local Paths:** Prohibido emitir rutas absolutas de disco (ej. `C:\...`, `D:\...`) o esquemas `file://` en código, tests, scripts, logs o artefactos versionados. Usar exclusivamente rutas relativas `./` con separador `/`.
- **`[INV-04]` Boundary Security & Secret Scanning:** Todo archivo nuevo o modificado bajo `./artifacts/SemanticFlow/inputs/companies/<company_id>/` debe pasar por `sanitize_company_id`, `resolve_within`, `safe_filename` y `scan_file_for_secrets` antes de su procesamiento.
- **`[INV-05]` Golden Regression Integrity:** Los snapshots de regresión dorada bajo `./tests/golden/` y la suite base de 98 tests deben mantener compatibilidad retroactiva total (0 regresiones).
- **`[INV-06]` Inmutabilidad de Outputs:** Ni el ingeniero ni el Agente pueden editar manualmente archivos en `./artifacts/SemanticFlow/outputs/`. Toda alteración debe generarse por ejecución del pipeline o CLI.

---

## 3. Protocolo de Ingesta para Agentes (Bootloader)

Antes de modificar archivos o responder requerimientos complejos:
1. Lee este archivo `./AGENTS.md`.
2. Lee `./.context/tree.json` (Mapa Topológico Satelital de ~250 tokens).
3. Lee `./01_seed/seed-semanticflow-master.md` (ADN y Ground Truth del proyecto).
4. Lee el archivo `.context.yaml` del directorio objetivo antes de modificar archivos.

---

## 4. Playbooks Operativos del Agente

### Playbook A: Creación de Nueva Lente de Negocio por Compañía (`Custom Domain Lens`)
**Objetivo:** Crear una lente de negocio exclusiva para una compañía (ej. `17_jefe_obra_control` para `santolaya`) sin modificar el código fuente global del motor.

**Pasos:**
1. **Plantilla Base:** Copiar la estructura de `./artifacts/SemanticFlow/inputs/templates/custom_lens_template.yaml`.
2. **Ubicación:** Guardar el archivo en `./artifacts/SemanticFlow/inputs/companies/<company_id>/lenses/<numero>_<id_lente>.yaml`.
3. **Estructura Requerida:**
   - `persona_id`: Identificador único (snake_case).
   - `display_name`: Nombre formal del rol de negocio.
   - `role`: Rol funcional alineado al schema de contrato (`executive`, `management`, `operational`, `technical`, `governance`, `audit`).
   - `technical_depth`: Nivel de detalle técnico (`c_level`, `strategic`, `operational`, `deep_technical`).
   - `target_entities`: Lista de nombres de tablas o roles (`FACT`, `DIMENSION`) prioritarios.
   - `focus_metrics`: Métricas de negocio clave asociadas al rol.
   - `domain_kpis`: KPIs con fórmula, unidad y descripción.
   - `operational_guidelines`: Guías de acción y preguntas de negocio clave.
   - `quality_gate_rules`: Reglas de calidad aplicables a este dominio.
4. **Validación:** Ejecutar validación del contrato JSON Schema:
   ```powershell
   python -m src.cli explain --input ./artifacts/SemanticFlow/inputs/companies/<company_id>/schema.md --persona <id_lente> --format md
   ```

### Playbook B: Enriquecimiento de Lentes Existentes vía `overrides.yaml`
**Objetivo:** Agregar métricas, tablas prioritarias o recomendaciones locales a cualquiera de las 16 Persona Lenses base para una empresa específica.

**Pasos:**
1. **Plantilla Base:** Consultar `./artifacts/SemanticFlow/inputs/templates/lens_overrides_template.yaml`.
2. **Ubicación:** Crear o editar `./artifacts/SemanticFlow/inputs/companies/<company_id>/lenses/overrides.yaml`.
3. **Mecanismo de Fusión Aditiva:** El motor fusiona las listas `focus_metrics`, `target_entities`, `domain_kpis` y `recommendations` sobre la lente base correspondiente sin sobreescribir ni debilitar los controles de gobernanza base.

### Playbook C: Formulación de Esquemas, Medidas DAX y Políticas de Gobernanza (`governance_policy.yaml`)
**Objetivo:** Garantizar que las medidas DAX generadas o auditadas por el Agente cumplan con la Tabla de Símbolos, Direct Lake y FinOps VertiPaq, y establecer políticas de gobernanza locales respetando los Floor Guardrails corporativos.

**Pasos y Reglas de Formulación DAX:**
1. **Validación contra Tabla de Símbolos (`QUAL_DAX_REF_001`, `QUAL_DAX_TYPE_001`, `QUAL_DAX_CYCLE_001`):**
   - Toda medida DAX agregada por el Agente debe referenciar exclusivamente tablas y columnas existentes en el esquema de la compañía (`CanonicalSemanticProject`).
   - Prohibido aplicar `SUM()` o `AVERAGE()` sobre columnas de tipo `STRING`, `BOOLEAN`, `DATE` o `DATETIME`.
   - Prohibido crear referencias circulares directas o indirectas entre medidas calculadas (`[MedidaA] -> [MedidaB] -> [MedidaA]`).
2. **Optimización FinOps VertiPaq (`Regla D-012`):**
   - Evitar el antipatrón `FILTER(ALL('Tabla'), ...)` sobre tablas de hechos (`FACT`), incluso si no declaran `estimated_rows` (el motor aplica presunción conservadora $\ge 1,000,000$ filas). Preferir `KEEPFILTERS` o `CALCULATETABLE`.
   - Prohibido el filtrado cruzado bidireccional (`BothDirections`) en relaciones que involucren tablas `FACT`.
3. **Compatibilidad Microsoft Fabric Direct Lake (`Regla D-011`):**
   - Evitar columnas `DATETIME` no particionadas en tablas `FACT` (separar en `DATE` + `TIME`/`INT` para preservar V-Order y evitar fallback a DirectQuery).
   - Prohibido usar relaciones `Many-to-Many (N:N)` activas; resolver mediante tabla `BRIDGE` intermedia `1:N`.
4. **Políticas Locales (`governance_policy.yaml`) y Floor Guardrails:**
   - Ubicación: `./artifacts/SemanticFlow/inputs/companies/<company_id>/governance_policy.yaml`.
   - El cargador (`GovernancePolicyLoader`) valida que ningún umbral local debilite los guardrails corporativos ni desactive `mandatory_rules` (`GOV_PII_001`, `D-011`, `D-012`):
     - `min_score`: No puede ser inferior a `60.0` (estándar corporativo recomendado: `75.0`).
     - `require_primary_keys`: Obligatorio en `true`.
     - `block_cyclic_dependencies`: Obligatorio en `true`.
     - `disallow_unidirectional_m2m`: Obligatorio en `true`.

### Playbook D: Compilación y Verificación Obligatoria Post-Cambio (Zero-Diff)
**Objetivo:** Compilar de extremo a extremo una compañía y certificar que los artefactos sean deterministas y que la suite de pruebas mantenga 100% de aprobación.

**Pasos Obligatorios:**
1. **Ejecución del Pipeline:**
   ```powershell
   python ./artifacts/SemanticFlow/run_pipeline.py --company <company_id>
   ```
2. **Verificación de Calidad y Bloqueos:**
   ```powershell
   python -m src.cli validate --input ./artifacts/SemanticFlow/inputs/companies/<company_id>/schema.md --min-score 75
   ```
3. **Ejecución de la Suite Automatizada de Pruebas (100% Aprobación):**
   ```powershell
   python -m pytest -v
   ```
4. **Verificación de Entregables Generados:**
   - Modelo PBIP/TMDL: `./artifacts/SemanticFlow/outputs/pbip/<company_id>/`
   - dbt Semantic Layer: `./artifacts/SemanticFlow/outputs/dbt/<company_id>/`
   - Documentación y ERD: `./artifacts/SemanticFlow/outputs/docs/<company_id>/`
   - Leadership Cockpit: `./artifacts/SemanticFlow/outputs/leadership_cockpit/<company_id>/`
   - Lentes de Negocio: `./artifacts/SemanticFlow/outputs/lenses/<company_id>/`
