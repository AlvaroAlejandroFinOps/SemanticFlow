# 05. MATRIZ DE BRECHAS DEL DATA LEADERSHIP COCKPIT

**Proyecto:** SemanticFlow  
**Fecha de Auditoría:** 2026-09-19  
**Commit:** `59f3c929b3e7a2d52ceb3553b9285388a52eee52`  

---

## 1. REQUISITOS ARQUITECTÓNICOS DEL LEADERSHIP COCKPIT

| Requisito Arquitectónico | Estado Actual | Evidencia de Código | Diagnóstico y Brecha |
|---|---|---|---|
| **Aislamiento en `src/core/leadership/`** | ❌ NOT_IMPLEMENTED | Reside en `src/core/personas/cockpit.py` | Paquete `src/core/leadership/` no existe físicamente en el árbol de código. |
| **Personas no importan Leadership** | ✅ VERIFIED | `src/core/personas/lenses/*.py` | Ningún lente individual importa clases de Cockpit ni Leadership. |
| **Leadership consume contratos públicos** | ✅ VERIFIED | `PersonaProjection`, `CanonicalSemanticProject` | Consume únicamente las proyecciones y el AST canónico. |
| **Legacy Adapter si permanece en personas** | ⚠️ PARTIAL | `src/core/personas/cockpit.py` | Actualmente `cockpit.py` es el motor activo; requiere desacople y convertirse en wrapper de compatibilidad. |
| **Generación independiente de Power BI** | ✅ VERIFIED | `tests/test_leadership_cockpit.py` | Se genera en memoria y disco sin requerir módulos de emisión TMDL ni PBIP. |
| **No mutación del CanonicalProject** | ✅ VERIFIED | `tests/test_persona_projector.py` | Hash profundo del proyecto permanece idéntico antes y después de la síntesis del Cockpit. |
| **No duplicación de cálculo central** | ✅ VERIFIED | `src/core/personas/projector.py` | Agrega los diagnósticos y métricas ya calculadas, sin reejecutar el scorer ni inferencias. |

---

## 2. EVALUACIÓN DE MÓDULOS FUNCIONALES (8 MÓDULOS)

| Módulo Funcional | Estado | Ubicación Actual | Fuente de Datos / Métrica | Brecha / Acción Siguiente |
|---|---|---|---|---|
| **1. Portfolio** | `PARTIAL` | `PersonaProjector.build_leadership_cockpit()` | Conteo de entidades, métricas y relaciones del proyecto | Extraer a `src/core/leadership/portfolio.py`. |
| **2. Health** | `PARTIAL` | Agregado en `governance_overview` | Estatus de certificación, score cQS y diagnósticos | Extraer a `src/core/leadership/health.py`. |
| **3. Ownership** | `PARTIAL` | `ProjectGovernance.owner`, `steward` | Cobertura de responsables y stewards por entidad | Extraer a `src/core/leadership/ownership.py`. |
| **4. Capability Gaps** | `PARTIAL` | `TargetCapabilityPlanner` | Estado de soporte de dialectos de destino | Extraer a `src/core/leadership/capability_gaps.py`. |
| **5. Team Dependencies** | `PARTIAL` | `TeamInteraction` en proyecciones | Handoffs entre roles organizacionales | Extraer a `src/core/leadership/team_dependencies.py` con exportación Mermaid. |
| **6. Delivery Flow** | `PARTIAL` | `governance.lifecycle` | Estado de madurez del data product (`Draft`, `Production`, `Deprecated`) | Extraer a `src/core/leadership/delivery_flow.py`. |
| **7. Value Indicators** | `PARTIAL` | `governance.strategic_value` | Métricas certificadas alineadas a valor de negocio | Extraer a `src/core/leadership/value_indicators.py`. |
| **8. Risk & Exceptions** | `PARTIAL` | Matriz de recomendaciones prioritarias | Diagnósticos `BLOCKING` y `WARNING` | Extraer a `src/core/leadership/risk.py`. |

---

## 3. ESPECIFICACIÓN DE ARTEFACTOS DE SALIDA (TO-BE)

Actualmente el Cockpit exporta 2 artefactos unificados:
- `output/personas/data_leadership_cockpit.md`
- `output/personas/data_leadership_cockpit.json`

Para alcanzar la especificación Enterprise completa, se modularizarán las salidas en el directorio `output/leadership/`:

```
output/leadership/
├── LEADERSHIP_SUMMARY.md      # Resumen ejecutivo C-Level para directores
├── PORTFOLIO_HEALTH.json      # Telemetría de salud y madurez por dominio
├── OWNERSHIP_COVERAGE.json    # Cobertura de dueños, stewards y gaps
├── CAPABILITY_GAPS.json       # Incompatibilidades con dialectos de destino
├── TEAM_DEPENDENCIES.mmd      # Grafo Mermaid de interacciones entre equipos
├── DELIVERY_FLOW.json         # Ciclo de vida y velocidad de entrega
├── VALUE_INDICATORS.json      # KPIs certificados y valor de negocio
├── RISK_OVERVIEW.json         # Matriz de riesgos y excepciones no resueltas
└── RECOMMENDED_ACTIONS.md     # Plan de acción priorizado (Critical/High)
```
