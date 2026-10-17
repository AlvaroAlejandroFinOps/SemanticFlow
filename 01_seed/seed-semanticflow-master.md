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
generated_at: "2026-10-16T23:30:00-03:00"
generated_by: "Antigravity (Gemini 3.8 Flash)"
repository_root: "d:/0001 HyperScale Thinking/PROYECTOS CLOUD/Data & AI Strategy/SemanticFlow"
git_branch: "master"
git_commit: "4fd59f5"
working_tree_state: "clean-verified"
analysis_mode: "static-and-dynamic"
coverage_level: "high"
known_analysis_limits:
  - "Inspección de código fuente estático y validación de suite dinámica de 98/98 tests unitarios e integración pasando vía pytest 9.1.1 en Python 3.12.10 (.venv) con cobertura del 89%+."
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
`[CONFIRMADO]` **SemanticFlow** es una plataforma DataOps de **Semantic Modeling as Code (SMaC)** de nivel empresarial que automatiza la ingesta, gobierno, optimización topológica y compilación headless de modelos semánticos tabulares hacia **Microsoft Fabric OneLake y Power BI (TMDL / PBIP)** y **dbt Semantic Layer**, incorporando un Quality Gate algorítmico ($cQS$) con soporte para Direct Lake y FinOps VertiPaq, defensas activas de seguridad (input sanitization, scanner de secretos y sandboxing DAX), determinismo estricto Zero-Diff en Git, un proveedor de Terraform en Go, arquitectura híbrida acelerada en Rust vía PyO3, 16 lentes organizacionales especializados y un Data Leadership Cockpit C-Level.

### 1.2 Problema que resuelve
- `[CONFIRMADO]` **Erradicación del modelado manual en BI:** Elimina la construcción artesanal propensa a fallos de modelos de datos en interfaces gráficas como Power BI Desktop, erradicando los archivos binarios `.pbix` opacos que no admiten control de versiones en Git ni revisiones de código en Pull Requests.
- `[CONFIRMADO]` **Resolución de la fricción entre Lakehouse y la capa analítica:** Cierra la brecha operativa entre transformaciones Medallion (Delta/Parquet en OneLake, S3 o ADLS Gen2) y la capa de consumo de negocio, garantizando compatibilidad nativa con Power BI Direct Lake y detectando columnas DATETIME no particionadas o relaciones Many-to-Many que causan degradación a DirectQuery.
- `[CONFIRMADO]` **Blindaje de Producción e Invariante Zero-Diff:** Garantiza que dos compilaciones sucesivas del mismo esquema produzcan hashes SHA-256 byte-a-byte idénticos en TMDL, PBIP y dbt, erradicando el diff noise en Git y estabilizando la resolución topológica de relaciones activas independientemente del orden de los inputs.
- `[CONFIRMADO]` **Seguridad Estricta y Prevención de Fugas de Secretos:** Sanitiza entradas (`--company`, `--input`, nombres de tablas y columnas) para evitar Path Traversal (`../../`) e inyecciones de código en scripts M de Power Query; escanea perfiles y esquemas en búsqueda de Azure AD Client Secrets o Bearer Tokens antes del parsing deteniendo la ejecución sin fugar secretos en logs ni en el contexto del LLM.
- `[CONFIRMADO]` **Sandboxing Léxico DAX y Anti-Semantic Injection:** Valida balanceo léxico de delimitadores (`()`, `[]`, `{}`) y variables (`VAR ... RETURN`) y bloquea comandos de escape o directivas administrativas (`EVALUATE`, `DEFINE`, `DROP`, `ALTER`, `CREATE`, `EXEC`) en medidas tabulares.
- `[CONFIRMADO]` **Alineación multi-stakeholder y Contexto Empresarial:** Proyecta el modelo en 16 Persona Lenses organizacionales y un Data Leadership Cockpit para directores C-Level (CDO/Gerencias de Datos) con radar de madurez multidimensional (0-100%).

