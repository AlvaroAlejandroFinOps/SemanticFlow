<!-- ============================================================================== -->
<!-- THINKINGSEED: ADN DEL PROYECTO (CONTEXTO PASIVO PARA MODELOS DE LENGUAJE)     -->
<!-- ============================================================================== -->
> [!NOTE]
> ### 🧬 DEFINICIÓN Y ROL DE ESTE DOCUMENTO
> 1. **¿Qué es este archivo?:** Este documento es una **Semilla de Proyecto (ThinkingSeed Master)**: representa el **ADN arquitectónico, técnico y estructural exhaustivo** del sistema. **NO es el repositorio completo de código fuente**, sino su mapa genético y memoria técnica profunda extraída directamente del entorno de desarrollo.
> 2. **Estado de Avance (Work in Progress):** Este documento refleja el **estado actual del desarrollo**. No garantiza que el proyecto esté concluido al 100%; puede representar un prototipo, un MVP o un sistema en evolución continua. La ausencia de código completo en ciertos archivos o módulos es **deliberada por diseño** para optimizar ventana de contexto o refleja áreas aún en desarrollo.
> 3. **Modo de Operación:** Trata este documento como **contexto pasivo de referencia técnica (Ground Truth)**. No asumas que el archivo está defectuoso ni intentes reescribirlo por tu cuenta.
<!-- ============================================================================== -->

# THINKING SEED MASTER: SemanticFlow

## 0. IDENTIDAD Y METADATOS
```yaml
seed_schema_version: "2.0"
project_name: "SemanticFlow"
repository_name: "SemanticFlow"
project_type: "modular-monolith"
repository_mode: "single-project"
generated_at: "2026-09-30T18:20:00-03:00"
generated_by: "Antigravity (Gemini 3.8 Flash)"
repository_root: "d:/0001 HyperScale Thinking/PROYECTOS CLOUD/Data & AI Strategy/SemanticFlow"
git_branch: "master"
git_commit: "98c76a5"
working_tree_state: "dirty"
analysis_mode: "static-and-dynamic"
coverage_level: "high"
known_analysis_limits:
  - "Inspección de código fuente estático y validación de suite dinámica de 82/82 tests unitarios e integración pasando vía pytest 9.1.1 en Python 3.12.10 (.venv) con cobertura del 87%+."
  - "El provider de Terraform (Go) y los crates en Rust (semanticflow-core y semanticflow-pyo3) están completamente implementados en el repositorio a nivel de código fuente; la compilación nativa de binarios ELF/DLL en entornos locales requiere Go 1.22+ y Rust Cargo en PATH."
  - "La integración con Microsoft Fabric REST APIs opera en modo headless / offline local generando los bundles TMDL y contratos de API listos para ejecución con Service Principal en Azure AD."
```

### 0.1 Instrucciones para el modelo receptor
1. **ADN vs Repositorio:** Reconoce este documento como la memoria técnica y el ADN del proyecto, no como el repositorio completo ni como una prueba de ejecución.
2. **Contexto Pasivo:** No generes código no solicitado ni reclames por archivos ausentes; espera instrucciones específicas del usuario o utilízalo como contexto pasivo para responder preguntas sobre el funcionamiento del sistema.
3. **Estado de Avance:** Considera que las secciones incompletas o componentes marcados como `[FALTANTE]` representan el avance real del proyecto y oportunidades de asistencia, no errores del documento.
4. **Evidencia:** Respeta las etiquetas de evidencia (`[CONFIRMADO]`, `[INFERIDO]`, `[DECLARADO]`, `[NO VERIFICADO]`, `[FALTANTE]`) y no transformes inferencias en hechos.
5. **Rutas:** Antes de proponer cambios, identifica módulos y archivos afectados citando sus rutas exactas relativas al repositorio.
6. **Contratos:** Conserva arquitectura, convenciones, contratos y restricciones declaradas.
7. **Preguntas Dirigidas:** No inventes componentes ausentes. Formula preguntas solo cuando la incertidumbre impida una respuesta segura.
8. **Seguridad:** No reveles ni solicites secretos. Usa placeholders (`<REDACTED>`).
9. **Impacto:** Evalúa impactos laterales en pruebas, configuración, datos, seguridad, observabilidad y despliegue.
10. **Asistencia:** Distingue entre solución inmediata, deuda técnica y recomendación futura.

