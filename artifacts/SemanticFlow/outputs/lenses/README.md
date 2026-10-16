# Lentes Organizacionales de SemanticFlow (Persona Lenses)

El sistema de **Persona Lenses** de SemanticFlow proyecta el modelo semántico canónico a través de **16 perspectivas organizacionales especializadas**.

Cada lente filtra el ruido técnico no relevante para su rol, proyecta métricas certificadas, expone recomendaciones de mejora y define interfaces de colaboración inter-equipos basadas en el estándar **Team Topologies** y matrices **RACI**.

---

## 1. Directorio de Lentes Especializados

| Carpeta | Rol Organizacional | Nivel Técnico | Foco Principal |
| :--- | :--- | :---: | :--- |
| [`01_data_analyst/`](./01_data_analyst/) | **Data Analyst** | `SUMMARY` | Simplicidad de consumo, catálogo de KPIs certificados y dimensiones limpias. |
| [`02_analytics_engineer/`](./02_analytics_engineer/) | **Analytics Engineer** | `TECHNICAL` | Modelado dimensional en estrella, dbt MetricFlow, grano y transformaciones. |
| [`03_data_engineer/`](./03_data_engineer/) | **Data Engineer** | `TECHNICAL` | Esquema físico, particiones, fuentes upstream y salud de pipelines de ingesta. |
| [`04_data_scientist/`](./04_data_scientist/) | **Data Scientist** | `TECHNICAL` | Features analíticas, variables continuas y estabilidad para entrenamiento de modelos. |
| [`05_bi_developer/`](./05_bi_developer/) | **BI Developer** | `TECHNICAL` | Medidas DAX, carpetas de despliegue, relaciones TMDL y rendimiento en Power BI. |
| [`06_data_architect/`](./06_data_architect/) | **Data Architect** | `EXHAUSTIVE` | Dígrafo relacional, componentes conexos, topología y ciclo de vida de entidades. |
| [`07_data_governance_officer/`](./07_data_governance_officer/) | **Data Governance Officer** | `SUMMARY` | Calidad semántica, PII, linaje regulatorio, certificación y propiedad de datos. |
| [`08_platform_engineer/`](./08_platform_engineer/) | **Platform Engineer** | `TECHNICAL` | Capacidad de cómputo en OneLake, Direct Lake vs Import, memoria y SLAs de refresh. |
| [`09_domain_owner/`](./09_domain_owner/) | **Domain Owner** | `SUMMARY` | Propiedad de productos de datos de negocio y alineación estratégica. |
| [`10_audit_risk/`](./10_audit_risk/) | **Audit & Risk Officer** | `EXHAUSTIVE` | Cumplimiento normativo, trazabilidad de procedencia y excepciones de riesgo. |
| [`11_analytics_leader/`](./11_analytics_leader/) | **Analytics Leader (CDO)** | `EXECUTIVE` | Visión ejecutiva consolidada, radar de madurez (0-100%) y liderazgo de datos. |
| [`12_data_product_manager/`](./12_data_product_manager/) | **Data Product Manager** | `SUMMARY` | Ciclo de vida del producto de datos, feedback de consumidores y SLOs. |
| [`13_finops_specialist/`](./13_finops_specialist/) | **FinOps Specialist** | `SUMMARY` | Consumo de cómputo, costos por consulta y atribución de capacidad en Fabric. |
| [`14_ai_systems_engineer/`](./14_ai_systems_engineer/) | **AI Systems Engineer** | `TECHNICAL` | Compatibilidad con Feature Stores, embeddings vectoriales y baja latencia. |
| [`15_business_consumer/`](./15_business_consumer/) | **Business Consumer** | `SUMMARY` | Terminología de negocio intuitiva y exploración analítica simplificada. |
| [`16_compliance_auditor/`](./16_compliance_auditor/) | **Compliance Auditor** | `EXHAUSTIVE` | Auditoría de procedencia de extremo a extremo y barreras de privacidad PII. |

---

## 2. Estructura Interna de Cada Carpeta de Lente

Cada subdirectorio contiene:
- **`README.md`**: Ficha técnica del lente con objetivo, profundidad técnica, áreas de foco, objetos visibles permitidos, y modelo de madurez.
- **`ACTIONS.md`**: Protocolo de acción operativa para el rol, comandos de inspección en el CLI, checklist antes del despliegue y respuestas ante incidentes.
- Archivos generados de proyecciones (`<persona>_lens.md` y `<persona>_lens.json`) resultantes de la ejecución del pipeline para cada empresa.
