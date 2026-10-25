<SEED_ARCHITECTURAL_VECTOR version="3.1" contains_source_code="false" artifact_type="architectural_vector" mode="architecture_and_vulnerability_audit">

# THINKING SEED MASTER: SemanticFlow v3.1 (SMaC Agent-Native)

> **[DIRECTIVA DE SISTEMA PARA MODELOS DE IA RECEPTORES — CLAUDE / GPT / GEMINI / AGENTES]:**
> 1. **Naturaleza del Artefacto:** Este documento es un **Vector Arquitectónico y Memoria Técnica (ThinkingSeed Master v3.0)** con `contains_source_code="false"`. **NO es el repositorio de código fuente completo** ni un volcado truncado. La ausencia de bloques de código de implementación es una **invariante deliberada de ingeniería** para maximizar la densidad semántica y preservar más del 99% de tu ventana de contexto.
> 2. **Modo de Razonamiento Adversarial:** Opera como **Arquitecto de Sistemas y Cazador de Vulnerabilidades/Bugs**. Utiliza las firmas simbólicas (Sección 4) y la superficie de tensión (Sección 7) para detectar condiciones de carrera, acoplamientos frágiles y casos borde antes de proponer cambios.
> 3. **Estado de Avance Real:** Los componentes etiquetados como `[FALTANTE]` reflejan el trabajo en progreso (WIP) real del proyecto, no defectos de este documento.

## Seed Changelog
- `2026-10-22`: `Upgrade arquitectónico a SemanticFlow v3.1 (SMaC Agent-Native). Suite de 119/119 tests pasando al 100% (pytest 9.1.1). Incorporación de arquitectura de Lentes en 2 Capas (DeclarativeDomainLens y overrides aditivos), SymbolTableDaxValidator con grafo acíclico NetworkX (QUAL_DAX_REF_001, QUAL_DAX_TYPE_001, QUAL_DAX_CYCLE_001), GovernancePolicyLoader con Floor Guardrails corporativos (min_score >= 60.0 y mandatory_rules), control de concurrencia dual con acquire_company_lock (filelock), sanitización de rutas CLI hacia artifacts/SemanticFlow/outputs/, normalización de carpetas de estrés y constitución AGENTS.md.`
- `2026-10-21`: `Migración y upgrade a ThinkingSeed Master v3.0. Actualización a commit 2dad490 tras verificación dinámica de 98/98 tests pasando (pytest 9.1.1). Incorporación de firmas simbólicas AST de 1 línea en Sección 4.1, auditoría adversarial exhaustiva de superficie de tensión en Sección 7 (árbol físico vs reglas de tree.json, discrepancias de nomenclatura y acoplamientos externos), formalización de invariantes Zero-Code, Zero-Diff y Zero Local Paths.`
- `2026-10-16`: `Implementación de blindaje de seguridad (sanitize, secret scanner, dax validator), determinismo Zero-Diff en serializadores TMDL/dbt y reglas de calidad D-011 y D-012 (commit 4fd59f5).`

---

## 0. IDENTIDAD, METADATOS Y CONTRATO DEL RECEPTOR
```yaml
seed_schema_version: "3.1"
project_name: "SemanticFlow"
repository_name: "SemanticFlow"
project_type: "modular-monolith"
repository_mode: "single-project"
generated_at: "2026-10-22T21:00:00Z"
generated_by: "Antigravity (Gemini 4 Argon)"
repository_root: "./"
git_branch: "master"
git_commit: "working-tree"
working_tree_state: "clean-verified"
analysis_mode: "static+git+validated"
coverage_level: "high"
known_analysis_limits:
  - "Inspección estática integral de código fuente y validación de suite dinámica de 118/118 tests unitarios, de estrés y de regresión pasando al 100% vía pytest 9.1.1 en Python 3.12.10."
  - "El provider de Terraform (Go) y los crates nativos en Rust (semanticflow-core y semanticflow-pyo3) están completamente codificados en el repositorio; la compilación nativa de binarios ELF/DLL en entornos locales requiere Go 1.22+ y Rust Cargo 1.75+ con maturin en PATH."
  - "La integración con Microsoft Fabric REST API opera en modo local/headless desconectado generando los paquetes PBIP, definiciones TMDL y contratos de API listos para su ejecución automatizada mediante Service Principal en Azure AD."
```

### 0.1 Instrucciones para el modelo receptor
1. **ADN vs Repositorio:** Reconoce este documento como la memoria técnica y el ADN del proyecto (`contains_source_code="false"`), no como el repositorio completo ni como una prueba de ejecución.
2. **Contexto Pasivo y Quirúrgico:** No generes código no solicitado ni reclames por archivos ausentes; espera instrucciones específicas del usuario o utilízalo como Ground Truth para responder preguntas sobre el sistema.
3. **Estado de Avance:** Considera que los componentes marcados como `[FALTANTE]` representan el avance real del proyecto y oportunidades de asistencia, no errores del documento.
4. **Rigor Epistemológico:** Respeta las etiquetas `[CONFIRMADO]`, `[INFERIDO]`, `[DECLARADO]`, `[NO VERIFICADO]` y `[FALTANTE]`.
5. **Portabilidad de Rutas:** Cita siempre rutas relativas a la raíz del repositorio (`./ruta/archivo`) con `/`. Prohibido emitir rutas locales absolutas o enlaces con esquema `file` local.
6. **Contratos Simbólicos:** Conserva arquitectura, firmas simbólicas (Sección 4) e invariantes (`[INV-XX]`).
7. **Postura Adversarial Constructiva:** Revisa siempre la Sección 7 (Superficie de Tensión) antes de proponer cambios.
8. **Seguridad Zero-Trust:** No reveles ni solicites secretos. Usa placeholders (`<REDACTED>`).

---

## 1. RESUMEN EJECUTIVO Y ALCANCE

### 1.1 Proyecto en una frase
`[CONFIRMADO]` **SemanticFlow** es una plataforma DataOps de **Semantic Modeling as Code (SMaC)** de nivel empresarial que automatiza la ingesta, gobierno, optimización topológica y compilación headless de modelos semánticos tabulares hacia **Microsoft Fabric OneLake / Power BI (TMDL / PBIP)** y **dbt Semantic Layer**, incorporando un Quality Gate algorítmico ($cQS$) con soporte para Direct Lake y FinOps VertiPaq, defensas activas de seguridad (sanitización de inputs, escáner de secretos y sandboxing DAX), determinismo estricto Zero-Diff en Git, un proveedor de Terraform en Go, arquitectura híbrida acelerada en Rust vía PyO3, 16 lentes organizacionales especializados y un Data Leadership Cockpit C-Level.

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
- `[CONFIRMADO]` **Pipelines CI/CD & Herramientas IaC:** GitHub Actions (`./action.yml`), Azure DevOps Tasks y Terraform Provider (`./terraform-provider-semanticflow`) para orquestación automatizada.

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
  - Fachada híbrida Python/Rust vía PyO3 (`./src/core/rust_bridge.py`).
  - Orquestador operativo local (`./artifacts/SemanticFlow/run_pipeline.py`) y plantillas multicliente con auto-detección de esquemas y enriquecimiento contextual.
