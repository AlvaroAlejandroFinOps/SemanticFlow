# Acciones Operativas: Platform Engineer

Protocolo de trabajo del Ingeniero de Plataforma al interactuar con SemanticFlow.

---

## 1. Comandos de Inspección Recomendados

```bash
# Proyectar lente de plataforma de datos
python -m src.cli explain -i artifacts/SemanticFlow/inputs/companies/<empresa_id>/schema.md --persona platform_engineer
```

---

## 2. Acciones Clave del Rol

1. **Definición de Modos de Almacenamiento:**
   - Asegurarse de que hechos con volumen superior a 10 millones de filas operen en Direct Lake para no consumir memoria VertiPaq.
2. **Supervisión de Capacidad Fabric:**
   - Revisar que la compilación no genere relaciones N:M que disparen Cartesian Joins en la capacidad de Fabric.
3. **Despliegue Continuo (CI/CD):**
   - Configurar la tarea de Azure DevOps o GitHub Actions (`action.yml`) para ejecutar `validate` y `compile` en cada Pull Request.
