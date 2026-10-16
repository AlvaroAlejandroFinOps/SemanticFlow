# Acciones Operativas: BI Developer

Protocolo de trabajo del desarrollador de BI al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección y Compilación

```bash
# Proyectar lente de BI
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona bi_developer

# Compilar proyecto Power BI Developer (PBIP)
python -m src.cli compile -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md -o artifacts/SemanticFlow/outputs/pbip/<empresa_id>
```

---

## 2. Acciones Clave del Rol

1. **Apertura y Verificación en Power BI Desktop:**
   - Navegar a `outputs/pbip/<empresa_id>/` y abrir el archivo `.pbip`.
   - Comprobar que el diagrama de relaciones en Power BI Desktop sea un Star Schema limpio con líneas continuas 1:N unidireccionales.
2. **Revisión de Medidas DAX Sintetizadas:**
   - Comprobar que las fórmulas DAX generadas utilicen `SUM`, `AVERAGE` o `DISTINCTCOUNT` correctamente según la naturaleza del atributo.
3. **Control de Versiones en Git:**
   - Commitear las modificaciones de TMDL en Git sin generar conflictos binarios `.pbix`.