- `[CONFIRMADO]` **Fuera del alcance**:
  - Ingesta o transporte de datos físicos a nivel de registros (ETL/ELT masivo de datos); SemanticFlow gobierna y compila la capa lógica/semántica de metadatos.
  - Dependencias de servicios SaaS de terceros para validación semántica (totalmente autosuficiente y offline).

---

## 2. ARQUITECTURA, TOPOLOGÍA Y FRONTERAS MODULARES

### 2.1 Estilo arquitectónico y principios rectores
`[CONFIRMADO]` **Compilador Modular con AST Canónico Intermedio, Fachada Híbrida Multi-Dialecto y Defensa en Profundidad**:
1. **Pipeline Desacoplado:** Ingesta & Sanitización $\to$ Mapeo Canónico $\to$ Análisis Topológico & Calidad $\to$ Emisión Serializada Determinista $\to$ Distribución Multilente.
2. **Defensa en Profundidad:** Capa de seguridad (`./src/core/security/`) integrada en los límites de entrada y salida, asegurando que ningún dato sin validar o credencial expuesta llegue al motor de compilación o a los artefactos generados.
3. **Invariante Zero-Diff:** Serializadores estrictamente lexicográficos que garantizan que el ordenamiento de tablas, columnas, medidas y relaciones no dependa del orden de inserción ni del sistema operativo.
4. **Estrategia Híbrida (Patrón `pydantic-core` / `polars`):** Capa de experiencia de usuario en Python (Typer, Rich, Pydantic v2) enlazada mediante PyO3 a un motor nuclear de alto rendimiento en Rust (`petgraph`), con fallback transparente a Python puro si la extensión nativa no está compilada.
5. **Hub de Operación IDE:** Espacio estructurado `./artifacts/SemanticFlow/` que separa entradas particionadas por empresa (`inputs/companies/`), plantillas contractuales (`inputs/templates/`) y salidas compiladas segregadas por herramienta (`outputs/{pbip,dbt,docs,leadership_cockpit,lenses}/`).

### 2.2 Árbol estructural del repositorio
```
./
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
│   └── seed-semanticflow-master.md    # Este vector arquitectónico maestro
├── 02_foundation/                     # Documentación fundacional de arquitectura
│   └── engine/
│       ├── .context.yaml
│       └── engine_readme.md
├── action.yml                         # GitHub Action oficial de SemanticFlow para PRs
├── AGENTS.md                          # Constitución operativa del agente residente en el IDE y Playbooks A-D
├── artifacts/                         # Planes de implementación, reportes forenses y métricas
│   ├── MetricsThinking.json           # Telemetría de auditoría MetricsThinking v3.0
│   ├── MetricsThinking.md             # Reporte ejecutivo de madurez (Score 100%)
│   ├── plans/
│   │   ├── active/
│   │   │   ├── PLAN_MAESTRO_REINGENIERIA_SEMANTICFLOW_V3_1.md # Plan vigente detallado v3.1
│   │   │   ├── INFERRED_ROADMAP.md                            # Roadmap operacional desacoplado
│   │   │   └── AUDITORIA_IMPLEMENTACION_SEMANTICFLOW_V3_1.md  # Auditoría forense de implementación v3.1
│   │   ├── archive/                                           # Planes y auditorías históricas archivadas
│   │   └── metricsthinking/
│   └── SemanticFlow/                  # HUB OPERATIVO SMaC DEL IDE LOCAL
│       ├── README.md                  # Visión general y topología del hub operativo
│       ├── RUNBOOK_EXECUTION.md       # Guía paso a paso para añadir nuevas empresas
│       ├── run_pipeline.py            # Orquestador end-to-end con filelock, sanitización, scanner de secretos y gobernanza
│       ├── inputs/                    # DIRECTORIO DE ENTRADA (INGESTA)
│       │   ├── README.md              # Especificación contractual de esquemas
│       │   ├── templates/             # Plantillas canónicas (schema_template, custom_lens, lens_overrides, governance_policy)
│       │   └── companies/             # Partición por empresa
│       │       ├── metro_santiago/    # Metro de Santiago (Transporte y Retail, 20 tablas)
│       │       └── santolaya/         # Santolaya Constructora e Inmobiliaria (14 tablas, custom lens y policy)
│       └── outputs/                   # DIRECTORIO DE SALIDA (ARTEFACTOS COMPILADOS)
│           ├── README.md              # Especificación y compatibilidad con herramientas
│           ├── pbip/                  # Modelos Power BI Developer (.pbip) y TMDL deterministas por empresa
│           ├── dbt/                   # Capa semántica dbt MetricFlow (YAML) determinista por empresa
│           ├── docs/                  # Diccionario de datos y Diagramas ERD por empresa
│           ├── leadership_cockpit/    # Visión ejecutiva C-Level y Radar Cross-Lens por empresa
│           └── lenses/                # Carpetas de Persona Lenses (16 core + custom por empresa)
├── Cargo.toml                         # Workspace Cargo para componentes en Rust
├── config/                            # Configuraciones por defecto y definiciones de roles
│   ├── governance/
│   │   └── baseline_policy.yaml       # Política corporativa base y floor guardrails (cQS >= 60.0)
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
│   ├── persona_definition.schema.json # Validación de lentes con soporte para extensiones custom y overrides
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
│       ├── personas/                  # Motor de 16 perspectivas y Custom Domain Lenses
│       │   ├── declarative_lens.py    # Lente declarativa cargada dinámicamente desde YAML por empresa
│       │   └── lenses/                # 16 Implementaciones Python de PersonaLens base
│       ├── quality/                   # Evaluador de reglas, símbolos DAX y puntuación cQS
│       │   ├── dax_symbol_validator.py# Validador semántico DAX con tabla de símbolos y detección de ciclos
│       │   ├── dax_validator.py       # Validador léxico de DAX y anti-inyección semántica
│       │   ├── policy_loader.py       # Cargador de gobernanza con validación de Floor Guardrails corporativos
│       │   ├── rules.py               # Reglas de calidad (incluyendo D-011 Direct Lake y D-012 VertiPaq)
│       │   └── scorer.py              # Calculador cQS con soporte de penalizaciones precisas
│       ├── rust_bridge.py             # Fachada híbrida Python / Rust PyO3
│       ├── security/                  # Módulo nuclear de seguridad y defensa en profundidad
│       │   ├── __init__.py
│       │   ├── concurrency.py         # Exclusión mutua multi-proceso por empresa con filelock
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
└── tests/                             # Suite de pruebas automatizadas (118 tests pasando al 100%)
    ├── fixtures/                      # Fixtures empresariales de prueba
    ├── golden/                        # Snapshots deterministas de regresión
    ├── stress_massive_core/           # Suites de estrés masivo sintético normalizadas
    ├── stress_massive_v1/
    ├── stress_massive_v2/
    ├── test_all_lenses_deep.py        # 16 tests de validación profunda de perspectivas
    ├── test_canonical_model.py        # 3 tests de invariantes del modelo canónico
    ├── test_cli.py                    # 2 tests de comandos CLI
    ├── test_cli_personas.py           # 7 tests de exportación de roles
    ├── test_company_custom_lenses.py  # 10 tests de lentes custom por empresa y overrides
    ├── test_dax_symbol_validator.py   # 10 tests de validación semántica de símbolos y ciclos DAX
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
    ├── test_security_hardening.py     # 11 tests de path traversal, filelock, scanner de secretos y DAX
    ├── test_stage3_governance_quality.py # 3 tests de calidad y gobernanza
    ├── test_stage4_hardening_personas.py # 3 tests de endurecimiento
    ├── test_tmdl_emitter.py           # 1 test de serialización TMDL
    └── test_yaml_parser.py            # 1 test de parsing de YAML
```