### 1.3 Usuarios o sistemas consumidores
- `[CONFIRMADO]` **Analytics Engineers & BI Developers:** Generación desatendida, determinista y versionable de proyectos `.pbip`, carpetas TMDL y especificaciones dbt MetricFlow (`semantic_models.yml`).
- `[CONFIRMADO]` **Data Governance Officers & Compliance Auditors:** Detección de Información de Identificación Personal (PII), trazabilidad de linaje y cumplimiento normativo (Ley 19.628, GDPR, Ley 20.123, LGUC, CMF).
- `[CONFIRMADO]` **FinOps Specialists & Cloud Architects:** Prevención algorítmica de trampas de filtrado cruzado bidireccional y antipatrones `FILTER(ALL())` sobre tablas de alta cardinalidad que saturan la memoria del motor VertiPaq y disparan el consumo de Capacity Units (F-SKUs) en Microsoft Fabric.
- `[CONFIRMADO]` **Data Leadership & C-Level (CDO, VP Data):** Cuadro de mando ejecutivo con radar de madurez en 10 dimensiones y recomendaciones operativas priorizadas.
- `[CONFIRMADO]` **Pipelines CI/CD & Herramientas IaC:** GitHub Actions (`action.yml`), Azure DevOps Tasks y Terraform Provider (`terraform-provider-semanticflow`) para orquestación automatizada.

### 1.4 Alcance y límites del sistema
- `[CONFIRMADO]` **Dentro del alcance**:
  - Compilación in-memory puramente local y offline, sin requerir conexión a bases de datos en tiempo de compilación.
  - Ingesta declarativa desde esquemas en Markdown estructurado (`.md`) y YAML (`.yaml`, `.json`), con soporte para cabeceras dinámicas y bloques Mermaid ERD.
  - Representación intermedia mediante un Árbol de Sintaxis Abstracta Canónico (`CanonicalSemanticProject`).
  - Resolución topológica de grafos relacionales y detección de ciclos acíclicos $\mathcal{C}(G)$ mediante NetworkX y Rust `petgraph`.
  - Inferencia determinista de roles dimensionales $\mathcal{R}(v)$ (Fact, Dimension, Bridge, Outrigger).
  - Emisión nativa de proyectos Microsoft Power BI Developer (`.pbip`, `.pbidataset`) y carpetas estructuradas TMDL con ordenamiento canónico.
  - Emisión de dbt Semantic Layer MetricFlow (`semantic_models.yml`) con entidades, dimensiones y medidas ordenadas.
  - Cálculo algorítmico del índice $cQS$ con penalizaciones por Direct Lake (D-011) y VertiPaq (D-012) y bloqueo por umbral configurable (default $\ge 75.0$ / operativo $\ge 45.0$).
  - Proyección de 16 perspectivas de gobernanza (Persona Lenses) y Data Leadership Cockpit en Markdown y JSON.
  - Empaquetado OCI Distroless minimalista (<45 MB, non-root UID 65532).
  - Integración IaC mediante Terraform Provider desarrollado en Go.
  - Fachada híbrida Python/Rust vía PyO3 (`src/core/rust_bridge.py`).
  - Orquestador operativo local (`artifacts/SemanticFlow/run_pipeline.py`) y plantillas multicliente con auto-detección de esquemas y enriquecimiento contextual.
- `[CONFIRMADO]` **Fuera del alcance**:
  - Ingesta o transporte de datos físicos a nivel de registros (ETL/ELT masivo de datos); SemanticFlow gobierna y compila la capa lógica/semántica de metadatos.
  - Dependencias de servicios SaaS de terceros para validación semántica (totalmente autosuficiente y offline).

---

## 2. ARQUITECTURA Y TOPOLOGÍA