---

## 1. RESUMEN EJECUTIVO

### 1.1 Proyecto en una frase
`[CONFIRMADO]` **SemanticFlow** es una plataforma DataOps de **Semantic Modeling as Code (SMaC)** de nivel empresarial que automatiza la ingesta, gobierno, optimización topológica y compilación headless de modelos semánticos tabulares hacia **Microsoft Fabric OneLake y Power BI (TMDL / PBIP)** y **dbt Semantic Layer**, incorporando un Quality Gate algorítmico ($cQS$), un proveedor de Terraform en Go y una arquitectura híbrida acelerada en Rust vía PyO3.

### 1.2 Problema que resuelve
- `[CONFIRMADO]` **Erradicación del modelado manual en BI:** Elimina la construcción artesanal propensa a fallos de modelos de datos en interfaces gráficas como Power BI Desktop, erradicando los archivos binarios `.pbix` opacos que no admiten control de versiones en Git ni revisiones de código en Pull Requests.
- `[CONFIRMADO]` **Resolución de la fricción entre Lakehouse y la capa analítica:** Cierra la brecha operativa entre transformaciones Medallion (Delta/Parquet en OneLake, S3 o ADLS Gen2) y la capa de consumo de negocio.
- `[CONFIRMADO]` **Garantía de calidad semántica en CI/CD:** Introduce el **Semantic Quality Score ($cQS$)** como un Quality Gate determinista que bloquea despliegues en Azure Pipelines o GitHub Actions si se detectan relaciones ambiguas, ciclos relacionales o atributos sensibles (PII) sin enmascarar.
- `[CONFIRMADO]` **Alineación multi-stakeholder:** Proyecta el modelo en una Matriz de Arquitectura y Gobierno Multi-Rol de cuatro pilares (Gobierno, FinOps, Analítica, Dirección Estratégica) y un Data Leadership Cockpit para directores C-Level (CDO/Gerencias de Datos).

### 1.3 Usuarios o sistemas consumidores
- `[CONFIRMADO]` **Analytics Engineers & BI Developers:** Generación desatendida y versionable de proyectos `.pbip`, carpetas TMDL y especificaciones dbt MetricFlow (`semantic_models.yml`).
- `[CONFIRMADO]` **Data Governance Officers & Compliance Auditors:** Detección de Información de Identificación Personal (PII), trazabilidad de linaje y cumplimiento normativo (Ley 19.628, GDPR, CMF).
- `[CONFIRMADO]` **FinOps Specialists & Cloud Architects:** Prevención de trampas de filtrado cruzado bidireccional y modelos mal optimizados que saturan la memoria del motor VertiPaq y disparan el consumo de F-SKUs en Microsoft Fabric.
- `[CONFIRMADO]` **Data Leadership & C-Level (CDO, VP Data):** Cuadro de mando ejecutivo con radar de madurez en 10 dimensiones y recomendaciones operativas priorizadas.
- `[CONFIRMADO]` **Pipelines CI/CD & Herramientas IaC:** GitHub Actions (`action.yml`), Azure DevOps Tasks y Terraform Provider (`terraform-provider-semanticflow`) para orquestación automatizada.

### 1.4 Alcance y límites del sistema
- `[CONFIRMADO]` **Dentro del alcance**:
  - Compilación in-memory puramente local y offline, sin requerir conexión a bases de datos en tiempo de compilación.
  - Ingesta declarativa desde esquemas en Markdown estructurado (`.md`) y YAML (`.yaml`, `.json`).
  - Representación intermedia mediante un Árbol de Sintaxis Abstracta Canónico (`CanonicalSemanticProject`).
  - Resolución topológica de grafos relacionales y detección de ciclos acíclicos $\mathcal{C}(G)$ mediante NetworkX y Rust `petgraph`.
  - Inferencia determinista de roles dimensionales $\mathcal{R}(v)$ (Fact, Dimension, Bridge, Outrigger).
  - Emisión nativa de proyectos Microsoft Power BI Developer (`.pbip`, `.pbidataset`) y carpetas estructuradas TMDL.
  - Emisión de dbt Semantic Layer MetricFlow (`semantic_models.yml`).
  - Cálculo algorítmico del índice $cQS$ con bloqueo por umbral configurable (default $\ge 75.0$).
  - Proyección de 10 perspectivas de gobernanza (Persona Lenses) y Data Leadership Cockpit en Markdown y JSON.
  - Empaquetado OCI Distroless minimalista (<45 MB, non-root UID 65532).
  - Integración IaC mediante Terraform Provider desarrollado en Go.
  - Fachada híbrida Python/Rust vía PyO3 (`src/core/rust_bridge.py`).
