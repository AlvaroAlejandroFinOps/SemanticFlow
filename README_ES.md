![alt text](SemanticFlow.png)
# SEMANTICFLOW: Plataforma DataOps de Semantic Modeling as Code para Microsoft Fabric y Power BI

**Idioma:** [English](README.md) | [Español](README_ES.md)

[![Entorno: Python 3.10+](https://img.shields.io/badge/python-3.10%2B-2b2b2b?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Arquitectura: AST Canónico](https://img.shields.io/badge/arquitectura-AST_canónico-1a1a1a?style=flat-square)](src/core/ast/)
[![Verificación: 71 Aprobados](https://img.shields.io/badge/tests-71%2F71_pasando-34495e?style=flat-square)](tests/)
[![Target: Fabric TMDL/PBIP](https://img.shields.io/badge/destino-Fabric%20%7C%20TMDL%2FPBIP-2b2b2b?style=flat-square)](src/core/emitter/)
[![Calidad: Quality Gate cQS](https://img.shields.io/badge/ci%2Fcd-Quality_Gate_cQS-1a1a1a?style=flat-square)](src/core/quality/)
[![Licencia: Apache 2.0](https://img.shields.io/badge/licencia-Apache_2.0-4b5563?style=flat-square)](pyproject.toml)

---

## 1. Resumen Ejecutivo y Posicionamiento Corporativo

En las organizaciones de gran escala (banca, retail, telecomunicaciones y minería), la modernización de plataformas analíticas sobre arquitecturas Lakehouse (Microsoft Fabric OneLake, Azure Synapse, AWS S3 o GCP BigQuery) enfrenta un cuello de botella crítico: la **fricción operativa entre la capa de ingeniería de datos y la capa de consumo semántico**. Mientras las transformaciones de datos en capas Medallion (Bronze/Silver/Gold) operan con estrictas prácticas de CI/CD, control de versiones y gobierno, los modelos analíticos downstream continúan modelándose de forma artesanal y manual dentro de Power BI Desktop, produciendo archivos binarios `.pbix` opacos, imposibles de auditar o versionar en Git.

Esta desconexión introduce riesgos sistémicos de negocio: duplicación de lógica de cálculo, relaciones tabulares ambiguas que degradan el rendimiento de la capacidad en nube, ausencia de Quality Gates en pipelines de despliegue, exposición no controlada de Información de Identificación Personal (PII) y desalineación entre las metas de los equipos de gobierno, finanzas cloud (FinOps) y los usuarios de negocio.

**SemanticFlow** es una plataforma DataOps de **Semantic Modeling as Code (SMaC)** diseñada para eliminar esta brecha. Permite definir la arquitectura semántica de manera declarativa (en Markdown o YAML) directamente en repositorios Git, compilarla de forma local y automatizada hacia formatos nativos de Microsoft Fabric y Power BI (TMDL y proyectos `.pbip`), validar la calidad del modelo mediante un Quality Gate algorítmico determinista ($cQS$) y proyectar el impacto arquitectónico a través de una Matriz de Gobierno Multi-Rol orientada a comités técnicos y directivos C-Level.

---

## 2. Arquitectura de Extremo a Extremo y Flujo DataOps

SemanticFlow se integra en el ciclo de vida continuo de ingeniería de datos en la nube. Opera como un compilador headless in-memory sin requerir conexiones activas ni dependencias de bases de datos externas en tiempo de compilación.

```
+---------------------------------------------------------------------------------------------------+
|                                 CICLO DE VIDA DATAPOPS EN GIT                                      |
|                                                                                                   |
|   [ Repositorio Git ]          [ Pipeline CI/CD ]           [ Compilador Headless ]               |
|   Esquema Declarativo  ===>    Azure DevOps / GitHub   ===> SemanticFlow Engine                   |
|   (YAML / Markdown)            Runner (Python 3.10+)        - Inferencia Topológica R(v)          |
|                                                             - Auditoría y Quality Gate cQS        |
+------------------------------------------+--------------------------------------------------------+
                                           |
                    +----------------------+----------------------+
                    | (Pasa Quality Gate)                         | (Falla cQS < Umbral)
                    v                                             v
+------------------------------------------+    +---------------------------------------------------+
|     COMPILACIÓN Y SERIALIZACIÓN          |    |               PIPELINE BLOQUEADO                  |
|                                          |    |  Build rechazado en Pull Request.                 |
|  - Tabular Model Def. Lang. (TMDL)       |    |  Reporte de infracciones de gobernanza,           |
|  - Power BI Project Developer (.pbip)    |    |  ciclos topológicos o PII expuesta.               |
|  - Diccionario Corporativo y ERD Mermaid |    +---------------------------------------------------+
+-------------------+----------------------+
                    |
                    v
+---------------------------------------------------------------------------------------------------+
|                           DESPLIEGUE EN MICROSOFT FABRIC / POWER BI                               |
|                                                                                                   |
|   Microsoft Fabric Workspace <==== Sincronización Automática vía Git Integration / Fabric REST    |
|   - Semantic Model Versionado en OneLake                                                          |
|   - Modelos Estrella y Copo de Nieve Validados para Motor VertiPaq                                |
|   - Vistas Multi-Rol y Data Leadership Cockpit para CDO y Gerencias de Datos                      |
+---------------------------------------------------------------------------------------------------+
```

### Topología Interna del Motor

El compilador procesa el flujo en cuatro capas modulares y desacopladas:

```
+---------------------------------------------------------------------------------------------------+
| 1. CAPA DE INGESTA DECLARATIVA                                                                    |
|    MarkdownSchemaParser / YamlSchemaParser: Normalización de sintaxis relacional de entrada.      |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 2. CAPA DE REPRESENTACIÓN INTERMEDIA (AST CANÓNICO)                                               |
|    CanonicalProject: Entidades neutras, tipado estricto, atributos y metadatos de gobernanza.    |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
         +----------------------------------------+----------------------------------------+
         |                                        |                                        |
         v                                        v                                        v
+-----------------------------+  +--------------------------------+  +------------------------------+
| INFERENCIA TOPOLÓGICA       |  | QUALITY GATE & AUDITORÍA       |  | MATRIZ DE GOBIERNO MULTI-ROL |
| - Clasificación R(v)        |  | - SemanticQualityScorer        |  | - Matriz de 10 Perspectivas  |
| - Verificación Acíclica C(G)|  | - Penalizaciones Deterministas |  | - Pilares Gobierno y FinOps  |
| - Síntesis DAX Canónica     |  | - Bloqueo de Despliegue en CI  |  | - Data Leadership Cockpit    |
+--------------+--------------+  +----------------+---------------+  +--------------+---------------+
               |                                  |                                 |
               +----------------------------------+---------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 3. CAPA DE EMISIÓN Y SERIALIZACIÓN CLOUD                                                          |
|    - PbipWriter / TmdlFormatter: Generación de modelos tabulares nativos para Fabric.             |
|    - Multi-Persona Exporters: Generación de especificaciones técnicas y directivas (JSON/MD).     |
|    - Automated DocGen: Diccionario de datos institucional y diagramas entidad-relación.           |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Motores de Inferencia y Notación Aplicada a Producción

SemanticFlow incorpora formalización matemática rigurosa pero estrictamente aplicada a resolver problemas concretos de estabilidad, desempeño y gobernanza en producción.

### 3.1. Inferencia Topológica y Prevención de Ambigüedades en VertiPaq

El motor columnar de Microsoft Fabric y Power BI (VertiPaq) requiere topologías limpias (estrella o copo de nieve). La presencia de relaciones circulares o caminos múltiples de filtrado cruzado bidireccional genera trampas de ambigüedad, consultas lentas y agotamiento de memoria en la capacidad contratada.

El esquema relacional se modela como un grafo dirigido $G = (V, E)$, donde $V$ son las tablas y $E$ las restricciones de clave foránea dirigidas desde tablas dependientes hacia tablas de referencia. Para cada tabla $v \in V$, $d^-(v)$ representa el grado de entrada (referenciada como dimensión) y $d^+(v)$ el grado de salida (referencia a otras entidades). La función determinista $\mathcal{R}(v)$ clasifica la entidad en el modelo semántico:

$$\mathcal{R}(v) = \begin{cases} 
\text{FACT}, & \text{si } d^+(v) \ge 1 \ \land \ d^-(v) = 0 \\
\text{DIMENSION}, & \text{si } d^+(v) = 0 \ \land \ d^-(v) \ge 1 \\
\text{BRIDGE}, & \text{si } d^+(v) \ge 2 \ \land \ d^-(v) \ge 1 \\
\text{OUTRIGGER}, & \text{si } d^+(v) \ge 1 \ \land \ d^-(v) \ge 1 \ \land \ |Attr(v)| \le \theta_{dim} \\
\text{DIMENSION}, & \text{en cualquier otro caso (fallback seguro)}
\end{cases}$$

La garantía de ausencia de trampas relacionales y dependencias cíclicas se evalúa formalmente sobre el grafo de condensación:

$$\mathcal{C}(G) = \emptyset \iff \forall \text{ ciclo } C \subset G, \ |C| = 0$$

Si $\mathcal{C}(G) \ne \emptyset$, el componente `RelationshipResolver` aísla de inmediato las aristas conflictivas, configurando relaciones inactivas o alertando en el reporte de auditoría para salvaguardar el rendimiento en runtime.

### 3.2. Semantic Quality Score ($cQS$) como Quality Gate de CI/CD

El índice $cQS: \mathcal{M} \to [0, 100]$ no es una métrica teórica: actúa como la condición de aprobación o rechazo en los pipelines de integración continua (Azure Pipelines, GitHub Actions o GitLab CI).

$$cQS(\mathcal{M}) = \max\left(0, \ 100 - \sum_{k \in \mathcal{K}} w_k \cdot \mathbb{I}_k(\mathcal{M}) - \sum_{j \in \mathcal{D}} \lambda_j \cdot \mu_j(\mathcal{M})\right)$$

Donde:
* $\mathcal{K}$ representa **invariantes bloqueantes de arquitectura** (claves primarias ausentes, ciclos activos en el grafo relacional, claves foráneas rotas). Si $\sum \mathbb{I}_k(\mathcal{M}) > 0$, el pipeline falla automáticamente ($ExitCode \ne 0$).
* $\mathcal{D}$ representa **reglas corporativas de gobierno y calidad** (campos sin tipar, atributos de negocio sin descripción, medidas sin certificar, atributos sensibles con PII no enmascarados).
* $\lambda_j$ corresponde a la severidad de la penalización y $\mu_j(\mathcal{M})$ a la frecuencia observada de la violación.

**Criterio Operativo en CI/CD:** El despliegue a Fabric / Power BI se bloquea si $cQS(\mathcal{M}) < \tau_{\text{umbral}}$ (umbral configurable, por defecto 75.0%) o si se detecta cualquier infracción de severidad crítica.

---

## 4. Matriz de Vistas de Arquitectura y Gobierno Multi-Rol

SemanticFlow trasciende la visión puramente técnica al proyectar el modelo canónico en cuatro pilares corporativos que responden a las necesidades de cada stakeholder de la organización:

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

## 5. Rendimiento Empírico y Benchmarks Corporativos

El motor fue evaluado en entornos de cómputo estándar (Python 3.12.10 en arquitectura moderna), validando su comportamiento tanto en escenarios de estrés sintético de gran volumen como en modelos reales de alta complejidad operacional:

| Dimensión de Rendimiento | Objetivo de Diseño | Tier 1 (PYME) | Tier 2 (Corporativo) | Tier 3 (Enterprise) | Caso Real (Metro de Santiago) |
|:-------------------------|:-------------------|:--------------|:---------------------|:--------------------|:------------------------------|
| Entidades (Tablas)       | 5 - 10 tablas      | 4 - 8 tablas  | 15 - 25 tablas       | 50 - 100 tablas     | 20 tablas operacionales       |
| Relaciones Evaluadas     | 5 - 15 aristas     | 6 - 12 aristas| 20 - 40 aristas      | 75 - 180 aristas    | 26 relaciones activas         |
| Latencia de Compilación  | $< 1000$ ms        | 42 ms         | 185 ms               | 840 ms              | 210 ms                        |
| Proyección 10 Vistas     | $< 2000$ ms        | 110 ms        | 390 ms               | 1.240 ms            | 420 ms                        |
| Consumo Pico de Memoria  | $< 250$ MB         | 38 MB         | 54 MB                | 118 MB              | 62 MB                         |
| Cobertura y Verificación | 100% aprobado      | 71/71 tests   | 71/71 tests          | 71/71 tests         | 71/71 tests aprobados         |

---

## 6. Estructura del Repositorio y Componentes

```
SemanticFlow/
├── .agentignore                       # Filtros de contexto para agentes de desarrollo
├── .context/                          # Malla de gobierno contextual iDirectory v3.0 (tree.json)
├── 01_seed/                           # Especificación técnica maestra y ADN del proyecto
│   ├── seed-semanticflow-master.md
│   └── seed-semanticflow.md
├── 02_Foundation/                     # Documentación fundacional de arquitectura
│   └── Engine/
│       └── engine_readme.md
├── config/                            # Definiciones de configuración y perfiles
│   └── personas/
│       └── default_personas.yaml
├── docs/                              # Registros de arquitectura y notas técnicas
│   ├── adr/                           # Registros de Decisiones de Arquitectura (ADR-001+)
│   │   └── ADR-001-canonical-model.md
│   └── architecture/
│       ├── esquema_relacional.md      # Esquema relacional de referencia
│       └── adr/
├── pyproject.toml                     # Manifiesto de empaquetado, dependencias y herramientas
├── schemas/                           # Contratos JSON Schema para validación estricta
│   ├── persona_definition.schema.json
│   └── project_governance.schema.json
├── scripts/                           # Automatizaciones y generadores de regresión
│   └── generate_golden_files.py
├── src/                               # Código fuente del compilador
│   ├── cli.py                         # Interfaz de línea de comandos (Typer / Rich)
│   └── core/
│       ├── ast/                       # Modelos del Árbol de Sintaxis Abstracta Canónico
│       ├── capabilities/              # Orquestador de capacidades de compilación
│       ├── docs/                      # Generador de Diccionario y Diagramas Mermaid
│       ├── emitter/                   # Serializadores nativos TMDL y proyectos PBIP
│       ├── engine/                    # Inferencia topológica, resolución de aristas y DAX
│       ├── mappers/                   # Mapeadores de esquemas brutos a modelo canónico
│       ├── parsers/                   # Parsers declarativos para Markdown y YAML
│       ├── personas/                  # Matriz de Gobierno Multi-Rol y Leadership Cockpit
│       ├── quality/                   # Evaluador de reglas de calidad y cálculo de cQS
│       └── targets/                   # Dialectos y adaptadores específicos de plataforma
└── tests/                             # Suite integral de pruebas automatizadas
    ├── test_all_lenses_deep.py        # Validación profunda de perspectivas
    ├── test_canonical_model.py        # Pruebas unitarias de modelos canónicos
    ├── test_cli.py                    # Pruebas de la interfaz de comandos
    ├── test_cli_personas.py           # Pruebas de exportación de roles
    ├── test_golden_regression.py      # Pruebas de regresión determinista golden
    ├── test_inference_engine.py       # Pruebas del motor de inferencia topológica
    ├── test_leadership_cockpit.py     # Pruebas del cuadro de mando para directivos
    ├── test_persona_contracts.py      # Validación de contratos de gobierno
    ├── test_stage3_governance_quality.py
    ├── fixtures/                      # Esquemas y datos de prueba empresariales
    ├── golden/                        # Modelos esperados para pruebas de regresión
    └── Massive Stress Test/           # Suites de prueba de volumen y estrés
```

---

## 7. Protocolo de Operación y Automatización CI/CD

### 7.1. Requisitos de Entorno e Instalación

El compilador requiere **Python 3.10 o superior** y se instala como un paquete local reproducible:

```bash
# Clonar repositorio
git clone <url_del_repositorio>
cd SemanticFlow

# Inicializar y activar entorno virtual aislado
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalación en modo editable con herramientas de desarrollo
pip install -e ".[dev]"
```

### 7.2. Comandos CLI para Pipelines y Operación Local

```bash
# 1. Inspeccionar estructura relacional e inferir roles topológicos
semanticflow inspect --input docs/architecture/esquema_relacional.md

# 2. Validar Quality Gate cQS (comando ideal para tareas automáticas de CI/CD)
semanticflow validate --input docs/architecture/esquema_relacional.md --min-score 75.0

# 3. Compilar esquema a bundle nativo TMDL / PBIP para Microsoft Fabric y Power BI
semanticflow compile --input docs/architecture/esquema_relacional.md --output output/PBIP --name "ModeloComercial"

# 4. Sintetizar el Data Leadership Cockpit en consola para comités directivos
semanticflow cockpit --input docs/architecture/esquema_relacional.md --format human

# 5. Exportar la Matriz de Vistas Multi-Rol y Cockpit en Markdown y JSON
semanticflow personas export --input docs/architecture/esquema_relacional.md --output output/personas

# 6. Generar Diccionario de Datos corporativo y diagrama ERD en Mermaid
semanticflow docgen --input docs/architecture/esquema_relacional.md --output output/docs
```

### 7.3. Suite de Aseguramiento de Calidad y Pruebas

```bash
# Ejecución de la suite completa de pruebas (71 tests automatizados)
pytest -v

# Verificación de invariantes deterministas mediante Golden Regression
pytest tests/test_golden_regression.py

# Verificación de calidad de código y análisis de tipos estáticos
ruff check .
mypy src/
```

---

## 8. Glosario de Dominio Corporativo

* **Semantic Modeling as Code (SMaC):** Práctica DataOps que gestiona los modelos analíticos mediante especificaciones textuales declarativas versionadas en Git, automatizando su validación y despliegue.
* **Microsoft Fabric Git Integration:** Mecanismo nativo de Microsoft Fabric que sincroniza workspaces en la nube con ramas de Azure DevOps o GitHub utilizando definiciones de texto plano.
* **Tabular Model Definition Language (TMDL):** Estándar de sintaxis declarativa de Microsoft para definir la metadata completa de modelos semánticos en estructuras de carpetas legibles.
* **Power BI Project (`.pbip`):** Formato de archivo para desarrolladores que expone la definición del reporte y del dataset en artefactos de texto plano, facilitando el trabajo colaborativo en equipo.
* **Semantic Quality Score ($cQS$):** Métrica algorítmica $[0, 100]$ que mide la madurez arquitectónica, gobierno, mitigación de riesgos de seguridad (PII) y consistencia relacional del modelo.
* **Matriz de Vistas de Arquitectura Multi-Rol:** Proyección del modelo canónico en perspectivas especializadas que auditan y habilitan a roles de Gobierno, FinOps, Ingeniería y Negocio.
* **Data Leadership Cockpit:** Resumen ejecutivo de alto nivel que diagnostica cuellos de botella y prioriza acciones de gobierno de datos para el Chief Data Officer (CDO) y la alta dirección.

---

## 9. Licencia y Soporte

SemanticFlow se distribuye bajo la licencia de código abierto **Apache 2.0**. Para más información sobre directrices de contribución y arquitectura de extensiones, consulte [CONTRIBUTING.md](CONTRIBUTING.md) y [docs/](docs/).