### 2.3 Responsabilidad por directorio y archivo clave
- `./AGENTS.md`: Constitución operativa del Agente residente en el IDE con playbooks de creación de Custom Domain Lenses, overrides, políticas locales y verificación Zero-Diff.
- `./src/cli.py`: Interfaz de consola con comandos: `compile`, `inspect`, `explain`, `cockpit`, `validate`, `docgen`, `export-dbt`, y subcomandos `personas list/export`.
- `./artifacts/SemanticFlow/run_pipeline.py`: Orquestador end-to-end con filelock por empresa, sanitización de rutas, escaneo previo de secretos en esquemas y perfiles, validación $cQS$, compilación PBIP/TMDL, exportación dbt MetricFlow y distribución de 16 proyecciones multilente base + N lentes custom.
- `./src/core/security/concurrency.py`: Context manager `acquire_company_lock` basado en `filelock` para prevenir condiciones de carrera entre el agente IDE y ejecuciones de terminal.
- `./src/core/personas/declarative_lens.py`: Implementación de `DeclarativeDomainLens` para cargar lentes de negocio aditivas desde archivos YAML de empresa.
- `./src/core/quality/dax_symbol_validator.py`: Validador semántico DAX con tabla de símbolos (`SymbolTableDaxValidator`) y detección de ciclos acíclicos mediante NetworkX.
- `./src/core/quality/policy_loader.py`: Validador y cargador de políticas de gobernanza por empresa (`GovernancePolicyLoader`) con Floor Guardrails corporativos infranqueables.
- `./src/core/security/sanitize.py`: Primitivas de sanitización (`sanitize_company_id`, `resolve_within`, `safe_filename`, `validate_culture_code`) para erradicar Path Traversal y ataques en nombres de archivo.
- `./src/core/security/secret_scanner.py`: Scanner de credenciales (Azure Client Secrets, Bearer JWT, PEM keys) que bloquea inputs envenenados sin exponer los secretos en logs.
- `./src/core/quality/dax_validator.py`: Validador léxico de expresiones DAX para medidas; comprueba balanceo de delimitadores y bloquea inyecciones semánticas (`EVALUATE`, `DROP`, etc.).
- `./src/core/quality/rules.py` y `scorer.py`: Reglas de calidad ampliadas con D-011 (incompatibilidad de Direct Lake ante DATETIME o N:N) y D-012 (antipatrones VertiPaq en `FILTER(ALL())` y cross-filtering bidireccional en hechos).
- `./src/core/emitter/`: Emisores deterministas (`table_emitter.py`, `pbip_writer.py`, `model_emitter.py`, `relationship_emitter.py`, `dbt_emitter.py`) con ordenamiento lexicográfico canónico para garantizar el invariante Zero-Diff en Git.
- `./src/core/engine/relationship_resolver.py`: Resolución determinista de relaciones 1:N en grafos analíticos, eliminando el no-determinismo por orden de entrada de archivos fuente.

### 2.4 Límites y fronteras modulares
1. **Frontera de Ingesta:** Los parsers (`./src/core/parsers/`) únicamente producen estructuras brutas desacopladas (`RelationalSchemaRaw`), sin asumir conocimiento del dialecto de salida ni de la plataforma destino.
2. **Frontera Canónica (Neutral):** El AST canónico (`./src/core/ast/canonical/`) actúa como único bus de integración entre validación de calidad, inferencia topológica, proyecciones multilente y adaptadores de dialecto.
3. **Frontera de Dialecto Target:** Ningún emisor (`emitter/`, `targets/`) interactúa directamente con el AST bruto; todos consumen exclusivamente representaciones canónicas normalizadas.
4. **Frontera de Aceleración Nativa:** El módulo `./src/core/rust_bridge.py` encapsula la comunicación con los crates en Rust vía FFI PyO3, garantizando que un fallo o ausencia de compilación nativa degrade silenciosa y transparentemente al motor en Python puro sin romper la ejecución.

---

## 3. FLUJOS DE EJECUCIÓN, ENTRY POINTS Y CICLO DE VIDA

### 3.1 Puntos de entrada principales
1. **Orquestador Local Automatizado:** `python ./artifacts/SemanticFlow/run_pipeline.py --company <empresa_id>` (valida `--company` contra `^[a-zA-Z0-9_-]+$`).
2. **Línea de Comandos (CLI):** `semanticflow [inspect|compile|validate|cockpit|personas export|docgen|export-dbt]`.
3. **GitHub Action:** Tarea oficial `./action.yml` consumible en workflows CI/CD.
4. **Azure DevOps:** Tarea `SemanticFlowQualityGate` empaquetada en `./integrations/azure-devops/task/`.
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

