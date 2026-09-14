# ADR-001: Vendor-Neutral Canonical Semantic Model Architecture

- **Status**: Approved
- **Date**: 2026-09-14
- **Authors**: SemanticFlow Core Team

## Context

SemanticFlow v0.1.0 was built directly around Microsoft Power BI concepts. Its internal semantic AST (src/core/ast/semantic.py) directly bakes in Power BI specific constructs such as SummarizeBy, compatibility_level, m_partition_expression, and DAX measures.

To evolve SemanticFlow into an enterprise semantic model engineering platform capable of supporting multi-target planning and future BI targets (without breaking Power BI reference generation), we need a vendor-neutral canonical model representation.

## Decision

We adopt the **Strangler Fig Pattern** to introduce a vendor-neutral **Canonical Semantic Model** in src/core/ast/canonical/.

1. **Non-Breaking Parallel Layer**: The existing Power BI AST (src/core/ast/semantic.py) remains untouched during transition.
2. **Canonical Entities**:
   - CanonicalSemanticProject: Root container.
   - SemanticEntity: Logical tabular analytical domain (Fact, Dimension, Bridge, Calculated).
   - SemanticAttribute: Neutral attributes (data types, key flags, hidden flags).
   - SemanticMetric: First-class business metrics (Base, Derived, Ratio, Cumulative, Snapshot, KPI) decoupled from target expressions.
   - SemanticRelationship: Neutral entity associations.
   - GovernanceMetadata & ProvenanceRecord: Built-in auditing, stewardship, PII flagging, and rule inference lineage.
   - Diagnostic: Structured multi-category diagnostics.
3. **Mappers**:
   - Raw AST → Canonical Model: Maps ingested raw relational schema into the canonical representation.
   - Canonical Model → Power BI AST: Translates canonical representation back to existing Power BI AST for TMDL/PBIP emission.

## Consequences

- **Positive**: 
  - Complete vendor neutrality at the core.
  - Zero regression in existing TMDL/PBIP generation.
  - Auditability and explainability built-in via ProvenanceRecord.
- **Negative**:
  - Requires maintaining temporary mapper bridges until the old AST is fully replaced in future stages.