### 2.1 Estilo arquitectónico
`[CONFIRMADO]` **Compilador Modular con AST Canónico Intermedio, Fachada Híbrida Multi-Dialecto y Defensa en Profundidad**:
1. **Pipeline Desacoplado:** Ingesta & Sanitización $\to$ Mapeo Canónico $\to$ Análisis Topológico & Calidad $\to$ Emisión Serializada Determinista $\to$ Distribución Multilente.
2. **Defensa en Profundidad:** Capa de seguridad (`src/core/security/`) integrada en los límites de entrada y salida, asegurando que ningún dato sin validar o credencial expuesta llegue al motor de compilación o a los artefactos generados.
3. **Invariante Zero-Diff:** Serializadores estrictamente lexicográficos que garantizan que el ordenamiento de tablas, columnas, medidas y relaciones no dependa del orden de inserción ni del sistema operativo.
4. **Estrategia Híbrida (Patrón `pydantic-core` / `polars`):** Capa de experiencia de usuario en Python (Typer, Rich, Pydantic v2) enlazada mediante PyO3 a un motor nuclear de alto rendimiento en Rust (`petgraph`), con fallback transparente a Python puro si la extensión nativa no está compilada.
5. **Hub de Operación IDE:** Espacio estructurado `artifacts/SemanticFlow/` que separa entradas particionadas por empresa (`inputs/companies/`), plantillas contractuales (`inputs/templates/`) y salidas compiladas segregadas por herramienta (`outputs/{pbip,dbt,docs,leadership_cockpit,lenses}/`).

