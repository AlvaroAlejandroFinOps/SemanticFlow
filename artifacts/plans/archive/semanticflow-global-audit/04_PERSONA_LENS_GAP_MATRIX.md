# 04. MATRIZ DE BRECHAS DEL FRAMEWORK PERSONA LENS (DIMENSIÓN B)

**Proyecto:** SemanticFlow  
**Fecha de Auditoría:** 2026-09-19  
**Commit:** `59f3c929b3e7a2d52ceb3553b9285388a52eee52`  

---

## 1. REGLAS FUNDAMENTALES Y DIAGNÓSTICO DE DRIFT EN ROLES

> [!WARNING]
> **REGLAS DE IDENTIDAD CANÓNICA DE PERSONAS:**
> 1. No declarar equivalencia automática entre `DATA_SCIENTIST` y `AI_SYSTEMS_ENGINEER`.
> 2. No declarar equivalencia entre `DATA_ARCHITECT` y `ANALYTICS_LEADER`.
> 3. No sustituir `PLATFORM_ENGINEER` por `FINOPS_SPECIALIST`.
> 4. No sustituir `AUDIT_RISK` completamente por `COMPLIANCE_AUDITOR` sin delta documentado.
> 5. Las Extension Personas **no cuentan como reemplazo** de las diez Core Personas.

### Diagnóstico del Código Actual (`src/core/personas/lenses/`)
El repositorio cuenta con 10 archivos de lentes y 10 registros en `default_personas.yaml`, pero presenta el siguiente desacople frente a la norma de 10 Core Personas:

| Posición | Rol Implementado Actualmente | Estado Canónico | Brecha Detectada | Acción de Alineación Requerida |
|---|---|---|---|---|
| 1 | `data_engineer.py` | ✅ CORE | Ninguna | Mantener como `DATA_ENGINEER`. |
| 2 | `analytics_engineer.py` | ✅ CORE | Ninguna | Mantener como `ANALYTICS_ENGINEER`. |
| 3 | `bi_developer.py` | ✅ CORE | Ninguna | Mantener como `BI_DEVELOPER`. |
| 4 | `data_governance_officer.py` | ✅ CORE | Ninguna | Mantener como `DATA_GOVERNANCE_OFFICER`. |
| 5 | `business_consumer.py` | ⚠️ EXTENSION | Se utilizó en lugar de `DATA_ANALYST` | Crear lente `data_analyst.py` independiente; mantener `business_consumer.py` como extensión. |
| 6 | `ai_systems_engineer.py` | ⚠️ EXTENSION | Se utilizó en lugar de `DATA_SCIENTIST` | Crear lente `data_scientist.py` independiente; mantener `ai_systems_engineer.py` como extensión. |
| 7 | `analytics_leader.py` | ⚠️ EXTENSION | Se utilizó en lugar de `DATA_ARCHITECT` | Crear lente `data_architect.py` independiente; mantener `analytics_leader.py` como extensión. |
| 8 | `finops_specialist.py` | ⚠️ EXTENSION | Se utilizó en lugar de `PLATFORM_ENGINEER` | Crear lente `platform_engineer.py` independiente; mantener `finops_specialist.py` como extensión. |
| 9 | `data_product_manager.py` | ⚠️ EXTENSION | Se utilizó en lugar de `DOMAIN_OWNER` | Crear lente `domain_owner.py` independiente; mantener `data_product_manager.py` como extensión. |
| 10 | `compliance_auditor.py` | ⚠️ EXTENSION | Se utilizó en lugar de `AUDIT_RISK` | Crear lente `audit_risk.py` independiente; mantener `compliance_auditor.py` como extensión. |

---

## 2. MATRIZ DE EVALUACIÓN INDIVIDUAL POR CORE PERSONA

### 2.1 DATA_ANALYST (Core B1)
- **Propósito:** Consumo analítico de autoservicio, exploración de catálogos y KPIs certificadas.
- **Información Visible:** Hechos certificados, dimensiones conformadas, descripciones de negocio, KPIs.
- **Información Oculta:** Claves foráneas técnicas, expresiones DAX complejas, detalles de particionamiento.
- **Estado Actual:** `PARTIAL` (Actualmente servido por `business_consumer.py`).
- **Artefactos Probados:** Markdown (`tests/test_all_lenses_deep.py`), JSON, Golden file en `metro_santiago` y `enterprise`.
- **Acción:** Crear `src/core/personas/lenses/data_analyst.py` con foco en catálogo y exploración analítica.

### 2.2 ANALYTICS_ENGINEER (Core B2)
- **Propósito:** Modelado dimensional, definición de grano, diseño star-schema y lógica de métricas semánticas.
- **Información Visible:** Grano de tabla, llaves subrogadas, linaje de transformación, reglas de cálculo.
- **Información Oculta:** PII sin enmascarar, detalles de infraestructura física.
- **Estado Actual:** `VERIFIED` (`src/core/personas/lenses/analytics_engineer.py`).
- **Artefactos Probados:** Test unitario, Golden test, Privacy test, Mutation test pasando al 100%.

### 2.3 DATA_ENGINEER (Core B3)
- **Propósito:** Salud de pipelines, esquemas físicos, particionamiento, orígenes de datos y tipos de datos brutos.
- **Información Visible:** Tipos de datos físicos, columnas anulables, origen upstream, particiones.
- **Información Oculta:** Fórmulas DAX avanzadas de presentación de negocio.
- **Estado Actual:** `VERIFIED` (`src/core/personas/lenses/data_engineer.py`).
- **Artefactos Probados:** Test unitario, Golden test, Privacy test, Mutation test pasando al 100%.

