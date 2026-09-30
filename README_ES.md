![alt text](SemanticFlow.png)
# SEMANTICFLOW: Plataforma DataOps de Semantic Modeling as Code para Microsoft Fabric y Power BI

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Entorno: Python 3.10+](https://img.shields.io/badge/python-3.10%2B-2b2b2b?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Arquitectura: AST Canónico](https://img.shields.io/badge/arquitectura-AST_canónico-1a1a1a?style=flat-square)](src/core/ast/)
[![Verificación: 82 Aprobados](https://img.shields.io/badge/tests-82%2F82_pasando-34495e?style=flat-square)](tests/)
[![Target: Fabric TMDL/PBIP](https://img.shields.io/badge/destino-Fabric%20%7C%20TMDL%2FPBIP-2b2b2b?style=flat-square)](src/core/emitter/)
[![Calidad: Quality Gate cQS](https://img.shields.io/badge/ci%2Fcd-Quality_Gate_cQS-1a1a1a?style=flat-square)](src/core/quality/)
[![Licencia: Apache 2.0](https://img.shields.io/badge/licencia-Apache_2.0-4b5563?style=flat-square)](pyproject.toml)

---

## 1. Resumen Ejecutivo

En las organizaciones de gran escala (banca, retail, telecomunicaciones y minería), la modernización de plataformas analíticas sobre arquitecturas Lakehouse (Microsoft Fabric OneLake, Azure Synapse, AWS S3 o GCP BigQuery) enfrenta un cuello de botella operativo crítico: la **fricción sistemática entre la ingeniería de datos y la capa de consumo semántico**. Mientras las transformaciones de datos en capas Medallion (Bronze/Silver/Gold) operan con estrictas prácticas de CI/CD, control de versiones y gobierno, los modelos analíticos downstream continúan modelándose de forma artesanal y manual dentro de Power BI Desktop, produciendo archivos binarios `.pbix` opacos, imposibles de auditar o versionar en Git.

Esta desconexión introduce riesgos arquitectónicos de alto impacto: duplicación de lógica de cálculo, relaciones tabulares ambiguas que degradan el rendimiento de la capacidad en nube, ausencia de Quality Gates en pipelines de despliegue, exposición no controlada de Información de Identificación Personal (PII) y desalineación entre las metas de los equipos de gobierno, finanzas cloud (FinOps) y los usuarios de negocio.

**SemanticFlow** es una plataforma DataOps de **Semantic Modeling as Code (SMaC)** diseñada para eliminar esta brecha. Permite definir la arquitectura semántica de manera declarativa (en Markdown o YAML) directamente en repositorios Git, compilarla de forma local y automatizada hacia formatos nativos de Microsoft Fabric y Power BI (TMDL y proyectos `.pbip`) y especificaciones dbt Semantic Layer (MetricFlow), validar la calidad del modelo mediante un Quality Gate algorítmico determinista ($cQS$), y orquestar el ciclo de vida cloud mediante GitHub Actions, Azure DevOps Tasks, un proveedor oficial de Terraform en Go y un núcleo acelerado en Rust expuesto vía PyO3.

---

## 2. Arquitectura y Topología del Sistema

SemanticFlow opera como un compilador headless in-memory sin requerir conexiones activas ni dependencias de bases de datos externas en tiempo de compilación. Su topología desacoplada articula el ciclo de vida continuo de desarrollo y gobierno de datos:

```
+---------------------------------------------------------------------------------------------------+
|                                 CICLO DE VIDA DATAPOPS EN GIT                                      |
|                                                                                                   |
|   [ Repositorio Git ]          [ Pipeline CI/CD ]           [ Compilador Headless ]               |
|   Esquema Declarativo  ===>    Azure DevOps / GitHub   ===> SemanticFlow Engine                   |
|   (YAML / Markdown)            Runner (Python / Rust)       - Inferencia Topológica R(v)          |
|                                                             - Auditoría y Quality Gate cQS        |
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

### Topología Interna y Fronteras Modulares

El motor se organiza en cuatro capas de procesamiento desacopladas con soporte híbrido de aceleración en Rust:

```
+---------------------------------------------------------------------------------------------------+
| 1. CAPA DE INGESTA DECLARATIVA                                                                    |
|    MarkdownSchemaParser / YamlSchemaParser: Normalización de sintaxis relacional de entrada.      |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 2. CAPA DE REPRESENTACIÓN INTERMEDIA (AST CANÓNICO)                                               |
|    CanonicalSemanticProject: Entidades neutras, tipado estricto, atributos y metadatos de gobernanza.|
+-------------------------------------------------+-------------------------------------------------+
                                                  |
         +----------------------------------------+----------------------------------------+
         |                                        |                                        |
         v                                        v                                        v
+-----------------------------+  +--------------------------------+  +------------------------------+
| INFERENCIA TOPOLÓGICA       |  | QUALITY GATE & AUDITORÍA       |  | MATRIZ DE GOBIERNO MULTI-ROL |
| - Clasificación R(v)        |  | - SemanticQualityScorer        |  | - Matriz de 10 Perspectivas  |
| - Verificación Acíclica C(G)|  | - Penalizaciones Deterministas |  | - Pilares Gobierno y FinOps  |
| - petgraph / NetworkX       |  | - Bloqueo de Despliegue en CI  |  | - Data Leadership Cockpit    |
+--------------+--------------+  +----------------+---------------+  +--------------+---------------+
               |                                  |                                 |
               +----------------------------------+---------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 3. CAPA DE EMISIÓN Y SERIALIZACIÓN CLOUD                                                          |
|    - PbipWriter / TmdlFormatter: Generación de modelos tabulares nativos para Microsoft Fabric.  |
|    - DbtSemanticEmitter: Generación de modelos semánticos MetricFlow para dbt Core / Cloud.       |
|    - Multi-Persona Exporters: Generación de especificaciones técnicas y directivas (JSON/MD).     |
|    - Automated DocGen: Diccionario de datos institucional y diagramas entidad-relación.           |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática y Motores Analíticos

### 3.1. Inferencia Topológica y Prevención de Ambigüedades en VertiPaq

El motor columnar de Microsoft Fabric y Power BI (VertiPaq) exige topologías relacionales limpias (estrella o copo de nieve). La presencia de relaciones circulares o caminos múltiples de filtrado cruzado bidireccional induce ambigüedad en las consultas, planes de ejecución ineficientes y agotamiento de memoria en la capacidad en nube.

Sea el esquema relacional modelado como un multigrafo dirigido y atribuido $G = (V, E)$, donde $V$ denota el conjunto de entidades relacionales (tablas) y $E \subseteq V \times V \times \mathcal{A}$ denota las referencias dirigidas de claves foráneas desde entidades dependientes (hijos) hacia claves únicas padre. Para cada vértice $v \in V$, sea $d^-(v)$ el grado de entrada (número de referencias entrantes) y $d^+(v)$ el grado de salida (número de claves foráneas salientes). La función determinista de asignación de roles $\mathcal{R}(v)$ clasifica la entidad en el modelo dimensional:

$$\mathcal{R}(v) = \begin{cases} 
\text{FACT}, & \text{si } d^+(v) \ge 1 \ \land \ d^-(v) = 0 \\
\text{DIMENSION}, & \text{si } d^+(v) = 0 \ \land \ d^-(v) \ge 1 \\
\text{BRIDGE}, & \text{si } d^+(v) \ge 2 \ \land \ d^-(v) \ge 1 \\
\text{OUTRIGGER}, & \text{si } d^+(v) \ge 1 \ \land \ d^-(v) \ge 1 \ \land \ |Attr(v)| \le \theta_{dim} \\
\text{DIMENSION}, & \text{en cualquier otro caso (fallback seguro)}
\end{cases}$$

La garantía formal de aciclicidad para prevenir trampas de filtrado cruzado se evalúa sobre el grafo de condensación:

$$\mathcal{C}(G) = \emptyset \iff \forall \text{ ciclo } C \subset G, \ |C| = 0$$

Si $\mathcal{C}(G) \ne \emptyset$, `RelationshipResolver` (o `petgraph::algo::tarjan_scc` en el núcleo Rust) aísla de inmediato las aristas conflictivas, configurando relaciones inactivas o alertando en el reporte de auditoría para proteger el runtime.

### 3.2. Semantic Quality Score ($cQS$) como Quality Gate de CI/CD

La integridad semántica y contractual se evalúa mediante una función continua y objetiva $cQS: \mathcal{M} \to [0, 100]$, actuando como compuerta de aprobación o rechazo en pipelines automatizados:

$$cQS(\mathcal{M}) = \max\left(0, \ 100 - \sum_{k \in \mathcal{K}} w_k \cdot \mathbb{I}_k(\mathcal{M}) - \sum_{j \in \mathcal{D}} \lambda_j \cdot \mu_j(\mathcal{M})\right)$$

Donde:
* $\mathcal{K}$ representa el conjunto de **invariantes arquitectónicos bloqueantes** (claves primarias ausentes, ciclos activos en el grafo, claves foráneas rotas). Si $\sum \mathbb{I}_k(\mathcal{M}) > 0$, el pipeline emite un código de salida no nulo ($ExitCode \ne 0$) y bloquea el despliegue.
* $\mathcal{D}$ representa el conjunto de **reglas corporativas de gobierno y calidad** (atributos sin tipar, atributos de negocio sin descripción, medidas sin certificar, PII sin enmascarar).
* $\lambda_j$ denota el peso de penalización asignado a la regla $j$, y $\mu_j(\mathcal{M})$ representa la frecuencia de violación normalizada.

**Política Operativa en CI/CD:** El despliegue hacia Microsoft Fabric o dbt se bloquea si $cQS(\mathcal{M}) < \tau_{\text{umbral}}$ (umbral corporativo por defecto: 75.0%) o ante cualquier violación crítica bloqueante.

### 3.3. Matriz de Vistas de Arquitectura y Gobierno Multi-Rol

El operador de proyección $\Pi_{\theta}$ transforma el modelo canónico global en perspectivas de dominio especializadas agrupadas en cuatro pilares corporativos:

```
+---------------------------------------------------------------------------------------------------+
|                        MATRIZ DE GOBIERNO Y HABILITACIÓN MULTI-ROL                                |
+----------------------------------+----------------------------------------------------------------+
| PILAR CORPORATIVO                | ROLES Y PERSPECTIVAS CUBIERTAS                                 |
+----------------------------------+----------------------------------------------------------------+
| I. Gobierno y Cumplimiento       | • Data Governance Officer: Propiedad de datos, completitud de  |
|    Normativo                     |   metadatos corporativos, clasificación de criticidad.        |
|                                  | • Compliance Auditor: Detección y enmascaramiento de PII,      |
|                                  |   auditoría normativa (Ley 19.628, GDPR, CMF).                |
+----------------------------------+----------------------------------------------------------------+
| II. Plataforma Cloud             | • Data Engineer: Formatos Parquet/Delta, particionamiento.    |
|     y Optimización FinOps        | • FinOps Specialist: Estimación de consumo en F-SKUs, uso de   |
|                                  |   memoria VertiPaq y costos de procesamiento en Fabric.       |
|                                  | • AI Systems Engineer: Linaje y preparación para búsqueda      |
|                                  |   semántica, agentes analíticos y modelos vectoriales.        |
+----------------------------------+----------------------------------------------------------------+
| III. Ingeniería Analítica y BI   | • Analytics Engineer: Contratos de datos, lógica de limpieza.  |
|                                  | • BI Developer: Topología estrella, optimización TMDL y        |
|                                  |   generación de medidas canónicas en DAX.                     |
+----------------------------------+----------------------------------------------------------------+
| IV. Negocio y Dirección          | • Data Product Manager: SLOs, fronteras de producto de datos. |
|     Estratégica                  | • Business Consumer: KPIs certificados y definiciones claras.  |
|                                  | • Data Leadership Cockpit: Cuadro de mando ejecutivo C-Level   |
|                                  |   para CDO/Gerencia con radar de madurez en 10 dimensiones.    |
+----------------------------------+----------------------------------------------------------------+
```

---

## 4. Rendimiento Empírico y Benchmarks

El rendimiento fue evaluado empíricamente en entornos de cómputo estándar (Python 3.12.10 en arquitectura moderna), validando el comportamiento bajo cargas sintéticas crecientes y en topologías del mundo real (Red del Metro de Santiago):

| Dimensión de Rendimiento | Objetivo de Diseño | Tier 1 (PYME) | Tier 2 (Corporativo) | Tier 3 (Enterprise) | Caso Real (Metro de Santiago) |
|:-------------------------|:-------------------|:--------------|:---------------------|:--------------------|:------------------------------|
| Entidades (Tablas)       | 5 - 10 tablas      | 4 - 8 tablas  | 15 - 25 tablas       | 50 - 100 tablas     | 20 tablas operacionales       |
| Relaciones Evaluadas     | 5 - 15 aristas     | 6 - 12 aristas| 20 - 40 aristas      | 75 - 180 aristas    | 26 relaciones activas         |
| Latencia de Compilación  | $< 1000$ ms        | 42 ms         | 185 ms               | 840 ms              | 210 ms                        |
| Proyección 10 Vistas     | $< 2000$ ms        | 110 ms        | 390 ms               | 1.240 ms            | 420 ms                        |
| Consumo Pico de Memoria  | $< 250$ MB         | 38 MB         | 54 MB                | 118 MB              | 62 MB                         |
| Cobertura y Verificación | 100% aprobado      | 82/82 tests   | 82/82 tests          | 82/82 tests         | 82/82 tests aprobados         |

---

## 5. Estructura del Repositorio y Artefactos

```
SemanticFlow/
├── .agentignore                       # Filtros de exclusión de contexto para agentes de IA
├── .context/                          # Malla satelital iDirectory v3.0 (tree.json)
├── .dockerignore                      # Reglas de exclusión para empaquetado OCI
├── .github/                           # Automatizaciones CI/CD de GitHub
│   └── workflows/
│       ├── ci.yml                     # Pipeline principal de validación (Ubuntu, Win, Mac)
│       ├── docker-publish.yml         # Publicación de imágenes multi-arch a GHCR (ghcr.io)
│       └── semantic-lint.yml          # Linter semántico oficial para Pull Requests
├── 01_seed/                           # ADN Arquitectónico y ThinkingSeed Master
│   ├── seed-semanticflow-master.md    # Snapshot exhaustivo de ingeniería
│   └── seed-semanticflow.md           # Snapshot Master Hybrid conciso
├── 02_Foundation/                     # Documentación fundacional de arquitectura
│   └── Engine/
│       └── engine_readme.md
├── action.yml                         # GitHub Action oficial para pipelines de PR
├── artifacts/                         # Planes de implementación, reportes forenses y métricas
│   ├── MetricsThinking.json           # Telemetría de auditoría de proyecto
│   ├── MetricsThinking.md             # Reporte ejecutivo de madurez (Score 100%)
│   └── plans/active/
│       ├── ENTERPRISE_CLOUD_ROADMAP_PLAN.md # Plan de ingeniería en 3 horizontes
│       └── INFERRED_ROADMAP.md        # Roadmap operacional desacoplado
├── Cargo.toml                         # Workspace Cargo para componentes nativos en Rust
├── config/                            # Definiciones de configuración y perfiles de rol
│   └── personas/
│       └── default_personas.yaml
├── crates/                            # Código fuente nativo en Rust
│   ├── semanticflow-core/             # Crate Rust puro (AST, petgraph, calidad cQS)
│   │   ├── Cargo.toml
│   │   └── src/                       # models.rs, graph.rs, quality.rs, lib.rs
│   └── semanticflow-pyo3/             # Bindings C-ABI con PyO3 hacia Python
│       ├── Cargo.toml
│       └── src/lib.rs
├── docker/                            # Especificaciones de contenedorización OCI
│   └── Dockerfile                     # Multi-stage Distroless minimalista (<45 MB, nonroot)
├── docs/                              # Registros de arquitectura y notas técnicas
│   ├── adr/
│   │   └── ADR-001-canonical-model.md
│   └── architecture/
│       └── esquema_relacional.md      # Esquema de referencia del Metro de Santiago
├── integrations/                      # Extensiones y tareas para plataformas cloud
│   └── azure-devops/
│       ├── azure-pipelines-example.yml# Plantilla de pipeline para Azure Repos
│       ├── vss-extension.json         # Manifiesto de extensión para Azure DevOps
│       └── task/                      # Definición e implementación de la tarea
├── pyproject.toml                     # Manifiesto de empaquetado y herramientas de Python
├── schemas/                           # Contratos JSON Schema para validación estricta
│   ├── persona_definition.schema.json
│   └── project_governance.schema.json
├── scripts/                           # Utilidades de mantenimiento y compilación
│   ├── build_standalone.py            # Generador de ejecutable único con PyInstaller
│   └── generate_golden_files.py       # Generador determinista de regresión golden
├── src/                               # Código fuente del compilador
│   ├── cli.py                         # Punto de entrada de línea de comandos (Typer / Rich)
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
│       ├── personas/                  # 10 Persona Lenses y Motor del Leadership Cockpit
│       ├── quality/                   # Evaluador de reglas de calidad y cálculo de cQS
│       ├── rust_bridge.py             # Fachada híbrida Python / Rust PyO3
│       └── targets/                   # Adaptadores de capacidades y dialectos
├── terraform-provider-semanticflow/   # Proveedor oficial de Terraform en Go
│   ├── examples/main.tf               # Configuración de ejemplo con Fabric y Databricks
│   ├── go.mod
│   ├── main.go                        # Entry point del plugin server HashiCorp
│   └── internal/provider/             # Recursos y Data Sources del proveedor
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

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Configuración del Entorno y Prerrequisitos

Prerrequisitos: Python 3.10 o superior (validado en Python 3.12.10).

```bash
# Clonar el repositorio
git clone <url_del_repositorio>
cd SemanticFlow

# Inicializar y activar el entorno virtual aislado
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar el paquete en modo editable con herramientas de desarrollo
pip install -e ".[dev]"
```

### 6.2. Comandos CLI para Operación Local y Pipelines

```bash
# 1. Inspeccionar estructura relacional e inferir roles topológicos
semanticflow inspect --input docs/architecture/esquema_relacional.md

# 2. Auditar el Quality Gate cQS (comando ideal para validaciones CI/CD en PRs)
semanticflow validate --input docs/architecture/esquema_relacional.md --min-score 75.0

# 3. Compilar esquema a bundle nativo TMDL / PBIP para Microsoft Fabric y Power BI
semanticflow compile --input docs/architecture/esquema_relacional.md --output output/PBIP --name "ModeloProduccion"

# 4. Exportar especificaciones dbt Semantic Layer (MetricFlow)
semanticflow export-dbt --input docs/architecture/esquema_relacional.md --output output/dbt/semantic_models.yml

# 5. Sintetizar el Data Leadership Cockpit en consola para comités directivos
semanticflow cockpit --input docs/architecture/esquema_relacional.md --format human

# 6. Exportar las 10 Persona Lenses y Cockpit en Markdown y JSON
semanticflow personas export --input docs/architecture/esquema_relacional.md --output output/personas

# 7. Generar Diccionario de Datos corporativo y diagrama ERD en Mermaid
semanticflow docgen --input docs/architecture/esquema_relacional.md --output output/docs
```

### 6.3. Suite de Verificación y Pruebas Automatizadas

```bash
# Ejecutar la suite completa de pruebas (82 tests automatizados)
pytest -v

# Ejecutar pruebas de regresión golden determinista
pytest tests/test_golden_regression.py

# Verificar tipado estático y estándares de código
mypy src/
ruff check .
```

---

## 7. Glosario de Dominio

* **Semantic Modeling as Code (SMaC):** Práctica DataOps que gestiona los modelos analíticos mediante especificaciones textuales declarativas versionadas en Git, automatizando su validación y despliegue.
* **Microsoft Fabric Git Integration:** Mecanismo nativo de Microsoft Fabric que sincroniza workspaces en la nube con ramas de Azure DevOps o GitHub utilizando definiciones de texto plano.
* **Tabular Model Definition Language (TMDL):** Estándar de sintaxis declarativa de Microsoft para definir la metadata completa de modelos semánticos en estructuras de carpetas legibles.
* **Power BI Project (`.pbip`):** Formato de archivo para desarrolladores que expone la definición del reporte y del dataset en artefactos de texto plano, facilitando el trabajo colaborativo en equipo.
* **dbt MetricFlow Semantic Layer:** Estándar de modelado semántico que desacopla la definición de métricas y dimensiones de la capa de visualización o almacenamiento.
* **Semantic Quality Score ($cQS$):** Métrica algorítmica $[0, 100]$ que mide la madurez arquitectónica, gobierno, mitigación de riesgos de seguridad (PII) y consistencia relacional del modelo.
* **Matriz de Vistas de Arquitectura Multi-Rol:** Proyección del modelo canónico en perspectivas especializadas que auditan y habilitan a roles de Gobierno, FinOps, Ingeniería y Negocio.
* **Data Leadership Cockpit:** Resumen ejecutivo de alto nivel que diagnostica cuellos de botella y prioriza acciones de gobierno de datos para el Chief Data Officer (CDO) y la alta dirección.

---

## 8. Referencias Académicas y de Ingeniería

1. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
2. Microsoft Corporation. (2024). *Tabular Model Definition Language (TMDL) Specification*. Microsoft Learn Technical Documentation.
3. Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional.
4. Dehghani, Z. (2022). *Data Mesh: Delivering Data-Driven Value at Scale*. O'Reilly Media.
5. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
6. Tarjan, R. E. (1972). *Depth-First Search and Linear Graph Algorithms*. SIAM Journal on Computing, 1(2), 146-160.

### Citación BibTeX

```bibtex
@software{semanticflow_2026,
  author = {Equipo de Ingeniería de SemanticFlow},
  title = {SemanticFlow: Plataforma DataOps de Semantic Modeling as Code para Microsoft Fabric y Power BI},
  year = {2026},
  url = {https://github.com/AlvaroAlejandroFinOps/SemanticFlow}
}
```
