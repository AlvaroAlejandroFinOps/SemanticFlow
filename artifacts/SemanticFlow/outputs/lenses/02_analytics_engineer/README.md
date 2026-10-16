# Analytics Engineer Lens - Dimensional Modeling & dbt MetricFlow

**Rol Organizacional:** Analytics Engineer (`analytics_engineer`)  
**Profundidad Técnica:** `TECHNICAL`  
**Áreas de Foco:** `DATA_MODELING`, `MODELING_QUALITY`  
**Objetos Visibles:** `FACT`, `DIMENSION`, `BRIDGE`, `CALCULATED`  
**Tema de Color:** `#319795` | **Icono:** `code`  

---

## 1. Propósito y Alcance

Este lente está diseñado para ingenieros analíticos y desarrolladores de capas semánticas. Expone la topología completa del esquema en estrella (Star Schema), granularidades de tablas de hechos, lógica de claves subrogadas, definiciones dimensionales y la especificación de modelos semánticos compatibles con dbt MetricFlow.

---

## 2. Visibilidad y Responsabilidades Técnicas

- **Esquema Canónico:** Inspección de roles de tabla (`Fact`, `Dimension`, `Bridge`, `Outrigger`).
- **dbt MetricFlow:** Generación de contratos `semantic_models.yml` con entities, dimensions, time_grains y measures.
- **Calidad de Relaciones:** Garantía de cardinalidad estricta 1:N unidireccional para evitar trampas de abanico (chasm/fan traps).
