# ADR-005: Backward Compatibility and Legacy Persona Adaptation

## Status
Accepted

## Context
The repository includes an existing `PersonaViewGenerator` in `src/core/personas/views.py` consumed by tests (such as `tests/test_stage4_hardening_personas.py`). The existing `PersonaType` enum contains `EXECUTIVE`, `DATA_GOVERNANCE`, `BI_ENGINEER`, `ANALYTIC_CONSUMER`, and `FINOPS`. To maintain absolute backward compatibility without breaking existing user code or test fixtures, existing APIs must remain fully functional.

## Decision
1. Leave `src/core/personas/views.py` untouched with its exact existing interfaces, types, and method signatures.
2. Implement a `legacy_adapter.py` module that allows bidirectional conversion between legacy `PersonaView` objects and modern `PersonaProjection` objects.
3. Preserve `ANALYTIC_CONSUMER` and `FINOPS` in the Lens registry as specialized lenses (with `FINOPS` serving as a dedicated Lens for cost, consumption, capacity, and ROI value tracking).
4. Export both modern Lens classes and legacy generators cleanly through `src/core/personas/__init__.py`.

## Consequences
- **Positive**: 100% test suite green across all historical test suites; zero disruption for legacy consumers; smooth migration path.
- **Negative**: Temporary dual-surface API for persona generation.
- **Mitigation**: Clear documentation and deprecation notices guiding users toward the modern `PersonaRegistry` and `PersonaProjector` API.
