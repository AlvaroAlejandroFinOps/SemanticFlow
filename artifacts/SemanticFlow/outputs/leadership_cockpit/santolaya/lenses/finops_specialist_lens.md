# Optimización de Capacity Units (SKU F8 Direct Lake) y Memoria VertiPaq

**Persona Role**: `FINOPS_SPECIALIST` | **Technical Depth**: `SUMMARY`
**Generated At**: `2026-10-23T00:48:40.860637+00:00`

## Executive Summary

> [!NOTE]
> Analytical query efficiency, cloud resource consumption, and cost attribution for schema.

### Focus Areas
- **Cost Capacity**
- **Visualization Efficiency**

## Metrics & KPIs Portfolio

### Certified Metrics
| Metric Name | Status | Type |
| :--- | :--- | :--- |
| **EVM_AC_Total** | Certified | KPI / Core Metric |
| **Compras_Monto_Comprometido** | Certified | KPI / Core Metric |

## Entity Scope

- **Primary Entities (4)**: `dim_centro_costo`, `FACT_EVM_AVANCE_OBRA`, `FACT_COMPRAS_COMPROMISOS`, `FACT_RECEPCIONES_BODEGA`
- **Active Relationships**: 27

### Entity Topology Diagram
```mermaid
erDiagram
    dim_centro_costo {
        string role "Primary Asset"
    }
    FACT_EVM_AVANCE_OBRA {
        string role "Primary Asset"
    }
    FACT_COMPRAS_COMPROMISOS {
        string role "Primary Asset"
    }
    FACT_RECEPCIONES_BODEGA {
        string role "Primary Asset"
    }
```

## RACI Responsibility Matrix

| Task / Artifact | RACI Role | Description | Collaborators |
| :--- | :--- | :--- | :--- |
| Semantic Query Cost & Cloud Attribution | **RESPONSIBLE** | Tracks analytical query costs, identifies expensive Cartesian DAX/SQL queries, and allocates cloud capacity. | DATA_ENGINEER, ANALYTICS_LEADER |

## Cross-Functional Team Interactions

| Target Persona | Interaction Type | Frequency | Artifact / Interface | SLA / Expectation |
| :--- | :--- | :--- | :--- | :--- |
| **DATA_ENGINEER** | consultation | Monthly | `Cloud Cost & Capacity Telemetry Report` | Cost run-rate within quarterly budget limits |

### Interaction Flow
```mermaid
sequenceDiagram
    actor Current as FINOPS_SPECIALIST
    actor Target0 as DATA_ENGINEER
    Current->>Target0: [CONSULTATION] Cloud Cost & Capacity Telemetry Report (Monthly)
    Note over Current,Target0: SLA: Cost run-rate within quarterly budget limits
```

## Actionable Recommendations

| ID | Priority | Title | Impact | Effort | Suggested Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `FIN-01` | **MEDIUM** | Establish Cost Attribution Tags | Enables showback/chargeback to consuming business departments | Low | Configure custom_properties with cost_center in project governance. |
| `FINOPS_SPECIALIST-OVR-GUIDE-001` | **MEDIUM** | Directriz Local: Monitorear paginación Delta Parquet en OneLake para evitar f | Alineación operativa local de la compañía | Bajo | Monitorear paginación Delta Parquet en OneLake para evitar fallback a DirectQuery sobre SKU F8. |
| `FINOPS_SPECIALIST-OVR-GUIDE-002` | **MEDIUM** | Directriz Local: Evitar expresiones FILTER(ALL()) sobre FACT_EVM_AVANCE_OBRA  | Alineación operativa local de la compañía | Bajo | Evitar expresiones FILTER(ALL()) sobre FACT_EVM_AVANCE_OBRA y FACT_COMPRAS_COMPROMISOS (Regla D-012). |

## Domain Maturity Assessment

**Overall Score**: `72.0/100.0` (Managed)

| Maturity Dimension | Score | Level | Findings |
| :--- | :--- | :--- | :--- |
| Cost Transparency | 72.0% | Defined | 0 cost telemetry metrics |
| Capacity Governance | 85.0% | Defined | Resource limits established |

### Strengths
- Unit economics metrics present
- Cost center alignment

### Areas for Improvement
- Real-time query cost telemetry pipeline
