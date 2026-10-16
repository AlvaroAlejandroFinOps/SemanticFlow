# Acciones Operativas: Data Product Manager

Protocolo de trabajo del Gerente de Producto de Datos en SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de producto de datos
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona data_product_manager
```

---

## 2. Acciones Clave del Rol

1. **Definición de Contratos de Producto:**
   - Asegurarse de que el modelo semántico contenga metadatos claros de contacto, SLAs de actualización y canales de soporte.
2. **Monitoreo de Feedback de Consumidores:**
   - Recoger requerimientos de analistas y usuarios de negocio para incorporar nuevas métricas en el roadmap.
3. **Mantenimiento del Ciclo de Vida:**
   - Planificar la deprecación de versiones anteriores del modelo antes de liberar cambios que rompan compatibilidad (breaking changes).
