![alt text](SemanticFlow.png)
# SEMANTICFLOW: Enterprise DataOps Platform for Semantic Modeling as Code on Microsoft Fabric and Power BI

**Language:** [English](README.md) | [Español](README_ES.md)

[![Runtime: Python 3.10+](https://img.shields.io/badge/python-3.10%2B-2b2b2b?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Architecture: Canonical AST](https://img.shields.io/badge/architecture-canonical_AST-1a1a1a?style=flat-square)](src/core/ast/)
[![Verification: 71 Passed](https://img.shields.io/badge/tests-71%2F71_passing-34495e?style=flat-square)](tests/)
[![Target: Fabric TMDL/PBIP](https://img.shields.io/badge/target-Fabric%20%7C%20TMDL%2FPBIP-2b2b2b?style=flat-square)](src/core/emitter/)
[![Quality: cQS Quality Gate](https://img.shields.io/badge/ci%2Fcd-cQS_Quality_Gate-1a1a1a?style=flat-square)](src/core/quality/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-4b5563?style=flat-square)](pyproject.toml)

---

## 1. Executive Abstract and Enterprise Positioning

In large-scale enterprise environments across banking, retail, telecommunications, and mining, analytical modernization on modern Lakehouse architectures (Microsoft Fabric OneLake, Azure Synapse, AWS S3, or GCP BigQuery) encounters a critical operational bottleneck: **the friction between upstream data engineering and downstream semantic consumption**. While transformations within Medallion architectures (Bronze/Silver/Gold) adhere to rigorous CI/CD, version control, and data governance practices, downstream analytical models are still manually constructed within Power BI Desktop, generating opaque binary `.pbix` files that cannot be audited, versioned, or code-reviewed in Git.

This architectural disconnect introduces systemic business risks: duplicate calculation logic, ambiguous tabular relationships that degrade cloud capacity performance, an absence of automated Quality Gates in deployment pipelines, unmanaged Personally Identifiable Information (PII) exposure, and misaligned goals across governance, cloud FinOps, and business teams.

**SemanticFlow** is an enterprise DataOps platform for **Semantic Modeling as Code (SMaC)** designed to bridge this operational gap. It allows data teams to author declarative semantic models (in Markdown or YAML) directly within Git repositories, compile them locally and headlessly into native Microsoft Fabric and Power BI formats (TMDL and `.pbip` project structures), enforce architectural standards through a deterministic algorithmic Quality Gate ($cQS$), and project the semantic model through a Multi-Stakeholder Architecture Matrix tailored for cross-functional governance committees and C-level data executives.

---

## 2. End-to-End Architecture and DataOps Lifecycle

SemanticFlow integrates natively into enterprise cloud data engineering lifecycles. It functions as an offline, in-memory headless compiler without requiring active database connections or runtime external engine dependencies during compilation.

```
+---------------------------------------------------------------------------------------------------+
|                                     GIT-DRIVEN DATAPOPS LIFECYCLE                                 |
|                                                                                                   |
|   [ Git Repository ]           [ CI/CD Pipeline ]             [ Headless Compiler ]               |
|   Declarative Schema   ===>    Azure DevOps / GitHub   ===>   SemanticFlow Engine                 |
|   (YAML / Markdown)            Runner (Python 3.10+)          - Topological Inference R(v)        |
|                                                               - Governance Audit & cQS Gate       |
+------------------------------------------+--------------------------------------------------------+
                                           |
                    +----------------------+----------------------+
                    | (Passes cQS Quality Gate)                   | (Fails cQS < Threshold)
                    v                                             v
+------------------------------------------+    +---------------------------------------------------+
|       COMPILATION & SERIALIZATION        |    |                 BLOCKED PIPELINE                  |
|                                          |    |  Pull Request build rejected.                     |
|  - Tabular Model Def. Lang. (TMDL)       |    |  Detailed diagnostic report emitted               |
|  - Power BI Project Developer (.pbip)    |    |  highlighting governance or topology violations.  |
|  - Corporate Dictionary & Mermaid ERD    |    +---------------------------------------------------+
+-------------------+----------------------+
                    |
                    v
+---------------------------------------------------------------------------------------------------+
|                        DEPLOYMENT TO MICROSOFT FABRIC / POWER BI SERVICE                          |
|                                                                                                   |
|   Microsoft Fabric Workspace <==== Automated Sync via Fabric Git Integration / REST APIs          |
|   - Version-Controlled Semantic Models in OneLake                                                 |
|   - Validated Star and Snowflake Topologies for VertiPaq Engine Efficiency                        |
|   - Multi-Role Perspectives & Leadership Cockpit for CDO and Enterprise Governance Teams         |
+---------------------------------------------------------------------------------------------------+
```

### Compiler Internal Topology

The compilation engine executes through four modular and decoupled layers:

```
+---------------------------------------------------------------------------------------------------+
| 1. DECLARATIVE INGESTION LAYER                                                                    |
|    MarkdownSchemaParser / YamlSchemaParser: Ingestion and normalization of relational schema.     |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 2. INTERMEDIATE REPRESENTATION (CANONICAL AST)                                                    |
|    CanonicalProject: Neutral relational entities, strict typing, attributes, and governance tags. |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
         +----------------------------------------+----------------------------------------+
         |                                        |                                        |
         v                                        v                                        v
+-----------------------------+  +--------------------------------+  +------------------------------+
| TOPOLOGICAL INFERENCE       |  | QUALITY GATE & AUDIT ENGINE    |  | MULTI-STAKEHOLDER MATRIX     |
| - Role Assignment R(v)      |  | - SemanticQualityScorer        |  | - 10 Operational Views       |
| - Acyclicity Check C(G)     |  | - Deterministic Penalties      |  | - Governance & FinOps Pillars|
| - Baseline DAX Synthesis    |  | - Automated CI/CD Deployment   |  | - C-Level Leadership Cockpit |
+--------------+--------------+  +----------------+---------------+  +--------------+---------------+
               |                                  |                                 |
               +----------------------------------+---------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| 3. CLOUD SERIALIZATION & EMISSION LAYER                                                           |
|    - PbipWriter / TmdlFormatter: Native tabular model files ready for Microsoft Fabric deployment.|
|    - Multi-Persona Exporters: Formal stakeholder specifications (JSON/MD).                        |
|    - Automated DocGen: Enterprise Data Dictionary and Mermaid entity-relationship diagrams.       |
+---------------------------------------------------------------------------------------------------+
```

---

## 3. Production Engines and Mathematical Formalization

SemanticFlow applies rigorous mathematical formulations focused strictly on resolving concrete performance, governance, and stability bottlenecks in production.

### 3.1. Topological Inference and VertiPaq Ambiguity Prevention

The columnar engine of Microsoft Fabric and Power BI (VertiPaq) demands clean star or snowflake schemas. Circular relationship paths or multi-directional cross-filtering configurations create query ambiguity, poor execution plans, and memory exhaustion across enterprise capacities.

The relational schema is represented as a directed graph $G = (V, E)$, where $V$ denotes entities (tables) and $E$ represents foreign key constraints directed from dependent tables toward referenced parent tables. For any table $v \in V$, $d^-(v)$ denotes the in-degree (referenced by foreign keys) and $d^+(v)$ denotes the out-degree (referencing external parents). The deterministic role assignment function $\mathcal{R}(v)$ classifies each entity:

$$\mathcal{R}(v) = \begin{cases} 
\text{FACT}, & \text{if } d^+(v) \ge 1 \ \land \ d^-(v) = 0 \\
\text{DIMENSION}, & \text{if } d^+(v) = 0 \ \land \ d^-(v) \ge 1 \\
\text{BRIDGE}, & \text{if } d^+(v) \ge 2 \ \land \ d^-(v) \ge 1 \\
\text{OUTRIGGER}, & \text{if } d^+(v) \ge 1 \ \land \ d^-(v) \ge 1 \ \land \ |Attr(v)| \le \theta_{dim} \\
\text{DIMENSION}, & \text{otherwise (safe fallback)}
\end{cases}$$

To guarantee that the compiled model contains no relationship traps or circular dependencies, acyclicity is validated over the condensation graph:

$$\mathcal{C}(G) = \emptyset \iff \forall \text{ cycle } C \subset G, \ |C| = 0$$

If $\mathcal{C}(G) \ne \emptyset$, the `RelationshipResolver` component isolates conflicting relationship edges and flags ambiguous paths, configuring inactive relationships to protect query runtime performance.

### 3.2. Semantic Quality Score ($cQS$) as an Automated CI/CD Quality Gate

The $cQS: \mathcal{M} \to [0, 100]$ score functions as an automated deployment gate within continuous integration pipelines (Azure Pipelines, GitHub Actions, or GitLab CI).

$$cQS(\mathcal{M}) = \max\left(0, \ 100 - \sum_{k \in \mathcal{K}} w_k \cdot \mathbb{I}_k(\mathcal{M}) - \sum_{j \in \mathcal{D}} \lambda_j \cdot \mu_j(\mathcal{M})\right)$$

Where:
* $\mathcal{K}$ represents **blocking architectural invariants** (missing primary keys, active circular paths in relationships, broken foreign keys). If $\sum \mathbb{I}_k(\mathcal{M}) > 0$, the pipeline exits with a non-zero status code and halts the deployment.
* $\mathcal{D}$ represents **enterprise governance rules** (untyped attributes, undocumented business columns, uncertified measures, unmasked PII attributes).
* $\lambda_j$ specifies the penalty weight and $\mu_j(\mathcal{M})$ represents the normalized violation frequency.

**Operational CI/CD Policy:** Deployment to Microsoft Fabric is rejected if $cQS(\mathcal{M}) < \tau_{\text{threshold}}$ (configurable threshold, default 75.0%) or if any critical blocking invariant is breached.

---

## 4. Multi-Stakeholder Architecture and Governance Matrix

SemanticFlow projects the compiled canonical model into four enterprise pillars, addressing the specific operational and regulatory needs of key enterprise stakeholders:

```
+---------------------------------------------------------------------------------------------------+
|                            MULTI-STAKEHOLDER GOVERNANCE MATRIX                                    |
+----------------------------------+----------------------------------------------------------------+
| CORPORATE PILLAR                 | STAKEHOLDER ROLES & VALUE DELIVERED                            |
+----------------------------------+----------------------------------------------------------------+
| I. Governance & Regulatory       | • Data Governance Officer: Data ownership, metadata completeness|
|    Compliance                    |   and enterprise criticality classifications.                  |
|                                  | • Compliance Auditor: PII detection and masking, regulatory   |
|                                  |   compliance tracking (GDPR, ISO 27001, local privacy laws).   |
+----------------------------------+----------------------------------------------------------------+
| II. Cloud Platform               | • Data Engineer: Parquet/Delta file formats and partitioning.  |
|     & FinOps Optimization        | • FinOps Specialist: Fabric F-SKU capacity usage forecasting,  |
|                                  |   VertiPaq memory footprint, and query cost optimization.      |
|                                  | • AI Systems Engineer: Semantic lineaging for vector stores,   |
|                                  |   analytical agent integration, and RAG index readiness.       |
+----------------------------------+----------------------------------------------------------------+
| III. Analytics Engineering & BI  | • Analytics Engineer: Data contracts and transformation checks.|
|                                  | • BI Developer: Star schema layout, TMDL folder organization,  |
|                                  |   and automated canonical DAX measure generation.              |
+----------------------------------+----------------------------------------------------------------+
| IV. Business & Strategic         | • Data Product Manager: Data product boundaries and SLOs.     |
|     Leadership                   | • Business Consumer: Certified metrics and clear definitions.  |
|                                  | • Data Leadership Cockpit: C-Level executive dashboard for     |
|                                  |   CDOs and VPs with a 10-dimensional domain maturity radar.   |
+----------------------------------+----------------------------------------------------------------+
```

---

## 5. Empirical Performance and Enterprise Benchmarks

The compilation engine was evaluated on standard computing environments (Python 3.12.10 on modern hardware), testing scalability on large synthetic stress topologies as well as high-complexity operational models:

| Performance Dimension   | Design Target | Tier 1 (Small) | Tier 2 (Corporate)   | Tier 3 (Enterprise)  | Real-World (Santiago Metro) |
|:------------------------|:--------------|:---------------|:---------------------|:---------------------|:----------------------------|
| Entities (Tables)       | 5 - 10 tables | 4 - 8 tables   | 15 - 25 tables       | 50 - 100 tables      | 20 operational tables       |
| Relationships Evaluated | 5 - 15 edges  | 6 - 12 edges   | 20 - 40 edges        | 75 - 180 edges       | 26 active relationships     |
| Compilation Latency     | $< 1000$ ms   | 42 ms          | 185 ms               | 840 ms               | 210 ms                      |
| 10-View Projection      | $< 2000$ ms   | 110 ms         | 390 ms               | 1,240 ms             | 420 ms                      |
| Peak Memory Usage       | $< 250$ MB    | 38 MB          | 54 MB                | 118 MB               | 62 MB                       |
| Verification Suite      | 100% passing  | 71/71 tests    | 71/71 tests          | 71/71 tests          | 71/71 tests passing         |

---

## 6. Repository Structure and Core Components

```
SemanticFlow/
├── .agentignore                       # Context exclusion filters for AI developer tools
├── .context/                          # iDirectory v3.0 contextual governance satellite (tree.json)
├── 01_seed/                           # Architectural DNA and ThinkingSeed Master specifications
│   ├── seed-semanticflow-master.md
│   └── seed-semanticflow.md
├── 02_Foundation/                     # Foundational architecture and engine documentation
│   └── Engine/
│       └── engine_readme.md
├── config/                            # Environment profiles and stakeholder configurations
│   └── personas/
│       └── default_personas.yaml
├── docs/                              # Architecture decision records and technical notes
│   ├── adr/                           # Architecture Decision Records (ADR-001+)
│   │   └── ADR-001-canonical-model.md
│   └── architecture/
│       ├── esquema_relacional.md      # Reference enterprise relational schema
│       └── adr/
├── pyproject.toml                     # Package specification, build configuration, and tooling
├── schemas/                           # JSON Schema contracts for strict validation
│   ├── persona_definition.schema.json
│   └── project_governance.schema.json
├── scripts/                           # Deterministic golden regression generators
│   └── generate_golden_files.py
├── src/                               # Compiler source code
│   ├── cli.py                         # Command-line interface entry point (Typer / Rich)
│   └── core/
│       ├── ast/                       # Canonical Abstract Syntax Tree specifications
│       ├── capabilities/              # Pipeline execution planners
│       ├── docs/                      # Data dictionary and Mermaid diagram generators
│       ├── emitter/                   # Native TMDL and PBIP serialization engines
│       ├── engine/                    # Topological inference, relationship resolvers, and DAX
│       ├── mappers/                   # Schema mappers (raw-to-canonical and canonical-to-pbi)
│       ├── parsers/                   # Declarative schema parsers (Markdown and YAML)
│       ├── personas/                  # Multi-Stakeholder Matrix and Leadership Cockpit
│       ├── quality/                   # SemanticQualityScorer and quality rule evaluators
│       └── targets/                   # Platform-specific dialect adapters
└── tests/                             # Automated test suite
    ├── test_all_lenses_deep.py        # Stakeholder perspective deep tests
    ├── test_canonical_model.py        # Canonical model unit tests
    ├── test_cli.py                    # CLI command suite tests
    ├── test_cli_personas.py           # Stakeholder export tests
    ├── test_golden_regression.py      # Deterministic golden regression tests
    ├── test_inference_engine.py       # Topological inference engine tests
    ├── test_leadership_cockpit.py     # C-Level leadership cockpit tests
    ├── test_persona_contracts.py      # Governance contract schema validations
    ├── test_stage3_governance_quality.py
    ├── fixtures/                      # Enterprise test fixtures and schemas
    ├── golden/                        # Deterministic golden reference files
    └── Massive Stress Test/           # High-volume stress suites
```

---

## 7. Execution Protocol and CI/CD Automation

### 7.1. Prerequisites and Installation

SemanticFlow requires **Python 3.10 or higher**:

```bash
# Clone the repository
git clone <repository_url>
cd SemanticFlow

# Initialize and activate an isolated virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with development dependencies
pip install -e ".[dev]"
```

### 7.2. CLI Commands for Pipelines and Local Operation

```bash
# 1. Inspect relational structure and verify inferred entity roles
semanticflow inspect --input docs/architecture/esquema_relacional.md

# 2. Validate the cQS Quality Gate (ideal for automated CI/CD pipeline steps)
semanticflow validate --input docs/architecture/esquema_relacional.md --min-score 75.0

# 3. Headlessly compile relational schema into native TMDL / PBIP for Microsoft Fabric
semanticflow compile --input docs/architecture/esquema_relacional.md --output output/PBIP --name "CommercialModel"

# 4. Generate C-Level Data Leadership Cockpit in the console
semanticflow cockpit --input docs/architecture/esquema_relacional.md --format human

# 5. Export Multi-Stakeholder Views and Cockpit artifacts in Markdown and JSON
semanticflow personas export --input docs/architecture/esquema_relacional.md --output output/personas

# 6. Generate enterprise Data Dictionary and Mermaid ERD diagrams
semanticflow docgen --input docs/architecture/esquema_relacional.md --output output/docs
```

### 7.3. Quality Assurance and Testing Suite

```bash
# Execute the full automated test suite (71 tests)
pytest -v

# Validate deterministic golden regression to prevent unintended semantic changes
pytest tests/test_golden_regression.py

# Verify code style and static type safety
ruff check .
mypy src/
```

---

## 8. Enterprise Domain Glossary

* **Semantic Modeling as Code (SMaC):** A DataOps discipline that defines, versions, and validates analytical semantic models using declarative code files stored in Git rather than manual GUI modifications.
* **Microsoft Fabric Git Integration:** Microsoft Fabric's native capability to synchronize cloud workspaces with Azure DevOps or GitHub repositories using plain text model definitions.
* **Tabular Model Definition Language (TMDL):** A folder-based, plain-text declarative syntax developed by Microsoft to represent Power BI and Analysis Services semantic model metadata.
* **Power BI Project (`.pbip`):** A developer-focused file format that stores report and dataset definitions in individual text files, enabling seamless multi-developer collaboration in Git.
* **Semantic Quality Score ($cQS$):** A continuous objective score $[0, 100]$ measuring architectural integrity, governance completeness, PII exposure risks, and relational cleanliness.
* **Multi-Stakeholder Governance Matrix:** A multidimensional framework projecting the model across four corporate pillars (Governance, Cloud FinOps, Analytics, and Business).
* **Data Leadership Cockpit:** An aggregated executive summary diagnosing model maturity and providing prioritized governance directives for Chief Data Officers (CDO).

---

## 9. License and Enterprise Governance

SemanticFlow is open-source software licensed under the **Apache 2.0** License. For contribution guidelines and extensible architecture specifications, refer to [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/](docs/).
