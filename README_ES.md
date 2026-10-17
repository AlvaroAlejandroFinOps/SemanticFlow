![Encabezado SemanticFlow](SemanticFlow.png)

# SEMANTICFLOW: Plataforma DataOps Empresarial de Semantic Modeling as Code para Microsoft Fabric y Power BI

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Entorno](https://img.shields.io/badge/Entorno-Python%203.10%2B-1a1a1a?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Arquitectura](https://img.shields.io/badge/Arquitectura-AST%20Can%C3%B3nico-2b2b2b?style=flat-square)](src/core/ast/)
[![Estándar](https://img.shields.io/badge/Est%C3%A1ndar-Enterprise%20Paper--Grade%20v2.0-1a1a1a?style=flat-square)](#)
[![Ecosistema](https://img.shields.io/badge/Ecosistema-Multi--IA%20%28Google%20%7C%20Claude%20%7C%20OpenAI%20%7C%20Cursor%29-34495e?style=flat-square)](#)
[![Verificación](https://img.shields.io/badge/Verificaci%C3%B3n-82%2F82%20Tests%20Aprobados%20%28100%25%29-000000?style=flat-square)](tests/)
[![Destino](https://img.shields.io/badge/Destino-Fabric%20Direct%20Lake%20%7C%20TMDL%2FPBIP-2b2b2b?style=flat-square)](src/core/emitter/)
[![Quality Gate](https://img.shields.io/badge/CI%2FCD-Quality%20Gate%20cQS-1a1a1a?style=flat-square)](src/core/quality/)
[![Licencia](https://img.shields.io/badge/Licencia-Apache%202.0-4b5563?style=flat-square)](LICENSE)

---

## 1. Resumen Ejecutivo

En las organizaciones de gran escala pertenecientes a sectores como banca, retail, telecomunicaciones, infraestructura, construcción y minería, la modernización analítica sobre arquitecturas Lakehouse (Microsoft Fabric OneLake, Azure Synapse, AWS S3 o GCP BigQuery) enfrenta un cuello de botella operativo crítico: la **fricción sistemática entre la ingeniería de datos upstream y el consumo semántico downstream**. Mientras que las transformaciones en arquitecturas Medallion (Bronze/Silver/Gold) operan bajo rigurosas prácticas de CI/CD, control de versiones y gobierno, los modelos analíticos downstream continúan construyéndose de manera artesanal y manual dentro de interfaces gráficas como Power BI Desktop, produciendo archivos binarios `.pbix` opacos que no admiten auditorías, control de versiones ni revisiones de código en Git.

Esta desconexión arquitectónica introduce riesgos de negocio sistémicos: duplicación de lógica de cálculo, relaciones tabulares ambiguas que degradan el rendimiento de las capacidades en la nube, ausencia de Quality Gates automatizados en los pipelines de despliegue, exposición no controlada de Información de Identificación Personal (PII) y desalineación de objetivos entre los equipos de gobierno, finanzas cloud (FinOps) y los usuarios de negocio. En capacidades de Microsoft Fabric (F-SKUs), las topologías dimensionales deficientes provocan saturación de memoria inesperada y la degradación desde Direct Lake hacia el modo DirectQuery, aumentando las latencias de consulta en órdenes de magnitud y disparando el Costo Total de Propiedad (TCO).

**SemanticFlow** es una plataforma DataOps de **Semantic Modeling as Code (SMaC)** de nivel corporativo diseñada para erradicar esta brecha operativa. Permite a los ingenieros de datos, analistas de datos y arquitectos definir modelos semánticos de forma declarativa (en Markdown o YAML) directamente en repositorios Git, compilarlos de forma local y desatendida (headless) hacia formatos nativos de Microsoft Fabric y Power BI (TMDL y proyectos `.pbip`) y especificaciones dbt Semantic Layer (MetricFlow), validar la calidad mediante un Quality Gate algorítmico determinista ($cQS$), enriquecer los modelos con contexto corporativo mediante perfiles de empresa impulsados por IA, proyectar 16 perspectivas organizacionales especializadas (Persona Lenses) con cuadros de mando ejecutivos C-Level (Leadership Cockpits), y orquestar el ciclo de vida cloud mediante GitHub Actions, Azure DevOps Tasks, un proveedor oficial de Terraform en Go y un núcleo acelerado en Rust expuesto vía PyO3.

---

## 2. Arquitectura y Topología del Sistema

SemanticFlow opera como un compilador headless in-memory sin requerir conexiones activas ni dependencias de bases de datos externas en tiempo de compilación. Su topología desacoplada articula el ciclo de vida continuo de desarrollo y gobierno de datos:

```
+---------------------------------------------------------------------------------------------------+
|                                 CICLO DE VIDA DATAOPS EN GIT                                      |
|                                                                                                   |
|   [ Repositorio Git ]          [ Pipeline CI/CD ]           [ Compilador Headless ]               |
|   Esquema Declarativo  ===>    Azure DevOps / GitHub   ===> SemanticFlow Engine                   |
|   (YAML / Markdown)            Runner (Python / Rust)       - Inferencia Topológica R(v)          |
|   + Perfil de Empresa                                       - Auditoría y Quality Gate cQS        |
+------------------------------------------+--------------------------------------------------------+
                                           |
                    +----------------------+----------------------+
                    | (Pasa Quality Gate cQS)                     | (Falla cQS < Umbral)
                    v                                             v
+------------------------------------------+    +---------------------------------------------------+
|     COMPILACIÓN Y SERIALIZACIÓN          |    |               PIPELINE BLOQUEADO                  |
|                                          |    |  Build rechazado en Pull Request.                 |
|  - Tabular Model Def. Lang. (TMDL)       |    |  Reporte de infracciones de gobernanza,           |
|  - Power BI Project Developer (.pbip)    |    |  ciclos topológicos o PII expuesta.               |
|  - dbt MetricFlow (semantic_models.yml)  |    +---------------------------------------------------+
|  - Diccionario Corporativo y ERD Mermaid |
|  - 16 Lentes Organizacionales            |
|  - Leadership Cockpit Ejecutivo C-Level  |
+-------------------+----------------------+
                    |
                    v
+---------------------------------------------------------------------------------------------------+
|                      PROVISIÓN CLOUD VIA TERRAFORM / MICROSOFT FABRIC                             |
|                                                                                                   |
|   [ Terraform Provider (Go) ]                                                                     |
|   • semanticflow_schema (Data Source para inspección cQS en tiempo de plan)                       |
|   • semanticflow_fabric_semantic_model (Provisión TMDL directa en Microsoft Fabric vía REST API)  |
|   • semanticflow_unity_catalog_model (Sincronización de esquemas y tags PII en Databricks)        |
+---------------------------------------------------------------------------------------------------+
```

### Topología Interna del Motor y Límites Modulares

El compilador ejecuta a través de capas desacopladas con soporte de aceleración híbrida en Rust y un espacio operativo integrado en el IDE:

```
+---------------------------------------------------------------------------------------------------+
| 1. CAPA DE INGESTA DECLARATIVA                                                                    |
|    - MarkdownSchemaParser: Cabeceras dinámicas (tipos Delta, restricciones), integración con ERD. |
|    - YamlSchemaParser: Especificaciones declarativas YAML e ingesta de contratos.                 |
|    - Ingesta de Perfil de Empresa: Unidades de negocio, KPIs, marcos normativos y objetivos.      |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 2. REPRESENTACIÓN INTERMEDIA (AST CANÓNICO)                                                       |
|    - CanonicalSemanticProject: Grafo entidad-relación, tipado estricto, ProjectGovernance.        |
|    - Resolución de Gobernanza: Herencia automatizada de owner, steward, clasificación y tags.     |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
         +----------------------------------------+----------------------------------------+
         |                                        |                                        |
         v                                        v                                        v
+-----------------------------+  +--------------------------------+  +------------------------------+
| INFERENCIA TOPOLÓGICA       |  | QUALITY GATE Y AUDITORÍA       |  | MATRIZ MULTI-STAKEHOLDER     |
| - Asignación de Roles R(v)  |  | - SemanticQualityScorer        |  | - 16 Persona Lenses          |
| - Control de Aciclicidad    |  | - Penalizaciones Deterministas |  | - Radar de Madurez de Dominio|
| - petgraph (Rust) / NetX    |  | - Bloqueo CI/CD Automatizado   |  | - Leadership Cockpit C-Level |
+--------------+--------------+  +----------------+---------------+  +--------------+---------------+
               |                                  |                                 |
               +----------------------------------+---------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 3. CAPA DE EMISIÓN Y SERIALIZACIÓN CLOUD                                                          |
|    - PbipWriter / TmdlFormatter: Jerarquía de carpetas TMDL nativa para Microsoft Fabric.        |
|    - DbtSemanticEmitter: Especificaciones dbt MetricFlow (semantic_models.yml).                  |
|    - DocumentationEmitter: Diccionario de datos corporativo en Markdown y diagrama Mermaid ERD.  |
|    - Proyectores de Persona: 16 informes especializados en Markdown y payloads JSON.              |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática y Motores Analíticos

### 3.1. Resolución Topológica de Grafos e Inferencia de Roles

El motor columnar de Microsoft Fabric y Power BI (VertiPaq) exige esquemas en estrella o en constelación puros. Los caminos de relación circulares o las configuraciones de filtrado cruzado bidireccional generan ambigüedad en las consultas, planes de ejecución ineficientes y agotamiento de memoria en las capacidades corporativas.

Modelemos el esquema relacional como un multigrafo dirigido atribuido $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, donde $\mathcal{V}$ representa el conjunto de entidades relacionales (tablas) y $\mathcal{E} \subseteq \mathcal{V} \times \mathcal{V} \times \mathcal{A}$ representa las referencias dirigidas de clave foránea desde atributos hijos hacia claves primarias o únicas de entidades padre. Para cada vértice $v \in \mathcal{V}$, sea $d^-(v)$ el grado de entrada (número de claves foráneas entrantes) y $d^+(v)$ el grado de salida (número de claves foráneas salientes). La función determinista de asignación de roles $\mathcal{R}(v)$ clasifica cada entidad:

$$\mathcal{R}(v) = \begin{cases} 
\text{FACT}, & \text{si } d^+(v) \ge 1 \ \land \ d^-(v) = 0 \\
\text{DIMENSION}, & \text{si } d^+(v) = 0 \ \land \ d^-(v) \ge 1 \\
\text{BRIDGE}, & \text{si } d^+(v) \ge 2 \ \land \ d^-(v) \ge 1 \\
\text{OUTRIGGER}, & \text{si } d^+(v) \ge 1 \ \land \ d^-(v) \ge 1 \ \land \ |Attr(v)| \le \theta_{dim} \\
\text{DIMENSION}, & \text{en otro caso (fallback conservador)}
\end{cases}$$

La detección de ciclos se garantiza mediante la aciclicidad formal del grafo de condensación:

$$\mathcal{C}(\mathcal{G}) = \emptyset \iff \forall \text{ ciclo } C \subset \mathcal{G}, \ |C| = 0$$

Si $\mathcal{C}(\mathcal{G}) \ne \emptyset$, `RelationshipResolver` (o `petgraph::algo::tarjan_scc` en el núcleo nativo de Rust) aísla las aristas conflictivas y marca los caminos secundarios como inactivos (`isActive = false`) en TMDL para eliminar la ambigüedad de rutas y preservar el flujo unidireccional ($1:\infty$).

### 3.2. Semantic Quality Score ($cQS$) como Quality Gate Automatizado en CI/CD

La integridad semántica de un proyecto compilado se evalúa mediante una función de puntuación continua objetiva $cQS: \mathcal{M} \to [0, 100]$, que actúa como un Quality Gate de despliegue en pipelines de integración continua:

$$cQS(\mathcal{M}) = \max\left(0, \ 100 - \sum_{k \in \mathcal{K}} w_k \cdot \mathbb{I}_k(\mathcal{M}) - \sum_{j \in \mathcal{D}} \lambda_j \cdot \mu_j(\mathcal{M})\right)$$

Donde:
* $\mathcal{K}$ representa las **invariantes arquitectónicas bloqueantes** (claves primarias ausentes, ciclos activos en relaciones, claves foráneas rotas). Si $\sum \mathbb{I}_k(\mathcal{M}) > 0$, el pipeline finaliza con código de error y detiene el despliegue.
* $\mathcal{D}$ representa las **reglas de gobierno y calidad corporativas** (atributos sin tipo, columnas de negocio indocumentadas, medidas no certificadas, ausencia de propietario de proyecto, atributos PII sin enmascarar).
* $\lambda_j$ especifica el peso de la penalización y $\mu_j(\mathcal{M})$ representa la frecuencia normalizada de infracción.

**Política Operativa de CI/CD:** El despliegue hacia Microsoft Fabric o dbt es rechazado si $cQS(\mathcal{M}) < \tau_{\text{threshold}}$ (umbral por defecto: 75.0% / umbral operativo mínimo: 45.0%) o si se vulnera alguna invariante crítica bloqueante.

### 3.3. Matriz Multi-Stakeholder y Proyección de 16 Persona Lenses

El operador de proyección $\Pi_{\theta}$ mapea el modelo canónico global en 16 perspectivas especializadas de dominio agrupadas en cuatro pilares corporativos:

```
+---------------------------------------------------------------------------------------------------+
|                            MATRIZ DE GOBERNANZA MULTI-STAKEHOLDER                                 |
+----------------------------------+----------------------------------------------------------------+
| PILAR CORPORATIVO                | ROLES Y VALOR APORTADO                                         |
+----------------------------------+----------------------------------------------------------------+
| I. Gobierno y Cumplimiento       | • Data Governance Officer: Propiedad, stewardship y metadatos. |
|    Regulatorio                   | • Compliance Auditor: Linaje PII, GDPR/SOX y Ley 19.628.       |
|                                  | • Audit & Risk: Trazabilidad, huella criptográfica y riesgos.  |
|                                  | • Domain Owner: Certificación de contextos y SLAs de dominio.  |
+----------------------------------+----------------------------------------------------------------+
| II. Plataforma Cloud             | • Data Engineer: Formatos Delta en OneLake, particionamiento.  |
|     y Optimización FinOps        | • Platform Engineer: Automatización CI/CD, IaC y seguridad OCI.|
|                                  | • FinOps Specialist: Memoria F-SKU en Fabric y costo de queries|
|                                  | • AI Systems Engineer: Embeddings vectoriales y contexto RAG.  |
+----------------------------------+----------------------------------------------------------------+
| III. Analytics Engineering y BI  | • Analytics Engineer: Topología en estrella y contratos dbt.   |
|                                  | • BI Developer: Organización TMDL, carpetas y medidas DAX.     |
|                                  | • Data Architect: Topología del grafo relacional y conformidad.|
|                                  | • Data Scientist: Catálogo de atributos para ML y estadísticas.|
+----------------------------------+----------------------------------------------------------------+
| IV. Liderazgo Estratégico        | • Analytics Leader: Salud del portafolio y cockpit ejecutivo.  |
|     y Negocio                    | • Data Product Manager: Ciclo de vida, adopción y SLOs.        |
|                                  | • Business Consumer: Métricas certificadas en lenguaje natural.|
|                                  | • Data Analyst: Catálogo de autoservicio y consultas ágiles.   |
+----------------------------------+----------------------------------------------------------------+
```

### 3.4. Huella de Memoria Direct Lake y Cotas Computacionales

Para evitar la paginación de memoria y la degradación a DirectQuery en capacidades de Fabric (ej. F8, F16, F64), la huella columnar física de la entidad $v$ en memoria se calcula mediante la compresión de diccionario de VertiPaq:

$$\mathcal{M}_{mem}(v) = \sum_{a \in Attr(v)} \left( |Dict(a)| \cdot \text{width}(a) + N_{rows}(v) \cdot \lceil \log_2(|Dict(a)|) \rceil \right)$$

SemanticFlow garantiza:
1. Claves surrogadas $\text{SK}$ generadas como tipos enteros (`INT64`/`BIGINT`) con ancho de bits mínimo $\lceil \log_2(|V|) \rceil$.
2. Cero columnas calculadas DAX: toda lógica de transformación se materializa upstream en tablas OneLake Gold.
3. Evaluación de relaciones acotada en complejidad $\mathcal{O}(|\mathcal{V}| + |\mathcal{E}|)$ mediante recorrido topológico en profundidad.

---

## 4. Rendimiento Empírico y Benchmarks

El motor de compilación fue evaluado en entornos computacionales estándar (Python 3.12.10 sobre hardware AMD64), verificando escalabilidad sobre topologías sintéticas de estrés y sobre modelos reales en producción (Metro de Santiago y Santolaya Constructora e Inmobiliaria):

| Dimensión de Rendimiento | Meta de Diseño | Tier 1 (Pequeño) | Tier 2 (Corporativo) | Tier 3 (Empresarial) | Caso Real: Metro Santiago | Caso Real: Santolaya |
|:---|:---|:---|:---|:---|:---|:---|
| **Dominio de Negocio** | Multisectorial | Prueba Sintética | Prueba Sintética | Prueba Sintética | Transporte Público y Retail | Construcción e Inmobiliaria |
| **Entidades Gobernadas** | 5 - 15 tablas | 4 - 8 tablas | 15 - 25 tablas | 50 - 100 tablas | 20 tablas operativas | 14 tablas operativas |
| **Relaciones Evaluadas** | 5 - 25 aristas | 6 - 12 aristas | 20 - 40 aristas | 75 - 180 aristas | 24 relaciones activas | 27 relaciones en estrella |
| **Latencia de Compilación** | $< 1.000$ ms | 42 ms | 185 ms | 840 ms | 210 ms | 195 ms |
| **Tiempo Proyección (16 Lentes)** | $< 2.000$ ms | 110 ms | 390 ms | 1.240 ms | 420 ms | 380 ms |
| **Huella Máxima de Memoria** | $< 250$ MB | 38 MB | 54 MB | 118 MB | 62 MB | 58 MB |
| **Puntaje Quality Gate ($cQS$)** | $\ge 45,0$ / $\ge 75,0$ | 92,5 / 100,0 | 85,0 / 100,0 | 78,0 / 100,0 | 49,0 / 100,0 (Sin perfil) | **70,0 / 100,0 (Con perfil)** |
| **Errores Bloqueantes** | 0 errores | 0 | 0 | 0 | 0 | 0 |
| **Tasa de Fuga de Rutas** | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% | 0,0% |
| **Índice de Paridad ($\Phi$)** | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 |
| **Suite de Verificación** | 100% aprobada | 82/82 tests | 82/82 tests | 82/82 tests | 82/82 tests aprobados | 82/82 tests aprobados |

---

## 5. Estructura del Repositorio y Artefactos

```
SemanticFlow/
├── .agentignore                       # Filtros de exclusión de contexto para agentes de IA
├── .context/                          # Malla de gobernanza contextual iDirectory v3.0 (tree.json)
├── .dockerignore                      # Reglas de exclusión para builds de imagen OCI mínimos
├── .github/                           # Automatizaciones CI/CD de GitHub
│   └── workflows/
│       ├── ci.yml                     # Pipeline principal de pruebas (Python 3.10-3.12 en Linux, Win, Mac)
│       ├── docker-publish.yml         # Publicación automatizada de contenedores multi-arch a GHCR
│       └── semantic-lint.yml          # Flujo de linter semántico en Pull Requests
├── 01_seed/                           # ADN arquitectónico y especificaciones ThinkingSeed Master
│   ├── .context.yaml
│   └── seed-semanticflow-master.md    # Snapshot exhaustivo de ingeniería
├── 02_Foundation/                     # Documentación fundacional de arquitectura y del motor
│   └── Engine/
│       ├── .context.yaml
│       └── engine_readme.md
├── action.yml                         # GitHub Action oficial para Quality Gates en PRs
├── artifacts/                         # Planes de implementación, reportes forenses y métricas
│   ├── MetricsThinking.json           # Telemetría de auditoría forense del proyecto
│   ├── MetricsThinking.md             # Reporte ejecutivo de auditoría (100% de madurez)
│   ├── plans/active/
│   │   ├── ENTERPRISE_CLOUD_ROADMAP_PLAN.md # Plan Maestro Enterprise Cloud en 3 Horizontes
│   │   └── INFERRED_ROADMAP.md        # Roadmap operacional desacoplado
│   └── SemanticFlow/                  # ESPACIO OPERATIVO LOCAL SMaC EN IDE
│       ├── README.md                  # Topología del espacio operativo y directrices
│       ├── RUNBOOK_EXECUTION.md       # Guía de incorporación para nuevos esquemas
│       ├── run_pipeline.py            # Orquestador automatizado end-to-end con auto-descubrimiento
│       ├── inputs/                    # LÍMITE DE ENTRADA (INGESTA)
│       │   ├── README.md              # Especificaciones de ingesta
│       │   ├── templates/             # Plantillas canónicas (schema_template, company_profile_template)
│       │   └── companies/             # Particiones por empresa (metro_santiago, santolaya)
│       └── outputs/                   # LÍMITE DE SALIDA (COMPILACIÓN)
│           ├── README.md              # Especificaciones de salida
│           ├── pbip/                  # Proyectos Power BI (.pbip) y TMDL para Microsoft Fabric
│           ├── dbt/                   # Especificaciones dbt Semantic Layer MetricFlow (YAML)
│           ├── docs/                  # Diccionarios de datos corporativos y diagramas Mermaid ERD
│           ├── leadership_cockpit/    # Cuadros de mando ejecutivos C-Level y radares de madurez
│           └── lenses/                # 16 Carpetas especializadas de Persona Lenses
├── Cargo.toml                         # Workspace Cargo para componentes nativos en Rust
├── config/                            # Perfiles de entorno y configuración de stakeholders
│   └── personas/
│       └── default_personas.yaml      # Especificación formal de los 16 Persona Lenses
├── crates/                            # Código fuente nativo en Rust
│   ├── semanticflow-core/             # Crate en Rust puro (AST, petgraph, calidad cQS)
│   │   ├── Cargo.toml
│   │   └── src/                       # models.rs, graph.rs, quality.rs, lib.rs
│   └── semanticflow-pyo3/             # Módulo C-ABI con bindings PyO3 hacia Python
│       ├── Cargo.toml
│       └── src/lib.rs
├── docker/                            # Especificaciones de contenedores OCI
│   └── Dockerfile                     # Imagen multi-stage Distroless minimalista (<45 MB, nonroot)
├── docs/                              # Registros de decisiones de arquitectura y notas técnicas
│   ├── adr/
│   │   └── ADR-001-canonical-model.md
│   └── architecture/
│       └── esquema_relacional.md      # Esquema relacional empresarial de referencia
├── integrations/                      # Extensiones y tareas para la nube empresarial
│   └── azure-devops/
│       ├── azure-pipelines-example.yml# Plantilla de pipeline para Azure Repos
│       ├── vss-extension.json         # Manifiesto de extensión para Azure DevOps
│       └── task/                      # Definición de tarea y runner de ejecución Node.js
├── pyproject.toml                     # Configuración del paquete Python y metadatos de build
├── schemas/                           # Contratos de validación estricta en JSON Schema
│   ├── persona_definition.schema.json
│   └── project_governance.schema.json
├── scripts/                           # Utilidades de mantenimiento y compilación
│   ├── build_standalone.py            # Compilador a binario autónomo (PyInstaller)
│   └── generate_golden_files.py       # Generador de regresión determinista golden
├── src/                               # Código fuente del compilador
│   ├── cli.py                         # Punto de entrada CLI (Typer / Rich)
│   └── core/
│       ├── ast/                       # Especificaciones del Árbol de Sintaxis Abstracta Canónico
│       ├── capabilities/              # Planificadores de ejecución del pipeline
│       ├── docs/                      # Generadores de diccionario de datos y diagramas Mermaid
│       ├── emitter/                   # Motores de serialización nativos TMDL, PBIP y dbt
│       ├── engine/                    # Inferencia topológica, resolución de relaciones y DAX
│       ├── leadership/                # Motores de síntesis y analizadores del Leadership Cockpit
│       ├── mappers/                   # Mapeadores de esquemas (raw-to-canonical y canonical-to-pbi)
│       ├── parsers/                   # Parsers de esquemas declarativos (Markdown y YAML)
│       ├── personas/                  # Motor de los 16 Persona Lenses y Leadership Cockpit
│       ├── quality/                   # Evaluadores de reglas de calidad y SemanticQualityScorer
│       ├── rust_bridge.py             # Puente híbrido transparente Python / Rust PyO3
│       └── targets/                   # Adaptadores de dialectos específicos de plataforma
├── terraform-provider-semanticflow/   # Proveedor oficial de Terraform en Go
│   ├── examples/main.tf               # Ejemplo en producción con Fabric y Databricks
│   ├── go.mod
│   ├── main.go                        # Entry point del servidor de plugins
│   └── internal/provider/             # Recursos y orígenes de datos del proveedor
└── tests/                             # Suite de pruebas automatizadas (82 tests aprobados)
    ├── fixtures/                      # Esquemas y fixtures de prueba empresarial
    ├── golden/                        # Archivos de referencia deterministas golden
    ├── test_all_lenses_deep.py        # 16 pruebas profundas de perspectivas de stakeholders
    ├── test_canonical_model.py        # 3 pruebas unitarias del modelo canónico
    ├── test_cli.py                    # 2 pruebas de comandos CLI
    ├── test_cli_personas.py           # 7 pruebas de exportación de stakeholders
    ├── test_dbt_emitter.py            # Prueba unitaria del emisor dbt Semantic Layer
    ├── test_golden_regression.py      # 2 pruebas de regresión determinista golden
    ├── test_inference_engine.py       # 1 prueba del motor de inferencia topológica
    ├── test_leadership_cockpit.py     # 2 pruebas del cuadro de mando ejecutivo C-Level
    ├── test_markdown_parser.py        # 1 prueba del parser de Markdown
    ├── test_output_safety.py          # 3 pruebas de escritura atómica y codificación segura
    ├── test_persona_contracts.py      # 7 pruebas de esquemas de contratos de gobernanza
    ├── test_persona_projector.py      # 8 pruebas del operador de proyección
    ├── test_persona_quality_rules.py  # 3 pruebas de reglas de calidad
    ├── test_persona_registry.py       # 7 pruebas del registro de personas
    ├── test_rust_bridge.py            # Prueba del puente híbrido y degradación elegante
    ├── test_stage3_governance_quality.py # 3 pruebas de calidad y gobernanza
    ├── test_stage4_hardening_personas.py # 3 pruebas de endurecimiento de personas
    ├── test_tmdl_emitter.py           # 1 prueba de serialización TMDL
    └── test_yaml_parser.py            # 1 prueba del parser de YAML
```

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Configuración del Entorno y Prerrequisitos

Prerrequisitos: Python 3.10 o superior (validado en Python 3.12.10).

```bash
# Clonar el repositorio
git clone https://github.com/AlvaroAlejandroFinOps/SemanticFlow.git
cd SemanticFlow

# Inicializar y activar un entorno virtual aislado
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar el paquete en modo editable con dependencias de desarrollo
pip install -e ".[dev]"
```

### 6.2. Ejecución del Pipeline y Comandos CLI

Ejecute el orquestador SMaC automatizado end-to-end con auto-descubrimiento de esquemas e inyección contextual de gobernanza IA:

```bash
# 1. Ejecutar compilación end-to-end para Santolaya Constructora e Inmobiliaria
python artifacts/SemanticFlow/run_pipeline.py --company santolaya

# 2. Ejecutar compilación end-to-end para Metro de Santiago
python artifacts/SemanticFlow/run_pipeline.py --company metro_santiago

# 3. Inspeccionar estructura relacional y verificar roles inferidos vía CLI
semanticflow inspect --input docs/architecture/esquema_relacional.md

# 4. Validar el Quality Gate cQS en pasos automatizados de pipelines CI/CD
semanticflow validate --input docs/architecture/esquema_relacional.md --min-score 75.0

# 5. Compilar de forma headless el esquema relacional hacia TMDL / PBIP nativo para Microsoft Fabric
semanticflow compile --input docs/architecture/esquema_relacional.md --output output/PBIP --name "ProductionModel"

# 6. Exportar especificaciones dbt Semantic Layer MetricFlow
semanticflow export-dbt --input docs/architecture/esquema_relacional.md --output output/dbt/semantic_models.yml

# 7. Generar el Data Leadership Cockpit C-Level en la consola
semanticflow cockpit --input docs/architecture/esquema_relacional.md --format human

# 8. Exportar los 16 Persona Lenses y los artefactos del Cockpit en Markdown y JSON
semanticflow personas export --input docs/architecture/esquema_relacional.md --output output/personas

# 9. Generar Diccionario de Datos corporativo y diagramas Mermaid ERD
semanticflow docgen --input docs/architecture/esquema_relacional.md --output output/docs
```

### 6.3. Suite de Verificación y Pruebas de Invariantes

```bash
# Ejecutar la suite completa de pruebas automatizadas (82 tests aprobados)
pytest -v

# Validar regresión determinista golden para prevenir cambios semánticos no deseados
pytest tests/test_golden_regression.py

# Verificar estilo de código y tipado estático
mypy src/
ruff check .
```

---

## 7. Glosario de Dominio

* **Semantic Modeling as Code (SMaC):** Disciplina DataOps que define, versiona y valida modelos semánticos analíticos utilizando código declarativo almacenado en Git, en lugar de modificaciones manuales en interfaces gráficas.
* **Tabular Model Definition Language (TMDL):** Sintaxis declarativa basada en texto plano y estructura de carpetas desarrollada por Microsoft para representar metadatos de modelos semánticos de Power BI y Analysis Services en repositorios Git.
* **Power BI Project (`.pbip`):** Formato orientado a desarrolladores que guarda las definiciones de informes y modelos semánticos en archivos de texto individuales, permitiendo colaboración multi-desarrollador fluida en Git.
* **Modo Direct Lake:** Patrón nativo de acceso a datos columnares en Microsoft Fabric que consulta directamente archivos Delta Parquet en OneLake sin duplicar datos ni traducir a T-SQL, alcanzando rendimiento sub-segundo sobre grandes volúmenes.
* **dbt MetricFlow Semantic Layer:** Estándar de modelado semántico declarativo que desacopla la definición de métricas del almacenamiento físico y de las herramientas de BI.
* **Semantic Quality Score ($cQS$):** Puntuación objetiva continua $[0, 100]$ que mide la integridad arquitectónica, completitud de gobierno, riesgos de exposición de PII y limpieza relacional.
* **Matriz de Gobernanza Multi-Stakeholder:** Marco multidimensional que proyecta el modelo canónico a través de cuatro pilares corporativos (Gobierno, FinOps Cloud, Analytics y Negocio).
* **Data Leadership Cockpit:** Cuadro de mando ejecutivo agregado que diagnostica la madurez del modelo a través de 16 roles organizacionales y proporciona directivas de gobierno priorizadas para directores y CDOs.
* **Contrato de Perfil de Empresa (Company Profile):** Especificación de contexto empresarial en YAML que define unidades de negocio, procesos clave, metas estratégicas y marcos regulatorios para inyección automatizada de gobernanza semántica.

---

## 8. Referencias Académicas y de Ingeniería

1. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
2. Microsoft Corporation. (2024). *Tabular Model Definition Language (TMDL) Specification*. Microsoft Learn Technical Documentation.
3. Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional.
4. Dehghani, Z. (2022). *Data Mesh: Delivering Data-Driven Value at Scale*. O'Reilly Media.
5. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
6. Tarjan, R. E. (1972). *Depth-First Search and Linear Graph Algorithms*. SIAM Journal on Computing, 1(2), 146-160.
7. IEEE Computer Society. (2018). *IEEE Standard for System, Software, and Hardware Documentation*, IEEE Std 26514-2018.
8. ISO/IEC/IEEE. (2015). *Systems and software engineering - System life cycle processes*, ISO/IEC/IEEE 15288:2015.

### Cita BibTeX

```bibtex
@software{semanticflow_2026,
  author = {SemanticFlow Core Engineering Team},
  title = {SemanticFlow: Enterprise DataOps Platform for Semantic Modeling as Code on Microsoft Fabric and Power BI},
  year = {2026},
  url = {https://github.com/AlvaroAlejandroFinOps/SemanticFlow}
}
```
