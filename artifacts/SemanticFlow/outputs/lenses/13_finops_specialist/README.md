# FinOps Specialist Lens - Cloud Cost & Capacity Attribution

**Rol Organizacional:** FinOps Specialist (`finops_specialist` / `finops`)  
**Profundidad Técnica:** `SUMMARY`  
**Áreas de Foco:** `COST_CAPACITY`, `BUSINESS_VALUE`  
**Objetos Visibles:** `FACT`, `DIMENSION`, `CALCULATED`  
**Tema de Color:** `#38A169` | **Icono:** `dollar-sign`  

---

## 1. Propósito y Alcance

Este lente atiende a los economistas de nube y líderes de FinOps. Conecta la arquitectura del modelo semántico con los costos de cómputo en OneLake, la memoria consumida por el motor VertiPaq y la asignación de costos (showback / chargeback) por unidad de negocio consumidora.

---

## 2. Visibilidad y Responsabilidades Técnicas

- **Prevención de Filtrado Cruzado Bidireccional:** Erradicación de filtros bidireccionales que saturan la CPU de Fabric Capacity y disparan costos de auto-scaling.
- **Atribución de Costos:** Vinculación de centros de costos (`cost_center`) a cada tabla de hechos.
- **Eficiencia de Almacenamiento:** Monitoreo del footprint de compresión de columnas en OneLake.
