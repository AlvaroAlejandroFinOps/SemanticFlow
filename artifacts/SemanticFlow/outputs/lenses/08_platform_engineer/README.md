# Platform Engineer Lens - Infrastructure & Storage Capacity

**Rol Organizacional:** Platform Engineer (`platform_engineer`)  
**Profundidad Técnica:** `TECHNICAL`  
**Áreas de Foco:** `COST_CAPACITY`, `PIPELINE_HEALTH`  
**Objetos Visibles:** `FACT`, `DIMENSION`, `STORAGE_MODE`, `PARTITION`  
**Tema de Color:** `#DD6B20` | **Icono:** `hard-drive`  

---

## 1. Propósito y Alcance

Este lente atiende a los ingenieros de plataforma Cloud (Azure, GCP, AWS) e infraestructura de Microsoft Fabric. Evalúa los modos de almacenamiento requeridos (Direct Lake vs. Import en memoria), el footprint de almacenamiento, las cuotas de capacidad computacional y los tiempos de procesamiento.

---

## 2. Visibilidad y Responsabilidades Técnicas

- **Modos de Almacenamiento:** Decisión entre Direct Lake (lectura nativa de Parquet/Delta) o Import (caché VertiPaq en RAM).
- **Control de Memoria:** Monitoreo del tamaño del modelo para evitar throttling de capacidad en Microsoft Fabric (F-SKUs).
- **Automatización IaC:** Integración con el proveedor de Terraform (`terraform-provider-semanticflow`) para provisionamiento declarativo.
