# Data Governance Officer Lens - Quality & PII Boundaries

**Rol Organizacional:** Data Governance Officer (`data_governance_officer`)  
**Profundidad Técnica:** `SUMMARY`  
**Áreas de Foco:** `GOVERNANCE_COMPLIANCE`, `MODELING_QUALITY`  
**Objetos Visibles:** `FACT`, `DIMENSION`  
**Tema de Color:** `#805AD5` | **Icono:** `shield`  

---

## 1. Propósito y Alcance

Este lente proporciona al Oficial de Gobierno de Datos y a los Data Stewards visibilidad inmediata sobre la propiedad de los datos (`Ownership`), clasificación de privacidad (PII/GDPR/Ley 19.628), descripciones de negocio y la certificación del Semantic Quality Score ($cQS$).

---

## 2. Visibilidad y Responsabilidades Técnicas

- **Detección de Datos Sensibles (PII):** Identificación de RUTs, nombres, correos o datos salariales sin enmascarar.
- **Cobertura de Descripciones:** Porcentaje de entidades y atributos que cuentan con definición de negocio explícita.
- **Aprobación de Calidad Semántica ($cQS$):** Monitoreo del umbral determinista ($\ge 75.0$) para evitar modelos huérfanos en producción.
