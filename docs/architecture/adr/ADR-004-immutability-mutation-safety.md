# ADR-004: Immutability and Non-Destructive Projection

## Status
Accepted

## Context
A semantic compiler operates as a deterministic pipeline. If a persona lens projection or report generator mutates the in-memory `CanonicalSemanticProject` AST, downstream stages (such as TMDL code emission, quality scoring, or other lenses) could suffer non-deterministic bugs, state pollution, or race conditions.

## Decision
1. Persona Lenses must treat `CanonicalSemanticProject` as an immutable input.
2. Projections must construct new, independent `PersonaProjection` and `LeadershipCockpit` data structures without altering entities, metrics, or relationships in the canonical AST.
3. If deep transformation or synthetic attribute generation is required for a lens, the lens must work on deep copies or local projection views.
4. Add automated mutation-safety tests that assert AST checksums / hash equivalences before and after multi-lens projection execution.

## Consequences
- **Positive**: Strict determinism, side-effect-free projection, concurrency safety, predictable compilation.
- **Negative**: Slight memory overhead for projection models.
- **Mitigation**: Pydantic v2 efficient model instantiation and shallow references where safe.