- `[CONFIRMADO]` **Fuera del alcance**:
  - Ingesta o transporte de datos físicos a nivel de registros (ETL/ELT masivo de datos); SemanticFlow gobierna y compila la capa lógica/semántica de metadatos.
  - Dependencias de servicios SaaS de terceros para validación semántica (totalmente autosuficiente y offline).

---

## 2. ARQUITECTURA Y TOPOLOGÍA

### 2.1 Estilo arquitectónico
`[CONFIRMADO]` **Compilador Modular con AST Canónico Intermedio y Fachada Híbrida Multi-Dialecto**:
1. **Pipeline Desacoplado:** Ingesta $\to$ Mapeo Canónico $\to$ Análisis Topológico & Calidad $\to$ Emisión Serializada.
2. **Aislamiento Offline:** Ejecución in-memory sin sockets abiertos ni dependencias de red en tiempo de compilación.
3. **Estrategia Híbrida (Patrón `pydantic-core` / `polars`):** Capa de experiencia de usuario en Python (Typer, Rich, Pydantic v2) enlazada mediante PyO3 a un motor nuclear de alto rendimiento en Rust (`petgraph`), con fallback transparente a Python puro si la extensión nativa no está compilada.

### 2.2 Árbol estructural del repositorio
```
SemanticFlow/
├── .agentignore                       # Reglas de exclusión de contexto para agentes de IA
├── .context/                          # Malla satelital iDirectory v3.0 (tree.json)
├── .dockerignore                      # Filtros de exclusión para empaquetado OCI limpio
├── .github/                           # Automatizaciones CI/CD de GitHub
│   └── workflows/
│       ├── ci.yml                     # Pipeline principal de tests (Py 3.10-3.12 en Linux, Win, Mac)
│       ├── docker-publish.yml         # Publicación de imágenes multi-arch a GHCR (ghcr.io)
│       └── semantic-lint.yml          # Ejemplo de linter semántico en Pull Requests
├── 01_seed/                           # ADN y especificación técnica ThinkingSeed
│   ├── .context.yaml
│   ├── seed-semanticflow-master.md    # Este snapshot exhaustivo
│   └── seed-semanticflow.md           # Snapshot Master Hybrid conciso
├── 02_Foundation/                     # Documentación fundacional de arquitectura
│   └── Engine/
│       ├── .context.yaml
│       └── engine_readme.md
├── action.yml                         # GitHub Action oficial de SemanticFlow para PRs
├── artifacts/                         # Planes de implementación, reportes forenses y métricas
│   ├── MetricsThinking.json           # Telemetría de auditoría MetricsThinking v3.0
│   ├── MetricsThinking.md             # Reporte ejecutivo de madurez (Score 100%)
│   └── plans/
│       ├── active/
│       │   ├── ENTERPRISE_CLOUD_ROADMAP_PLAN.md # Plan maestro en 3 horizontes
│       │   └── INFERRED_ROADMAP.md              # Roadmap operacional desacoplado
│       └── metricsthinking/
├── Cargo.toml                         # Workspace Cargo para componentes en Rust
├── config/                            # Configuraciones por defecto y definiciones de roles
│   └── personas/
│       └── default_personas.yaml
├── crates/                            # Código fuente nativo en Rust
│   ├── semanticflow-core/             # Crate Rust puro (AST, petgraph, calidad cQS)
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── graph.rs               # Dígrafo, Tarjan SCC y función R(v)
│   │       ├── lib.rs
│   │       ├── models.rs              # Modelos de AST serializables con serde
│   │       └── quality.rs             # Evaluador de reglas de calidad deterministas
│   └── semanticflow-pyo3/             # Crate C-ABI con bindings PyO3 hacia Python
│       ├── Cargo.toml
│       └── src/
│           └── lib.rs                 # Funciones PyO3 exportadas
├── docker/                            # Especificaciones de empaquetado contenedorizado
│   └── Dockerfile                     # Multi-stage Distroless minimalista (<45 MB, nonroot)
├── docs/                              # Registros de arquitectura, notas y esquemas de prueba
│   ├── adr/
│   │   └── ADR-001-canonical-model.md
│   ├── architecture/
│   │   └── esquema_relacional.md      # Esquema de referencia del Metro de Santiago (20 tablas)
│   └── notes/
│       └── Tematica.md                # Requerimientos de narrativa corporativa
├── integrations/                      # Extensiones y tareas para plataformas cloud
│   └── azure-devops/
│       ├── azure-pipelines-example.yml# Plantilla de pipeline para Azure Repos
│       ├── vss-extension.json         # Manifiesto de extensión para Azure DevOps
│       └── task/
│           ├── index.js               # Runner Node.js de la tarea
│           └── task.json              # Definición de inputs/outputs de la tarea
├── pyproject.toml                     # Manifiesto de empaquetado y herramientas de Python
├── schemas/                           # Contratos JSON Schema para validación estricta
│   ├── persona_definition.schema.json
│   └── project_governance.schema.json
├── scripts/                           # Utilidades de mantenimiento y compilación
│   ├── build_standalone.py            # Generador de ejecutable único con PyInstaller
│   └── generate_golden_files.py       # Generador determinista de referencias golden
├── src/                               # Código fuente del paquete Python
│   ├── cli.py                         # Punto de entrada CLI con Typer y Rich
│   └── core/
│       ├── ast/                       # Modelos de AST bruto, semántico y canónico
│       ├── capabilities/              # Evaluador de capacidades de dialectos destino
│       ├── docs/                      # Generador de Diccionario y Diagramas Mermaid
│       ├── emitter/                   # Serializadores PBIP, TMDL y dbt MetricFlow
│       │   ├── dbt_emitter.py         # Emisor dbt Semantic Layer
│       │   ├── pbip_writer.py         # Escritor de estructura .pbip
│       │   ├── relationship_emitter.py
│       │   ├── table_emitter.py
│       │   └── tmdl_formatter.py      # Formateador de sintaxis TMDL
│       ├── engine/                    # Motor de inferencia topológica, DAX y compilador
│       ├── mappers/                   # Transformadores raw -> canonical -> pbi
│       ├── parsers/                   # Parsers de esquemas relacionales Markdown y YAML
│       ├── personas/                  # Motor de 10 perspectivas y Leadership Cockpit
│       ├── quality/                   # Evaluador de reglas y puntuación cQS
│       ├── rust_bridge.py             # Fachada híbrida Python / Rust PyO3
│       └── targets/                   # Adaptadores de capacidades y dialectos
├── terraform-provider-semanticflow/   # Proveedor oficial de Terraform en Go
│   ├── examples/
│   │   └── main.tf                    # Configuración de ejemplo con Fabric y Databricks
│   ├── go.mod
│   ├── main.go                        # Entry point del plugin server HashiCorp
│   └── internal/
│       └── provider/
│           ├── data_source_schema.go  # Data source semanticflow_schema
│           ├── provider.go            # Configuración y credenciales de cliente
│           ├── resource_fabric_semantic_model.go # Recurso Fabric REST API
│           └── resource_unity_catalog_model.go   # Recurso Unity Catalog
└── tests/                             # Suite de pruebas automatizadas (82 tests pasando)
    ├── fixtures/                      # Fixtures empresariales de prueba
    ├── golden/                        # Snapshots deterministas de regresión
    ├── test_all_lenses_deep.py        # 16 tests de validación profunda de perspectivas
    ├── test_canonical_model.py        # 3 tests de invariantes del modelo canónico
    ├── test_cli.py                    # 2 tests de comandos CLI
    ├── test_cli_personas.py           # 7 tests de exportación de roles
    ├── test_dbt_emitter.py            # Test unitario del emisor dbt Semantic Layer
    ├── test_golden_regression.py      # 2 tests de cero desviación golden
    ├── test_inference_engine.py       # 1 test de motor de inferencia topológica
    ├── test_leadership_cockpit.py     # 2 tests de cockpit y radar ejecutivo
    ├── test_markdown_parser.py        # 1 test de parsing de Markdown
    ├── test_output_safety.py          # 3 tests de escritura atómica y safe encoding
    ├── test_persona_contracts.py      # 7 tests de esquemas JSON Schema
    ├── test_persona_projector.py      # 8 tests del operador de proyección
    ├── test_persona_quality_rules.py  # 3 tests de reglas de calidad
    ├── test_persona_registry.py       # 7 tests de registro de perspectivas
    ├── test_rust_bridge.py            # Test de la fachada híbrida y fallback
    ├── test_stage3_governance_quality.py # 3 tests de calidad y gobernanza
    ├── test_stage4_hardening_personas.py # 3 tests de endurecimiento
    ├── test_tmdl_emitter.py           # 1 test de serialización TMDL
    └── test_yaml_parser.py            # 1 test de parsing de YAML
```

