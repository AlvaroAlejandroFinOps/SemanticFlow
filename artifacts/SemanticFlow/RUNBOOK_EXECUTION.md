# Runbook Operativo: Ingesta, Ejecución y Publicación Multicliente en SemanticFlow

Este runbook detalla el procedimiento estándar paso a paso para añadir la información y esquema relacional de cualquier empresa y compilar limpiamente todos sus artefactos semánticos dentro del entorno IDE.

---

## Procedimiento en 5 Pasos

### Paso 1: Crear el Espacio de Ingesta de la Empresa

1. Define un identificador único en minúsculas y sin espacios para la empresa (ej: `falabella_retail`, `banco_estado`, `cencosud_paris`).
2. Crea el directorio de trabajo bajo `inputs/companies/`:
   ```bash
   mkdir "artifacts/SemanticFlow/inputs/companies/<empresa_id>"
   ```
3. Copia la plantilla canónica Markdown:
   ```bash
   cp "artifacts/SemanticFlow/inputs/templates/schema_template.md" "artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md"
   ```

---

### Paso 2: Declarar el Esquema Relacional de Negocio

Edita el archivo `schema.md` asegurando las siguientes reglas de calidad:
- **Tablas de Hechos (`Fact_*`):** Define métricas aditivas (`monto`, `cantidad`, `tiempo_segundos`) con tipo de dato `decimal`, `int64` o `float32`.
- **Dimensiones (`Dim_*`):** Define atributos de corte analítico (`categoria`, `estado`, `region`).
- **Claves Primarias:** Añade la etiqueta `**PKey**` en la columna identificadora.
- **Claves Foráneas:** Asegúrate de que las tablas de hechos enlacen a las dimensiones con la sintaxis:
  ```markdown
  | **SK_Cliente** | `int64` | **FKey (`Dim_Cliente.SK_Cliente`)** | Enlace dimensional |
  ```
- **Campos Sensibles / Privacidad:** Si una columna contiene datos de contacto o personales (RUT, Teléfono, Correo, Salario), anota `(PII: True)` en la descripción.

---

### Paso 3: Ejecución Automatizada del Pipeline

Ejecuta el script orquestador indicando el ID de la empresa:

```bash
python artifacts/SemanticFlow/run_pipeline.py --company <empresa_id>
```

#### ¿Qué ejecuta este script automáticamente?
1. **Validación Determinista ($cQS$):** Evalúa el grafo relacional, detecta ciclos acíclicos y bloquea la compilación si $cQS < 75.0$.
2. **Compilación Power BI TMDL/PBIP:** Genera el bundle `.pbip` y el directorio `.SemanticModel/definition/` con sintaxis TMDL oficial.
3. **Compilación dbt MetricFlow:** Genera el archivo YAML canónico `semantic_models.yml` con entities, dimensions y measures sintetizadas.
4. **Generación Documental:** Genera el Data Dictionary Markdown y el Diagrama ERD en sintaxis Mermaid.
5. **C-Level Leadership Cockpit & Radar:** Calcula el radar de madurez en 10 dimensiones y genera el reporte consolidado.
6. **Distribución en Carpetas de Lentes:** Exporta las proyecciones específicas a cada una de las 16 carpetas de lentes organizacionales.

---

### Paso 4: Diagnóstico y Resolución de Fallos en el Quality Gate

Si la ejecución falla en el paso de validación (`cQS < 75.0` o `BLOCKING_ERRORS > 0`), ejecuta:

```bash
python -m src.cli validate -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --min-score 75
```

#### Errores Comunes y Solución:
- **`ERR_DANGLING_RELATIONSHIP`:** Una tabla de hechos hace referencia a una dimensión inexistente o mal escrita. Revisa el nombre exacto de la tabla destino.
- **`ERR_CYCLE_DETECTED`:** Existen referencias cruzadas circulares entre tablas ($A \rightarrow B \rightarrow C \rightarrow A$). Convierte una de las relaciones en unidireccional o utiliza una tabla puente (`Bridge`).
- **`WARN_PII_UNMASKED`:** Se detectó un atributo PII sin política de enmascaramiento. SemanticFlow lo ocultará por defecto en el modelo semántico.

---

### Paso 5: Exportación y Consumo en Herramientas Productivas

Una vez que la consola confirme `[EXITO COMPLETO]`:

| Herramienta | Ruta a Abrir / Consumir |
| :--- | :--- |
| **Power BI Desktop** | Abrir directamente el archivo `artifacts/SemanticFlow/outputs/pbip/<empresa_id>/<Modelo>.pbip`. |
| **Microsoft Fabric OneLake** | Commitear la carpeta `.SemanticModel/definition/` al repositorio Git sincronizado con el Workspace de Fabric. |
| **dbt Core / dbt Cloud** | Copiar `artifacts/SemanticFlow/outputs/dbt/<empresa_id>/semantic_models.yml` a la carpeta `models/semantic/` de tu proyecto dbt. |
| **Confluence / Wiki / GitHub** | Renderizar `outputs/docs/<empresa_id>/DATA_DICTIONARY.md` y copiar el diagrama Mermaid de `ARCHITECTURE_ERD.mmd`. |
| **Comité Ejecutivo / CDO** | Presentar `outputs/leadership_cockpit/<empresa_id>/data_leadership_cockpit.md` con el radar de madurez y recomendaciones priorizadas. |