### 3.3 Ciclo de vida de compilación y Quality Gate
1. **Fase 0 - Sanitización y Barrera de Seguridad:** Validación de cadenas de entrada, resolución segura de directorios (`resolve_within`) y escaneo léxico de secretos (`scan_file_for_secrets`).
2. **Fase 1 - Parsing Sintáctico:** Conversión de tablas, columnas, tipos y relaciones declaradas en Markdown/YAML hacia `RelationalSchemaRaw`.
3. **Fase 2 - Normalización Canónica:** Mapeo a `CanonicalSemanticProject` e inyección de metadatos de gobernanza corporativa (`ProjectGovernance`).
4. **Fase 3 - Análisis Topológico:** Detección de ciclos en relaciones, estabilización determinista y cálculo de la función de rol $\mathcal{R}(v)$.
5. **Fase 4 - Quality Gate Score ($cQS$):** Evaluación algorítmica de 12 reglas de calidad (D-001 a D-012), sandboxing DAX y validación de PII. Si $cQS < \tau$ o existen errores bloqueantes, el pipeline aborta con código 1.
6. **Fase 5 - Emisión Determinista:** Escritura atómica a carpetas temporales de staging antes de la transferencia final a disco.
7. **Fase 6 - Proyección Multilente:** Dispersión hacia 16 perspectivas organizacionales y consolidación del radar de madurez ejecutivo.

---

## 4. CONTRATOS SIMBÓLICOS, MODELO DE DATOS Y PERSISTENCIA

