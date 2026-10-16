# Acciones Operativas: Data Governance Officer

Protocolo de trabajo del Oficial de Gobierno de Datos al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección y Validación de Calidad

```bash
# Proyectar lente de gobierno de datos
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona data_governance_officer

# Ejecutar auditoría estricta de calidad semántica cQS
python -m src.cli validate -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --min-score 75
```

---

## 2. Acciones Clave del Rol

1. **Auditoría de Atributos Sensibles (PII):**
   - Asegurarse de que toda columna que identifique a una persona natural cuente con la etiqueta `(PII: True)` en el esquema Markdown.
   - Verificar que SemanticFlow oculte por defecto estos campos en el TMDL generado.
2. **Revisión del Diccionario de Datos:**
   - Validar el documento `outputs/docs/<empresa_id>/DATA_DICTIONARY.md`.
   - Exigir descripciones claras para campos sin documentación antes de certificar el modelo.
3. **Control del Quality Gate ($cQS$):**
   - Rechazar formalmente cualquier modelo que obtenga $cQS < 75.0$ o que contenga diagnósticos bloqueantes.