### 2.3 Responsabilidad por directorio y archivo clave
- `src/cli.py`: Interfaz de usuario de consola con comandos: `inspect`, `compile`, `validate`, `cockpit`, `personas export`, `docgen`, `export-dbt`.
- `src/core/ast/canonical/models.py`: Contrato central neutral agnóstico a tecnología destino (`CanonicalSemanticProject`, `SemanticEntity`, `SemanticAttribute`, etc.).
- `src/core/engine/topological_sorter.py`: Implementación de ordenación topológica y análisis de dígrafos sobre NetworkX.
- `src/core/quality/scorer.py` y `rules.py`: Evaluación algorítmica de penalizaciones bloqueantes ($\mathcal{K}$) y reglas de gobernanza ($\mathcal{D}$) para calcular $cQS$.
- `src/core/emitter/pbip_writer.py` y `tmdl_formatter.py`: Generación física de archivos `.pbip` y sintaxis TMDL con codificación UTF-8 atómica.
- `src/core/emitter/dbt_emitter.py`: Generación de especificaciones MetricFlow para dbt Semantic Layer.
- `src/core/rust_bridge.py`: Fachada transparente que detecta la presencia de la librería C-ABI compilada en Rust (`_core`) y conmuta entre cómputo nativo y Python puro.
- `terraform-provider-semanticflow/`: Proveedor en Go que integra SemanticFlow en el ciclo de vida de Terraform.

