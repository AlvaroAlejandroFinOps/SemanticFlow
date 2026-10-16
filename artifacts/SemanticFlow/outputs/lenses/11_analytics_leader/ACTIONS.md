# Acciones Operativas: Analytics Leader (CDO)

Protocolo directivo y acciones del Líder de Analítica al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección y Generación del Cockpit

```bash
# Proyectar lente ejecutivo
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona analytics_leader

# Visualizar el Data Leadership Cockpit en consola
python -m src.cli cockpit -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md

# Exportar Cockpit a directorio
python -m src.cli cockpit -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md -o artifacts/SemanticFlow/outputs/leadership_cockpit/<empresa_id>
```

---

## 2. Acciones Clave del Rol

1. **Evaluación de Madurez de Plataforma:**
   - Analizar el radar de madurez generado por el Cockpit y exigir planes de mitigación en dominios bajo el 70%.
2. **Asignación de Recursos y Presupuesto:**
   - Priorizar iniciativas de refactorización según las recomendaciones automáticas de mayor impacto.
3. **Comunicación al Directorio / C-Level:**
   - Presentar el resumen ejecutivo (`executive_summary`) en comités de transformación digital y comités ejecutivos.
