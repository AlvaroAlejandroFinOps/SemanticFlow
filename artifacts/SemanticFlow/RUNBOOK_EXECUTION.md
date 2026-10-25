# Runbook Operativo: Ingesta, Ejecución y Publicación Multicliente en SemanticFlow (v3.1)

Este runbook detalla el procedimiento estándar paso a paso para añadir la información, esquema relacional, lentes de negocio personalizadas y políticas de gobernanza de cualquier empresa, compilando limpiamente todos sus artefactos semánticos dentro del entorno IDE.

---

## Procedimiento en 6 Pasos

### Paso 1: Crear el Espacio de Ingesta de la Empresa

1. Define un identificador único en minúsculas y sin espacios para la empresa (ej: `falabella_retail`, `santolaya`, `metro_santiago`).
2. Crea el directorio de trabajo bajo `inputs/companies/`:
   ```bash
   mkdir -p "artifacts/SemanticFlow/inputs/companies/<empresa_id>/lenses"
   ```
3. Copia las plantillas canónicas según la necesidad del proyecto:
   ```bash
   cp "artifacts/SemanticFlow/inputs/templates/schema_template.md" "artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md"
   cp "artifacts/SemanticFlow/inputs/templates/company_profile_template.yaml" "artifacts/SemanticFlow/inputs/companies/<empresa_id>/company_profile.yaml"
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

### Paso 3: Definir Lentes de Dominio y Políticas Locales (Opcional)

1. **Lentes de Dominio Personalizadas (Layer 2):**
   Copia la plantilla `custom_lens_template.yaml` para modelar roles específicos de la empresa:
   ```bash
   cp "artifacts/SemanticFlow/inputs/templates/custom_lens_template.yaml" "artifacts/SemanticFlow/inputs/companies/<empresa_id>/lenses/17_jefe_obra_control.yaml"
   ```
2. **Enriquecimiento de Lentes Base (Overrides):**
   Crea `overrides.yaml` bajo la carpeta `lenses/` para agregar métricas foco y tablas a las 16 lentes base.
3. **Gobernanza Policy-as-Code:**
   Copia `governance_policy_template.yaml` para fijar umbrales locales (sujetos a los Floor Guardrails corporativos mínimos: `min_score >= 60.0`, detección de ciclos obligatoria).

---

### Paso 4: Ejecución Automatizada del Pipeline con Bloqueo de Concurrencia

Ejecuta el script orquestador indicando el ID de la empresa:

```bash
python artifacts/SemanticFlow/run_pipeline.py --company <empresa_id>
```

#### ¿Qué ejecuta este script automáticamente?
1. **Adquisición de Lock Exclusivo:** Adquiere un bloqueo de archivo por empresa (`acquire_company_lock`) para evitar colisiones entre el Agente IDE y terminales concurrentes.
2. **Escaneo de Seguridad y Secretos:** Verifica que ningún archivo de esquema, perfil o lente contenga secretos o fugas de credenciales.
3. **Validación Determinista ($cQS$) y DAX:** Evalúa el grafo relacional, resuelve la tabla de símbolos DAX y detecta ciclos entre tablas y medidas.
4. **Compilación Power BI TMDL/PBIP:** Genera el bundle `.pbip` y el directorio `.SemanticModel/definition/` con sintaxis TMDL oficial.
5. **Compilación dbt MetricFlow:** Genera el archivo YAML canónico `semantic_models.yml` con entities, dimensions y measures sintetizadas.
6. **Generación Documental:** Genera el Data Dictionary Markdown y el Diagrama ERD en sintaxis Mermaid.
7. **C-Level Leadership Cockpit & Radar:** Calcula el radar de madurez y genera el reporte consolidado.
8. **Distribución de Lentes:** Exporta las proyecciones a las 16 carpetas corporativas y a las carpetas de lentes personalizadas de la empresa.

---

### Paso 5: Diagnóstico y Resolución de Fallos en el Quality Gate

Si la ejecución falla en el paso de validación (`cQS < min_score` o `BLOCKING_ERRORS > 0`), ejecuta:

```bash
# Validación global del esquema
python -m src.cli validate -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --min-score 70.0

# Validación focalizada en una lente específica
python -m src.cli validate -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --lens 17_jefe_obra_control
```

#### Errores Comunes y Solución:
- **`QUAL_DAX_REF_001`:** Una fórmula DAX referencia una tabla o columna inexistente. Revisa el nombre exacto de la tabla o atributo.
- **`QUAL_DAX_CYCLE_001`:** Existe una dependencia circular entre medidas DAX ($M_1 \rightarrow M_2 \rightarrow M_1$). Rompe la recursión entre medidas.
- **`QUAL_DAX_TYPE_001`:** Se aplicó una agregación numérica (`SUM`, `AVERAGE`) sobre una columna de texto (`STRING`).
- **`QUAL_VPAQ_FILTER_012`:** Antipatrón `FILTER(ALL())` sobre tabla de hechos con alta cardinalidad sin optimización VertiPaq.
- **`ERR_CYCLE_DETECTED`:** Existen referencias circulares entre tablas. Convierte una relación en unidireccional o usa tabla puente.

---

### Paso 6: Exportación y Consumo en Herramientas Productivas

Una vez que la consola confirme `[PIPELINE COMPLETADO EXITOSAMENTE]`:

| Herramienta | Ruta a Abrir / Consumir |
| :--- | :--- |
| **Power BI Desktop** | Abrir directamente el archivo `artifacts/SemanticFlow/outputs/pbip/<empresa_id>/<Modelo>.pbip`. |
| **Microsoft Fabric OneLake** | Commitear la carpeta `.SemanticModel/definition/` al repositorio Git sincronizado con el Workspace de Fabric. |
| **dbt Core / dbt Cloud** | Copiar `artifacts/SemanticFlow/outputs/dbt/<empresa_id>/semantic_models.yml` a la carpeta `models/semantic/` de tu proyecto dbt. |
| **Confluence / Wiki / GitHub** | Renderizar `artifacts/SemanticFlow/outputs/docs/<empresa_id>/DATA_DICTIONARY.md` y copiar el diagrama Mermaid de `ARCHITECTURE_ERD.mmd`. |
| **Comité Ejecutivo / CDO** | Presentar `artifacts/SemanticFlow/outputs/leadership_cockpit/<empresa_id>/data_leadership_cockpit.md` con el radar de madurez y recomendaciones priorizadas. |
| **Lentes de Negocio** | Consumir proyecciones por rol en `artifacts/SemanticFlow/outputs/lenses/<id_lente>/<empresa_id>/`. |
