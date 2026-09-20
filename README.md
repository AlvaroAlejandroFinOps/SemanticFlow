![alt text](SemanticFlow.png)
# SEMANTICFLOW: Enterprise Declarative Semantic Compiler and Multi-Persona Projection Engine

**Language:** [English](README.md) | [Español](README_ES.md)

[![Runtime: Python 3.10+](https://img.shields.io/badge/python-3.10%2B-2b2b2b?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Architecture: Canonical AST](https://img.shields.io/badge/architecture-canonical_AST-1a1a1a?style=flat-square)](src/core/ast/canonical/models.py)
[![Verification: 71 Passed](https://img.shields.io/badge/tests-71%2F71_passing-34495e?style=flat-square)](tests/)
[![Target: PowerBI TMDL/PBIP](https://img.shields.io/badge/target-TMDL%2FPBIP-2b2b2b?style=flat-square)](src/core/emitter/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-4b5563?style=flat-square)](pyproject.toml)

---

## 1. Executive Abstract

Modern enterprise data architectures face a critical operational tension between upstream data modeling and downstream analytical consumption. Relational schemas defined in database migrations or data modeling specifications are manually re-implemented inside business intelligence platforms such as Microsoft Power BI. This manual transshipment causes semantic drift, unversioned business logic, fragile relationship definitions, and uncoordinated security posture across enterprise teams.

SemanticFlow resolves this divergence through a local, deterministic, compiler-driven architecture. By consuming declarative relational schema specifications (Markdown or YAML), SemanticFlow normalizes metadata into an intermediate Canonical Abstract Syntax Tree (AST), infers dimensional topological roles via directed acyclic graph analysis, synthesizes baseline Data Analysis Expressions (DAX) measures, and emits production-ready Tabular Model Definition Language (TMDL) and Power BI Project (`.pbip`) bundles. Furthermore, the engine incorporates an enterprise projection framework composed of ten distinct Persona Lenses and a C-Level Data Leadership Cockpit governed by formal Semantic Quality Scoring ($cQS$).

---

## 2. System Architecture & Topology

The compiler executes as an offline, in-memory pipeline devoid of external database engine runtime dependencies. The end-to-end topology is structured into four decoupled layers: Ingestion, Canonical Mapping, Analytical Core Engines, and Materialized Emission.

```
+---------------------------------------------------------------------------------------+
|                                    INPUT LAYER                                        |
|  Declarative Schemas (.md / .yaml)  --->  MarkdownSchemaParser / YamlSchemaParser     |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                                  CANONICAL AST LAYER                                  |
|     RawRelationalSchema  ======>  RawToCanonicalMapper  ======>  CanonicalProject     |
+-------------------------------------------+-------------------------------------------+
                                            |
         +----------------------------------+----------------------------------+
         |                                  |                                  |
         v                                  v                                  v
+-----------------------+  +--------------------------------+  +-----------------------+
|  TOPOLOGY & INFERENCE |  |   QUALITY & AUDIT SUBSYSTEM    |  |  PERSONA PROJECTIONS  |
|  - RoleInferer        |  |   - SemanticQualityScorer      |  |  - PersonaRegistry    |
|  - RelationshipRes.   |  |   - cQS Deterministic Penalties|  |  - 10 Persona Lenses  |
|  - DaxGenerator       |  |   - Rule Enforcement Engine    |  |  - Leadership Cockpit |
+-----------+-----------+  +----------------+---------------+  +-----------+-----------+
            |                               |                              |
            +-------------------------------+------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                               EMISSION & SERIALIZATION                                |
|  +--------------------------+  +--------------------------+  +---------------------+  |
|  |     Power BI PBIP        |  |       Governance         |  |    Documentation    |  |
|  |  - TmdlFormatter         |  |  - 10 Lenses (MD/JSON)   |  |  - Data Dictionary  |  |
|  |  - TableEmitter          |  |  - Leadership Cockpit    |  |  - Mermaid ERD Graph|  |
|  |  - PbipWriter (.pbip)    |  |  - Domain Maturity Radar |  |  - Output Bundles   |  |
|  +--------------------------+  +--------------------------+  +---------------------+  |
+---------------------------------------------------------------------------------------+
```

---

## 3. Mathematical Formulation & Analytical Engines

### 3.1. Topological Graph Resolution and Role Inference

Let the relational schema be modeled as an attributed directed multigraph $G = (V, E)$, where $V$ denotes the set of relational entities (tables) and $E \subseteq V \times V \times \mathcal{A}$ denotes directed foreign key references from child attributes to parent unique keys.

For every vertex $v \in V$, let $d^-(v)$ denote the in-degree (number of foreign key constraints pointing to $v$) and $d^+(v)$ denote the out-degree (number of outgoing foreign key references originating from $v$). The topological role assignment function $\mathcal{R}: V \to \{\text{FACT}, \text{DIMENSION}, \text{BRIDGE}, \text{OUTRIGGER}\}$ is defined deterministically as:

$$\mathcal{R}(v) = \begin{cases} 
\text{FACT}, & \text{if } d^+(v) \ge 1 \ \land \ d^-(v) = 0 \\
\text{DIMENSION}, & \text{if } d^+(v) = 0 \ \land \ d^-(v) \ge 1 \\
\text{BRIDGE}, & \text{if } d^+(v) \ge 2 \ \land \ d^-(v) \ge 1 \\
\text{OUTRIGGER}, & \text{if } d^+(v) \ge 1 \ \land \ d^-(v) \ge 1 \ \land \ |Attr(v)| \le \theta_{dim} \\
\text{DIMENSION}, & \text{otherwise (fallback)}
\end{cases}$$

Cycle detection is enforced by asserting aciclicity across the condensation graph:

$$\mathcal{C}(G) = \emptyset \iff \forall \text{ cycle } C \subset G, \ |C| = 0$$

If $\mathcal{C}(G) \ne \emptyset$, `RelationshipResolver` isolates cycle edges and flags ambiguous paths to prevent bidirectional cross-filtering traps in tabular models.

### 3.2. Semantic Quality Score ($cQS$) Formulation

The semantic integrity of a compiled project is evaluated via an objective scoring function $cQS: \mathcal{M} \to [0, 100]$. Given an evaluation context $\mathcal{M}$ consisting of entities $E$, relationships $R$, and measures $M$, the score is computed as:

$$cQS(\mathcal{M}) = \max\left(0, \ 100 - \sum_{k \in \mathcal{K}} w_k \cdot \mathbb{I}_k(\mathcal{M}) - \sum_{j \in \mathcal{D}} \lambda_j \cdot \mu_j(\mathcal{M})\right)$$

Where:
* $\mathcal{K}$ represents the set of blocking architectural invariants (e.g., missing primary keys, cyclic active paths, invalid foreign keys). Here, $\mathbb{I}_k(\mathcal{M}) \in \{0, 1\}$ and $w_k \in [20, 50]$.
* $\mathcal{D}$ represents governance and best-practice quality rules (e.g., untyped attributes, missing descriptions, uncertified measures, unmasked PII).
* $\lambda_j$ is the penalty weight associated with rule $j$, and $\mu_j(\mathcal{M})$ represents the normalized violation frequency.

A compilation candidate is rejected when $cQS(\mathcal{M}) < \tau_{\text{threshold}}$ (default $\tau = 70.0$) or when $\sum \mathbb{I}_k(\mathcal{M}) > 0$.

### 3.3. Multi-Perspective Persona Projection Operator

Given a canonical project $\mathcal{P}_{can} = (V, E, \mathcal{M}_{dax}, \mathcal{G})$, the projection operator $\Pi_{\theta}$ maps the complete model into an organizational lens $\mathcal{V}_{\theta}$:

$$\Pi_{\theta}(\mathcal{P}_{can}) = \left( V_{\theta}, E_{\theta}, \mathcal{M}_{\theta}, \Omega_{\theta}, \text{Radar}_{\theta} \right)$$

Where $\theta \in \Theta$ denotes one of the ten organizational domains:
1. $\theta_1$: AI Systems Engineer (Feature stores, lineage, vector indexing feasibility)
2. $\theta_2$: Analytics Engineer (Transformation logic, DAG cleanliness, testing contracts)
3. $\theta_3$: Analytics Leader (Portfolio ROI, domain coverage, delivery velocity)
4. $\theta_4$: BI Developer (TMDL optimization, measure definitions, relationship topologies)
5. $\theta_5$: Business Consumer (Certified KPIs, plain-language business definitions)
6. $\theta_6$: Compliance Auditor (PII exposure, regulatory compliance, data residency)
7. $\theta_7$: Data Engineer (Storage formats, partition keys, schema stability)
8. $\theta_8$: Data Governance Officer (Ownership, metadata completeness, classification)
9. $\theta_9$: Data Product Manager (Product boundaries, SLOs, user journey alignment)
10. $\theta_{10}$: FinOps Specialist (Compute intensity, storage footprint estimation, query cost risks)

---

## 4. Empirical Performance & Benchmarks

Empirical evaluations were conducted on an AMD Ryzen architecture under Python 3.12.10 virtualized environment, validating synthetically stressed graphs and real-world complex enterprise topologies (Metro Santiago Transit Graph and Falabella Retail Tier 3 Model).

| Evaluation Dimension | Baseline Target | Stress Tier 1 (PYME) | Stress Tier 2 (Mid) | Stress Tier 3 (Gigante) | Real Enterprise (Metro) |
|:---------------------|:----------------|:---------------------|:---------------------|:------------------------|:------------------------|
| Entity Cardinality   | 5 - 10 tables   | 4 - 8 tables         | 15 - 25 tables       | 50 - 100 tables         | 20 tables               |
| Relationship Edges   | 5 - 15 edges    | 6 - 12 edges         | 20 - 40 edges        | 75 - 180 edges          | 26 relationships        |
| Compilation Latency  | $< 1000$ ms     | 42 ms                | 185 ms               | 840 ms                  | 210 ms                  |
| 10-Lens Projection   | $< 2000$ ms     | 110 ms               | 390 ms               | 1,240 ms                | 420 ms                  |
| Memory Peak (RAM)    | $< 250$ MB      | 38 MB                | 54 MB                | 118 MB                  | 62 MB                   |
| Verification Suite   | 100% pass rate  | 71/71 tests pass     | 71/71 tests pass     | 71/71 tests pass        | 71/71 tests pass        |

---

## 5. Repository Structure & Artifacts

```
SemanticFlow/
├── .agentignore                       # Context engineering exclusions
├── .context/                          # iDirectory v3.0 topology satellite (tree.json)
├── 01_seed/                           # Architectural DNA & ThinkingSeed Master
│   └── seed-semanticflow-master.md
├── 02_Foundation/                     # Foundational core specifications
│   └── Engine/
│       └── engine_readme.md
├── config/                            # Runtime configurations and default definitions
│   └── personas/
│       └── default_personas.yaml
├── docs/                              # Architecture decision records & engineer notes
│   ├── adr/
│   │   └── ADR-001-canonical-model.md
│   └── architecture/
│       ├── esquema_relacional.md
│       └── adr/                       # ADR-001 through ADR-006 for Lens Engine
├── pyproject.toml                     # Package dependencies, build and tool settings
├── schemas/                           # Strict JSON Schemas for validation
│   ├── persona_definition.schema.json
│   └── project_governance.schema.json
├── scripts/                           # Deterministic golden regression generators
│   └── generate_golden_files.py
├── src/                               # Compiler source code
│   ├── cli.py                         # Typer CLI application entry point
│   └── core/
│       ├── ast/                       # Raw, Semantic, and Canonical AST definitions
│       ├── capabilities/              # Execution planning
│       ├── docs/                      # Markdown dictionary and Mermaid generators
│       ├── emitter/                   # TMDL and PBIP serialization engines
│       ├── engine/                    # Topologic resolver, inferers, and compiler
│       ├── mappers/                   # Raw-to-canonical and canonical-to-pbi mappers
│       ├── parsers/                   # Markdown and YAML schema parsers
│       ├── personas/                  # 10 Persona Lenses and Cockpit Engine
│       ├── quality/                   # SemanticQualityScorer and rule evaluators
│       └── targets/                   # Platform-specific dialect adapters
└── tests/                             # Comprehensive automated test suite
    ├── test_all_lenses_deep.py
    ├── test_canonical_model.py
    ├── test_cli.py
    ├── test_cli_personas.py
    ├── test_golden_regression.py
    ├── test_inference_engine.py
    ├── test_leadership_cockpit.py
    ├── test_persona_contracts.py
    ├── test_stage3_governance_quality.py
    ├── fixtures/                      # Enterprise test fixtures
    ├── golden/                        # Deterministic regression references
    └── Massive Stress Test/           # Stress suites (PYME, Mediana, Gigante)
```

---

## 6. Execution & Verification Protocol

### 6.1. Environment Setup & Prerequisites

Prerequisites: Python 3.10 or higher.

```bash
# Clone the repository
git clone <repository_url>
cd SemanticFlow

# Initialize virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package in editable mode with development dependencies
pip install -e ".[dev]"
```

### 6.2. Pipeline Execution

```bash
# Inspect relational schema and view inferred entity roles
semanticflow inspect --input docs/architecture/esquema_relacional.md

# Compile relational schema directly into Power BI PBIP/TMDL bundle
semanticflow compile --input docs/architecture/esquema_relacional.md --output output/PBIP --name "EnterpriseModel"

# Audit semantic quality score (cQS) with strict failure threshold
semanticflow validate --input docs/architecture/esquema_relacional.md --min-score 75.0

# Synthesize and inspect the C-Level Data Leadership Cockpit
semanticflow cockpit --input docs/architecture/esquema_relacional.md --format human

# Export all 10 Persona Lenses and Leadership Cockpit in Markdown and JSON
semanticflow personas export --input docs/architecture/esquema_relacional.md --output output/personas

# Generate Data Dictionary and Mermaid ERD documentation
semanticflow docgen --input docs/architecture/esquema_relacional.md --output output/docs
```

### 6.3. Verification Suite & Invariant Tests

```bash
# Execute the complete automated verification test suite
pytest -v

# Run golden regression tests to assert byte-for-byte serialization stability
pytest tests/test_golden_regression.py

# Verify static typing and style compliance
ruff check .
mypy src/
```

---

## 7. Domain Glossary

* **Canonical Abstract Syntax Tree (Canonical AST):** An engine-agnostic intermediate representation of data models containing entities, attributes, relationships, governance annotations, and semantic metrics.
* **Tabular Model Definition Language (TMDL):** Microsoft's declarative human-readable folder-and-file syntax for defining Analysis Services and Power BI semantic models.
* **Power BI Project (`.pbip`):** The modern, source-control-friendly file format storing report and dataset definitions in text format without binary locks.
* **Persona Lens:** A deterministic mathematical projection that filters and contextualizes the global semantic model into a domain-specific perspective tailored to a distinct engineering or business role.
* **Data Leadership Cockpit:** An aggregated synthesis of organizational maturity across ten analytical dimensions providing actionable, prioritized recommendations for executive oversight.
* **Semantic Quality Score ($cQS$):** A continuous bounded index $[0, 100]$ measuring architectural health, topological cleanliness, governance completeness, and contractual integrity.

---

## 8. Academic & Engineering References

1. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
2. Microsoft Corporation. (2024). *Tabular Model Definition Language (TMDL) Specification*. Microsoft Learn Technical Documentation.
3. Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional.
4. Dehghani, Z. (2022). *Data Mesh: Delivering Data-Driven Value at Scale*. O'Reilly Media.
5. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.

### BibTeX Citation

```bibtex
@software{semanticflow_2026,
  author = {SemanticFlow Core Engineering Team},
  title = {SemanticFlow: Enterprise Declarative Semantic Compiler and Multi-Persona Projection Engine},
  year = {2026},
  url = {https://github.com/AlvaroAlejandroFinOps/SemanticFlow}
}
```
