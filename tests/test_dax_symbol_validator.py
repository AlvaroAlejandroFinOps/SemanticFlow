"""
Tests for DAX Symbol Table Validator, VertiPaq FinOps Rule D-012, and Concurrency FileLock.
Verifies QUAL_DAX_REF_001, QUAL_DAX_TYPE_001, QUAL_DAX_CYCLE_001, QUAL_CARD_001, and acquire_company_lock.
"""
import pytest
from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    DataType,
    EntityRole,
    SemanticAttribute,
    SemanticEntity,
    SemanticMetric,
)
from src.core.quality.dax_symbol_validator import SymbolTableDaxValidator
from src.core.quality.rules import validate_vertipaq_performance
from src.core.security.concurrency import acquire_company_lock


@pytest.fixture
def base_dax_project() -> CanonicalSemanticProject:
    return CanonicalSemanticProject(
        id="dax_test_proj",
        name="DaxTestProject",
        entities=[
            SemanticEntity(
                id="fact_orders",
                name="Fact_Orders",
                role=EntityRole.FACT,
                grain=["order_id"],
                estimated_rows=2_000_000,
                attributes=[
                    SemanticAttribute(id="o1", name="order_id", is_key=True, data_type=DataType.INT64),
                    SemanticAttribute(id="o2", name="amount", data_type=DataType.DECIMAL),
                    SemanticAttribute(id="o3", name="customer_name", data_type=DataType.STRING),
                ],
                metrics=[
                    SemanticMetric(id="m_total", name="Total_Amount", expression="SUM('Fact_Orders'[amount])"),
                ],
            ),
            SemanticEntity(
                id="dim_store",
                name="Dim_Store",
                role=EntityRole.DIMENSION,
                grain=["store_id"],
                attributes=[
                    SemanticAttribute(id="s1", name="store_id", is_key=True, data_type=DataType.INT64),
                    SemanticAttribute(id="s2", name="store_name", data_type=DataType.STRING),
                ],
            ),
        ],
    )


def test_dax_symbol_validator_clean_expression_passes(base_dax_project):
    """Verify valid DAX references produce zero symbol errors."""
    validator = SymbolTableDaxValidator(base_dax_project)
    diags = validator.validate_project()
    assert len(diags) == 0


def test_dax_symbol_validator_missing_table_error(base_dax_project):
    """Verify referencing a nonexistent table emits QUAL_DAX_REF_001."""
    base_dax_project.entities[0].metrics.append(
        SemanticMetric(
            id="m_bad_tab",
            name="Bad_Table_Metric",
            expression="SUM('NonExistent_Table'[amount])",
        )
    )
    validator = SymbolTableDaxValidator(base_dax_project)
    diags = validator.validate_project()
    assert any(d.code == "QUAL_DAX_REF_001" and "NonExistent_Table" in d.message for d in diags)


def test_dax_symbol_validator_missing_column_error(base_dax_project):
    """Verify referencing a nonexistent column in an existing table emits QUAL_DAX_REF_001."""
    base_dax_project.entities[0].metrics.append(
        SemanticMetric(
            id="m_bad_col",
            name="Bad_Column_Metric",
            expression="SUM('Fact_Orders'[non_existent_column])",
        )
    )
    validator = SymbolTableDaxValidator(base_dax_project)
    diags = validator.validate_project()
    assert any(d.code == "QUAL_DAX_REF_001" and "non_existent_column" in d.message for d in diags)


def test_dax_symbol_validator_local_vars_no_false_positives(base_dax_project):
    """Verify local variables declared with VAR ... RETURN do not produce false positive symbol errors."""
    base_dax_project.entities[0].metrics.append(
        SemanticMetric(
            id="m_var",
            name="Var_Metric",
            expression=(
                "VAR CurrentTotal = SUM('Fact_Orders'[amount]) "
                "VAR Multiplier = 1.19 "
                "RETURN CurrentTotal * Multiplier"
            ),
        )
    )
    validator = SymbolTableDaxValidator(base_dax_project)
    diags = validator.validate_project()
    ref_errors = [d for d in diags if d.code == "QUAL_DAX_REF_001"]
    assert len(ref_errors) == 0


