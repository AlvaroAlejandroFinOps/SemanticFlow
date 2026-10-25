# Perspectiva de Negocio: Ejecución de Obras y Venta Inmobiliaria

**Persona Role**: `DOMAIN_OWNER` | **Technical Depth**: `SUMMARY`
**Generated At**: `2026-10-23T00:48:40.860637+00:00`

## Executive Summary

> [!NOTE]
> Domain data products, certified KPIs, business ownership, and strategic alignment for schema.

### Focus Areas
- **Business Value**
- **Pipeline Health**

## Metrics & KPIs Portfolio

_No certified metrics assigned to this primary scope._

## Entity Scope

- **Primary Entities (6)**: `fact_evm_avance_obra`, `fact_compras_compromisos`, `fact_recepciones_bodega`, `fact_facturacion_contratista`, `fact_ventas_inmobiliarias`, `fact_postventa_servicio`
- **Secondary Entities (8)**: `dim_proyecto_obra`, `dim_tiempo`, `dim_tercero`, `dim_centro_costo`, `dim_partida_edt`, `dim_unidad_inmobiliaria`, `seguridad_usuarios_obra`, `DIM_EMPRESA_SOCIEDAD`
- **Active Relationships**: 27

### Entity Topology Diagram
```mermaid
erDiagram
    fact_evm_avance_obra {
        string role "Primary Asset"
    }
    fact_compras_compromisos {
        string role "Primary Asset"
    }
    fact_recepciones_bodega {
        string role "Primary Asset"
    }
    fact_facturacion_contratista {
        string role "Primary Asset"
    }
    fact_ventas_inmobiliarias {
        string role "Primary Asset"
    }
    fact_postventa_servicio {
        string role "Primary Asset"
    }
```

## RACI Responsibility Matrix

| Task / Artifact | RACI Role | Description | Collaborators |
| :--- | :--- | :--- | :--- |
| Domain Data Product Accountability & Business Sign-Off | **ACCOUNTABLE** | Approves semantic data product definitions and certified business KPIs. | DATA_ANALYST, DATA_GOVERNANCE_OFFICER |

## Cross-Functional Team Interactions

| Target Persona | Interaction Type | Frequency | Artifact / Interface | SLA / Expectation |
| :--- | :--- | :--- | :--- | :--- |
| **DATA_ANALYST** | consultation | Sprint | `Domain Data Product Backlog` | Bi-weekly review |

### Interaction Flow
```mermaid
sequenceDiagram
    actor Current as DOMAIN_OWNER
    actor Target0 as DATA_ANALYST
    Current->>Target0: [CONSULTATION] Domain Data Product Backlog (Sprint)
    Note over Current,Target0: SLA: Bi-weekly review
```

## Actionable Recommendations

| ID | Priority | Title | Impact | Effort | Suggested Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `REC-DO-001` | **HIGH** | Promote Certified Domain Metrics to Production Status | Increases data product trust and executive adoption. | Low | Review domain KPIs with data governance officer for formal sign-off. |

## Domain Maturity Assessment

**Overall Score**: `89.0/100.0` (Defined)

| Maturity Dimension | Score | Level | Findings |
| :--- | :--- | :--- | :--- |
| Domain Ownership | 89.0% | Defined | Domain owner assigned |

### Strengths
- Clear business accountability
- Certified core KPIs

### Areas for Improvement
- Continuous consumer feedback telemetry
