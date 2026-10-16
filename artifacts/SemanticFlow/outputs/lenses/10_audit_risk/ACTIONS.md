# Acciones Operativas: Audit & Risk Officer

Protocolo de trabajo del Oficial de Auditoría y Riesgo en SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de auditoría exhaustiva
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona audit_risk
```

---

## 2. Acciones Clave del Rol

1. **Revisión de Excepciones de Riesgo:**
   - Inspeccionar advertencias sobre dependencias relacionales dudosas o tablas desconectadas (islas de datos).
2. **Validación de Consistencia Forense:**
   - Exigir que tablas financieras (ej: `Fact_Estado_Resultado`) posean controles de reconciliación cruzada.
3. **Emisión de Dictámenes de Riesgo:**
   - Documentar hallazgos formales en caso de que un modelo no cumpla con los estándares de trazabilidad institucional.