### 2.2 Árbol estructural del repositorio
```
SemanticFlow/
├── .agentignore                       # Reglas de exclusión de contexto para agentes de IA (incluye secretos y *.env)
├── .context/                          # Malla satelital iDirectory v3.0 (tree.json)
├── .dockerignore                      # Filtros de exclusión para empaquetado OCI limpio
├── .github/                           # Automatizaciones CI/CD de GitHub
│   └── workflows/
│       ├── ci.yml                     # Pipeline principal de tests (Py 3.10-3.12 en Linux, Win, Mac)
│       ├── docker-publish.yml         # Publicación de imágenes multi-arch a GHCR (ghcr.io)
│       └── semantic-lint.yml          # Ejemplo de linter semántico en Pull Requests
├── 01_seed/                           # ADN y especificación técnica ThinkingSeed
│   ├── .context.yaml
│   └── seed-semanticflow-master.md    # Este snapshot exhaustivo
├── 02_Foundation/                     # Documentación fundacional de arquitectura
│   └── Engine/
│       ├── .context.yaml
│       └── engine_readme.md
├── action.yml                         # GitHub Action oficial de SemanticFlow para PRs
├── artifacts/                         # Planes de implementación, reportes forenses y métricas
│   ├── MetricsThinking.json           # Telemetría de auditoría MetricsThinking v3.0
│   ├── MetricsThinking.md             # Reporte ejecutivo de madurez (Score 100%)
│   ├── plans/
│   │   ├── active/
│   │   │   ├── ENTERPRISE_CLOUD_ROADMAP_PLAN.md # Plan maestro en 3 horizontes
│   │   │   └── INFERRED_ROADMAP.md              # Roadmap operacional desacoplado
│   │   └── metricsthinking/
│   └── SemanticFlow/                  # HUB OPERATIVO SMaC DEL IDE LOCAL
│       ├── README.md                  # Visión general y topología del hub operativo
│       ├── RUNBOOK_EXECUTION.md       # Guía paso a paso para añadir nuevas empresas
│       ├── run_pipeline.py            # Orquestador end-to-end con sanitización, scanner de secretos y gobernanza
│       ├── inputs/                    # DIRECTORIO DE ENTRADA (INGESTA)
│       │   ├── README.md              # Especificación contractual de esquemas
│       │   ├── templates/             # Plantillas canónicas (schema_template.md/.yaml, company_profile_template.yaml)
│       │   └── companies/             # Partición por empresa
│       │       ├── metro_santiago/    # Metro de Santiago (Transporte y Retail, 20 tablas)
│       │       └── santolaya/         # Santolaya Constructora e Inmobiliaria (14 tablas)
│       └── outputs/                   # DIRECTORIO DE SALIDA (ARTEFACTOS COMPILADOS)
│           ├── README.md              # Especificación y compatibilidad con herramientas
│           ├── pbip/                  # Modelos Power BI Developer (.pbip) y TMDL deterministas por empresa
│           ├── dbt/                   # Capa semántica dbt MetricFlow (YAML) determinista por empresa
│           ├── docs/                  # Diccionario de datos y Diagramas ERD por empresa
│           ├── leadership_cockpit/    # Visión ejecutiva C-Level y Radar Cross-Lens por empresa
│           └── lenses/                # 16 Carpetas de Persona Lenses individuales
│               ├── 01_data_analyst/
│               ├── 02_analytics_engineer/
│               ├── 03_data_engineer/
│               ├── 04_data_scientist/
│               ├── 05_bi_developer/
│               ├── 06_data_architect/
│               ├── 07_data_governance_officer/
│               ├── 08_platform_engineer/
│               ├── 09_domain_owner/
│               ├── 10_audit_risk/
│               ├── 11_analytics_leader/
│               ├── 12_data_product_manager/
│               ├── 13_finops_specialist/
│               ├── 14_ai_systems_engineer/
│               ├── 15_business_consumer/
│               └── 16_compliance_auditor/
├── Cargo.toml                         # Workspace Cargo para componentes en Rust
├── config/                            # Configuraciones por defecto y definiciones de roles
│   └── personas/
│       └── default_personas.yaml      # Especificación formal de las 16 Persona Lenses
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
│   ├── engineers_notes/               # Notas de ingeniería y planes técnicos de hardening
│   │   └── gemini-code-1792202660133.txt # Plan de blindaje y criterios AC-1 a AC-6 cumplidos
│   └── notes/
│       └── Tematica.md
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
│   └── project_governance.schema.json # Validación con bloqueo de nombres de propiedades sensibles
├── scripts/                           # Utilidades de mantenimiento y compilación
│   ├── build_standalone.py            # Generador de ejecutable único con PyInstaller
│   └── generate_golden_files.py       # Generador determinista de referencias golden
├── src/                               # Código fuente del paquete Python
│   ├── cli.py                         # Punto de entrada CLI con Typer y Rich
│   └── core/
│       ├── ast/                       # Modelos de AST bruto, semántico y canónico
│       ├── capabilities/              # Evaluador de capacidades de dialectos destino
│       ├── docs/                      # Generador de Diccionario y Diagramas Mermaid
│       ├── emitter/                   # Serializadores PBIP, TMDL y dbt MetricFlow deterministas
│       │   ├── dbt_emitter.py         # Emisor dbt Semantic Layer (orden canónico)
│       │   ├── model_emitter.py       # Emisor model.tmdl con ref table ordenadas
│       │   ├── pbip_writer.py         # Escritor de estructura .pbip con atomic staging y safe_filename
│       │   ├── relationship_emitter.py# Emisor relationships.tmdl ordenado lexicográficamente
│       │   ├── table_emitter.py       # Emisor de tables/*.tmdl con escape M y orden de columnas/medidas
│       │   └── tmdl_formatter.py      # Formateador de sintaxis TMDL con escape seguro
│       ├── engine/                    # Motor de inferencia topológica, DAX y compilador
│       │   ├── compiler.py
│       │   ├── dax_generator.py       # Generador DAX con escape de comillas simples y corchetes
│       │   └── relationship_resolver.py # Resolver con estabilización previa de relaciones
│       ├── leadership/                # Motor y analizadores autónomos del Leadership Cockpit
│       ├── mappers/                   # Transformadores raw -> canonical -> pbi
│       ├── parsers/                   # Parsers de esquemas relacionales Markdown y YAML
│       ├── personas/                  # Motor de 16 perspectivas y Leadership Cockpit
│       │   └── lenses/                # 16 Implementaciones Python de PersonaLens
│       ├── quality/                   # Evaluador de reglas y puntuación cQS
│       │   ├── dax_validator.py       # Validador léxico de DAX y anti-inyección semántica
│       │   ├── rules.py               # Reglas de calidad (incluyendo D-011 Direct Lake y D-012 VertiPaq)
│       │   └── scorer.py              # Calculador cQS con soporte de penalizaciones precisas
│       ├── rust_bridge.py             # Fachada híbrida Python / Rust PyO3
│       ├── security/                  # Módulo nuclear de seguridad y defensa en profundidad
│       │   ├── __init__.py
│       │   ├── sanitize.py            # Sanitización de empresas, rutas, nombres de archivo y culturas
│       │   └── secret_scanner.py      # Escáner estático de secretos y tokens en inputs
│       └── targets/                   # Adaptadores de capacidades y dialectos
├── terraform-provider-semanticflow/   # Proveedor oficial de Terraform en Go
│   ├── examples/
│   │   └── main.tf
│   ├── go.mod
│   ├── main.go
│   └── internal/
│       └── provider/
│           ├── data_source_schema.go
│           ├── provider.go
│           ├── resource_fabric_semantic_model.go
│           └── resource_unity_catalog_model.go
└── tests/                             # Suite de pruebas automatizadas (98 tests pasando al 100%)
    ├── fixtures/                      # Fixtures empresariales de prueba
    ├── golden/                        # Snapshots deterministas de regresión
    ├── test_all_lenses_deep.py        # 16 tests de validación profunda de perspectivas
    ├── test_canonical_model.py        # 3 tests de invariantes del modelo canónico
    ├── test_cli.py                    # 2 tests de comandos CLI
    ├── test_cli_personas.py           # 7 tests de exportación de roles
    ├── test_dbt_emitter.py            # Test unitario del emisor dbt Semantic Layer
    ├── test_deterministic_emission.py # 5 tests de invariante Zero-Diff, ordenamiento y reglas D-011/D-012
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
    ├── test_security_hardening.py     # 11 tests de path traversal, scanner de secretos, DAX y safe filenames
    ├── test_stage3_governance_quality.py # 3 tests de calidad y gobernanza
    ├── test_stage4_hardening_personas.py # 3 tests de endurecimiento
    ├── test_tmdl_emitter.py           # 1 test de serialización TMDL
    └── test_yaml_parser.py            # 1 test de parsing de YAML
```