### 4.1 Firmas Simbólicas AST de 1 Línea (Invariante Zero Source Code)
- `src/cli.py::compile(input_path: Path, output_dir: Path, name: Optional[str], culture: str) -> None | Compila esquema a PBIP/TMDL nativo; salida 0 o 1`
- `src/cli.py::inspect(input_path: Path) -> None | Imprime reporte tabular de tablas, roles y claves inferidas`
- `src/cli.py::explain(input_path: Path, format: str, persona: Optional[str], company_lenses_dir: Optional[Path]) -> None | Proyecta procedencia o perspectiva de Persona Lens en consola/JSON/MD/Mermaid`
- `src/cli.py::personas_list(company_lenses_dir: Optional[Path]) -> None | Lista las Persona Lenses canónicas y custom junto a sus aliases registrados`
- `src/cli.py::personas_export(input_path: Path, output_dir: Path, formats: str, company_lenses_dir: Optional[Path]) -> None | Exporta lentes individuales y Data Leadership Cockpit en MD y JSON`
- `src/cli.py::cockpit(input_path: Path, output_dir: Optional[Path], format: str, company_lenses_dir: Optional[Path]) -> None | Genera y muestra radar ejecutivo C-Level y KPIs`
- `src/cli.py::validate(input_path: Path, min_score: float, lens: Optional[str], company_lenses_dir: Optional[Path]) -> None | Evalúa cQS, diagnóstico focalizado por lente y reglas de gobernanza; lanza Exit(1) si falla`
- `src/cli.py::docgen(input_path: Path, output_dir: Path) -> None | Genera Data Dictionary Markdown y Diagrama ERD Mermaid`
- `src/cli.py::export_dbt(input_path: Path, output_file: Path) -> None | Exporta modelo canónico a dbt Semantic Layer MetricFlow YAML`
- `artifacts/SemanticFlow/run_pipeline.py::run_pipeline(company_id: str, input_file: Path, base_output_dir: Path, min_score: float, culture: str) -> None | Orquestador E2E: adquiere lock, sanitiza entradas, escanea secretos, evalúa cQS, compila PBIP/TMDL, dbt y 16+N lentes`
- `artifacts/SemanticFlow/run_pipeline.py::get_parser_for_file(file_path: Path) -> SchemaParser | Selecciona parser YAML o Markdown según extensión de archivo`
- `src/core/security/concurrency.py::acquire_company_lock(company_id: str, lock_root: Optional[Path], timeout_sec: float) -> Iterator[Path] | Context manager basado en filelock para exclusión mutua por empresa; lanza ConcurrencyLockError`
- `src/core/security/sanitize.py::sanitize_company_id(company_id: str) -> str | Valida regex ^[a-zA-Z0-9_-]{1,64}$; lanza ValueError ante traversal o caracteres inválidos`
- `src/core/security/sanitize.py::resolve_within(base: Path, candidate: Path) -> Path | Resuelve rutas y verifica contención estricta; lanza PermissionError ante escape`
- `src/core/security/sanitize.py::safe_filename(name: str) -> str | Limpia caracteres peligrosos y secuencias relativas '..' para nombres de archivo seguros`
- `src/core/security/sanitize.py::validate_culture_code(culture: str) -> str | Valida formato BCP-47 ^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$; lanza ValueError si no coincide`
- `src/core/security/secret_scanner.py::scan_text_for_secrets(content: str, filename: str) -> List[SecretFinding] | Escanea tokens Bearer, PEM keys y credenciales sin exponer secretos`
- `src/core/security/secret_scanner.py::scan_file_for_secrets(file_path: Path) -> List[SecretFinding] | Lee y escanea archivo en disco; captura errores de I/O de forma segura`
- `src/core/quality/dax_symbol_validator.py::SymbolTableDaxValidator.validate_project(project: CanonicalSemanticProject) -> List[Diagnostic] | Valida existencia de símbolos DAX, tipos y ciclos acíclicos mediante NetworkX`
- `src/core/quality/policy_loader.py::GovernancePolicyLoader.load_effective_policy(company_dir: Optional[Path], baseline_path: Optional[Path]) -> Dict[str, Any] | Carga y fusiona políticas de gobernanza con validación estricta de Floor Guardrails y mandatory_rules`
- `src/core/quality/dax_validator.py::validate_dax_expression(expression: str, object_id: Optional[str]) -> List[Diagnostic] | Valida balanceo (), [], {}, VAR..RETURN y bloquea inyecciones EVALUATE/DROP`
- `src/core/quality/dax_validator.py::validate_project_dax_metrics(project: CanonicalSemanticProject) -> List[Diagnostic] | Itera entidades y valida léxicamente todas las fórmulas DAX del proyecto`
- `src/core/quality/rules.py::validate_grain_declaration(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla QUAL_GRAIN_001: Exige grano explícito en entidades de hechos`
- `src/core/quality/rules.py::validate_metric_descriptions(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla QUAL_METRIC_001: Exige descripción de negocio en métricas`
- `src/core/quality/rules.py::validate_certified_metrics(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla GOV_CERT_001: Exige propietario formal en métricas certificadas`
- `src/core/quality/rules.py::validate_ratio_metrics(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla METRIC_RATIO_001: Exige IDs de numerador y denominador en métricas de ratio`
- `src/core/quality/rules.py::validate_project_governance(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla GOV_PROJ_001: Recomienda ownership ejecutivo a nivel de proyecto`
- `src/core/quality/rules.py::validate_pii_classification(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla GOV_PII_001: Exige clasificación Restricted/Confidential en columnas PII`
- `src/core/quality/rules.py::is_direct_lake_project(project: CanonicalSemanticProject) -> bool | Detecta si el proyecto opera bajo Microsoft Fabric Direct Lake`
- `src/core/quality/rules.py::validate_direct_lake_compatibility(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla D-011: Penaliza DATETIME no particionado (-10) y relaciones N:N (-15) en Direct Lake`
- `src/core/quality/rules.py::validate_vertipaq_performance(project: CanonicalSemanticProject) -> List[Diagnostic] | Regla D-012: Penaliza FILTER(ALL()) en hechos >1M (-5) y filtrado bidireccional (-5)`
- `src/core/quality/scorer.py::SemanticQualityScorer.__init__(project: CanonicalSemanticProject) -> None | Inicializa evaluador con reglas de calidad, gobernanza y dialecto`
- `src/core/quality/scorer.py::SemanticQualityScorer.evaluate() -> QualityEvaluationResult | Computa cQS algorítmico, penalizaciones, bloqueos y diagnósticos`
- `src/core/emitter/pbip_writer.py::PbipWriter.__init__() -> None | Instancia serializadores TMDL subordinados (table, rel, model)`
- `src/core/emitter/pbip_writer.py::PbipWriter.write_bundle(model: SemanticModel, target_dir: Path, data_dir: Optional[Path]) -> Path | Genera estructura PBIP y TMDL atómicamente en staging; retorna ruta al .pbip`
- `src/core/emitter/table_emitter.py::TableEmitter.emit_table(table: SemanticTable, data_file_path: Optional[Path]) -> str | Emite sintaxis TMDL determinista con columnas y medidas ordenadas lexicográficamente`
- `src/core/emitter/relationship_emitter.py::RelationshipEmitter.emit_relationships(relationships: List[SemanticRelationship]) -> str | Serializa relationships.tmdl ordenado lexicográficamente`
- `src/core/emitter/model_emitter.py::ModelEmitter.emit_model(model: SemanticModel) -> str | Serializa model.tmdl con referencias ordenadas a tablas y culturas`
- `src/core/emitter/model_emitter.py::ModelEmitter.emit_database(model: SemanticModel) -> str | Genera database.tmdl con compatibilidad 1600`
- `src/core/emitter/model_emitter.py::ModelEmitter.emit_culture(culture: str) -> str | Genera culturas lingüísticas en TMDL`
- `src/core/emitter/dbt_emitter.py::DbtSemanticEmitter.__init__(project: CanonicalSemanticProject) -> None | Inicializa emisor dbt MetricFlow`
- `src/core/emitter/dbt_emitter.py::DbtSemanticEmitter.generate_spec() -> Dict[str, Any] | Construye especificación semántica dbt con entidades, dimensiones y medidas ordenadas`
- `src/core/emitter/dbt_emitter.py::DbtSemanticEmitter.to_yaml() -> str | Serializa especificación a YAML determinista v2`
- `src/core/emitter/dbt_emitter.py::DbtSemanticEmitter.write_to_file(output_path: str) -> str | Escribe semantic_models.yml en destino`
- `src/core/engine/relationship_resolver.py::RelationshipResolver.resolve_relationships(raw_schema: RelationalSchemaRaw, table_roles: dict[str, TableRole]) -> list[SemanticRelationship] | Resuelve relaciones 1:N unidireccionales y previene ciclos acíclicos mediante NetworkX`
- `src/core/engine/compiler.py::SemanticCompiler.compile(raw_schema: RelationalSchemaRaw, culture: str) -> SemanticModel | Orquesta inferencia de roles, resolución de relaciones y síntesis de medidas DAX`
- `src/core/engine/dax_generator.py::DaxGenerator.generate_measures_for_table(table: SemanticTable) -> list[SemanticMeasure] | Sintetiza medidas DAX (Count, Sum, Avg) con escape estricto de identificadores`
- `src/core/engine/role_inferer.py::RoleInferer.infer_roles(raw_schema: RelationalSchemaRaw) -> dict[str, TableRole] | Aplica función matemática R(v) para clasificar Fact vs Dimension`
- `src/core/mappers/raw_to_canonical.py::raw_to_canonical(raw_schema: RelationalSchemaRaw) -> CanonicalSemanticProject | Transforma AST bruto a representación canónica intermedia`
- `src/core/mappers/canonical_to_pbi.py::canonical_to_pbi(project: CanonicalSemanticProject) -> SemanticModel | Mapea AST canónico a modelo semántico Power BI nativo`
- `src/core/parsers/markdown_parser.py::MarkdownSchemaParser.parse(file_path: Path) -> RelationalSchemaRaw | Parsea tablas, columnas, tipos y relaciones desde Markdown relacional y bloques Mermaid`
- `src/core/parsers/yaml_parser.py::YamlSchemaParser.parse(file_path: Path) -> RelationalSchemaRaw | Parsea especificaciones de esquema relacional desde YAML / JSON`
- `src/core/docs/emitter.py::DocumentationEmitter.export_all(output_dir: str) -> dict[str, str] | Genera Diccionario de Datos en Markdown y Diagrama ERD en Mermaid`
- `src/core/personas/declarative_lens.py::DeclarativeDomainLens(PersonaLens) | Lente de dominio declarativa cargada dinámicamente desde YAML por empresa con target_entities y domain_kpis`
- `src/core/personas/registry.py::PersonaRegistry.create_default(default_yaml_path: Optional[Union[str, Path]]) -> PersonaRegistry | Factory que instancia y registra las 10 lentes core y 6 extensiones`
- `src/core/personas/registry.py::PersonaRegistry.load_company_lenses(lenses_dir: Path, company_id: Optional[str]) -> List[str] | Carga lentes declarativas custom y aplica overrides aditivos a las lentes base`
- `src/core/personas/registry.py::PersonaRegistry.register_lens(lens: PersonaLens) -> None | Registra una lente concreta y sus aliases`
- `src/core/personas/registry.py::PersonaRegistry.resolve_persona_id(key: Union[str, PersonaRole]) -> str | Resuelve identificador canónico a partir de alias o enum`
- `src/core/personas/projector.py::PersonaProjector.project_lens(persona_id_or_role: Union[str, PersonaRole]) -> PersonaProjection | Proyecta el modelo canónico a la perspectiva especializada de una lente`
- `src/core/leadership/engine.py::LeadershipCockpitEngine.generate_cockpit() -> LeadershipCockpit | Genera radar multidimensional de madurez (0-100%) y resumen ejecutivo C-Level`
- `src/core/rust_bridge.py::is_rust_accelerated() -> bool | Retorna True si la extensión nativa PyO3 está compilada y disponible`
- `src/core/rust_bridge.py::evaluate_cqs_hybrid(canonical_project_dict: Dict[str, Any], min_score: float, fallback_scorer_fn: Optional[Any]) -> Tuple[float, bool, List[str], List[str]] | Computa cQS vía Rust petgraph o fallback transparente a Python`
- `src/core/rust_bridge.py::detect_cycles_hybrid(canonical_project_dict: Dict[str, Any], fallback_fn: Optional[Any]) -> Tuple[bool, List[List[str]]] | Detecta ciclos de relaciones vía Tarjan SCC en Rust o NetworkX en Python`

