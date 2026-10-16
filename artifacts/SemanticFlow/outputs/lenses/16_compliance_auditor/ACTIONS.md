# Acciones Operativas: Compliance Auditor

Protocolo de trabajo del Auditor de Cumplimiento Normativo en SemanticFlow.

---

## 1. Comandos de Inspección y Auditoría Legal

```bash
# Proyectar lente de auditoría regulatoria
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona compliance_auditor
```

---

## 2. Acciones Clave del Rol

1. **Auditoría de Cumplimiento de Privacidad:**
   - Inspeccionar el archivo `schema.md` de la empresa para certificar que ningún dato personal identificable (PII) se transmita sin clasificar.
2. **Revisión del Diccionario de Datos para Entes Reguladores:**
   - Extraer `outputs/docs/<empresa_id>/DATA_DICTIONARY.md` como evidencia formal para auditorías externas.
3. **Bloqueo Legal Preventivo:**
   - En caso de detección de campos confidenciales expuestos en la capa de consumo, exigir la detención del despliegue en CI/CD.
