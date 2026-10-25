# Data Leadership Cockpit: schema
**Version**: `1.0.0` | **Generated At**: `2026-10-23T00:48:40.860637+00:00`

## Executive Overview
> [!IMPORTANT]
> Leadership Cockpit for 'schema' (v1.0.0). Data Product Status: Certified (CONFIDENTIAL). Encompassing 14 entities, 27 relationships, and 0 certified metrics across 10 active organizational domains.

## Governance & Portfolio Health

| Metric | Value |
| :--- | :--- |
| Data Product Status | **Certified** |
| Classification | **CONFIDENTIAL** |
| Executive Owner | **Gerencia General y Control de Gestión Santolaya** |
| Entities Governed | **14** |
| Active Relationships | **27** |
| Certified Kpis Count | **0** |
| Diagnostics Count | **0** |

## Domain Maturity Radar

| Persona / Domain | Maturity Score | Target Band |
| :--- | :--- | :--- |
| **CUSTOM** | `80.0%` | Optimal (>=80%) |
| **AI_SYSTEMS_ENGINEER** | `88.0%` | Optimal (>=80%) |
| **ANALYTICS_ENGINEER** | `80.0%` | Optimal (>=80%) |
| **ANALYTICS_LEADER** | `54.0%` | Attention Required (<60%) |
| **AUDIT_RISK** | `94.0%` | Optimal (>=80%) |
| **BI_DEVELOPER** | `90.0%` | Optimal (>=80%) |
| **BUSINESS_CONSUMER** | `88.0%` | Optimal (>=80%) |
| **COMPLIANCE_AUDITOR** | `94.0%` | Optimal (>=80%) |
| **DATA_ANALYST** | `88.0%` | Optimal (>=80%) |
| **DATA_ARCHITECT** | `92.0%` | Optimal (>=80%) |
| **DATA_ENGINEER** | `45.0%` | Attention Required (<60%) |
| **DATA_GOVERNANCE_OFFICER** | `92.5%` | Optimal (>=80%) |
| **DATA_PRODUCT_MANAGER** | `95.0%` | Optimal (>=80%) |
| **DATA_SCIENTIST** | `85.0%` | Optimal (>=80%) |
| **DOMAIN_OWNER** | `89.0%` | Optimal (>=80%) |
| **FINOPS_SPECIALIST** | `72.0%` | Satisfactory (>=60%) |
| **PLATFORM_ENGINEER** | `87.0%` | Optimal (>=80%) |

## Executive Priority Action Matrix

| ID | Priority | Title | Impact | Effort | Owner Persona |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `QG_SANTOLAYA_EVM_001` | **HIGH** | Consistencia de Partidas EVM con Centro de Costo | Gobernanza y confiabilidad del modelo de datos | Bajo | dim_centro_costo |
| `REC-JO-001` | **HIGH** | Auditoría de Curva S y Mitigación de Desviación SPI | Prevención de multas contractuales por atraso de entrega | Bajo | FACT_EVM_AVANCE_OBRA |
| `EXEC-01` | **HIGH** | Expand Certified Metric Coverage | Ensures single source of truth for C-level dashboards | Low | Enterprise Leadership |
| `REC-RISK-001` | **HIGH** | Verify Complete End-to-End Transformation Provenance | Guarantees full audit defense and regulatory compliance for financial metrics. | Medium | dim_proyecto_obra |
| `AUD-01` | **HIGH** | Conduct Quarterly SOX/GDPR Re-Certification | Required to maintain regulatory certifications | Medium | Enterprise Leadership |
| `REC-ARCH-001` | **HIGH** | Maintain Canonical Semantic Model Vendor Neutrality | Ensures semantic model remains portable across Power BI, Looker, and dbt. | Low | dim_proyecto_obra |
| `REC-DO-001` | **HIGH** | Promote Certified Domain Metrics to Production Status | Increases data product trust and executive adoption. | Low | fact_evm_avance_obra |

## Registered Persona Lens Perspectives

- **[Perspectiva Operativa: Jefe de Obra y Control de Faena](#17_jefe_obra_control)**: Perspectiva Operativa para Jefe de Obra y Control de Obras en 'schema'. Monitoreo de 6 entidades primarias, 5 KPIs foco ...
- **[AI Feature Store, Embeddings & Low-Latency Analytics Lens](#ai_systems_engineer)**: Feature readiness, embeddings/ML attributes, training data provenance, and AI inference latency for schema....
- **[Analytics Engineering, Dimensional Modeling & Transformation Lens](#analytics_engineer)**: Star-schema topology, semantic metrics, SQL transformations, and grain definitions for schema....
- **[Perspectiva C-Level: Retorno de Cartera Inmobiliaria y Control EVM](#analytics_leader)**: Executive portfolio perspective for schema highlighting strategic KPIs and domain maturity....
- **[Regulatory Compliance, Audit Provenance & Risk Lens](#audit_risk)**: Regulatory compliance (GDPR/SOX), provenance audit trail, and risk exceptions for schema....
- **[Modelo Direct Lake Gold OneLake - Rendimiento F8 y V-Order](#bi_developer)**: Power BI / TMDL semantic measures, relationships, DAX formulas, and display folders for schema....
- **[Business Self-Service & Consumption Simplicity Lens](#business_consumer)**: Certified business terms, plain-language metric glossary, and intuitive report navigation for schema....
- **[Regulatory Audit, Lineage Provenance & Risk Lens](#compliance_auditor)**: Full regulatory audit trace, GDPR/SOX compliance verification, PII lineage, and access boundaries for schema....
- **[Data Analyst & Self-Service Consumption Lens](#data_analyst)**: Certified KPIs, domain dimensions, and self-service exploration catalog for schema....
- **[Enterprise Data Architecture & Domain Modeling Lens](#data_architect)**: Relational graph topology, domain conformances, entity lifecycle, and architectural standards for schema....
- **[Data Engineering, Ingestion & Pipeline Health Lens](#data_engineer)**: Physical schema, partition grain, upstream sources, and pipeline integrity for schema....
- **[Data Governance, Quality & Ownership Lens](#data_governance_officer)**: Asset ownership, PII privacy boundaries, certification lifecycle, and quality scores for schema....
- **[Data Product Lifecycle, SLOs & Feedback Lens](#data_product_manager)**: Data product SLA, consumer adoption contracts, release maturity, and product telemetry for schema....
- **[Data Science, Feature Engineering & Statistical Lens](#data_scientist)**: Analytical features, continuous variables, entity grains, and training dimensions for schema....
- **[Perspectiva de Negocio: Ejecución de Obras y Venta Inmobiliaria](#domain_owner)**: Domain data products, certified KPIs, business ownership, and strategic alignment for schema....
- **[Optimización de Capacity Units (SKU F8 Direct Lake) y Memoria VertiPaq](#finops_specialist)**: Analytical query efficiency, cloud resource consumption, and cost attribution for schema....
- **[Data Platform Infrastructure & Storage Capacity Lens](#platform_engineer)**: Engine compute capacity, storage modes (Import/DirectLake), partitions, and refresh SLAs for schema....