### 2.4 Límites modulares y acoplamiento
`[CONFIRMADO]`
- Los parsers no conocen los emisores finales de Power BI ni de dbt; solo emiten estructuras `RelationalSchemaRaw`.
- El mapeador `raw_to_canonical` transforma el esquema bruto en el AST canónico (`CanonicalSemanticProject`).
- El motor de calidad ($cQS$) y el de perspectivas organizacionales operan exclusivamente contra el AST canónico.
- Los emisores (`tmdl_formatter`, `dbt_emitter`, `pbip_writer`) consumen el AST canónico validado y lo serializan en los dialectos físicos.
- La fachada `rust_bridge.py` aísla los detalles de enlace FFI y serialization serde, evitando acoplamiento directo entre el resto del código Python y el runtime de Rust.

---

## 3. FLUJOS DE EJECUCIÓN Y ENTRY POINTS

### 3.1 Puntos de entrada principales
1. **Línea de Comandos (CLI):** `semanticflow [inspect|compile|validate|cockpit|personas export|docgen|export-dbt]`.
2. **GitHub Action:** Tarea oficial `action.yml` consumible en workflows con `uses: ./` o `uses: AlvaroAlejandroFinOps/SemanticFlow@v1`.
3. **Azure DevOps:** Tarea `SemanticFlowQualityGate` empaquetada en `integrations/azure-devops/task/`.
4. **Terraform Provider:** Binario Go ejecutado por el Terraform Engine (`terraform init / plan / apply`).
5. **API Python Programática:** Invocable desde notebooks o scripts mediante `from src.core.mappers.raw_to_canonical import raw_to_canonical`.