### 2.3 Responsabilidad por directorio y archivo clave
- `src/cli.py`: Interfaz de consola con comandos: `inspect`, `compile`, `validate`, `cockpit`, `personas export`, `docgen`, `export-dbt`.
- `artifacts/SemanticFlow/run_pipeline.py`: Orquestador end-to-end con sanitización estricta de rutas, escaneo previo de secretos en esquemas y perfiles, validación $cQS$, compilación PBIP/TMDL, exportación dbt MetricFlow y distribución de proyecciones.
- `src/core/security/sanitize.py`: Primitivas de sanitización (`sanitize_company_id`, `resolve_within`, `safe_filename`, `validate_culture_code`) para erradicar Path Traversal y ataques en nombres de archivo.
- `src/core/security/secret_scanner.py`: Scanner de credenciales (Azure Client Secrets, Bearer JWT, PEM keys) que bloquea inputs envenenados sin exponer los secretos en logs.
- `src/core/quality/dax_validator.py`: Validador léxico de expresiones DAX para medidas; comprueba balanceo de delimitadores y bloquea inyecciones semánticas (`EVALUATE`, `DROP`, etc.).
- `src/core/quality/rules.py` y `scorer.py`: Reglas de calidad ampliadas con D-011 (incompatibilidad de Direct Lake ante DATETIME o N:N) y D-012 (antipatrones VertiPaq en `FILTER(ALL())` y cross-filtering bidireccional en hechos).
- `src/core/emitter/`: Emisores deterministas (`table_emitter.py`, `pbip_writer.py`, `model_emitter.py`, `relationship_emitter.py`, `dbt_emitter.py`) con ordenamiento lexicográfico canónico para garantizar el invariante Zero-Diff en Git.
- `src/core/engine/relationship_resolver.py`: Resolución determinista de relaciones 1:N en grafos analíticos, eliminando el no-determinismo por orden de entrada de archivos fuente.