def test_dax_symbol_validator_cyclic_dependency_direct(base_dax_project):
    """Verify direct cycle between two measures (M1 -> M2 -> M1) emits QUAL_DAX_CYCLE_001."""
    base_dax_project.entities[0].metrics.extend([
        SemanticMetric(id="m_a", name="Metric_A", expression="[Metric_B] + 10"),
        SemanticMetric(id="m_b", name="Metric_B", expression="[Metric_A] * 2"),
    ])
    validator = SymbolTableDaxValidator(base_dax_project)
    diags = validator.validate_project()
    assert any(d.code == "QUAL_DAX_CYCLE_001" for d in diags)


def test_dax_symbol_validator_cyclic_dependency_indirect(base_dax_project):
    """Verify indirect 3-way cycle (M1 -> M2 -> M3 -> M1) emits QUAL_DAX_CYCLE_001."""
    base_dax_project.entities[0].metrics.extend([
        SemanticMetric(id="m_1", name="Metric_1", expression="[Metric_2] + 1"),
        SemanticMetric(id="m_2", name="Metric_2", expression="[Metric_3] + 2"),
        SemanticMetric(id="m_3", name="Metric_3", expression="[Metric_1] + 3"),
    ])
    validator = SymbolTableDaxValidator(base_dax_project)
    diags = validator.validate_project()
    assert any(d.code == "QUAL_DAX_CYCLE_001" for d in diags)


def test_dax_symbol_validator_type_mismatch_string_aggregation(base_dax_project):
    """Verify numeric aggregation function SUM on a STRING column emits QUAL_DAX_TYPE_001."""
    base_dax_project.entities[0].metrics.append(
        SemanticMetric(
            id="m_type_err",
            name="Bad_Sum_String",
            expression="SUM('Fact_Orders'[customer_name])",
        )
    )
    validator = SymbolTableDaxValidator(base_dax_project)
    diags = validator.validate_project()
    assert any(d.code == "QUAL_DAX_TYPE_001" and "customer_name" in d.message for d in diags)


def test_vertipaq_finops_rule_detects_unindexed_fact_filter_all(base_dax_project):
    """Verify FILTER(ALL('Fact_Orders')) on high-cardinality table emits QUAL_VPAQ_FILTER_012."""
    base_dax_project.entities[0].metrics.append(
        SemanticMetric(
            id="m_filter_all",
            name="Vpaq_Antipattern",
            expression="CALCULATE([Total_Amount], FILTER(ALL('Fact_Orders'), [amount] > 100))",
        )
    )
    diags = validate_vertipaq_performance(base_dax_project)
    assert any(d.code == "QUAL_VPAQ_FILTER_012" for d in diags)


def test_vertipaq_finops_rule_presumes_high_cardinality_when_none():
    """Verify Fact entity without estimated_rows emits QUAL_CARD_001 and triggers QUAL_VPAQ_FILTER_012."""
    project = CanonicalSemanticProject(
        id="fact_none_rows",
        name="FactNoneRowsProject",
        entities=[
            SemanticEntity(
                id="f_no_card",
                name="Fact_No_Card",
                role=EntityRole.FACT,
                grain=["id"],
                estimated_rows=None,
                attributes=[
                    SemanticAttribute(id="id", name="id", is_key=True, data_type=DataType.INT64),
                ],
                metrics=[
                    SemanticMetric(
                        id="m_vpaq",
                        name="Vpaq_Metric",
                        expression="CALCULATE(COUNTROWS('Fact_No_Card'), FILTER(ALL('Fact_No_Card'), [id] > 0))",
                    )
                ],
            )
        ],
    )
    diags = validate_vertipaq_performance(project)
    codes = {d.code for d in diags}
    assert "QUAL_CARD_001" in codes
    assert "QUAL_VPAQ_FILTER_012" in codes


def test_concurrency_filelock_prevents_race_condition():
    """Verify acquire_company_lock prevents concurrent executions for the same company."""
    with acquire_company_lock("lock_test_co", timeout_seconds=1.0):
        # Nested attempt with small timeout should raise TimeoutError
        with pytest.raises(TimeoutError, match="No se pudo adquirir el bloqueo exclusivo"):
            with acquire_company_lock("lock_test_co", timeout_seconds=0.1):
                pass