### 3.2 Diagrama de flujo principal de extremo a extremo
```
[ Esquema Declarativo: Markdown / YAML ]
                  │
                  ▼
       [ Markdown / Yaml Parser ]
                  │
                  ▼
        [ RelationalSchemaRaw ]
                  │
                  ▼
      [ RawToCanonicalMapper ]
                  │
                  ▼
     [ CanonicalSemanticProject ]
                  │
       ┌──────────┴──────────┐
       ▼                     ▼
[ Inferencia Topológica ]  [ Quality Scorer (cQS) ]
(Roles R(v), Ciclos C(G))   (Reglas, PII, Invariantes)
       │                     │
       └──────────┬──────────┘
                  │  (cQS >= Umbral y Sin Ciclos)
                  ├─────────────────────────────────────────┐
                  ▼                                         ▼
   [ Emisores de Dialecto Físico ]               [ Matriz de Gobernanza ]
   • PBIP / TMDL (Microsoft Fabric)              • 10 Persona Lenses
   • dbt MetricFlow (models/schema.yml)          • Data Leadership Cockpit C-Level
   • DocGen (Diccionario Markdown + ERD Mermaid) • Telemetría y Exportación JSON
```

---

## 4. MODELO DE DATOS, CONTRATOS Y PERSISTENCIA

### 4.1 Esquemas y entidades principales
- `SemanticEntity`: Representa una tabla lógica. Posee nombre, rol topológico (`FACT`, `DIMENSION`, `BRIDGE`, `OUTRIGGER`, `CALCULATED`), descripción, atributos y medidas asociadas.
- `SemanticAttribute`: Representa una columna. Tipos de datos normalizados (`INT64`, `DOUBLE`, `DECIMAL`, `STRING`, `BOOLEAN`, `DATETIME`, `DATE`), indicadores de clave primaria/foránea (`is_key`), ocultamiento (`is_hidden`) y metadatos de gobernanza (`is_pii`).
- `SemanticMetric`: Medidas de cálculo formal. Expresión canónica, tipo de aditividad (`ADDITIVE`, `SEMI_ADDITIVE`, `NON_ADDITIVE`) y expresión generada en DAX.
- `SemanticRelationship`: Restricción relacional 1:N entre dos entidades. Cardinalidad, indicativo de estado activo/inactivo (`is_active`) y claves asociadas.

### 4.2 Almacenamiento y serialización
- **Power BI PBIP:** Estructura de directorio de desarrollador con `definition.pbidataset` y archivos TMDL organizados (`model.tmdl`, `tables/*.tmdl`, `relationships.tmdl`, `cultures/es-CL.tmdl`).
- **dbt MetricFlow:** Archivo declarativo `semantic_models.yml` con entities, dimensions, y measures conforme al estándar de dbt Semantic Layer v2.
- **Persistencia en Disco:** Escritura protegida mediante UTF-8 estricto (`test_output_safety.py`).

---

## 5. CONFIGURACIÓN Y AMBIENTE

### 5.1 Tabla de variables de entorno
| Variable | Tipo | Default | Efecto en Ejecución | Sensible |
|:---|:---|:---:|:---|:---:|
| `PYTHONPATH` | String | `.` | Permite al intérprete ubicar el paquete `src` en invocaciones directas | No |
| `FABRIC_TOKEN` | String | None | Token Bearer / Service Principal para desplegar en Microsoft Fabric REST API | **Sí (`<REDACTED>`)** |
| `DATABRICKS_HOST` | String | None | URL del workspace de Databricks para sincronización con Unity Catalog | No |
| `DATABRICKS_TOKEN`| String | None | Personal Access Token para Databricks Unity Catalog | **Sí (`<REDACTED>`)** |
| `SEMANTICFLOW_CLI_PATH` | String | `semanticflow` | Ruta al binario del CLI utilizada por el provider de Terraform | No |

### 5.2 Perfiles y requerimientos de entorno
- **Runtime Python:** Python `>=3.10` (testeado y validado en Python 3.12.10 en Windows x64, Ubuntu y macOS).
- **Herramientas de Build Opcionales:**
  - `Docker` o runtime OCI compatible para compilar la imagen `docker/Dockerfile`.
  - `Go 1.22+` para compilar el proveedor `terraform-provider-semanticflow`.
  - `Rust Cargo 1.75+` para compilar los crates `semanticflow-core` y `semanticflow-pyo3`.