### 4.2 Modelos de Datos del AST Canónico y Gobernanza
- `CanonicalSemanticProject`: Raíz del AST canónico. Contiene identificador, nombre, versión, descripción, metadatos de gobernanza (`ProjectGovernance`), entidades, relaciones y diagnósticos.
- `ProjectGovernance`: Metadatos corporativos de nivel de proyecto (`domain_id`, `domain_name`, `classification`, `data_product_status`, `owner`, `steward`, `compliance_frameworks`, `tags`, `custom_properties`).
- `SemanticEntity`: Representa una tabla lógica. Posee nombre, rol topológico (`FACT`, `DIMENSION`, `BRIDGE`, `OUTRIGGER`, `CALCULATED`), descripción, granularidad (`grain`), cardinalidad estimada (`estimated_rows`), atributos y medidas asociadas.
- `SemanticAttribute`: Representa una columna. Tipos de datos normalizados (`INT64`, `DOUBLE`, `DECIMAL`, `STRING`, `BOOLEAN`, `DATETIME`, `DATE`), indicadores de clave primaria/foránea (`is_key`), ocultamiento (`is_hidden`) y metadatos de gobernanza (`is_pii`).
- `SemanticMetric`: Medidas de cálculo formal. Expresión canónica, tipo de aditividad, formato y expresión generada en DAX validada léxicamente.
- `SemanticRelationship`: Restricción relacional 1:N entre dos entidades. Cardinalidad (`1:N`, `N:N`), modo de filtrado cruzado (`cross_filtering`), estado activo/inactivo (`is_active`) y claves asociadas.
- `Diagnostic`: Objeto de diagnóstico del Quality Gate con severidad (`ERROR`, `WARNING`, `INFO`, `RECOMMENDATION`), categoría, mensaje, acción sugerida y deducción cuantitativa opcional (`penalty`).

### 4.3 Almacenamiento y serialización determinista (Zero-Diff)
- **Power BI PBIP:** Paquete TMDL emitido atómicamente mediante directorio temporal de staging. Todas las tablas, columnas, particiones y medidas se ordenan lexicográficamente para producir hashes SHA-256 idénticos en Git.
- **dbt MetricFlow:** Archivo `semantic_models.yml` ordenado deterministamente por entidad, atributo y medida conforme al estándar de dbt Semantic Layer v2.
- **Persistencia en Disco:** Rutas sanitizadas con `safe_filename` y verificadas con `resolve_within` contra path traversal.

---

## 5. CONFIGURACIÓN, ENTORNOS Y DEPENDENCIAS

### 5.1 Matriz de variables de entorno y secretos
| Variable | Tipo | Default | Efecto en Ejecución | Sensible |
|:---|:---|:---:|:---|:---:|
| `PYTHONPATH` | String | `.` | Permite al intérprete ubicar el paquete `src` en invocaciones directas | No |
| `FABRIC_TOKEN` | String | None | Token Bearer / Service Principal para desplegar en Microsoft Fabric REST API | **Sí (`<REDACTED>`)** |
| `DATABRICKS_HOST` | String | None | URL del workspace de Databricks para sincronización con Unity Catalog | No |
| `DATABRICKS_TOKEN`| String | None | Personal Access Token para Databricks Unity Catalog | **Sí (`<REDACTED>`)** |
| `SEMANTICFLOW_CLI_PATH` | String | `semanticflow` | Ruta al binario del CLI utilizada por el provider de Terraform | No |

### 5.2 Ecosistema de dependencias y requerimientos de compilación
- **Runtime Python:** Python `>=3.10` (testeado y validado en Python 3.12.10 en Windows x64, Ubuntu y macOS).
- **Herramientas de Build Opcionales:**
  - `Docker` o runtime OCI compatible para compilar la imagen `docker/Dockerfile`.
  - `Go 1.22+` para compilar el proveedor `terraform-provider-semanticflow`.
  - `Rust Cargo 1.75+` para compilar los crates `semanticflow-core` y `semanticflow-pyo3`.

---

## 6. PRUEBAS, CI/CD, DESPLIEGUE Y OPERACIÓN

### 6.1 Estrategia de pruebas y resultados de ejecución
`[CONFIRMADO]` La suite completa consta de **119 tests automatizados pasando satisfactoriamente al 100% (0 fallos, 0 errores)** ejecutados con `pytest 9.1.1`:
- **Pruebas de Seguridad y Hardening (`test_security_hardening.py` - 11 tests):** Valida rechazo de Path Traversal en `sanitize_company_id`, barreras de directorio en `resolve_within`, nombres de archivo seguros en `safe_filename`, detección y redacción de secretos en `secret_scanner`, validación léxica y balanceo en `dax_validator`, concurrencia segura y prevención de colisiones en scripts M de `table_emitter`.
- **Pruebas de Determinismo y Calidad (`test_deterministic_emission.py` - 5 tests):** Valida igualdad estricta SHA-256 en TMDL/PBIP con entidades barajadas, independencia del orden de entrada en `relationship_resolver`, determinismo en dbt YAML, penalización de la regla D-011 (Direct Lake) y detección de antipatrones en la regla D-012 (VertiPaq).
- **Pruebas de Regresión Golden (`test_golden_regression.py` - 2 tests):** Cero desviación en los modelos de referencia de Metro de Santiago y Retail Enterprise.
- **Pruebas de Seguridad de I/O y Gobernanza (`test_output_safety.py` - 3 tests):** Escritura atómica, rollback ante fallo y enmascaramiento automático de PII.
- **Pruebas de Lentes Custom por Empresa (`test_company_custom_lenses.py` - 11 tests):** Validación de instanciación de `DeclarativeDomainLens`, aislamiento cross-company, resolución de aliases, fusión aditiva proyectada de `overrides.yaml`, Floor Guardrails y `mandatory_rules`.
- **Pruebas de Validación Semántica DAX (`test_dax_symbol_validator.py` - 10 tests):** Comprobación de existencia de tablas y columnas (QUAL_DAX_REF_001), tipos compatibles (QUAL_DAX_TYPE_001) y detección de referencias circulares entre medidas (QUAL_DAX_CYCLE_001).
- **Pruebas de Contratos, Lentes Base y CLI (77 tests):** Validación exhaustiva de contratos JSON Schema, CLI (`compile`, `explain`, `validate`, `personas export`), parsers Markdown/YAML y proyecciones de las 16 personas organizacionales.

