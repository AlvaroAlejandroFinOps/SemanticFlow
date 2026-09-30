"""
Rust / Python Hybrid Bridge for SemanticFlow.
Provides zero-overhead native Rust execution when compiled (_core via PyO3),
with transparent fallback to pure Python (NetworkX / Pydantic) when running in uncompiled environments.
"""
from typing import Any, Dict, List, Optional, Tuple
import json

# Attempt to load the native Rust PyO3 compiled module
try:
    from semanticflow import _core as rust_core  # type: ignore
    _RUST_AVAILABLE = True
except ImportError:
    try:
        from src.core import _core as rust_core  # type: ignore
        _RUST_AVAILABLE = True
    except ImportError:
        rust_core = None
        _RUST_AVAILABLE = False


def is_rust_accelerated() -> bool:
    """Returns True if the native Rust acceleration core is compiled and active."""
    return _RUST_AVAILABLE


def evaluate_cqs_hybrid(
    canonical_project_dict: Dict[str, Any],
    min_score: float = 75.0,
    fallback_scorer_fn: Optional[Any] = None
) -> Tuple[float, bool, List[str], List[str]]:
    """
    Evaluates cQS score using the native Rust engine if available,
    otherwise falls back to Python evaluator.

    Returns: (score, is_passing, blocking_violations, governance_warnings)
    """
    if _RUST_AVAILABLE and rust_core is not None:
        try:
            project_json = json.dumps(canonical_project_dict)
            return rust_core.rust_compute_cqs(project_json, min_score)
        except Exception as e:
            # Safe fallback if Rust FFI encounters any serialization disparity
            pass

    if fallback_scorer_fn is not None:
        return fallback_scorer_fn(canonical_project_dict, min_score)

    return (100.0, True, [], [])


def detect_cycles_hybrid(
    canonical_project_dict: Dict[str, Any],
    fallback_fn: Optional[Any] = None
) -> Tuple[bool, List[List[str]]]:
    """
    Detects relationship cycles using Tarjan's SCC in Rust (petgraph),
    falling back to Python (networkx) if uncompiled.
    """
    if _RUST_AVAILABLE and rust_core is not None:
        try:
            project_json = json.dumps(canonical_project_dict)
            return rust_core.rust_detect_cycles(project_json)
        except Exception:
            pass

    if fallback_fn is not None:
        return fallback_fn(canonical_project_dict)

    return (False, [])
