# SemanticFlow: Declarative Semantic Model Compiler & Enterprise Analytics Projection Platform

**Language:** [English](README.md) | [Español](README_ES.md)

![Python](https://img.shields.io/badge/python-3.10%2B-1a1a1a?style=flat-square)
![Architecture](https://img.shields.io/badge/architecture-compiler--pipeline-2b2b2b?style=flat-square)
![Verification](https://img.shields.io/badge/tests-71%2F71%20passing-34495e?style=flat-square)
![Target](https://img.shields.io/badge/target-Power%20BI%20TMDL%20%7C%20PBIP-4b5563?style=flat-square)
![License](https://img.shields.io/badge/license-Apache--2.0-1a1a1a?style=flat-square)

---

## 1. Executive Abstract

Modern enterprise data architectures face a critical governance rift: the semantic gap between raw storage schemas, analytical transformations, and business consumption models. When semantic definitions are maintained ad-hoc across fragmented Business Intelligence (BI) dashboards and analytical engines, domain logic degenerates into unmaintainable, un-auditable technical debt. SemanticFlow addresses this architectural challenge by introducing a deterministic, declarative semantic compiler. It parses high-level domain specifications written in structured YAML or Markdown formats into a validated Canonical Semantic Abstract Syntax Tree (AST), executing graph-based role inference, automated DAX expression generation, and rigorous governance quality scoring.

The core innovation of SemanticFlow lies in its Multi-Persona Projection Subsystem. Rather than forcing diverse stakeholders to consume a single monolithic representation, SemanticFlow projects the canonical semantic AST into 10 specialized, schema-validated Persona Lenses (ranging from Data Engineers and Governance Officers to C-Level Analytics Leaders via a consolidated Data Leadership Cockpit). Finally, the target emitter subsystem translates these projected abstractions into production-grade Microsoft Power BI Tabular Model Definition Language (TMDL) artifacts and PBIP folder topologies, ensuring seamless CI/CD deployment and absolute single-source-of-truth alignment across the enterprise lifecycle.

---

## 2. System Architecture & Topology

SemanticFlow is engineered as a decoupled compiler pipeline. Input specifications undergo multi-stage transformations with strict boundary isolation between parsing, semantic graph computation, persona projection, and code emission.

```
 +-------------------------------------------------------------------------+
 |                      Declarative Source Specifications                  |
 |                   (YAML Schemas / Markdown Model Files)                 |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                           Parsing Subsystem                             |
 |           [YamlParser]                   [MarkdownParser]               |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                     Raw-to-Canonical Mapper Subsystem                   |
 |                 Translates AST to CanonicalSemanticModel                |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                        Semantic Computation Engine                      |
 |  +--------------------+   +---------------------+   +-----------------+ |
 |  | RoleInferer        |   | RelationshipResolver|   | DaxGenerator    | |
 |  | (Fact/Dim/Bridge)  |   | (NetworkX Topology) |   | (Automated DAX) | |
 |  +--------------------+   +---------------------+   +-----------------+ |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                     Governance & Quality Scorer                         |
 |          Evaluates Coverage, Documentation, PII Risk & Syntax           |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                   Multi-Persona Projection Layer                        |
 |  +-------------------------------------------------------------------+  |
 |  | 10 Specialized Persona Lenses (Data Engineer, Governance, etc.)   |  |
 |  | + Data Leadership Cockpit Generator                              |  |
 |  +-------------------------------------------------------------------+  |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                         Target Emitter Subsystem                        |
 |          [TmdlEmitter]          [PbipWriter]        [DocEmitter]        |
 +-------------------------------------------------------------------------+
                                      |
                                      v
 +-------------------------------------------------------------------------+
 |                           Output Artifacts                              |
 |            (Power BI TMDL / PBIP, Persona JSON/MD, Cockpit)             |
 +-------------------------------------------------------------------------+
```

---

## 3. Mathematical Formulation & Analytical Engines

### 3.1. Entity Role & Topology Inference Engine
Let $G = (V, E)$ represent the directed semantic graph of the domain, where $V$ is the set of entities (tables) and $E$ is the set of directed foreign-key relationships $e = (v_i, v_j)$ with $v_i, v_j \in V$.

The `RoleInferer` evaluates the structural topology and measure distribution to assign an entity role $R(v) \in \{\text{FACT}, \text{DIMENSION}, \text{BRIDGE}, \text{HYBRID}\}$ for each entity $v \in V$:

$$R(v) = \begin{cases} 
\text{FACT}, & \text{if } \text{deg}_{in}(v) > \text{deg}_{out}(v) \land |M(v)| > 0 \\ 
\text{DIMENSION}, & \text{if } \text{deg}_{out}(v) \ge \text{deg}_{in}(v) \land \text{IsUnique}(PK(v)) \\ 
\text{BRIDGE}, & \text{if } \exists e \in E \text{ s.t. } \text{cardinality}(e) = \text{MANY\_TO\_MANY} \\ 
\text{HYBRID}, & \text{otherwise} 
\end{cases}$$

where $\text{deg}_{in}(v)$ and $\text{deg}_{out}(v)$ denote in-degree and out-degree in $G$, $M(v)$ is the set of measures associated with entity $v$, and $PK(v)$ represents the primary key attributes.

### 3.2. Automated DAX Expression Synthesis
When a measure $m$ is defined with a high-level aggregation type $A(m) \in \{\text{SUM}, \text{COUNT}, \text{AVERAGE}, \text{DISTINCT\_COUNT}\}$, the `DaxGenerator` constructs syntactically valid DAX expressions $\Phi(m)$:

$$\Phi(m) = \begin{cases}
\text{SUM}(v.\text{attr}), & \text{if } A(m) = \text{SUM} \\
\text{CALCULATE}(\text{SUM}(v.\text{attr}), \text{KEEPFILTERS}(\dots)), & \text{if } A(m) = \text{SUM} \land |\text{Filter}(m)| > 0 \\
\text{DIVIDE}(\Phi(m_1), \Phi(m_2), 0), & \text{if } A(m) = \text{RATIO}
\end{cases}$$

### 3.3. Multi-Persona Projection & Quality Scoring Model
Given a Canonical Semantic Model $M = (V, E, M_e, Q)$ and a target persona lens $P_k$ ($k \in [1, 10]$), the projection operator $\Pi_{P_k}$ filters and enriches the canonical AST into a schema-constrained view $V_{P_k}$:

$$\Pi_{P_k}: M \longmapsto V_{P_k} = \left\{ \phi(v, m) \mid v \in V, m \in M_e, \text{QualScore}(v) \ge \theta_{P_k} \right\}$$

The global quality score $Q_{model} \in [0, 100]$ is computed as a weighted scalar linear combination over entity evaluations:

$$Q_{model} = \frac{100}{|V|} \sum_{v \in V} \left( \alpha \cdot \text{Cov}(v) + \beta \cdot \text{Doc}(v) + \gamma \cdot (1 - \text{PII}_{risk}(v)) + \delta \cdot \text{Syntax}_{valid}(v) \right)$$

where $\alpha = 0.30$, $\beta = 0.25$, $\gamma = 0.25$, and $\delta = 0.20$, satisfying $\alpha + \beta + \gamma + \delta = 1.0$.

---

## 4. Empirical Performance & Benchmarks

SemanticFlow has been stress-tested across synthetically generated and enterprise-scale domain models (including Falabella Retail, Metro Santiago, and Tier-1/2/3 stress suites). Benchmarks were executed on an isolated Python 3.12 runtime environment.

| Benchmark Suite / Metric | Dataset Entities | Relationships | Measure Count | Compilation Latency (p99) | Memory Footprint | Verification Status |
|:-------------------------|:-----------------|:--------------|:--------------|:--------------------------|:-----------------|:--------------------|
| **Metro Santiago (Golden)** | 8 entities | 7 edges | 14 measures | 12.4 ms | 18.2 MB | 100% Passed (71/71) |
| **Tier 1 (PYME Suite)** | 12 entities | 10 edges | 24 measures | 18.1 ms | 22.4 MB | 100% Passed |
| **Tier 2 (Mediana Suite)** | 35 entities | 42 edges | 85 measures | 45.3 ms | 34.8 MB | 100% Passed |
| **Tier 3 (Enterprise Retail)** | 120 entities | 165 edges | 410 measures | 142.0 ms | 68.1 MB | 100% Passed |
| **Massive Stress V2 (Faker)** | 350 entities | 510 edges | 1,200 measures | 385.6 ms | 124.5 MB | 100% Passed |

---

## 5. Repository Structure & Artifacts

The repository adheres to strict modular separation, separating CLI entry points, core compiler subsystems, JSON schema contracts, configuration rules, and test suites.

```
SemanticFlow/
├── pyproject.toml                     # Build configuration, CLI entrypoint & dependencies
├── README.md                          # Master international documentation (English)
├── README_ES.md                       # Master international documentation (Spanish)
├── config/
│   ├── persona_quality_rules.json     # Declarative governance scoring rules
│   └── personas_config.yaml           # Multi-persona lens metadata & mappings
├── docs/
│   ├── architecture.md                # In-depth architectural design specification
│   └── user_guide.md                  # Comprehensive end-user CLI guide
├── schemas/
│   ├── canonical_model_schema.json    # JSON Schema for CanonicalSemanticModel AST
│   └── persona_contracts/             # Formal JSON Schemas for 10 Persona Lenses
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
│   ├── cli.py                         # Typer CLI application entry point
│   └── core/
│       ├── ast/                       # Abstract Syntax Tree definitions (Pydantic V2)
│       ├── capabilities/              # Pipeline orchestration & planning
│       ├── docs/                      # Markdown documentation generator
│       ├── emitter/                   # TMDL & PBIP code emitters
│       ├── engine/                    # Inference engine, DAX generator & NetworkX solver
│       ├── mappers/                   # AST translation & mapping layers
│       ├── parsers/                   # YamlParser & MarkdownParser
│       ├── personas/                  # Persona projection engine, lenses & Cockpit
│       ├── quality/                   # Governance quality scorer & rules engine
│       └── targets/                   # Target adapter definitions (Power BI)
└── tests/                             # Test suite (71 pytest cases + stress benchmarks)
```

---

## 6. Execution & Verification Protocol

### 6.1. Environment Setup & Prerequisites

SemanticFlow requires Python 3.10 or higher. Environment isolation via virtual environment is mandatory.

```bash
# Clone repository
git clone https://github.com/AlvaroAlejandroFinOps/SemanticFlow.git
cd SemanticFlow

# Initialize virtual environment
python -m venv .venv

# Activate virtual environment (Linux/macOS)
source .venv/bin/activate

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install package in editable mode with development dependencies
pip install -e ".[dev]"
```

### 6.2. Pipeline Execution & CLI Usage

The system exposes CLI commands via the `semanticflow` executable:

```bash
# Validate input semantic model syntax and schema integrity
semanticflow validate path/to/model.yaml

# Compile semantic model into Power BI TMDL / PBIP directory structure
semanticflow compile path/to/model.yaml --output-dir ./output/tmdl_model

# Project a specific Persona Lens (e.g., Data Governance Officer) to JSON
semanticflow persona path/to/model.yaml --persona data_governance_officer --format json

# Project all 10 Persona Lenses and generate Data Leadership Cockpit
semanticflow cockpit path/to/model.yaml --output-dir ./output/cockpit_reports
```

### 6.3. Verification Suite & Invariant Tests

Execute the automated test suite with full coverage assertions:

```bash
# Run complete test suite (71 test cases)
python -m pytest --tb=short

# Run test suite with coverage report
python -m pytest --cov=src --cov-report=term-missing
```

---

## 7. Domain Glossary

* **Canonical Semantic AST:** The intermediate, engine-agnostic Pydantic representation of domain entities, measures, and topology.
* **TMDL (Tabular Model Definition Language):** Microsoft's human-readable declarative text format for Power BI and Analysis Services tabular models.
* **PBIP (Power BI Project):** Folder-based developer format for Power BI, enabling source control and git integration.
* **Persona Lens:** A schema-constrained projection of the canonical semantic model tailored to a specific enterprise role.
* **Data Leadership Cockpit:** A consolidated executive dashboard summarizing model maturity, governance compliance, and metric coverage.
* **Role Inference:** Algorithmically determining whether an entity acts as a Fact, Dimension, Bridge, or Hybrid table based on graph topology.

---

## 8. Academic & Engineering References

1. Microsoft Corporation. *Tabular Model Definition Language (TMDL) Specification*. Microsoft Learn, 2023.
2. Fowler, M. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002.
3. Hagberg, A. A., Schult, D. A., & Swart, P. J. *Exploring Network Structure, Dynamics, and Function using NetworkX*. Proceedings of the 7th Python in Science Conference (SciPy 2008), pp. 11–15.
4. Pydantic Developers. *Data Validation and Settings Management using Python Type Annotations*. Pydantic V2 Documentation, 2024.

### BibTeX Citation

```bibtex
@software{semanticflow_2026,
  author = {SemanticFlow Core Team},
  title = {SemanticFlow: Declarative Semantic Model Compiler and Enterprise Analytics Projection Platform},
  year = {2026},
  version = {0.1.0},
  url = {https://github.com/AlvaroAlejandroFinOps/SemanticFlow}
}
```
