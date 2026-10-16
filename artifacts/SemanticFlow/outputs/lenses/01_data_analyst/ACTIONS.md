# Acciones Operativas: Data Analyst

Guía de acciones, comandos y flujos de trabajo para Analistas de Datos al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

Para visualizar únicamente los KPIs certificados y las entidades de negocio relevantes para análisis:

```bash
# Proyección en consola
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona data_analyst

# Exportación a Markdown de la perspectiva
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona data_analyst -f md
```

---

## 2. Acciones Clave del Rol

1. **Validación de Métricas Certificadas:**
   - Comprobar que cada medida de negocio requerida en los tableros analíticos esté presente en la lista de `Certified KPIs`.
   - Si falta una métrica aditiva o compuesta (ej: Margen % o Ticket Promedio), solicitar su inclusión formal al *Analytics Engineer*.

2. **Detección de Fricción en Nombres de Campos:**
   - Reportar nombres de columnas técnicos o poco claros para el usuario final (ej: cambiar `ID_Formacion` por `Formación del Tren`).

3. **Consumo en Power BI Desktop:**
   - Abrir el archivo `.pbip` generado en `outputs/pbip/<empresa_id>/`.
   - Crear reportes interactivos utilizando las medidas de las carpetas de visualización sin crear columnas calculadas en Power BI.
