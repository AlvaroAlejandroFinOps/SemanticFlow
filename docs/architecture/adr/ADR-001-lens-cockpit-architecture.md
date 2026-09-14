# ADR-001: Persona Lens Framework and Data Leadership Cockpit Architecture

## Status
Accepted

## Context
SemanticFlow initially featured a flat, static 3-persona view generator (`PersonaViewGenerator` in `src/core/personas/views.py`) generating basic string summaries and entity lists. Modern enterprise data organizations require specialized perspectives across 10 discrete roles (Analytics Leader, Data Engineer, Analytics Engineer, BI Developer, Data Governance Officer, Data Product Manager, FinOps Specialist, AI Systems Engineer, Business Consumer, and Compliance Auditor), along with an aggregate Executive/Data Leadership Cockpit for C-level data decision making.

## Decision
1. Introduce a pluggable **Persona Lens Framework** where each Persona is represented by a dedicated, strongly-typed Lens implementing the `PersonaLens` interface.
2. Create an aggregate **Data Leadership Cockpit** that synthesizes individual lens projections into cross-functional maturity scores, alignment matrices, RACI responsibilities, and executive telemetry.
3. Decouple persona models from the compiler's canonical AST while allowing bidirectional enrichment via deterministic projection.
4. Provide structured outputs in Markdown, JSON, and Mermaid formats with zero external cloud dependencies.

## Consequences
- **Positive**: Rich, tailored views for all organizational roles; centralized data leadership metrics; modular and extensible architecture.
- **Negative**: Increased model complexity and contract surface area.
- **Mitigation**: Comprehensive test suite with contract validation and automated fixture testing.
