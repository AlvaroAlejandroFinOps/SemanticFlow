# SEMANTICFLOW: Enterprise-Grade Declarative Semantic Model Compiler & Quality Platform

**Language:** [English](README.md) | [Español](README_ES.md)

![Python Version](https://img.shields.io/badge/python-3.10%2B-1a1a1a?style=flat-square)
![Architecture](https://img.shields.io/badge/architecture-Canonical%20AST%20%2B%20Persona%20Lenses-2b2b2b?style=flat-square)
![Verification](https://img.shields.io/badge/verification-71%2F71%20PASSED-34495e?style=flat-square)
![License](https://img.shields.io/badge/license-Apache--2.0-4b5563?style=flat-square)

---

## 1. Executive Abstract

SemanticFlow is a vendor-agnostic, enterprise-grade semantic engineering platform designed to compile relational schemas into unified canonical semantic models, emit native Business Intelligence (BI) artifacts (Microsoft Power BI TMDL/PBIP), project tailored **Persona Lenses across 10 distinct enterprise roles**, and synthesize aggregate **C-Level Data Leadership Cockpits**.

The platform resolves structural fragility, vendor lock-in, and governance silos by decoupling syntax parsing from code generation. Through its intermediate Canonical AST, SemanticFlow enforces two-level cascading governance, deterministic non-destructive projections, NetworkX star-schema graph topology inference, and automated Semantic Quality Scoring ($cQS$).

---

## 2. System Architecture & Topology

```
+-----------------------------------------------------------------------------------+
|                                 RELATIONAL INPUTS                                 |
|            +-----------------------+     +-----------------------+                |
|            | Markdown Schemas (.md)|     |  YAML Schemas (.yaml) |                |
|            +-----------+-----------+     +-----------+-----------+                |
+------------------------|-----------------------------|----------------------------+
                         |                             |
                         v                             v
+-----------------------------------------------------------------------------------+
|                                SYNTAX PARSING LAYER                               |
|                     +-----------------------------------+                         |
|                     | Markdown & YAML Relational Parsers|                         |
|                     +-----------------+-----------------+                         |
+---------------------------------------|-------------------------------------------+
                                        v
+-----------------------------------------------------------------------------------+
|                            CANONICAL TRANSFORMATION LAYER                         |
|                   +---------------------------------------+                       |
|                   |   Raw AST to Canonical Semantic Mapper|                       |
|                   +-------------------+-------------------+                       |
|                                       |                                           |
|                                       v                                           |
|                   +---------------------------------------+                       |
|                   |       CanonicalSemanticProject        |                       |
|                   |  (Entities, Attributes, Metrics,      |                       |
|                   |   ProjectGovernance, Provenance)      |                       |
|                   +-------------------+-------------------+                       |
+---------------------------------------|-------------------------------------------+
                                        |
        +-------------------------------+-------------------------------+
        |                               |                               |
        v                               v                               v
+----------------------+     +----------------------+     +--------------------------+
| QUALITY & GOVERNANCE |     |   INFERENCE ENGINE   |     | PERSONA LENS FRAMEWORK   |
|  SemanticQualityScorer|     | NetworkX RoleInferer |     |  10 Domain Roles         |
|  cQS Evaluation (0-100|     |  SemanticExplainer   |     |  Leadership Cockpit      |
|  PII & Project Rules |     |  Provenance Engine   |     |  Override Classifier     |
+----------+-----------+     +----------+-----------+     +-------------+------------+
           |                            |                               |
           +----------------------------+-------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                              TARGET ADAPTATION LAYER                              |
|                    +------------------------------------------+                   |
|                    |          PowerBiTargetAdapter            |                   |
|                    |     (Canonical -> Power BI Model AST)    |                   |
|                    +------------------+-----------------------+                   |
+---------------------------------------|-------------------------------------------+
                                        v
+-----------------------------------------------------------------------------------+
|                              EMISSION & OUTPUT LAYER                              |
|            +-----------------------+     +-----------------------+                |
|            | TMDL Model Definitions|     |  PBIP Directory Bundle|                |
|            +-----------------------+     +-----------------------+                |
|            | Leadership Cockpit MD |     |  10x Persona Lens JSON|                |
|            +-----------------------+     +-----------------------+                |
+-----------------------------------------------------------------------------------+
```

---

## 3. Mathematical Formulation & Analytical Engines

### 3.1. Canonical Quality Score ($cQS$) Formulation

SemanticFlow computes an objective, normalized Semantic Quality Score $cQS \in [0, 100]$ evaluating the structural integrity, governance adherence, and documentation depth of a canonical project $P = (E, R, G)$.

$$cQS(P) = w_g \cdot S_{\text{grain}}(E) + w_m \cdot S_{\text{metric}}(M) + w_c \cdot S_{\text{cert}}(M) + w_r \cdot S_{\text{ratio}}(M)$$

Subject to weight normalization:

$$w_g + w_m + w_c + w_r = 1.0 \quad (w_g = 0.35, \, w_m = 0.25, \, w_c = 0.20, \, w_r = 0.20)$$

---

## 4. The 10 Enterprise Persona Lenses

SemanticFlow introduces 10 dedicated lenses implementing the `PersonaLens` interface, projecting tailored domain perspectives without mutating the underlying canonical AST:

| Persona ID | Role | Technical Depth | Primary Focus Areas |
| :--- | :--- | :--- | :--- |
| `analytics_leader` | `ANALYTICS_LEADER` | `EXECUTIVE` | Strategic Alignment, Business Value, Certified KPIs |
| `data_engineer` | `DATA_ENGINEER` | `TECHNICAL` | Ingestion Pipelines, Partitioning, Storage Formats |
| `analytics_engineer` | `ANALYTICS_ENGINEER` | `TECHNICAL` | Star Schema Topology, Metric Definitions, Grains |
| `bi_developer` | `BI_DEVELOPER` | `TECHNICAL` | Power BI / TMDL Models, DAX Measures, Formatting |
| `data_governance_officer`| `DATA_GOVERNANCE_OFFICER`| `SUMMARY` | Data Ownership, PII Sensitivity, Catalog Lineage |
| `data_product_manager` | `DATA_PRODUCT_MANAGER` | `SUMMARY` | Data Product Lifecycle, Consumer Adoption, SLAs |
| `finops_specialist` | `FINOPS_SPECIALIST` | `SUMMARY` | Analytical Query Cost, Cloud Capacity Attribution |
| `ai_systems_engineer` | `AI_SYSTEMS_ENGINEER` | `TECHNICAL` | Feature Store Readiness, Embeddings, Training Lineage |
| `business_consumer` | `BUSINESS_CONSUMER` | `EXECUTIVE` | Plain-Language Glossary, Self-Service Analytics |
| `compliance_auditor` | `COMPLIANCE_AUDITOR` | `EXHAUSTIVE` | Regulatory Traceability (GDPR/SOX), Provenance Audit |

### 4.1. Override Safety Classification Matrix

Custom organizational overrides configured via YAML/JSON are deterministically classified:

- **`SAFE`**: Cosmetic and presentation properties (`display_name`, `title`, `description`, `icon`, `aliases`). Applied without warnings.
- **`REVIEW_REQUIRED`**: Behavioral adjustments (`technical_depth`, `visible_object_types`, `focus_areas`). Applied with diagnostic audit logging.
- **`PROHIBITED`**: Invariants (`persona_id`, `role`, security guardrails). Enforced with `ConfigurationValidationError`.

---

## 5. CLI Command Reference

```bash
# 1. Compile relational schema to Power BI PBIP/TMDL
semanticflow compile -i schema.md -o output/PBIP

# 2. Project tailored Persona Lens perspective
semanticflow explain -i schema.md --persona executive
semanticflow explain -i schema.md --persona bi_engineer --format md
semanticflow explain -i schema.md --persona data_governance --format json

# 3. List all 10 registered Persona Lenses
semanticflow personas list

# 4. Export all 10 Persona Lenses and Leadership Cockpit
semanticflow personas export -i schema.md -o output/personas --formats md,json

# 5. Synthesize C-Level Data Leadership Cockpit
semanticflow cockpit -i schema.md
semanticflow cockpit -i schema.md -o output/cockpit
```

---

## 6. Verification and Regression Benchmark

The test suite contains 71 automated tests across unit, integration, stress, and deterministic golden-file regression suites:

```bash
.venv/Scripts/python.exe -m pytest tests/ -v
# 71 passed in 9.01s (100% PASS)
```

---

## 7. Citation & BibTeX

```bibtex
@software{semanticflow2026,
  author = {SemanticFlow Engineering Team},
  title = {SemanticFlow: Declarative Semantic Compiler, Persona Lens Framework and Leadership Cockpit},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/SemanticFlow/SemanticFlow}}
}
```