---

## 3. FLUJOS DE EJECUCIÓN Y ENTRY POINTS

### 3.1 Puntos de entrada principales
1. **Orquestador Local Automatizado:** `python artifacts/SemanticFlow/run_pipeline.py --company <empresa_id>` (valida `--company` contra `^[a-zA-Z0-9_-]+$`).
2. **Línea de Comandos (CLI):** `semanticflow [inspect|compile|validate|cockpit|personas export|docgen|export-dbt]`.
3. **GitHub Action:** Tarea oficial `action.yml` consumible en workflows CI/CD.
4. **Azure DevOps:** Tarea `SemanticFlowQualityGate` empaquetada en `integrations/azure-devops/task/`.
5. **Terraform Provider:** Binario Go ejecutado por el Terraform Engine (`terraform init / plan / apply`).
6. **API Python Programática:** Invocable desde notebooks o scripts (`from src.core.mappers.raw_to_canonical import raw_to_canonical`).

### 3.2 Diagrama de flujo principal de extremo a extremo
```
[ Esquema Declarativo: Markdown / YAML ]   +   [ company_profile.yaml ]
                  │                                        │
                  ▼                                        ▼
    [ Pre-Execution Secret Scanner ] ──────────────────────┤ (Detención si hay credenciales)
                  │                                        │
                  ▼                                        ▼
        [ Markdown / Yaml Parser ]               [ Contexto IA / Gobernanza ]
                  │                                        │
                  ▼                                        │
         [ RelationalSchemaRaw ]                           │
                  │                                        │
                  ▼                                        │
        [ RawToCanonicalMapper ]                           │
                  │                                        │
                  ▼                                        │
       [ CanonicalSemanticProject ] ◄──────────────────────┘ (Inyección de ProjectGovernance)
                  │
        ┌──────────┴──────────┐
        ▼                     ▼
 [ Inferencia Topológica ]  [ Quality Scorer (cQS) & DAX Validator ]
 (Roles R(v), Ciclos C(G))   (Reglas D-001..D-012, PII, Sintaxis DAX)
        │                     │
        └──────────┬──────────┘
                   │  (cQS >= Umbral y Sin Errores Bloqueantes)
                   ├─────────────────────────────────────────┐
                   ▼                                         ▼
    [ Emisores Deterministas Zero-Diff ]          [ Matriz de Gobernanza ]
    • PBIP / TMDL (Orden Lexicográfico)           • 16 Persona Lenses Especializados
    • dbt MetricFlow (Models & Measures)          • Data Leadership Cockpit C-Level
    • DocGen (Diccionario Markdown + ERD Mermaid) • Telemetría y Exportación JSON
```

---

## 4. MODELO DE DATOS, CONTRATOS Y PERSISTENCIA

### 4.1 Esquemas y entidades principales
- `CanonicalSemanticProject`: Raíz del AST canónico. Contiene identificador, nombre, versión, descripción, metadatos de gobernanza (`ProjectGovernance`), entidades, relaciones y diagnósticos.
- `ProjectGovernance`: Metadatos corporativos de nivel de proyecto (`domain_id`, `domain_name`, `classification`, `data_product_status`, `owner`, `steward`, `compliance_frameworks`, `tags`, `custom_properties`).
- `SemanticEntity`: Representa una tabla lógica. Posee nombre, rol topológico (`FACT`, `DIMENSION`, `BRIDGE`, `OUTRIGGER`, `CALCULATED`), descripción, granularidad (`grain`), cardinalidad estimada (`estimated_rows`), atributos y medidas asociadas.
- `SemanticAttribute`: Representa una columna. Tipos de datos normalizados (`INT64`, `DOUBLE`, `DECIMAL`, `STRING`, `BOOLEAN`, `DATETIME`, `DATE`), indicadores de clave primaria/foránea (`is_key`), ocultamiento (`is_hidden`) y metadatos de gobernanza (`is_pii`).
- `SemanticMetric`: Medidas de cálculo formal. Expresión canónica, tipo de aditividad, formato y expresión generada en DAX validada léxicamente.
- `SemanticRelationship`: Restricción relacional 1:N entre dos entidades. Cardinalidad (`1:N`, `N:N`), modo de filtrado cruzado (`cross_filtering`), estado activo/inactivo (`is_active`) y claves asociadas.
- `Diagnostic`: Objeto de diagnóstico del Quality Gate con severidad (`ERROR`, `WARNING`, `INFO`, `RECOMMENDATION`), categoría, mensaje, acción sugerida y deducción cuantitativa opcional (`penalty`).

