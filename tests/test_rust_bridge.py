"""
Tests for the Rust / Python Hybrid Bridge.
"""
from src.core.rust_bridge import is_rust_accelerated, evaluate_cqs_hybrid, detect_cycles_hybrid


def test_rust_bridge_fallback():
    # In non-compiled environments, is_rust_accelerated() should report False gracefully
    accelerated = is_rust_accelerated()
    assert isinstance(accelerated, bool)

    dummy_project = {
        "project_name": "TestProject",
        "entities": [
            {
                "id": "fact_sales",
                "name": "fact_sales",
                "role": "FACT",
                "description": "Sales fact table",
                "attributes": [
                    {"id": "fact_sales.id", "name": "id", "data_type": "INT64", "is_key": True, "is_hidden": False, "description": "PK", "is_pii": False}
                ],
                "metrics": []
            }
        ],
        "relationships": []
    }

    # Test cQS evaluation with fallback
    def mock_fallback(proj, min_score):
        return (95.0, True, [], ["Sample warning"])

    score, passing, blocking, warnings = evaluate_cqs_hybrid(dummy_project, min_score=75.0, fallback_scorer_fn=mock_fallback)
    assert score == 95.0
    assert passing is True
    assert len(warnings) == 1

    # Test cycle detection with fallback
    def mock_cycles(proj):
        return (False, [])

    has_cycles, cycle_nodes = detect_cycles_hybrid(dummy_project, fallback_fn=mock_cycles)
    assert has_cycles is False
    assert cycle_nodes == []
