# Acciones Operativas: Data Architect

Protocolo de trabajo del Arquitecto de Datos al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección y Documentación

```bash
# Proyectar lente de arquitectura exhaustiva
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona data_architect

# Generar documentación técnica y diagrama Mermaid ERD
python -m src.cli docgen -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md -o artifacts/SemanticFlow/outputs/docs/<empresa_id>
```

---

## 2. Acciones Clave del Rol

1. **Auditoría de Topología Relacional:**
   - Revisar el archivo `outputs/docs/<empresa_id>/ARCHITECTURE_ERD.mmd` para verificar la aciclicidad del grafo relacional.
2. **Homologación de Dominios Conformes:**
   - Asegurar que dimensiones compartidas (`Dim_Tiempo`, `Dim_Organizacion`) mantengan definiciones uniformes en todos los esquemas de la empresa.
3. **Resolución de Ciclos y Dependencias Complejas:**
   - Intervenir en caso de advertencias de dependencias circulares mediante tablas puente (`Bridge`) o copias de rol (Role-Playing Dimensions).
