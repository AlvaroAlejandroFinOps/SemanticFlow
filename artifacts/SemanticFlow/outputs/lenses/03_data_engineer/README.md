# Data Engineer Lens - Ingestion & Pipeline Integrity

**Rol Organizacional:** Data Engineer (`data_engineer`)  
**Profundidad Técnica:** `TECHNICAL`  
**Áreas de Foco:** `PIPELINE_HEALTH`, `DATA_MODELING`  
**Objetos Visibles:** `FACT`, `DIMENSION`, `BRIDGE`  
**Tema de Color:** `#2B6CB0` | **Icono:** `server`  

---

## 1. Propósito y Alcance

Este lente orienta a los ingenieros de datos responsables de la capa de almacenamiento físico (OneLake Delta Lake, ADLS Gen2, Snowflake, BigQuery) y de los pipelines de ingesta y transformación (Spark, Databricks, Data Factory). Conecta el esquema físico de las tablas con los contratos de modelado semántico.

---

## 2. Visibilidad y Responsabilidades Técnicas

- **Esquema Físico y Tipos de Datos:** Coincidencia exacta de tipos (`int64`, `decimal`, `timestamp`) entre las tablas Delta y el modelo semántico.
- **Particionamiento y Rendimiento:** Garantía de que las tablas de hechos masivas (ej. `Fact_Validacion`, `Fact_Telemetria`) dispongan de particiones temporales coincidentes con `Dim_Tiempo`.
