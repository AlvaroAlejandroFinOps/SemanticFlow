# ADR-006: Deterministic Evidence and Golden Files in Source Control

## Status
Accepted

## Context
SemanticFlow acts as an enterprise-grade compiler and governance engine. For a deterministic compiler, generated artifacts (TMDL files, Data Dictionaries, ERDs, Persona Lenses, Leadership Cockpit Markdown, JSON projections) serve as verifiable evidence of compilation correctness. Relying solely on in-memory ephemeral tests does not protect against subtle output regressions across versions.

## Decision
1. Maintain deterministic golden master files in version control under `tests/golden/`.
2. Generate golden files for standard benchmark projects (e.g., Metro Santiago and Enterprise Multi-Domain).
3. Include golden file regression tests that compare compiler output against committed golden artifacts line-by-line or structure-by-structure.
4. Establish a deterministic test runner with sorted key serialization and fixed timestamps (or normalized timestamps) to avoid false drift.

## Consequences
- **Positive**: Complete visual and programmatic diffs on any change in TMDL generation, documentation, or persona projection; zero silent regressions.
- **Negative**: Golden files require explicit updates when intentional formatting changes occur.
- **Mitigation**: Provide an automated `--update-golden` testing flag or script for controlled baseline updates.
