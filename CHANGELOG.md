# Changelog

All notable changes to the **SemanticFlow** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-10-17

### Security
- **Strict Input Sanitization & Path Traversal Eradication**:
  - Implemented `sanitize_company_id` using strict regex whitelisting (`^[a-zA-Z0-9_-]+$`) in `src/core/security/sanitize.py` and `artifacts/SemanticFlow/run_pipeline.py`.
  - Added `resolve_within` boundary checks preventing directory traversal out of input and workspace roots.
  - Hardened `PbipWriter` with `safe_filename` preventing table names from traversing outside `tables/`.
  - Escaped column names and CSV paths in Power Query M scripts in `src/core/emitter/table_emitter.py`.
- **Pre-Execution Secret Scanner**:
  - Implemented `src/core/security/secret_scanner.py` scanning schemas and profiles for Azure AD Client Secrets, Bearer tokens, and private keys without leaking secret values to logs or LLM context.
  - Added credential mask rules to `.agentignore`.
  - Added sensitive property name rejection to `schemas/project_governance.schema.json`.
- **DAX Lexical Sandboxing & Anti-Injection**:
  - Implemented `src/core/quality/dax_validator.py` with delimiter balancing (`()`, `[]`, `{}`), string literal isolation, and prohibition of administrative escape statements (`EVALUATE`, `DEFINE`, `DROP`, `EXEC`).
  - Escaped single quotes in `src/core/engine/dax_generator.py`.

### Added
- **Quality Gate (cQS) Rules D-011 and D-012**:
  - Rule D-011 (`validate_direct_lake_compatibility`): Flags unpartitioned DATETIME attributes on FACT tables and active Many-to-Many (`N:N`) relationships in Microsoft Fabric Direct Lake models.
  - Rule D-012 (`validate_vertipaq_performance`): Identifies high-cardinality `FILTER(ALL())` antipatterns and bidirectional cross-filtering involving fact tables.
- **Zero-Diff Deterministic Invariant**:
  - Canonical lexicographical ordering across tables, columns, measures, and relationships in `PbipWriter`, `TableEmitter`, `ModelEmitter`, `RelationshipEmitter`, `RelationshipResolver`, and `DbtSemanticEmitter`.

---

## [2.0.0-rc1] - 2026-09-20

### Added
- **Data Leadership Cockpit Isolated Sub-Package (`src/core/leadership/`)**:
  - Full modularization of 8 leadership telemetry domains: `portfolio.py`, `health.py`, `ownership.py`, `capability_gaps.py`, `team_dependencies.py`, `delivery_flow.py`, `value_indicators.py`, and `risk.py`.
  - Zero coupling between individual lens implementations and leadership aggregation logic.
- **10 Core Canonical Personas & 6 Specialized Extensions**:
  - Complete implementation of the 10 Core Canonical Organizational Personas: `DataAnalyst`, `AnalyticsEngineer`, `DataEngineer`, `DataScientist`, `BiDeveloper`, `DataArchitect`, `DataGovernanceOfficer`, `PlatformEngineer`, `DomainOwner`, and `AuditRisk`.
  - 6 Specialized Extensions: `AiSystemsEngineer`, `AnalyticsLeader`, `BusinessConsumer`, `ComplianceAuditor`, `DataProductManager`, and `FinOpsSpecialist`.
- **Output Safety & Defense-in-Depth**:
  - `PbipWriter` temporary atomic staging directory with rollback on compilation failure.
  - Root directory overwrite protection rejecting writes to system volumes.
  - Automatic PII masking and redaction for consumer-facing persona lenses.
- **Continuous Integration & Quality Automation**:
  - Multi-OS (`ubuntu-latest`, `windows-latest`, `macos-latest`) and multi-version (`Python 3.10, 3.11, 3.12`) GitHub Actions CI pipeline (`.github/workflows/ci.yml`).
  - Automated Ruff linting, Mypy static typing verification, and deterministic Golden Regression test suites.
- **Comprehensive Global Audit Suite**:
  - 13 formal audit deliverable artifacts documenting executive status, claim verification, checklist items, architecture gap analysis, security, test coverage, and prioritized remediation backlog.

### Changed
- Refactored `src/core/personas/cockpit.py` into a thin backward-compatible adapter delegating to `src/core/leadership/engine.py`.
- Enforced strict deterministic normalization for Golden Regression tests across dynamic ISO timestamps.

### Removed
- Removed unreferenced dead code `src/core/engine/inference.py`.

---

## [1.2.0] - 2026-09-14

### Added
- **Data Leadership Cockpit V1**: Initial executive synthesis engine and markdown reporting.
- **Persona Lens Framework**: Role-tailored filtering, RACI responsibility assignments, and team interaction SLAs.
- **Golden Regression Suite**: Deterministic byte-for-byte baseline comparisons for Metro Santiago and Enterprise Retail models.
- **PII Governance Inheritance**: Semantic quality rules enforcing sensitivity classification and data ownership tags.

### Changed
- Unified AST canonical representations across Markdown and YAML parsers.
- Enhanced TMDL emitter with DAX measure formatting strings and folder hierarchies.

---

## [1.1.0] - 2026-09-01

### Added
- **Multi-Dialect Capability Planner**: Compatibility matrix analysis for Power BI, Looker, and dbt Semantic Layer targets.
- **Enterprise Fixtures**: Multi-domain retail schema fixture with complex snowflake topologies and KPI definitions.
- **Typer CLI Interface**: Commands for `inspect`, `compile`, `personas list`, `explain`, and `cockpit`.

---

## [1.0.0] - 2026-08-15

### Added
- Initial release of the **SemanticFlow** compiler core.
- Markdown table schema parser (`MarkdownSchemaParser`) with relationship inference.
- Canonical Semantic Model (`CanonicalSemanticProject`) with Pydantic validation.
- Power BI TMDL and PBIP project emitter (`TmdlEmitter`, `PbipWriter`).
- Massive stress testing suite validating synthetic schema compilation up to 100+ entities.
