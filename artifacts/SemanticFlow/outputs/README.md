# Especificación de Outputs - SemanticFlow (SMaC Emitters)

Este directorio alberga los artefactos generados por el compilador **SemanticFlow**, desacoplados por tecnología y audiencia de consumo.

---

## 1. Estructura de Salidas

```
outputs/
├── README.md                  # Este documento
│
├── pbip/                      # Microsoft Power BI Developer & TMDL
│   └── <empresa_id>/          # Proyecto .pbip, .pbidataset y carpetas TMDL
│
├── dbt/                       # dbt Semantic Layer (MetricFlow)
│   └── <empresa_id>/          # semantic_models.yml canónico
│
├── docs/                      # Documentación Técnica & Diagramas
│   └── <empresa_id>/          # DATA_DICTIONARY.md y ARCHITECTURE_ERD.mmd
│
├── leadership_cockpit/        # Visión Ejecutiva C-Level & Radar Transversal
│   ├── README.md              # Estructura del Cockpit y matriz de 10 dimensiones
│   ├── ACTIONS.md             # Decisiones estratégicas C-Level y Quality Gates
│   └── <empresa_id>/          # data_leadership_cockpit.md y .json
│
└── lenses/                    # 16 Perspectivas Organizacionales (Persona Lenses)
    ├── README.md              # Matriz de roles, profundidad técnica y RACI
    ├── 01_data_analyst/
    ├── 02_analytics_engineer/
    ├── 03_data_engineer/
    ├── 04_data_scientist/
    ├── 05_bi_developer/
    ├── 06_data_architect/
    ├── 07_data_governance_officer/
    ├── 08_platform_engineer/
    ├── 09_domain_owner/
    ├── 10_audit_risk/
    ├── 11_analytics_leader/
    ├── 12_data_product_manager/
    ├── 13_finops_specialist/
    ├── 14_ai_systems_engineer/
    ├── 15_business_consumer/
    └── 16_compliance_auditor/
```

---

## 2. Destinos de Exportación y Compatibilidad

| Directorio | Herramienta Destino | Formato | Propósito Principal |
| :--- | :--- | :--- | :--- |
| `pbip/` | Power BI Desktop / Fabric | `.pbip`, `.tmdl` | Apertura directa en Power BI Desktop sin compilar PBIX manual. |
| `dbt/` | dbt Core / dbt Cloud | `.yml` | Definición de métricas, dimensiones y joins para MetricFlow. |
| `docs/` | Git / Wikis / Confluence | `.md`, `.mmd` | Auditoría de esquema, catalogación y visualización ERD en Mermaid. |
| `leadership_cockpit/` | CDO / VP Data / C-Level | `.md`, `.json` | Radar de madurez (0-100%), riesgos de negocio y priorización de inversión. |
| `lenses/` | Equipos Técnicos y Negocio | `.md`, `.json` | Vistas filtradas según el rol del colaborador (RACI, KPIs, recomendaciones). |