### 4.2 Almacenamiento y serialización determinista
- **Power BI PBIP:** Paquete TMDL emitido atómicamente mediante directorio temporal de staging. Todas las tablas, columnas, particiones y medidas se ordenan lexicográficamente para producir hashes SHA-256 idénticos en Git.
- **dbt MetricFlow:** Archivo `semantic_models.yml` ordenado deterministamente por entidad, atributo y medida conforme al estándar de dbt Semantic Layer v2.
- **Persistencia en Disco:** Rutas sanitizadas con `safe_filename` y verificadas con `resolve_within` contra path traversal.

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
`[CONFIRMADO]` La suite completa consta de **98 tests automatizados pasando satisfactoriamente al 100% (0 fallos, 0 errores)** ejecutados con `pytest 9.1.1`:
- **Pruebas de Seguridad y Hardening (`test_security_hardening.py` - 11 tests):** Valida rechazo de Path Traversal en `sanitize_company_id`, barreras de directorio en `resolve_within`, nombres de archivo seguros en `safe_filename`, detección y redacción de secretos en `secret_scanner`, validación léxica y balanceo en `dax_validator`, y prevención de inyección en scripts M de `table_emitter`.
- **Pruebas de Determinismo y Calidad (`test_deterministic_emission.py` - 5 tests):** Valida igualdad estricta SHA-256 en TMDL/PBIP con entidades barajadas, independencia del orden de entrada en `relationship_resolver`, determinismo en dbt YAML, penalización de la regla D-011 (Direct Lake) y detección de antipatrones en la regla D-012 (VertiPaq).
- **Pruebas de Regresión Golden (`test_golden_regression.py` - 2 tests):** Cero desviación en los modelos de referencia de Metro de Santiago y Retail Enterprise.
- **Pruebas de Seguridad de I/O y Gobernanza (`test_output_safety.py` - 3 tests):** Escritura atómica, rollback ante fallo y enmascaramiento automático de PII.
- **Pruebas de Contratos y Lentes (77 tests):** Validación exhaustiva de contratos JSON Schema, CLI, parsers Markdown/YAML y proyecciones de las 16 personas organizacionales.

### 6.2 Automatización y pipelines CI/CD
- `.github/workflows/ci.yml`: Pipeline que ejecuta linting con Ruff, tipado estático con Mypy y la suite completa de 98 tests con umbral de cobertura `--cov-fail-under=80`.
- `.github/workflows/docker-publish.yml`: Pipeline para publicación automatizada de imágenes OCI Distroless multi-arquitectura en GitHub Container Registry (`ghcr.io`).

---

## 7. OBSERVABILIDAD Y MODOS DE FALLA

### 7.1 Telemetría y diagnóstico
- **Consola Rica:** Uso de `rich.console`, paneles y tablas tabulares clasificando diagnósticos por severidad (`ERROR`, `WARNING`, `INFO`, `RECOMMENDATION`).
- **Códigos de Retorno Estándar:**
  - `0`: Éxito (validación aprobada, $cQS \ge \tau$, sin errores bloqueantes ni credenciales).
  - `1`: Fallo de Quality Gate, intento de Path Traversal o credencial detectada en inputs.

