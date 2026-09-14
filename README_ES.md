# SemanticFlow: Compilador Declarativo de Modelos Semánticos y Plataforma Enterprise de Proyección Analítica

**Idioma:** [English](README.md) | [Español](README_ES.md)

![Python](https://img.shields.io/badge/python-3.10%2B-1a1a1a?style=flat-square)
![Arquitectura](https://img.shields.io/badge/arquitectura-compiler--pipeline-2b2b2b?style=flat-square)
![Verificación](https://img.shields.io/badge/pruebas-71%2F71%20aprobadas-34495e?style=flat-square)
![Objetivo](https://img.shields.io/badge/objetivo-Power%20BI%20TMDL%20%7C%20PBIP-4b5563?style=flat-square)
![Licencia](https://img.shields.io/badge/licencia-Apache--2.0-1a1a1a?style=flat-square)

---

## 1. Resumen Ejecutivo

Las arquitecturas de datos empresariales modernas enfrentan una grieta de gobernanza crítica: la brecha semántica entre los esquemas de almacenamiento crudos, las transformaciones analíticas y los modelos de consumo de negocio. Cuando las definiciones semánticas se mantienen de forma ad-hoc en tableros de Business Intelligence (BI) y motores analíticos fragmentados, la lógica de dominio degenera en deuda técnica inalcanzable de auditar y mantener. SemanticFlow aborda este desafío arquitectónico mediante la introducción de un compilador semántico declarativo y determinista. Este procesa especificaciones de dominio de alto nivel escritas en formatos estructurados YAML o Markdown hacia un Árbol de Sintaxis Abstracta (AST) Semántico Canónico validado, ejecutando inferencia de roles basada en grafos, generación automatizada de expresiones DAX y rigurosa puntuación de calidad de gobernanza.

La innovación central de SemanticFlow reside en su Subsistema de Proyección Multi-Persona. En lugar de forzar a los diversos actores a consumir una única representación monolítica, SemanticFlow proyecta el AST semántico canónico en 10 Lentes de Persona especializadas y validadas por esquema JSON (desde Ingenieros de Datos y Oficiales de Gobernanza hasta Líderes de Analítica C-Level mediante un Cockpit de Liderazgo de Datos consolidado). Finalmente, el subsistema emisor de código traduce estas abstracciones proyectadas en artefactos Tabular Model Definition Language (TMDL) de Microsoft Power BI y topologías de carpetas PBIP de nivel de producción, garantizando un despliegue CI/CD sin fricciones y una alineación absoluta con la fuente única de verdad en todo el ciclo de vida empresarial.

---

## 2. Arquitectura y Topología del Sistema

SemanticFlow está diseñado como una tubería de compilación desacoplada. Las especificaciones de entrada se someten a transformaciones multietapa con un estricto aislamiento de fronteras entre el análisis sintáctico (parsing), la computación de grafos semánticos, la proyección de personas y la emisión de código.

```
 +-------------------------------------------------------------------------+
 |                 Especificaciones de Fuente Declarativas                 |
 |                (Esquemas YAML / Archivos de Modelo Markdown)            |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                          Subsistema de Parsing                          |
 |           [YamlParser]                   [MarkdownParser]               |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                 Subsistema Mapper Crudo a Canónico                      |
 |                Traduce AST a CanonicalSemanticModel                     |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                     Motor de Computación Semántica                      |
 |  +--------------------+   +---------------------+   +-----------------+ |
 |  | RoleInferer        |   | RelationshipResolver|   | DaxGenerator    | |
 |  | (Hecho/Dim/Bridge) |   | (Topología NetworkX)|   | (DAX Automático)| |
 |  +--------------------+   +---------------------+   +-----------------+ |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                     Scorer de Gobernanza y Calidad                      |
 |         Evalúa Cobertura, Documentación, Riesgo PII y Sintaxis          |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                   Capa de Proyección Multi-Persona                      |
 |  +-------------------------------------------------------------------+  |
 |  | 10 Lentes de Persona (Ingeniería de Datos, Gobernanza, etc.)     |  |
 |  | + Generador de Cockpit de Liderazgo de Datos                      |  |
 |  +-------------------------------------------------------------------+  |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                        Subsistema Emisor Destino                        |
 |          [TmdlEmitter]          [PbipWriter]        [DocEmitter]        |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                           Artefactos de Salida                          |
 |            (Power BI TMDL / PBIP, Persona JSON/MD, Cockpit)             |
 +-------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática y Motores Analíticos

### 3.1. Motor de Inferencia Topológica y Roles de Entidad
Sea $G = (V, E)$ el grafo semántico dirigido del dominio, donde $V$ representa el conjunto de entidades (tablas) y $E$ el conjunto de relaciones dirigidas por clave foránea $e = (v_i, v_j)$ con $v_i, v_j \in V$.

El componente `RoleInferer` evalúa la topología estructural y la distribución de métricas para asignar un rol de entidad $R(v) \in \{\text{FACT}, \text{DIMENSION}, \text{BRIDGE}, \text{HYBRID}\}$ a cada entidad $v \in V$:

$$R(v) = \begin{cases} 
\text{FACT}, & \text{si } \text{deg}_{in}(v) > \text{deg}_{out}(v) \land |M(v)| > 0 \\ 
\text{DIMENSION}, & \text{si } \text{deg}_{out}(v) \ge \text{deg}_{in}(v) \land \text{IsUnique}(PK(v)) \\ 
\text{BRIDGE}, & \text{si } \exists e \in E \text{ tal que } \text{cardinality}(e) = \text{MANY\_TO\_MANY} \\ 
\text{HYBRID}, & \text{en otro caso} 
\end{cases}$$

donde $\text{deg}_{in}(v)$ y $\text{deg}_{out}(v)$ denotan el grado de entrada y salida en $G$, $M(v)$ es el conjunto de medidas asociadas a la entidad $v$, y $PK(v)$ representa los atributos de clave primaria.

### 3.2. Síntesis Automatizada de Expresiones DAX
Cuando una medida $m$ se define con un tipo de agregación de alto nivel $A(m) \in \{\text{SUM}, \text{COUNT}, \text{AVERAGE}, \text{DISTINCT\_COUNT}\}$, el componente `DaxGenerator` construye expresiones DAX sintácticamente válidas $\Phi(m)$:

$$\Phi(m) = \begin{cases}
\text{SUM}(v.\text{attr}), & \text{si } A(m) = \text{SUM} \\
\text{CALCULATE}(\text{SUM}(v.\text{attr}), \text{KEEPFILTERS}(\dots)), & \text{si } A(m) = \text{SUM} \land |\text{Filter}(m)| > 0 \\
\text{DIVIDE}(\Phi(m_1), \Phi(m_2), 0), & \text{si } A(m) = \text{RATIO}
\end{cases}$$

### 3.3. Proyección Multi-Persona y Modelo de Puntuación de Calidad
Dado un Modelo Semántico Canónico $M = (V, E, M_e, Q)$ y una lente de persona objetivo $P_k$ ($k \in [1, 10]$), el operador de proyección $\Pi_{P_k}$ filtra y enriquece el AST canónico en una vista restringida por esquema $V_{P_k}$:

$$\Pi_{P_k}: M \longmapsto V_{P_k} = \left\{ \phi(v, m) \mid v \in V, m \in M_e, \text{QualScore}(v) \ge \theta_{P_k} \right\}$$

La puntuación global de calidad $Q_{model} \in [0, 100]$ se calcula como una combinación lineal escalar ponderada sobre la evaluación de las entidades:

$$Q_{model} = \frac{100}{|V|} \sum_{v \in V} \left( \alpha \cdot \text{Cov}(v) + \beta \cdot \text{Doc}(v) + \gamma \cdot (1 - \text{PII}_{risk}(v)) + \delta \cdot \text{Syntax}_{valid}(v) \right)$$

donde $\alpha = 0.30$, $\beta = 0.25$, $\gamma = 0.25$ y $\delta = 0.20$, cumpliendo $\alpha + \beta + \gamma + \delta = 1.0$.

---

## 4. Rendimiento Empírico y Benchmarks

SemanticFlow ha sido probado bajo condiciones de estrés en modelos de dominio reales y sintéticos a gran escala (incluyendo Falabella Retail, Metro Santiago y suites de estrés Tier 1, Tier 2 y Tier 3). Los benchmarks se ejecutaron en un entorno de tiempo de ejecución Python 3.12 aislado.

| Suite de Benchmark / Métrica | Entidades | Relaciones | Cantidad de Medidas | Latencia de Compilación (p99) | Huella de Memoria | Estado de Verificación |
|:-----------------------------|:----------|:-----------|:--------------------|:------------------------------|:------------------|:-----------------------|
| **Metro Santiago (Golden)** | 8 entidades | 7 aristas | 14 medidas | 12.4 ms | 18.2 MB | 100% Aprobado (71/71) |
| **Tier 1 (Suite PYME)** | 12 entidades | 10 aristas | 24 medidas | 18.1 ms | 22.4 MB | 100% Aprobado |
| **Tier 2 (Suite Mediana)** | 35 entidades | 42 aristas | 85 medidas | 45.3 ms | 34.8 MB | 100% Aprobado |
| **Tier 3 (Enterprise Retail)** | 120 entidades | 165 aristas | 410 medidas | 142.0 ms | 68.1 MB | 100% Aprobado |
| **Massive Stress V2 (Faker)** | 350 entidades | 510 aristas | 1,200 medidas | 385.6 ms | 124.5 MB | 100% Aprobado |

---

## 5. Estructura del Repositorio y Artefactos

El repositorio cumple con una estricta separación modular entre la interfaz CLI, los subsistemas del compilador, los contratos de esquema JSON, las reglas de configuración y la suite de pruebas.

```
SemanticFlow/
├── pyproject.toml                     # Configuración de build, entrypoint CLI y dependencias
├── README.md                          # Documentación maestra internacional (Inglés)
├── README_ES.md                       # Documentación maestra internacional (Español)
├── config/
│   ├── persona_quality_rules.json     # Reglas declarativas de puntuación de gobernanza
│   └── personas_config.yaml           # Metadatos y mapeos de las lentes de persona
├── docs/
│   ├── architecture.md                # Especificación detallada del diseño arquitectónico
│   └── user_guide.md                  # Guía completa de uso de la interfaz CLI
├── schemas/
│   ├── canonical_model_schema.json    # JSON Schema para AST CanonicalSemanticModel
│   └── persona_contracts/             # JSON Schemas formales para las 10 Lentes de Persona
│       ├── ai_systems_engineer.json
│       ├── analytics_engineer.json
│       ├── analytics_leader.json
│       ├── bi_developer.json
│       ├── business_consumer.json
│       ├── compliance_auditor.json
│       ├── data_engineer.json
│       ├── data_governance_officer.json
│       ├── data_product_manager.json
│       └── finops_specialist.json
├── src/
│   ├── cli.py                         # Punto de entrada de la aplicación Typer CLI
│   └── core/
│       ├── ast/                       # Definición del Árbol de Sintaxis Abstracta (Pydantic V2)
│       ├── capabilities/              # Orquestación de tuberías y planificación
│       ├── docs/                      # Generador de documentación en Markdown
│       ├── emitter/                   # Emisores de código TMDL y PBIP
│       ├── engine/                    # Motor de inferencia, generador DAX y solver NetworkX
│       ├── mappers/                   # Capas de traducción y mapeo de AST
│       ├── parsers/                   # YamlParser y MarkdownParser
│       ├── personas/                  # Motor de proyección de personas, lentes y Cockpit
│       ├── quality/                   # Scorer de calidad de gobernanza y motor de reglas
│       └── targets/                   # Definición de adaptadores destino (Power BI)
└── tests/                             # Suite de pruebas (71 casos pytest + benchmarks)
```

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Configuración del Entorno y Prerrequisitos

SemanticFlow requiere Python 3.10 o superior. El aislamiento mediante entorno virtual es obligatorio.

```bash
# Clonar el repositorio
git clone https://github.com/AlvaroAlejandroFinOps/SemanticFlow.git
cd SemanticFlow

# Inicializar el entorno virtual
python -m venv .venv

# Activar el entorno virtual (Linux/macOS)
source .venv/bin/activate

# Activar el entorno virtual (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalar el paquete en modo editable con dependencias de desarrollo
pip install -e ".[dev]"
```

### 6.2. Ejecución de la Tubería y Uso de la CLI

El sistema expone comandos CLI a través del ejecutable `semanticflow`:

```bash
# Validar la sintaxis e integridad del esquema de un modelo semántico
semanticflow validate path/to/model.yaml

# Compilar un modelo semántico a una estructura de carpetas Power BI TMDL / PBIP
semanticflow compile path/to/model.yaml --output-dir ./output/tmdl_model

# Proyectar una Lente de Persona específica (ej. Oficial de Gobernanza de Datos) a JSON
semanticflow persona path/to/model.yaml --persona data_governance_officer --format json

# Proyectar las 10 Lentes de Persona y generar el Cockpit de Liderazgo de Datos
semanticflow cockpit path/to/model.yaml --output-dir ./output/cockpit_reports
```

### 6.3. Suite de Verificación y Pruebas de Invariantes

Ejecutar la suite de pruebas automatizadas con aserciones de cobertura completas:

```bash
# Ejecutar la suite completa de pruebas (71 casos de prueba)
python -m pytest --tb=short

# Ejecutar la suite de pruebas con reporte de cobertura
python -m pytest --cov=src --cov-report=term-missing
```

---

## 7. Glosario de Dominio

* **Canonical Semantic AST:** Representación Pydantic intermedia e independiente del motor destino que modela entidades, medidas y topología de dominio.
* **TMDL (Tabular Model Definition Language):** Formato de texto declarativo y legible por humanos de Microsoft para modelos tabulares de Power BI y Analysis Services.
* **PBIP (Power BI Project):** Formato para desarrolladores basado en carpetas para Power BI, que habilita el control de versiones e integración con Git.
* **Lente de Persona (Persona Lens):** Proyección adaptada a un esquema específico del modelo semántico canónico para un rol empresarial particular.
* **Data Leadership Cockpit:** Tablero ejecutivo consolidado que resume la madurez del modelo, el cumplimiento de gobernanza y la cobertura de métricas.
* **Inferencia de Roles:** Determinación algorítmica de si una entidad actúa como tabla de Hecho, Dimensión, Puente o Híbrida en función de la topología del grafo.

---

## 8. Referencias Académicas y de Ingeniería

1. Microsoft Corporation. *Tabular Model Definition Language (TMDL) Specification*. Microsoft Learn, 2023.
2. Fowler, M. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002.
3. Hagberg, A. A., Schult, D. A., & Swart, P. J. *Exploring Network Structure, Dynamics, and Function using NetworkX*. Proceedings of the 7th Python in Science Conference (SciPy 2008), pp. 11–15.
4. Pydantic Developers. *Data Validation and Settings Management using Python Type Annotations*. Pydantic V2 Documentation, 2024.

### Citación BibTeX

```bibtex
@software{semanticflow_2026,
  author = {SemanticFlow Core Team},
  title = {SemanticFlow: Declarative Semantic Model Compiler and Enterprise Analytics Projection Platform},
  year = {2026},
  version = {0.1.0},
  url = {https://github.com/AlvaroAlejandroFinOps/SemanticFlow}
}
```
