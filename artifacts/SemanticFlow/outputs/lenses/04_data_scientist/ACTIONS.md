# Acciones Operativas: Data Scientist

Protocolo de trabajo del Data Scientist al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de Data Science
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona data_scientist
```

---

## 2. Acciones Clave del Rol

1. **Selección de Features de Entrenamiento:**
   - Extraer tablas de hechos continuas (ej. `Fact_Sensoraje_Via`, `Fact_Simulacion_Flujo`) para modelado predictivo.
2. **Validación de Integridad Temporal:**
   - Verificar la consistencia de series de tiempo en `Dim_Tiempo` para evitar saltos en variables cronológicas.
3. **Consumo vía Fabric Lakehouse / Python:**
   - Consumir las tablas Delta canónicas mediante PySpark o DuckDB manteniendo las relaciones descubiertas por SemanticFlow.
