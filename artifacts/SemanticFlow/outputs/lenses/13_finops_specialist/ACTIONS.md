# Acciones Operativas: FinOps Specialist

Protocolo de trabajo del Especialista en FinOps en SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de FinOps y costos de capacidad
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona finops_specialist
```

---

## 2. Acciones Clave del Rol

1. **Detección de Tablas Ineficientes:**
   - Identificar tablas con exceso de columnas de tipo `string` libre o timestamps de alta granularidad que disparan la memoria RAM.
2. **Asignación de Etiquetas de Centro de Costos:**
   - Asegurarse de que cada dominio de datos tenga tags de atribución para reportar el consumo mensual a finanzas.
3. **Auditoría de Consultas DAX Cartesianas:**
   - Bloquear el pase a producción de modelos que generen ambigüedad o relaciones muchos a muchos no optimizadas.
