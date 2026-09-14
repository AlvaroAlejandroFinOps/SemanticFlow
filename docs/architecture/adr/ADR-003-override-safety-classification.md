# ADR-003: Override Safety Classification Framework

## Status
Accepted

## Context
Organizations need the ability to customize Persona definitions, titles, summaries, technical depths, and focus areas via configuration files (YAML/JSON). However, arbitrary overrides can corrupt semantic model integrity, break deterministic projection, or bypass security/governance invariants.

## Decision
Classify all configuration overrides into three deterministic safety levels:
1. **`SAFE`**: Purely presentation and labeling overrides (e.g., `display_name`, `title`, `description`, `aliases`, `icon`, `color_theme`). These are automatically applied without warnings or gating.
2. **`REVIEW_REQUIRED`**: Behavioral adjustments that modify visibility or depth (e.g., changing `technical_depth` level, expanding `visible_object_types`, customizing `metric_filters`, adjusting `responsibility_matrix`). These are applied but produce a `REVIEW_REQUIRED` diagnostic notification in the projection metadata.
3. **`PROHIBITED`**: Invariants that cannot be overridden via organization config (e.g., altering `persona_id`, bypassing PII masking rules, disabling diagnostic checks, mutating canonical AST relationships or entity types). Attempting a `PROHIBITED` override raises a `ConfigurationValidationError` and halts projection compilation.

## Consequences
- **Positive**: Maximum organizational flexibility while enforcing strict semantic and security guardrails.
- **Negative**: Configuration loader must validate every override against the classification schema before application.
- **Mitigation**: Implement `OverrideSafetyClassifier` with comprehensive unit tests for all override vectors.