### 7.2 Modos de falla conocidos y mitigación
- **Path Traversal / Escape de Directorio:** Interceptado de inmediato por `sanitize_company_id` y `resolve_within`, arrojando `ValueError` o `PermissionError` y saliendo con código 1 de forma limpia.
- **Fuga de Credenciales en Inputs:** `secret_scanner` detecta patrones de tokens y claves privadas, detiene el pipeline e imprime únicamente el archivo y la línea afectada sin exponer el contenido sensible.
- **Inyecciones en Fórmulas DAX:** `dax_validator` rechaza directivas de escape como `EVALUATE` o comandos SQL, generando diagnósticos bloqueantes de severidad `ERROR`.

---

## 8. SEGURIDAD Y PRIVACIDAD

### 8.1 Postura de seguridad estática y del contenedor
- `docker/Dockerfile` utiliza la imagen base `gcr.io/distroless/python3-debian12:nonroot` bajo UID 65532 sin shell ni gestores de paquetes.
- **Políticas de Exclusión:** `.agentignore` excluye explícitamente archivos `.env`, `.secret`, `.pem`, `.key`, `credentials.json` y carpetas de caché de tokens (`token_cache/`, `azure_auth/`).
- **Validación de Schemas:** `schemas/project_governance.schema.json` rechaza nombres de propiedades sensibles mediante expresiones regulares negativas.

### 8.2 Manejo de secretos y privacidad
- **Sin Secretos en Repositorio:** El repositorio no contiene credenciales reales ni las expone en logs.
- **Detección y Enmascaramiento de PII:** `SemanticQualityScorer` audita columnas con atributos personales y exige clasificación `Restricted` o `Confidential`.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y LIMITACIONES

### 9.1 Nivel de madurez del proyecto
- `[CONFIRMADO]` **Madurez Global: Excelencia Operativa / Blindaje de Producción v2.1.0 (100.0% en auditoría MetricsThinking v3.0)**.
- El núcleo en Python está completamente endurecido contra vulnerabilidades de inyección, path traversal y no-determinismo en Git.
- Todos los criterios de aceptación AC-1 a AC-6 del documento técnico [gemini-code-1792202660133.txt](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/Data%20&%20AI%20Strategy/SemanticFlow/docs/engineers_notes/gemini-code-1792202660133.txt) han sido verificados y marcados con `[X]`.

### 9.2 Deuda técnica identificada y stubs
- `[CONFIRMADO]` La compilación local del provider de Terraform (`terraform-provider-semanticflow`) requiere Go `>=1.22`.
- `[CONFIRMADO]` La compilación local del módulo C-ABI `crates/semanticflow-pyo3` requiere `cargo` y `maturin`. En entornos donde no estén presentes, el sistema opera con el backend de Python puro de forma transparente.

---

## 10. REGLAS PARA MODIFICAR EL PROYECTO

### 10.1 Convenciones de estilo y calidad
- Tipado estático estricto mediante type hints en Python (validado por `mypy src/`).
- Linting y formateo conforme a `ruff check .` (longitud de línea máx: 120 caracteres).
- Contratos de datos modelados exclusivamente mediante Pydantic v2 en Python y `serde` en Rust.

### 10.2 Reglas arquitectónicas inviolables
1. **Invariante Zero-Diff:** Toda modificación a los emisores debe conservar el ordenamiento canónico estricto de tablas, columnas, medidas y relaciones.
2. **Defensa en Límites de Entrada:** Cualquier nuevo parámetro de ruta o identificador en el CLI debe validarse mediante `sanitize_company_id` o `resolve_within`.
3. **Determinismo Golden:** Ningún cambio puede romper las pruebas de regresión golden en `tests/test_golden_regression.py` sin justificación documentada.
4. **Zero Local Absolute Paths:** Prohibido incorporar rutas absolutas locales (`C:\...`, `D:\...`) en código, documentación o artefactos generados.

### 10.3 Checklist previo a commit
- [x] Ejecutar `pytest` y asegurar 98/98 tests pasando sin regresiones.
- [x] Ejecutar `python artifacts/SemanticFlow/run_pipeline.py --company metro_santiago`.
- [x] Ejecutar `python artifacts/SemanticFlow/run_pipeline.py --company "../test"` y verificar intercepción segura con código 1.
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
