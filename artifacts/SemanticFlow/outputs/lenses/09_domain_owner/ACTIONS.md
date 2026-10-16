# Acciones Operativas: Domain Owner

Protocolo de trabajo del Líder de Dominio de Negocio en SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de dominio de negocio
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona domain_owner
```

---

## 2. Acciones Clave del Rol

1. **Definición de Términos de Negocio:**
   - Validar que las definiciones en `schema.md` reflejen el vocabulario estándar de la industria.
2. **Priorización de Nuevos Requerimientos:**
   - Solicitar formalmente la adición de nuevas entidades o tablas de hechos cuando surjan nuevos procesos comerciales.
3. **Validación de Resultados en Negocio:**
   - Confirmar que los reportes generados a partir del modelo semántico coinciden con los balances contables y operacionales de la empresa.
