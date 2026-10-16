# Acciones Operativas: AI Systems Engineer

Protocolo de trabajo del Ingeniero de Sistemas de IA en SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de IA y preparación de features
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona ai_systems_engineer
```

---

## 2. Acciones Clave del Rol

1. **Evaluación de Compatibilidad Text-to-SQL:**
   - Comprobar que los nombres de las entidades y medidas sean descriptivos y autoexplicativos para modelos LLM analíticos.
2. **Definición de Entidades Clave en Feature Stores:**
   - Conectar las dimensiones principales (`Dim_Cliente`, `Dim_Producto`) con registros de características en tiempo real.
3. **Auditoría de Enmascaramiento para Inferencia:**
   - Garantizar que datos PII no sean expuestos a prompts de modelos de lenguaje generativo sin enmascaramiento previo.
