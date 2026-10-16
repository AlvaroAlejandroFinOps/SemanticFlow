# Compliance Auditor Lens - Regulatory Audit & Privacy Enforcements

**Rol Organizacional:** Compliance Auditor (`compliance_auditor` / `compliance`)  
**Profundidad Técnica:** `EXHAUSTIVE`  
**Áreas de Foco:** `AUDIT_TRACEABILITY`, `GOVERNANCE_COMPLIANCE`  
**Objetos Visibles:** `FACT`, `DIMENSION`  
**Tema de Color:** `#E53E3E` | **Icono:** `file-text`  

---

## 1. Propósito y Alcance

Este lente atiende a los auditores externos, reguladores y oficiales de cumplimiento normativo (GDPR, Ley 19.628 de Protección de Datos Personales, normativas CMF). Asegura que el modelo no vulnere las leyes de privacidad y que todo acceso o transformación sea auditable.

---

## 2. Visibilidad y Responsabilidades Técnicas

- **Enmascaramiento Obligatorio:** Verificación de que campos sensibles (RUT, teléfonos, direcciones) estén anonimizados o aislados con seguridad a nivel de fila (RLS).
- **Linaje de Extremo a Extremo:** Capacidad de demostrar de dónde provino cada número presentado a los entes reguladores.
- **Registro de No Conformidades:** Bloqueo preventivo ante infracciones normativas identificadas en el Quality Gate.
