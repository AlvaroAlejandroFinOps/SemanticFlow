# SemanticFlow - Enterprise SMaC Operations Hub

Bienvenido al centro de operaciones y arquitectura de **SemanticFlow** dentro del entorno IDE.

**SemanticFlow** es un compilador de *Semantic Modeling as Code (SMaC)* que transforma especificaciones relacionales puramente declarativas (Markdown/YAML) en artefactos de nivel empresarial para **Microsoft Fabric OneLake**, **Power BI (TMDL/PBIP)**, **dbt Semantic Layer** y el **Data Leadership Cockpit**.

---

## 1. Topología del Entorno

```
artifacts/SemanticFlow/
├── README.md                      # Este manual de arquitectura general
├── RUNBOOK_EXECUTION.md           # Guía operativa para ejecutar y añadir empresas
├── run_pipeline.py                # Script de automatización end-to-end de 1 comando
│
├── inputs/                        # DIRECTORIO DE ENTRADA (INGESTA)
│   ├── README.md                  # Especificación contractual de esquemas
│   ├── templates/                 # Plantillas reutilizables (Markdown y YAML)
│   └── companies/                 # Esquemas particionados por cliente/empresa
│       └── metro_santiago/        # Caso de referencia industrial (20 tablas)
│
└── outputs/                       # DIRECTORIO DE SALIDA (ARTEFACTOS COMPILADOS)
    ├── README.md                  # Mapa de exportación a herramientas
    ├── pbip/                      # Modelos Power BI Developer (.pbip) y TMDL
    ├── dbt/                       # Capa semántica dbt MetricFlow (YAML)
    ├── docs/                      # Diccionario de datos y Diagramas ERD
    ├── leadership_cockpit/        # Visión ejecutiva C-Level y Radar Cross-Lens
    └── lenses/                    # 16 Perspectivas organizacionales especializadas
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

## 2. Flujo Operativo Rápido (Quickstart)

Para ejecutar el pipeline completo sobre el caso de referencia o cualquier nueva empresa registrada en `inputs/companies/`:

```bash
# Ejecución completa (Validación cQS -> PBIP -> dbt -> Docs -> Cockpit -> Lentes)
python artifacts/SemanticFlow/run_pipeline.py --company metro_santiago
```

Si deseas inspeccionar los comandos individuales del compilador:
```bash
# 1. Inspeccionar topología y roles
python -m src.cli inspect -i artifacts/SemanticFlow/inputs/companies/metro_santiago/schema.md

# 2. Evaluar Semantic Quality Score (Quality Gate)
python -m src.cli validate -i artifacts/SemanticFlow/inputs/companies/metro_santiago/schema.md --min-score 75

# 3. Compilar a Power BI TMDL/PBIP
python -m src.cli compile -i artifacts/SemanticFlow/inputs/companies/metro_santiago/schema.md -o artifacts/SemanticFlow/outputs/pbip/metro_santiago

# 4. Exportar a dbt MetricFlow
python -m src.cli export-dbt -i artifacts/SemanticFlow/inputs/companies/metro_santiago/schema.md -o artifacts/SemanticFlow/outputs/dbt/metro_santiago/semantic_models.yml

# 5. Generar Diccionario de Datos y ERD Mermaid
python -m src.cli docgen -i artifacts/SemanticFlow/inputs/companies/metro_santiago/schema.md -o artifacts/SemanticFlow/outputs/docs/metro_santiago

# 6. Exportar Leadership Cockpit & Persona Lenses
python -m src.cli personas export -i artifacts/SemanticFlow/inputs/companies/metro_santiago/schema.md -o artifacts/SemanticFlow/outputs/leadership_cockpit/metro_santiago
```