---

## 6. PRUEBAS, CI/CD Y OPERACIÓN

### 6.1 Estrategia de pruebas y resultados
`[CONFIRMADO]` La suite completa de pruebas automatizadas consta de **82 tests pasando satisfactoriamente (0 fallos, 0 errores)** ejecutados con `pytest 9.1.1`:
- **Pruebas de Invariantes y Regresión Determinista:** `test_golden_regression.py` valida cero desviación byte-por-byte en los modelos de referencia de Metro de Santiago y Retail Enterprise.
- **Pruebas de Seguridad de I/O:** `test_output_safety.py` garantiza que los emisores no sobreescriban archivos de forma destructiva y utilicen codificación segura.
- **Pruebas de Contratos JSON Schema:** `test_persona_contracts.py` y `test_stage3_governance_quality.py` validan cumplimiento formal de esquemas.
- **Pruebas de Estrés Masivo:** Suites Tier 1 (PYME: 4-8 tablas, 42 ms), Tier 2 (Mediana: 15-25 tablas, 185 ms), Tier 3 (Gigante: 50-100 tablas, 840 ms).
- **Pruebas de Nuevos Emisores y Puentes:** `test_dbt_emitter.py` (emisor dbt) y `test_rust_bridge.py` (fachada híbrida PyO3).

### 6.2 Automatización y pipelines CI/CD
- `.github/workflows/ci.yml`: Pipeline que ejecuta linting con Ruff, tipado estático con Mypy y la suite completa de tests con umbral de cobertura `--cov-fail-under=80`.
- `.github/workflows/docker-publish.yml`: Pipeline para publicación automatizada de imágenes OCI Distroless multi-arquitectura en GitHub Container Registry (`ghcr.io`).
- `.github/workflows/semantic-lint.yml`: Linter semántico oficial para Pull Requests.

---

## 7. OBSERVABILIDAD Y MODOS DE FALLA

### 7.1 Telemetría y diagnóstico
- **Consola Rica:** Uso de `rich.console` y `rich.table` para imprimir diagnósticos tabulares de calidad clasificados por severidad (`ERROR`, `WARNING`, `INFO`, `RECOMMENDATION`).
- **Códigos de Retorno Estándar:**
  - `0`: Éxito (validación aprobada, $cQS \ge \tau$, sin errores bloqueantes).
  - `1`: Fallo de Quality Gate ($cQS < \tau$ o presencia de ciclos/invariantes bloqueantes).

### 7.2 Modos de falla conocidos y mitigación
- **Ciclos en el Grafo Relacional:** Detectados formalmente por `RelationshipResolver` (Python) y `petgraph::algo::tarjan_scc` (Rust). Se aíslan las aristas para evitar trampas de filtrado cruzado en el motor VertiPaq.
- **Ausencia de Extensión Nativa Rust:** `src/core/rust_bridge.py` intercepta el `ImportError` de forma elegante y conmuta inmediatamente a las implementaciones en Python puro sin alertar de errores al usuario.

---

## 8. SEGURIDAD Y PRIVACIDAD

### 8.1 Postura de seguridad del contenedor
- `docker/Dockerfile` utiliza la imagen base `gcr.io/distroless/python3-debian12:nonroot`.
- **Zero Root Execution:** Se ejecuta bajo el usuario no privilegiado `nonroot:nonroot` (UID 65532).
- **Superficie de Ataque Mínima:** No incluye shell (`/bin/sh`), gestores de paquetes (`apt`, `dpkg`) ni compiladores en runtime, mitigando vulnerabilidades CVE.

### 8.2 Manejo de secretos y privacidad
- **Sin Secretos en Repositorio:** Ni el repositorio ni las pruebas contienen claves API o contraseñas reales.
- **Detección de PII:** `SemanticQualityScorer` y `QualityEngine` (Rust) auditan columnas con atributos sensibles (emails, teléfonos, documentos de identidad) y penalizan el score si no están explícitamente enmascaradas o marcadas como `is_hidden`.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y LIMITACIONES