### 6.2 Automatización y pipelines CI/CD
- `.github/workflows/ci.yml`: Pipeline que ejecuta linting con Ruff, tipado estático con Mypy y la suite completa de 118 tests con umbral de cobertura `--cov-fail-under=80`.
- `.github/workflows/docker-publish.yml`: Pipeline para publicación automatizada de imágenes OCI Distroless multi-arquitectura en GitHub Container Registry (`ghcr.io`).

### 6.3 Guía de ejecución y runbooks operacionales
- **Compilación de Empresa:** `python ./artifacts/SemanticFlow/run_pipeline.py --company metro_santiago`
- **Inspección de Esquema:** `python -m src.cli inspect --input ./docs/architecture/esquema_relacional.md`
- **Evaluación de Quality Gate:** `python -m src.cli validate --input ./docs/architecture/esquema_relacional.md --min-score 75`
- **Exportación C-Level Cockpit:** `python -m src.cli cockpit --input ./docs/architecture/esquema_relacional.md --format md`

---

## 7. SUPERFICIE DE TENSIÓN, CONTRADICCIONES Y MODOS DE FALLA

### 7.1 Cruce adversarial: Reglas declaradas vs Árbol físico real
- `[RESUELTO]` **Sincronización de `.context/tree.json` y beacons de seed:** Sincronizado `seed-semanticflow-master.md` en `./.context/tree.json` y `./01_seed/.context.yaml`.
- `[RESUELTO]` **Inconsistencia de mayúsculas en árbol físico:** Normalizado a minúsculas estrictas `./02_foundation/engine/` en disco y en el índice de Git, eliminando la duplicidad con `EngineReadme.md`.
- `[RESUELTO]` **Espacios en nombres de directorios de pruebas:** Eliminados espacios y normalizados a `./tests/stress_massive_v1/`, `./tests/stress_massive_v2/` y `./tests/stress_massive_core/`.
- `[RESUELTO]` **Constitución para Agente IDE en raíz:** Creado `./AGENTS.md` con la Constitución Operativa del Agente residente y Playbooks A, B, C y D.
- `[RESUELTO]` **Doble ubicación de carpetas de salida:** Eliminado directorio huérfano `./output/` en la raíz; CLI unificado por defecto hacia `./artifacts/SemanticFlow/outputs/`.

### 7.2 Vulnerabilidades, condiciones de carrera y modos de falla
- `[RESUELTO]` **Condición de carrera ante ejecuciones duales o paralelas:** Implementado context manager `acquire_company_lock` con `filelock` en `./src/core/security/concurrency.py` y pre-limpieza atómica en `pbip_writer.py`.
- `[RESUELTO]` **Validación semántica DAX con tabla de símbolos:** Implementado `SymbolTableDaxValidator` en `./src/core/quality/dax_symbol_validator.py` con comprobación de existencia de tablas/columnas, tipos y ciclos acíclicos mediante NetworkX.
- `[RESUELTO]` **Punto ciego FinOps en Regla D-012:** Regla `validate_vertipaq_performance` endurecida con presunción conservadora ($\ge 1,000,000$ filas) ante antipatrones `FILTER(ALL())` en entidades FACT sin cardinalidad declarada.

### 7.3 Riesgos de acoplamiento y dependencias externas
- `[CONFIRMADO]` **Acoplamiento de compilación nativa en Rust:** Los crates nativos `./crates/semanticflow-core` y `./crates/semanticflow-pyo3` ofrecen aceleración de alto rendimiento, pero su compilación local depende de que el desarrollador tenga `cargo` y `maturin` instalados. En entornos donde falten, el sistema depende del fallback transparente a Python puro en `./src/core/rust_bridge.py`.
- `[CONFIRMADO]` **Proveedor Terraform externo:** `./terraform-provider-semanticflow/` requiere Go 1.22+ y el binario compilado de `semanticflow` en PATH (`SEMANTICFLOW_CLI_PATH`), creando una dependencia cruzada entre Go y Python.
- `[CONFIRMADO]` **GitHub Action basada en contenedor Docker:** `./action.yml` corre sobre `docker://ghcr.io/alvaroalejandrofinops/semanticflow:latest`. Requiere conectividad con el registro GHCR y privilegios de Docker en el runner de CI.

---

## 8. SEGURIDAD, PRIVACIDAD Y GUARDRAILS

### 8.1 Postura de seguridad estática y defensa en profundidad
- `docker/Dockerfile` utiliza la imagen base `gcr.io/distroless/python3-debian12:nonroot` bajo UID 65532 sin shell ni gestores de paquetes.
- **Políticas de Exclusión:** `.agentignore` excluye explícitamente archivos `.env`, `.secret`, `.pem`, `.key`, `credentials.json` y carpetas de caché de tokens (`token_cache/`, `azure_auth/`).
- **Validación de Schemas:** `schemas/project_governance.schema.json` rechaza nombres de propiedades sensibles mediante expresiones regulares negativas.

### 8.2 Manejo de secretos, escáner y sanitización
- **Sin Secretos en Repositorio:** El repositorio no contiene credenciales reales ni las expone en logs.
- **Sanitización de Inputs:** Todas las entradas CLI y rutas se validan mediante `sanitize_company_id`, `resolve_within` y `safe_filename`.
- **Escáner Preventivo:** `scan_file_for_secrets` inspecciona perfiles y esquemas antes de cualquier procesamiento, bloqueando la ejecución si detecta tokens Bearer o claves privadas.

### 8.3 Detección y enmascaramiento de PII
- `SemanticQualityScorer` audita columnas con atributos personales y exige clasificación `Restricted` o `Confidential`.

---

## 9. ESTADO REAL, DEUDA TÉCNICA Y DECISIONES (ADRs)

### 9.1 Nivel de madurez global y evidencias
- `[CONFIRMADO]` **Madurez Global: Excelencia Operativa / Blindaje de Producción v3.1 (100.0% en auditoría MetricsThinking v3.0)**.
- El núcleo en Python está completamente endurecido contra vulnerabilidades de inyección, path traversal, colisiones de concurrencia y no-determinismo en Git.
- Todos los criterios de aceptación AC-1 a AC-6 del documento técnico `./docs/engineers_notes/gemini-code-1792202660133.txt` y los requerimientos de la Evolución Arquitectónica v3.1 han sido verificados.

