# Acciones Operativas: Data Engineer

Protocolo de trabajo del Data Engineer al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de ingeniería de datos
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona data_engineer

# Inspeccionar claves y columnas físicas
python -m src.cli inspect -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md
```

---

## 2. Acciones Clave del Rol

1. **Alineación de Tipos de Datos:**
   - Asegurar que columnas numéricas utilizadas en medidas aditivas sean numéricas reales y no `string` en el Delta Lake.

2. **Garantía de Claves Primarias:**
   - Evitar valores nulos en claves foráneas y primarias para prevenir filas ficticias en las relaciones 1:N de Power BI.

3. **Optimización de Almacenamiento:**
   - Validar que las tablas físicas subyacentes cuenten con compactación (V-Order en Fabric / Z-Order en Delta) para acelerar Direct Lake.