### 2.4 DATA_SCIENTIST (Core B4)
- **Propósito:** Features numéricas y categóricas para modelos ML, cardinalidad, completitud y distribuciones.
- **Información Visible:** Atributos de features, tipos estadísticos, dimensiones conformadas, etiquetas.
- **Información Oculta:** Detalles de display folders de Power BI y DAX de formato.
- **Estado Actual:** `PARTIAL` (Actualmente sustituido por `ai_systems_engineer.py`).
- **Acción:** Crear `src/core/personas/lenses/data_scientist.py` con contrato enfocado en feature analysis.

### 2.5 BI_DEVELOPER (Core B5)
- **Propósito:** Generación de modelos tabulares, relaciones TMDL, display folders, formateo y medidas DAX.
- **Información Visible:** TMDL, DAX, relaciones activas/inactivas, carpetas de despliegue, cadenas de formato.
- **Información Oculta:** Metadatos de infraestructura cloud no tabulares.
- **Estado Actual:** `VERIFIED` (`src/core/personas/lenses/bi_developer.py`).
- **Artefactos Probados:** Test unitario, Golden test, TMDL integration test pasando al 100%.

### 2.6 DATA_ARCHITECT (Core B6)
- **Propósito:** Topología global de datos, dominios analíticos, conformación de dimensiones y compatibilidad multi-target.
- **Información Visible:** Grafo relacional, dependencias entre entidades, evaluación de dialectos de destino.
- **Información Oculta:** Detalles de visualización individual de reportes.
- **Estado Actual:** `PARTIAL` (Actualmente sustituido por `analytics_leader.py`).
- **Acción:** Crear `src/core/personas/lenses/data_architect.py` enfocado en topología de grafo y arquitectura neutral.

### 2.7 DATA_GOVERNANCE_OFFICER (Core B7)
- **Propósito:** Clasificación de datos, identificación PII, estatus de certificación, dueños y score cQS.
- **Información Visible:** Clasificación (`Confidential`, `Public`, `PII`), estado de certificación, diagnósticos de calidad.
- **Información Oculta:** Ninguna restricción de metadatos de gobierno.
- **Estado Actual:** `VERIFIED` (`src/core/personas/lenses/data_governance_officer.py`).
- **Artefactos Probados:** Test unitario, Golden test, Governance inheritance test pasando al 100%.

### 2.8 PLATFORM_ENGINEER (Core B8)
- **Propósito:** Capacidad del motor analítico, modos de almacenamiento (Import/Direct Lake), latencia y SLOs.
- **Información Visible:** Modos de almacenamiento, métricas de escalabilidad, tamaño de metadatos.
- **Información Oculta:** Lógica de negocio específica de métricas.
- **Estado Actual:** `PARTIAL` (Actualmente sustituido por `finops_specialist.py`).
- **Acción:** Crear `src/core/personas/lenses/platform_engineer.py` enfocado en capacidad de cómputo y storage modes.

### 2.9 DOMAIN_OWNER (Core B9)
- **Propósito:** Alineación de productos de datos con objetivos del dominio de negocio, KPIs certificados y ciclo de vida.
- **Información Visible:** Catálogo del producto de datos, KPIs de dominio, estado de madurez, acuerdos de nivel de servicio.
- **Información Oculta:** Código DAX interno y claves técnicas foráneas.
- **Estado Actual:** `PARTIAL` (Actualmente sustituido por `data_product_manager.py`).
- **Acción:** Crear `src/core/personas/lenses/domain_owner.py` enfocado en ownership de dominio y valor de negocio.

### 2.10 AUDIT_RISK (Core B10)
- **Propósito:** Auditoría de cumplimiento normativo (GDPR, SOX), trazabilidad de linaje y registro de excepciones.
- **Información Visible:** Matriz de excepciones, trazabilidad de cambios, severidad de riesgos sin mitigar.
- **Información Oculta:** Datos personales en texto claro.
- **Estado Actual:** `PARTIAL` (Actualmente sustituido por `compliance_auditor.py`).
- **Acción:** Crear `src/core/personas/lenses/audit_risk.py` con foco en matriz de riesgos y excepciones.

---

## 3. AGGREGATE PERSONA: DATA_LEADERSHIP

- **Propósito:** Síntesis holística ejecutiva C-Level para CDO, VP de Datos y líderes estratégicos.
- **Capacidades:** Radar de madurez por dominio, KPIs certificados, matriz RACI consolidada, acciones prioritarias.
- **Estado Actual:** `VERIFIED` en generación de modelo consolidado (`LeadershipCockpit`), pero `PARTIAL` en modularidad física.

---

## 4. EXTENSION PERSONAS COMPLEMENTARIAS (6 EXTENSIONES)

Las siguientes 6 personas se mantienen operativas en `src/core/personas/lenses/` como extensiones organizacionales válidas:
1. `AI_SYSTEMS_ENGINEER`: Feature stores y pipelines de inferencia.
2. `ANALYTICS_LEADER`: Gestión de portafolio y estrategia ejecutiva de analítica.
3. `BUSINESS_CONSUMER`: Auto-servicio y consumo de reportes operativos.
4. `DATA_PRODUCT_MANAGER`: Gestión de producto de datos y feedback loop.
5. `COMPLIANCE_AUDITOR`: Verificación formal de controles de cumplimiento.
6. `FINOPS_SPECIALIST`: Atribución de costos y optimización de cómputo cloud.
