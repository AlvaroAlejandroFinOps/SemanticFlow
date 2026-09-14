# Plan de Implementación Maestro: Framework Persona Lens y Data Leadership Cockpit
*(Generado con Opus Thinking - Profundidad Máxima)*

## Documento Base
[SemanticFlow_Persona_Lens_Leadership_Cockpit_Master_Plan.txt](file:///d:/0001%20HyperScale%20Thinking/PROYECTOS%20CLOUD/Data%20&%20AI%20Strategy/SemanticFlow/output/Planes/Vigentes/SemanticFlow_Persona_Lens_Leadership_Cockpit_Master_Plan.txt)

---

## 1. Estado Observado del Repositorio (Línea Base)

Se ha realizado una auditoría profunda del estado actual de SemanticFlow. El sistema base se encuentra en un estado de **madurez alta para la emisión de TMDL y validación de calidad**, sirviendo como base sólida para esta expansión.

### Suite de Pruebas (Baseline) — 25/25 PASS ✅
Se ejecutó la suite completa sin alterar código funcional. El resultado es 100% exitoso en 7.28s, incluyendo pruebas de estrés masivas. Esto establece nuestra garantía de "Cero Regresiones".
- `tests/test_canonical_model.py` (3 tests)
- `tests/test_cli.py` (2 tests)
- `tests/test_inference_engine.py` (1 test)
- `tests/test_markdown_parser.py` (1 test)
- `tests/test_stage3_governance_quality.py` (3 tests)
- `tests/test_stage4_hardening_personas.py` (3 tests)
- `tests/test_tmdl_emitter.py` (1 test)
- `tests/test_yaml_parser.py` (1 test)
- Pruebas de Estrés (Masivas, Tier 1, 2 y 3) (10 tests)

### Arquitectura Actual (As-Is)
La arquitectura sigue un modelo de Monolito Modular. Los componentes críticos identificados para este plan son:
- **`src/core/ast/canonical/models.py`**: Contiene la única verdad semántica (`CanonicalSemanticProject`). **Nota:** Carece del campo de gobernanza a nivel de proyecto requerido por el plan maestro.
- **`src/core/personas/views.py`**: Implementación actual y muy básica de Personas. Solo soporta 5 roles (3 activos) y genera vistas planas (strings) sin políticas de visibilidad ni recomendaciones estructuradas.

---

## 2. Estrategia Integral y Rigurosa de Testing (El Núcleo de la Funcionalidad)

> [!IMPORTANT]
> **GARANTÍA DE FUNCIONALIDAD**
> Siguiendo el requerimiento explícito de hacer un *"fuerte hincapié en testeos"*, ninguna fase de este plan avanzará sin superar las siguientes 8 dimensiones de prueba. Este rigor asegura que la escalabilidad a 10+ Lenses no destruya la estabilidad actual.

1. **Tests de Mutación (Mutation Safety Tests)**:
   - **Objetivo**: Probar matemáticamente que ningún Lens altera el `CanonicalSemanticProject`.
   - **Mecanismo**: Generar hashes profundos del objeto canónico antes y después de la proyección. Si el hash cambia, el test falla y bloquea la compilación.
2. **Tests de Privacidad y Visibilidad (Privacy by Projection)**:
   - **Objetivo**: Garantizar que campos técnicos/sensibles no se filtren a roles de negocio (ej. `DATA_ANALYST` no puede ver claves subrogadas ni DAX).
3. **Tests Golden (Regresión Determinista)**:
   - **Objetivo**: Los mismos inputs *siempre* deben generar exactamente las mismas proyecciones JSON/Markdown. Los "Golden Files" actuarán como anclas de regresión.
4. **Tests de Consistencia Cruzada (Cross-Lens Consistency)**:
   - **Objetivo**: Validar que un mismo `metric_id` signifique exactamente lo mismo, tenga el mismo dueño y estado de certificación en los 10 Lenses y en el Leadership Cockpit.
5. **Tests de Recomendación Organizacional**:
   - **Objetivo**: Asegurar que toda recomendación organizacional posea evidencia rastreable, y evitar inferencias algorítmicas de "desempeño" personal (Safety Tests).
6. **Tests de Fronteras Arquitectónicas (Boundary Tests)**:
   - **Objetivo**: Evitar el acoplamiento espagueti. Se probará a nivel de AST/Imports que el paquete `leadership` NUNCA sea importado por los Lenses individuales, y que el núcleo canónico jamás importe de `personas`.
7. **Tests de Contratos (Pydantic Validation)**:
   - **Objetivo**: Validar la serialización determinista y estricta de las 7 nuevas entidades de proyección (`PersonaProjection`, `ResponsibilityAssignment`, etc.).
8. **Tests End-to-End (E2E)**:
   - **Objetivo**: Recorrer el ciclo de vida completo: Parser → Calidad → Proyección de Personas → Leadership Cockpit → Emisión TMDL.

---

## 3. Conflictos Identificados y Resoluciones Arquitectónicas (ADRs)

El plan exige no romper las vistas actuales (`EXECUTIVE`, `DATA_GOVERNANCE`, `BI_ENGINEER`), pero el nuevo marco es incompatible. Se crearán los siguientes Documentos de Decisión (ADRs) en la Fase 1:

- **ADR-001: Persona como Perfil de Responsabilidad**. Transición de un simple "Job Title" a un marco componible.
- **ADR-002: Lenses como Proyecciones de Solo-Lectura**. Obligación de usar *Deep Copies* controlados.
- **ADR-003: Aislamiento del Leadership Cockpit**. Separación física en `src/core/leadership/`. No recalcula, solo agrega.
- **ADR-004: Compatibilidad Legacy**. Creación de un `legacy_adapter.py` en `personas` que mapeará los enums antiguos (`PersonaType`) hacia el nuevo motor de proyecciones, para mantener los tests de la Etapa 4 en verde mientras se migra.
- **ADR-005: Seguridad Organizacional**. Prohibición sistémica de medir "productividad individual".

---

## 4. Roadmap de Implementación Escalonada (12 Fases)

La transición no será un "Big Bang". Se estructurará en 12 fases incrementales, cada una protegida por un "Gate" de testing.

### FASE 0: Baseline & Discovery
- **Estado**: ✅ **COMPLETADO** mediante la auditoría actual y la confirmación de los 25/25 tests exitosos.

### FASE 1: Decisiones Arquitectónicas (ADRs)
- **Acción**: Redacción de los ADRs (001 a 005) en `docs/architecture/adr/`.
- **Test Gate**: Revisión documental. Cero impacto en código.

### FASE 2: Contratos Comunes (Cimientos)
- **Acción**: Creación de los contratos Pydantic v2 en `src/core/personas/models.py` (`PersonaDefinition`, `PersonaProjection`, `PersonaRecommendation`, `ResponsibilityAssignment`, `TeamInteraction`, `PersonaMaturityAssessment`) y la interfaz `PersonaLens`.
- **Acción Crítica**: Modificar `CanonicalSemanticProject` para incluir el campo opcional `governance: Optional[GovernanceMetadata] = None`.
- **Test Gate**: Tests de serialización, determinismo y no-regresión de la base canónica.

### FASE 3: Registro y Configuración
- **Acción**: Creación de `PersonaRegistry` y carga de configuraciones desde `config/personas.default.yaml`.
- **Acción Crítica**: Implementación de `legacy_adapter.py` para asegurar que el método antiguo `PersonaViewGenerator.generate_views()` siga funcionando (envolviendo el nuevo sistema).
- **Test Gate**: Los tests originales de `test_stage4_hardening_personas.py` deben seguir pasando intactos.

### FASE 4: Motor de Proyección y Renderizadores
- **Acción**: Construcción de `PersonaProjector`, el motor de políticas de visibilidad (`VisibilityPolicy`), y los renderizadores Markdown y JSON.
- **Test Gate**: Pruebas explícitas de **Mutation Safety** probando que el motor copia y no muta los datos de entrada.

### FASE 5: Primer "Slice" Vertical (4 Lenses Core)
- **Acción**: Implementación iterativa de los primeros Lenses:
  1. `DOMAIN_OWNER` (Negocio/Valor)
  2. `ANALYTICS_ENGINEER` (Diseño Semántico)
  3. `BI_DEVELOPER` (Implementación Target/PowerBI)
  4. `DATA_ANALYST` (Consumo/Catálogo)
- **Test Gate**: 10+ pruebas rigurosas por Lens (Golden Tests, Consistencia, Privacidad).

### FASE 6: Lenses de Control y Gobierno
- **Acción**: Implementación de `DATA_GOVERNANCE_OFFICER`, `AUDIT_RISK` y `DATA_ARCHITECT`.
- **Test Gate**: Reconciliación cruzada entre los Lenses de Ingeniería y los de Gobierno (las dependencias y clasificaciones deben cuadrar perfectamente).

### FASE 7: Lenses de Ingeniería y Analítica Avanzada
- **Acción**: Implementación de `DATA_ENGINEER`, `PLATFORM_ENGINEER` y `DATA_SCIENTIST`.
- **Test Gate**: Verificación del ecosistema completo (10 Lenses base).

### FASE 8: Framework de Responsabilidad e Interacción (RACI)
- **Acción**: Implementación de matrices de responsabilidad configurables y topologías de equipo basadas en metadatos, evitando hardcore logic. Configuración en `config/team_interactions.default.yaml`.
- **Test Gate**: Tests de **Seguridad Organizacional** (sin identificación indebida de personal, y manejo explícito de missing data).

### FASE 9: Cimientos del Leadership Cockpit
- **Acción**: Creación del paquete aislado `src/core/leadership/`. Implementación del `LeadershipCockpit` que consume los `PersonaProjections` generados.
- **Acción Crítica**: Módulos fundacionales: `portfolio.py`, `health.py`, `ownership.py`.
- **Test Gate**: Boundary tests. Confirmar algorítmicamente que Leadership no incluye lógicas de calidad (`cQS`) o linaje duplicadas.

### FASE 10: Módulos Avanzados del Leadership Cockpit
- **Acción**: Integración de métricas de Brechas de Capacidad (`capability_gaps`), Flujo de Entrega (`delivery_flow`), Riesgos (`risk`) y Recomendaciones ejecutivas.
- **Test Gate**: Trazabilidad completa. Todo agregado numérico debe tener punteros a la evidencia (IDs de métricas o entidades).

### FASE 11: CLI, SDK y Automatización
- **Acción**: Expandir `src/cli.py` (comandos `semanticflow personas generate`, `list`, `semanticflow leadership health`, etc.). Implementación de SDK público en `src/core/personas/sdk.py`.
- **Test Gate**: Tests End-to-End en la interfaz CLI. Soporte Dry-run.

### FASE 12: Documentación de Grado Enterprise
- **Acción**: Guías de arquitectura, documentación por Lens, manuales del Cockpit y guías de configuración.
- **Test Gate**: Un usuario externo puede comprender el framework, generar un Lens y rastrear la evidencia.

---

## 5. Diseño de la Primera Iteración Ejecutable (Fases 1 y 2)

Para dar el primer paso sin riesgo, la iteración inicial se limitará estrictamente a los contratos y la documentación, preparando el terreno sin romper funcionalidades:

**Archivos a Crear:**
1. `docs/architecture/adr/ADR-001-persona-vs-job-title.md`
2. `docs/architecture/adr/ADR-002-persona-lens-read-only-projection.md`
3. `docs/architecture/adr/ADR-003-leadership-cockpit-isolation.md`
4. `docs/architecture/adr/ADR-004-legacy-view-compatibility.md`
5. `src/core/personas/__init__.py`
6. `src/core/personas/models.py` (Los 7 contratos principales Pydantic v2)
7. `src/core/personas/interfaces.py` (`PersonaLens` Base Class)
8. `tests/test_persona_contracts.py` (Nuevos tests)

**Archivos a Modificar:**
1. `src/core/ast/canonical/models.py` (Agregar el campo de gobierno).

**Criterio de Éxito de la Iteración 1:**
- Los 25 tests actuales + los ~16 nuevos tests de contratos pasan exitosamente.
- El objeto canónico retiene total retrocompatibilidad.
- No se toca aún `views.py`.
