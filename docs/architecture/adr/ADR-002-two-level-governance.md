# ADR-002: Two-Level Governance Model and Asset Inheritance

## Status
Accepted

## Context
Previously, governance metadata (`GovernanceMetadata`) existed only at the granular level: on individual `SemanticEntity`, `SemanticAttribute`, and `SemanticMetric` instances. However, `views.py` attempted to access `project.governance` defensively. Furthermore, enterprise data architectures require project-level/domain-level governance (domain ID, data product lifecycle status, classification, compliance frameworks, project owner/steward, SLAs) that cascades down to child assets unless specifically overridden.

## Decision
1. Introduce a dedicated `ProjectGovernance` Pydantic model separate from asset-level `GovernanceMetadata`.
2. Add an optional `governance: Optional[ProjectGovernance] = None` field to `CanonicalSemanticProject`.
3. Establish a clear inheritance rule: Child entities, attributes, and metrics inherit project-level governance defaults (e.g., classification, domain, compliance frameworks, owner) when their own governance fields are unset.
4. Granular overrides at the asset level are explicitly preserved and take precedence over inherited project-level defaults.

## Consequences
- **Positive**: Clean separation of project/domain-wide governance from attribute-level metadata; avoids schema pollution; enables automated governance cascading and audit compliance.
- **Negative**: Resolvers must implement inheritance lookup logic.
- **Mitigation**: Implement a helper method `resolve_asset_governance()` to encapsulate cascading rules deterministically.
