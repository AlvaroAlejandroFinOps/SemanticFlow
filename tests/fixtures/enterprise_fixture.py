"""
Enterprise-grade test fixture providing a rich CanonicalSemanticProject
for testing all 10 Persona Lenses and the Leadership Cockpit.
"""
import pytest
from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    DataType,
    Diagnostic,
    DiagnosticCategory,
    DiagnosticSeverity,
    EntityRole,
    GovernanceMetadata,
    MetricAdditivity,
    MetricType,
    ProjectGovernance,
    ProvenanceRecord,
    SemanticAttribute,
    SemanticEntity,
    SemanticMetric,
    SemanticRelationship,
)


def create_enterprise_project() -> CanonicalSemanticProject:
    """Constructs a production-scale enterprise CanonicalSemanticProject."""
    # 1. Project-level Governance
    proj_gov = ProjectGovernance(
        domain_id="DOMAIN-RETAIL-01",
        domain_name="Omnichannel Retail & E-Commerce",
        classification="Confidential",
        data_product_status="Certified",
        owner="VP of Analytics & AI",
        steward="Enterprise Data Governance Board",
        criticality="Tier-1 High Criticality",
        sla="99.95% Daily Refresh by 06:00 UTC",
        tags=["enterprise", "retail", "omnichannel", "production", "gold"],
        compliance_frameworks=["GDPR", "CCPA", "SOX-404", "PCI-DSS"],
        custom_properties={"business_unit": "Retail Global", "cost_center": "CC-90412"}
    )

    # 2. Entities & Attributes
    # Entity: fact_orders
    attr_order_id = SemanticAttribute(
        id="fact_orders.order_id",
        name="order_id",
        display_name="Order ID",
        data_type=DataType.STRING,
        is_key=True,
        governance=GovernanceMetadata(certification_status="CERTIFIED", tags=["identifier"])
    )
    attr_cust_fk = SemanticAttribute(
        id="fact_orders.customer_id",
        name="customer_id",
        display_name="Customer Key",
        data_type=DataType.STRING,
        is_key=True
    )
    attr_prod_fk = SemanticAttribute(
        id="fact_orders.product_id",
        name="product_id",
        display_name="Product Key",
        data_type=DataType.STRING,
        is_key=True
    )
    attr_store_fk = SemanticAttribute(
        id="fact_orders.store_id",
        name="store_id",
        display_name="Store Key",
        data_type=DataType.STRING,
        is_key=True
    )
    attr_order_datetime = SemanticAttribute(
        id="fact_orders.order_datetime",
        name="order_datetime",
        display_name="Order Timestamp",
        data_type=DataType.DATETIME
    )
    attr_net_amount = SemanticAttribute(
        id="fact_orders.net_amount",
        name="net_amount",
        display_name="Net Sales Amount",
        data_type=DataType.DECIMAL
    )
    attr_discount_amount = SemanticAttribute(
        id="fact_orders.discount_amount",
        name="discount_amount",
        display_name="Discount Amount",
        data_type=DataType.DECIMAL
    )
    attr_quantity = SemanticAttribute(
        id="fact_orders.quantity",
        name="quantity",
        display_name="Units Sold",
        data_type=DataType.INT64
    )

    metric_total_revenue = SemanticMetric(
        id="metric.total_revenue",
        name="Total Revenue",
        display_name="Total Net Revenue",
        description="Sum of all net order sales after discounts",
        metric_type=MetricType.KPI,
        additivity=MetricAdditivity.ADDITIVE,
        expression="SUM(fact_orders.net_amount)",
        format_string="$#,##0.00",
        unit="USD",
        governance=GovernanceMetadata(
            owner="VP Analytics",
            steward="Finance BI Team",
            certification_status="CERTIFIED",
            tags=["financial_kpi", "certified_metric"]
        ),
        target_expressions={"dax": "CALCULATE(SUM(fact_orders[net_amount]))", "sql": "SUM(fact_orders.net_amount)"}
    )

    metric_order_count = SemanticMetric(
        id="metric.order_count",
        name="Order Count",
        display_name="Total Orders",
        description="Count of distinct completed transactions",
        metric_type=MetricType.BASE,
        additivity=MetricAdditivity.ADDITIVE,
        expression="DISTINCTCOUNT(fact_orders.order_id)",
        governance=GovernanceMetadata(certification_status="CERTIFIED", tags=["operational_kpi"])
    )

    metric_aov = SemanticMetric(
        id="metric.average_order_value",
        name="Average Order Value",
        display_name="AOV",
        description="Average revenue per order transaction",
        metric_type=MetricType.RATIO,
        additivity=MetricAdditivity.NON_ADDITIVE,
        expression="[Total Revenue] / [Order Count]",
        numerator_metric_id="metric.total_revenue",
        denominator_metric_id="metric.order_count",
        format_string="$#,##0.00",
        governance=GovernanceMetadata(certification_status="CERTIFIED", tags=["financial_kpi"])
    )

    fact_orders = SemanticEntity(
        id="entity.fact_orders",
        name="fact_orders",
        role=EntityRole.FACT,
        description="Central transaction table recording omnichannel customer orders",
        grain=["order_id", "product_id"],
        attributes=[
            attr_order_id, attr_cust_fk, attr_prod_fk, attr_store_fk,
            attr_order_datetime, attr_net_amount, attr_discount_amount, attr_quantity
        ],
        metrics=[metric_total_revenue, metric_order_count, metric_aov],
        governance=GovernanceMetadata(
            owner="Commerce Operations Data Team",
            certification_status="CERTIFIED",
            tags=["core_fact", "gold_layer"]
        )
    )

    # Entity: dim_customers
    attr_c_id = SemanticAttribute(
        id="dim_customers.customer_id",
        name="customer_id",
        data_type=DataType.STRING,
        is_key=True
    )
    attr_c_name = SemanticAttribute(
        id="dim_customers.full_name",
        name="full_name",
        data_type=DataType.STRING,
        governance=GovernanceMetadata(is_pii=True, sensitivity_classification="Restricted", tags=["pii"])
    )
    attr_c_email = SemanticAttribute(
        id="dim_customers.email",
        name="email",
        data_type=DataType.STRING,
        governance=GovernanceMetadata(is_pii=True, sensitivity_classification="Restricted", tags=["pii", "contact"])
    )
    attr_c_segment = SemanticAttribute(
        id="dim_customers.segment",
        name="segment",
        data_type=DataType.STRING
    )
    attr_c_churn_score = SemanticAttribute(
        id="dim_customers.ai_churn_risk_score",
        name="ai_churn_risk_score",
        display_name="AI Predicted Churn Risk (0-1)",
        data_type=DataType.DOUBLE,
        governance=GovernanceMetadata(
            owner="AI/ML Systems Engineering",
            certification_status="CERTIFIED",
            tags=["ai_feature", "ml_prediction"]
        )
    )

    dim_customers = SemanticEntity(
        id="entity.dim_customers",
        name="dim_customers",
        role=EntityRole.DIMENSION,
        description="Master customer profiles with AI behavioral scoring and privacy controls",
        grain=["customer_id"],
        attributes=[attr_c_id, attr_c_name, attr_c_email, attr_c_segment, attr_c_churn_score],
        governance=GovernanceMetadata(
            owner="Customer Identity Governance Lead",
            steward="Privacy Officer",
            sensitivity_classification="Restricted",
            is_pii=True,
            certification_status="CERTIFIED",
            tags=["customer_360", "privacy_sensitive"]
        )
    )

    # Entity: dim_products
    dim_products = SemanticEntity(
        id="entity.dim_products",
        name="dim_products",
        role=EntityRole.DIMENSION,
        description="Master product catalog containing hierarchical categories and unit pricing",
        grain=["product_id"],
        attributes=[
            SemanticAttribute(id="dim_products.product_id", name="product_id", data_type=DataType.STRING, is_key=True),
            SemanticAttribute(id="dim_products.sku", name="sku", data_type=DataType.STRING),
            SemanticAttribute(id="dim_products.product_name", name="product_name", data_type=DataType.STRING),
            SemanticAttribute(id="dim_products.category", name="category", data_type=DataType.STRING),
            SemanticAttribute(id="dim_products.unit_price", name="unit_price", data_type=DataType.DECIMAL),
        ],
        governance=GovernanceMetadata(certification_status="CERTIFIED")
    )

    # Entity: dim_stores
    dim_stores = SemanticEntity(
        id="entity.dim_stores",
        name="dim_stores",
        role=EntityRole.DIMENSION,
        description="Store locations, regional distribution hubs, and digital channels",
        grain=["store_id"],
        attributes=[
            SemanticAttribute(id="dim_stores.store_id", name="store_id", data_type=DataType.STRING, is_key=True),
            SemanticAttribute(id="dim_stores.store_name", name="store_name", data_type=DataType.STRING),
            SemanticAttribute(id="dim_stores.region", name="region", data_type=DataType.STRING),
            SemanticAttribute(id="dim_stores.channel", name="channel", data_type=DataType.STRING),
        ],
        governance=GovernanceMetadata(certification_status="CERTIFIED")
    )

    # Entity: fact_cloud_consumption (FinOps)
    attr_fin_date = SemanticAttribute(id="fact_cloud_consumption.date", name="consumption_date", data_type=DataType.DATE)
    attr_fin_service = SemanticAttribute(id="fact_cloud_consumption.service", name="service_name", data_type=DataType.STRING)
    attr_fin_cost = SemanticAttribute(id="fact_cloud_consumption.cost", name="compute_cost_usd", data_type=DataType.DECIMAL)

    metric_total_compute = SemanticMetric(
        id="metric.total_compute_cost",
        name="Total Compute Cost USD",
        display_name="Cloud Compute Cost",
        description="Aggregated cloud compute expenditure across analytical clusters",
        metric_type=MetricType.BASE,
        expression="SUM(fact_cloud_consumption.compute_cost_usd)",
        format_string="$#,##0.00",
        unit="USD",
        governance=GovernanceMetadata(owner="FinOps Specialist", certification_status="CERTIFIED", tags=["finops_kpi"])
    )

    fact_cloud_consumption = SemanticEntity(
        id="entity.fact_cloud_consumption",
        name="fact_cloud_consumption",
        role=EntityRole.FACT,
        description="FinOps telemetry tracking semantic query compute costs and capacity usage",
        grain=["consumption_date", "service_name"],
        attributes=[attr_fin_date, attr_fin_service, attr_fin_cost],
        metrics=[metric_total_compute],
        governance=GovernanceMetadata(owner="FinOps Cloud Economics", certification_status="CERTIFIED", tags=["finops"])
    )

    # 3. Relationships
    rel_orders_customers = SemanticRelationship(
        id="rel_orders_customers",
        name="orders_to_customers",
        from_entity_id="entity.fact_orders",
        from_attribute_id="fact_orders.customer_id",
        to_entity_id="entity.dim_customers",
        to_attribute_id="dim_customers.customer_id",
        cardinality="N:1",
        is_active=True
    )
    rel_orders_products = SemanticRelationship(
        id="rel_orders_products",
        name="orders_to_products",
        from_entity_id="entity.fact_orders",
        from_attribute_id="fact_orders.product_id",
        to_entity_id="entity.dim_products",
        to_attribute_id="dim_products.product_id",
        cardinality="N:1",
        is_active=True
    )
    rel_orders_stores = SemanticRelationship(
        id="rel_orders_stores",
        name="orders_to_stores",
        from_entity_id="entity.fact_orders",
        from_attribute_id="fact_orders.store_id",
        to_entity_id="entity.dim_stores",
        to_attribute_id="dim_stores.store_id",
        cardinality="N:1",
        is_active=True
    )

    # 4. Diagnostics
    diag_1 = Diagnostic(
        code="SEM-GOV-001",
        severity=DiagnosticSeverity.INFO,
        category=DiagnosticCategory.GOVERNANCE,
        message="PII attributes detected in dim_customers with appropriate restricted classification.",
        object_id="entity.dim_customers"
    )

    return CanonicalSemanticProject(
        id="proj_enterprise_retail",
        name="EnterpriseRetailPlatform",
        version="2.5.0",
        description="Enterprise multi-domain semantic model for Omnichannel Retail, FinOps, and AI Predictions.",
        governance=proj_gov,
        entities=[fact_orders, dim_customers, dim_products, dim_stores, fact_cloud_consumption],
        relationships=[rel_orders_customers, rel_orders_products, rel_orders_stores],
        diagnostics=[diag_1]
    )


@pytest.fixture
def enterprise_canonical_project() -> CanonicalSemanticProject:
    """Pytest fixture returning the enterprise CanonicalSemanticProject."""
    return create_enterprise_project()
