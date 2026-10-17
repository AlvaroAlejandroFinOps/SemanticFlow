# Data Governance, Quality & Ownership Lens

**Persona Role**: `DATA_GOVERNANCE_OFFICER` | **Technical Depth**: `SUMMARY`
**Generated At**: `2026-10-17T00:56:17.167537+00:00`

## Executive Summary

> [!NOTE]
> Asset ownership, PII privacy boundaries, certification lifecycle, and quality scores for esquema_estrella_unificado_santolaya.

### Focus Areas
- **Governance Compliance**
- **Modeling Quality**

## Metrics & KPIs Portfolio

_No certified metrics assigned to this primary scope._

## Entity Scope

- **Primary Entities (14)**: `dim_proyecto_obra`, `dim_tiempo`, `dim_tercero`, `dim_centro_costo`, `dim_partida_edt`, `dim_unidad_inmobiliaria`, `fact_evm_avance_obra`, `fact_compras_compromisos`, `fact_recepciones_bodega`, `fact_facturacion_contratista`, `fact_ventas_inmobiliarias`, `fact_postventa_servicio`, `seguridad_usuarios_obra`, `DIM_EMPRESA_SOCIEDAD`
- **Active Relationships**: 27

### Entity Topology Diagram
```mermaid
erDiagram
    dim_proyecto_obra {
        string role "Primary Asset"
    }
    dim_tiempo {
        string role "Primary Asset"
    }
    dim_tercero {
        string role "Primary Asset"
    }
    dim_centro_costo {
        string role "Primary Asset"
    }
    dim_partida_edt {
        string role "Primary Asset"
    }
    dim_unidad_inmobiliaria {
        string role "Primary Asset"
    }
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
```

## RACI Responsibility Matrix

| Task / Artifact | RACI Role | Description | Collaborators |
| :--- | :--- | :--- | :--- |
| Enterprise Data Governance & PII Classification | **ACCOUNTABLE** | Audits data sensitivity, enforces privacy tagging, approves domain certifications, and manages glossary. | COMPLIANCE_AUDITOR, ANALYTICS_ENGINEER |

## Cross-Functional Team Interactions

| Target Persona | Interaction Type | Frequency | Artifact / Interface | SLA / Expectation |
| :--- | :--- | :--- | :--- | :--- |
| **COMPLIANCE_AUDITOR** | approval | Milestone | `Enterprise Data Protection Audit Artifact` | Zero unauthorized PII exposures in production semantic datasets |

### Interaction Flow
```mermaid
sequenceDiagram
    actor Current as DATA_GOVERNANCE_OFFICER
    actor Target0 as COMPLIANCE_AUDITOR
    Current->>Target0: [APPROVAL] Enterprise Data Protection Audit Artifact (Milestone)
    Note over Current,Target0: SLA: Zero unauthorized PII exposures in production semantic datasets
```

## Actionable Recommendations

| ID | Priority | Title | Impact | Effort | Suggested Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GOV-REV-01` | **LOW** | Conduct Asset Ownership Re-Certification | Maintains active data stewardship and lineage validity | Low | Schedule quarterly review with domain stewards. |

## Domain Maturity Assessment

**Overall Score**: `92.5/100.0` (Optimizing)

| Maturity Dimension | Score | Level | Findings |
| :--- | :--- | :--- | :--- |
| PII & Privacy Protection | 90.0% | Optimizing | 0 PII attributes mapped |
| Stewardship & Ownership | 95.0% | Optimizing | 14/14 entities owned |

### Strengths
- Two-level cascading governance model
- Automated PII detection

### Areas for Improvement
- Continuous policy compliance verification
