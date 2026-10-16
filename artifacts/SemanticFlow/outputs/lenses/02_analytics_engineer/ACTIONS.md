# Acciones Operativas: Analytics Engineer

Protocolo de trabajo y acciones del Analytics Engineer en SemanticFlow.

---

## 1. Comandos de Inspección y Exportación

```bash
# Proyectar lente dimensional
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona analytics_engineer

# Exportar modelo dbt MetricFlow
python -m src.cli export-dbt -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md -o artifacts/SemanticFlow/outputs/dbt/<empresa_id>/semantic_models.yml
```

---

## 2. Acciones Clave del Rol

1. **Resolución de Granularidad Relacional:**
   - Asegurar que cada tabla de hechos posea una granularidad unívoca (ej: transacción individual vs. consolidado mensual).
   - En hechos multivariables, vincular dimensiones conformadas (`Dim_Tiempo`, `Dim_Organizacion`).

2. **Integración con dbt Core / Cloud:**
   - Revisar el archivo `outputs/dbt/<empresa_id>/semantic_models.yml`.
   - Incorporar el archivo en el proyecto dbt bajo `models/semantic/`.
   - Ejecutar `dbt compile` para verificar que MetricFlow valida correctamente las dimensiones y métricas.

3. **Corrección de Errores cQS:**
   - Atender de inmediato diagnósticos `WARN_RELATIONSHIP_BIDIRECTIONAL` convirtiéndolas en relaciones unidireccionales 1:N.