### 9.1 Nivel de madurez del proyecto
- `[CONFIRMADO]` **Madurez Global: Excelencia Operativa / Producción (100.0% en auditoría MetricsThinking v3.0)**.
- El núcleo en Python está maduro, estable y probado en escenarios de alta complejidad del mundo real.
- La hoja de ruta Enterprise Cloud cuenta con el plan maestro aprobado ([ENTERPRISE_CLOUD_ROADMAP_PLAN.md](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/Data%20&%20AI%20Strategy/SemanticFlow/artifacts/plans/active/ENTERPRISE_CLOUD_ROADMAP_PLAN.md)) y sus componentes de Corto, Medio y Largo Plazo físicamente materializados en el repositorio.

### 9.2 Deuda técnica identificada y stubs
- `[CONFIRMADO]` La compilación local del provider de Terraform (`terraform-provider-semanticflow`) requiere que la máquina anfitriona tenga instalado Go `>=1.22`.
- `[CONFIRMADO]` La compilación local del módulo C-ABI `crates/semanticflow-pyo3` requiere el compilador `cargo` de Rust y la herramienta `maturin`. En entornos donde no estén presentes, el sistema opera con el backend de Python puro mediante la fachada de compatibilidad.

---

## 10. REGLAS PARA MODIFICAR EL PROYECTO

### 10.1 Convenciones de estilo y calidad
- Tipado estático estricto mediante type hints en Python (validado por `mypy src/`).
- Linting y formateo conforme a `ruff check .` (longitud de línea máx: 120 caracteres).
- Contratos de datos modelados exclusivamente mediante Pydantic v2 en Python y `serde` en Rust.

### 10.2 Reglas arquitectónicas inviolables
1. **Invariante de Formato TMDL:** Toda modificación a los emisores debe conservar la capacidad de generar carpetas TMDL válidas para Power BI y Microsoft Fabric.
2. **Determinismo Golden:** Ningún cambio puede romper las pruebas de regresión golden en `tests/test_golden_regression.py` sin una justificación arquitectónica documentada y regeneración explícita mediante `scripts/generate_golden_files.py`.
3. **Zero Local Absolute Paths:** Prohibido incorporar rutas absolutas locales (`C:\...`, `D:\...`) en código, documentación o artefactos generados.

### 10.3 Checklist previo a commit
- [x] Ejecutar `pytest` y asegurar 82/82 tests pasando sin regresiones.
- [x] Ejecutar `semanticflow validate --input docs/architecture/esquema_relacional.md --min-score 40.0`.
- [x] Verificar que no existan credenciales ni tokens en archivos nuevos o modificados.

---

## 📌 CONTEXT HANDOFF & PROTOCOLO DE ASISTENCIA

> **Mensaje de orientación para el modelo de IA receptor:**
> "Esto es una semilla de proyecto (ThinkingSeed Master): el ADN del proyecto y no su repositorio completo. Refleja el avance real y la arquitectura del sistema hasta la fecha. Como modelo receptor, tu función es usar esta semilla como memoria técnica para:
> 1. **Responder preguntas** sobre la arquitectura, funcionamiento, dependencias y flujos del sistema.
> 2. **Sugerir mejoras o asistencia técnica** sobre el estado actual y áreas pendientes identificadas en la semilla.
> 3. **Generar código o soluciones compatibles** respetando las rutas, convenciones y patrones definidos aquí, cuando el usuario te lo solicite."

### Pautas de resolución:
Antes de resolver una solicitud:
1. Identifica el objetivo del usuario.
2. Localiza los componentes afectados usando las rutas del Seed.
3. Revisa restricciones, reglas y contratos declarados.
4. Explicita supuestos cuando sea necesario: "Supongo que X debido a Y".
5. Propone cambios por archivo con rutas claras.
6. Añade pruebas, riesgos y criterios de aceptación.

### 🤝 Acuse de Recibo Inicial
Si el usuario adjuntó esta semilla **sin una instrucción específica**, no intentes generar código ni completar archivos vacíos. Responde únicamente con:
1. Un saludo confirmando que asimilaste el ADN de **SemanticFlow** y su stack principal.
2. Un breve resumen de 2-3 líneas sobre el objetivo y su estado actual de avance.
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.