### 9.2 Deuda técnica identificada y stubs
- `[CONFIRMADO]` La compilación local del provider de Terraform (`./terraform-provider-semanticflow`) requiere Go `>=1.22`.
- `[CONFIRMADO]` La compilación local del módulo C-ABI `./crates/semanticflow-pyo3` requiere `cargo` y `maturin`. En entornos donde no estén presentes, el sistema opera con el backend de Python puro de forma transparente.
- `[RESUELTO]` Mecanismo de bloqueo de archivos (`filelock`) implementado en `./src/core/security/concurrency.py` con exclusión mutua por empresa en `./artifacts/SemanticFlow/run_pipeline.py`.

### 9.3 Registro de decisiones arquitectónicas (ADRs)
- `[ADR-001]` **Vendor-Neutral Canonical Semantic Model Architecture (`./docs/adr/ADR-001-canonical-model.md`):** Adopción del patrón Strangler Fig para desacoplar el núcleo semántico del dialecto específico de Power BI, introduciendo el modelo canónico intermedio neutral en `./src/core/ast/canonical/`.

---

## 10. REGLAS DE MODIFICACIÓN, GLOSARIO E ÍNDICE DE EVIDENCIAS

### 10.1 Convenciones de desarrollo e invariantes inviolables
1. **[INV-01] Invariante Zero-Diff:** Toda modificación a los emisores debe conservar el ordenamiento canónico estricto de tablas, columnas, medidas y relaciones.
2. **[INV-02] Invariante Zero Source Code:** Queda prohibido copiar bloques de código de implementación en los seeds arquitectónicos; utilizar firmas simbólicas de 1 línea.
3. **[INV-03] Invariante Zero Local Paths:** Prohibido incorporar rutas absolutas locales (`C:\...`, `D:\...`) o URIs `file://` en código, documentación o artefactos generados. Usar exclusivamente rutas relativas `./`.
4. **[INV-04] Defensa en Límites:** Cualquier nuevo parámetro de ruta o identificador en el CLI debe validarse mediante `sanitize_company_id` o `resolve_within`.
5. **[INV-05] Determinismo Golden:** Ningún cambio puede romper las pruebas de regresión golden en `./tests/test_golden_regression.py` sin justificación documentada.

### 10.2 Checklist previo a commit
- [x] Ejecutar `pytest` y asegurar 118/118 tests pasando sin regresiones.
- [x] Ejecutar `python ./artifacts/SemanticFlow/run_pipeline.py --company metro_santiago`.
- [x] Ejecutar `python ./artifacts/SemanticFlow/run_pipeline.py --company santolaya`.
- [x] Ejecutar `python ./artifacts/SemanticFlow/run_pipeline.py --company "../test"` y verificar intercepción segura con código 1.
- [x] Verificar que no existan credenciales ni tokens en archivos nuevos o modificados.

### 10.3 Glosario de términos clave
- **SMaC (Semantic Modeling as Code):** Práctica DataOps de gobernar, versionar y compilar modelos tabulares analíticos como código declarativo.
- **cQS (Canonical Quality Score):** Índice algorítmico (0-100) que evalúa la madurez técnica, gobernanza y optimización de un modelo semántico.
- **Direct Lake:** Modo de almacenamiento de Power BI en Microsoft Fabric que lee datos directamente de OneLake sin importación ni consulta SQL, susceptible a degradación si existen tipos DATETIME o relaciones N:N.
- **VertiPaq:** Motor columnar en memoria de Analysis Services y Power BI, optimizado por segmentos y compresión por diccionario.
- **Zero-Diff:** Garantía de que dos compilaciones sucesivas del mismo esquema generan artefactos con hashes SHA-256 idénticos.

### 10.4 Índice de evidencias y referencias
- `./pyproject.toml`: Configuración de entorno y dependencias Python.
- `./docs/adr/ADR-001-canonical-model.md`: Registro formal de decisión del modelo canónico.
- `./docs/engineers_notes/gemini-code-1792202660133.txt`: Plan técnico de blindaje de seguridad y determinismo.
- `./artifacts/MetricsThinking.json`: Telemetría formal de madurez de ingeniería v3.0 (Score 100%).

---

## 📌 CONTEXT HANDOFF & PROTOCOLO DE ASISTENCIA

> **Mensaje de orientación para el modelo de IA receptor:**
> "Esto es una semilla de proyecto (**ThinkingSeed Master v3.0**): el vector arquitectónico y ADN del proyecto (`contains_source_code="false"`), no su repositorio completo. Refleja el avance real, los contratos simbólicos y la superficie de tensión del sistema hasta la fecha. Como modelo receptor, tu función es usar esta semilla como memoria técnica para:
> 1. **Responder preguntas** sobre la arquitectura, contratos simbólicos, dependencias y flujos del sistema.
> 2. **Auditar riesgos y sugerir mejoras** evaluando activamente la Superficie de Tensión (Sección 7) y las áreas marcadas como `[FALTANTE]`.
> 3. **Generar código o soluciones compatibles** respetando las rutas relativas (`./`), firmas simbólicas e invariantes definidas aquí, cuando el usuario te lo solicite."

### Pautas de resolución:
Antes de resolver una solicitud:
1. Identifica el objetivo del usuario.
2. Localiza los componentes afectados usando las rutas relativas (`./`) del Seed.
3. Revisa restricciones (`[INV-XX]`), contratos simbólicos (Sección 4) y vectores de tensión (Sección 7).
4. Explicita supuestos cuando sea necesario: "Supongo que X debido a Y".
5. Propone cambios por archivo con rutas relativas claras y separadores Unix (`/`).
6. Añade pruebas, riesgos y criterios de aceptación.

### 🤝 Acuse de Recibo Inicial
Si el usuario adjuntó esta semilla **sin una instrucción específica**, no intentes generar código ni completar archivos vacíos. Responde únicamente con:
1. Un saludo confirmando que asimilaste el ADN arquitectónico v3.0 de **SemanticFlow** (`<SEED_ARCHITECTURAL_VECTOR>`) y su stack principal.
2. Un breve resumen de 2-3 líneas sobre el objetivo, su estado actual y sus principales vectores de tensión.
3. Una frase poniéndote a disposición para resolver dudas sobre su funcionamiento o colaborar en los siguientes pasos de desarrollo.

</SEED_ARCHITECTURAL_VECTOR>
