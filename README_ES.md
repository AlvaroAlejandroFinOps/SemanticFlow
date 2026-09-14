# SEMANTICFLOW: Plataforma Declarativa de Compilación Semántica, Lentes de Personas y Cockpit de Liderazgo

**Idioma:** [English](README.md) | [Español](README_ES.md)

![Python Version](https://img.shields.io/badge/python-3.10%2B-1a1a1a?style=flat-square)
![Arquitectura](https://img.shields.io/badge/arquitectura-AST%20Can%C3%B3nico%20%2B%20Lentes%20de%20Personas-2b2b2b?style=flat-square)
![Verificación](https://img.shields.io/badge/verificaci%C3%B3n-71%2F71%20PASSED-34495e?style=flat-square)
![Licencia](https://img.shields.io/badge/licencia-Apache--2.0-4b5563?style=flat-square)

---

## 1. Resumen Ejecutivo

SemanticFlow es una plataforma de ingeniería semántica desacoplada y de nivel empresarial diseñada para compilar esquemas relacionales en modelos semánticos canónicos unificados, emitir artefactos nativos de Business Intelligence (Microsoft Power BI TMDL/PBIP), proyectar **Lentes de Personas especializadas para 10 roles organizacionales** y sintetizar **Cockpits de Liderazgo de Datos para nivel C-Suite**.

La plataforma elimina la fragilidad estructural, el bloqueo de proveedor y los silos de gobierno al separar el análisis sintáctico de la generación de código. A través de su AST Canónico intermedio, SemanticFlow implementa gobierno en cascada de dos niveles, proyecciones deterministas no destructivas, inferencia topológica estrella con NetworkX y calificación automática de calidad semántica ($cQS$).

---

## 2. Arquitectura y Topología del Sistema

```
+-----------------------------------------------------------------------------------+
|                                ENTRADAS RELACIONALES                              |
|            +-----------------------+     +-----------------------+                |
|            | Esquemas Markdown(.md)|     |  Esquemas YAML (.yaml)|                |
|            +-----------+-----------+     +-----------+-----------+                |
+------------------------|-----------------------------|----------------------------+
                         |                             |
                         v                             v
+-----------------------------------------------------------------------------------+
|                            CAPA DE PARSEO SINTÁCTICO                              |
|                     +-----------------------------------+                         |
|                     | Parsers Relacionales Markdown/YAML|                         |
|                     +-----------------+-----------------+                         |
+---------------------------------------|-------------------------------------------+
                                        v
+-----------------------------------------------------------------------------------+
|                       CAPA DE TRANSFORMACIÓN CANÓNICA                             |
|                   +---------------------------------------+                       |
|                   |   Mapeador Raw AST a Canónico         |                       |
|                   +-------------------+-------------------+                       |
|                                       |                                           |
|                                       v                                           |
|                   +---------------------------------------+                       |
|                   |       CanonicalSemanticProject        |                       |
|                   |  (Entidades, Atributos, Métricas,     |                       |
|                   |   ProjectGovernance, Provenance)      |                       |
|                   +-------------------+-------------------+                       |
+---------------------------------------|-------------------------------------------+
                                        |
        +-------------------------------+-------------------------------+
        |                               |                               |
        v                               v                               v
+----------------------+     +----------------------+     +--------------------------+
|  CALIDAD Y GOBIERNO  |     | MOTOR DE INFERENCIA  |     |   LENTES DE PERSONAS     |
|  SemanticQualityScorer|     | NetworkX RoleInferer |     |  10 Roles Organizacionales|
|  Evaluación cQS (0-100|    |  SemanticExplainer   |     |  Leadership Cockpit      |
|  Reglas PII y Proyecto|     |  Motor de Procedencia|     |  Clasificador Overrides  |
+----------+-----------+     +----------+-----------+     +-------------+------------+
           |                            |                               |
           +----------------------------+-------------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                           CAPA DE ADAPTACIÓN DE DESTINOS                          |
|                    +------------------------------------------+                   |
|                    |          PowerBiTargetAdapter            |                   |
|                    |     (Canónico -> Power BI Model AST)     |                   |
|                    +------------------+-----------------------+                   |
+---------------------------------------|-------------------------------------------+
                                        v
+-----------------------------------------------------------------------------------+
|                             CAPA DE EMISIÓN Y SALIDAS                             |
|            +-----------------------+     +-----------------------+                |
|            | Definiciones TMDL     |     |  Bundle PBIP Completo |                |
|            +-----------------------+     +-----------------------+                |
|            | Leadership Cockpit MD |     |  10x Lentes JSON/MD   |                |
|            +-----------------------+     +-----------------------+                |
+-----------------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática del Score de Calidad Canónica ($cQS$)

SemanticFlow calcula un Semantic Quality Score objetivo y normalizado $cQS \in [0, 100]$:

$$cQS(P) = w_g \cdot S_{\text{grain}}(E) + w_m \cdot S_{\text{metric}}(M) + w_c \cdot S_{\text{cert}}(M) + w_r \cdot S_{\text{ratio}}(M)$$

Con normalización de pesos:

$$w_g + w_m + w_c + w_r = 1.0 \quad (w_g = 0.35, \, w_m = 0.25, \, w_c = 0.20, \, w_r = 0.20)$$

---

## 4. Las 10 Lentes de Personas Empresariales

| ID de Persona | Rol | Profundidad Técnica | Foco Principal |
| :--- | :--- | :--- | :--- |
| `analytics_leader` | `ANALYTICS_LEADER` | `EXECUTIVE` | Alineación Estratégica, Valor de Negocio, KPIs Certificados |
| `data_engineer` | `DATA_ENGINEER` | `TECHNICAL` | Pipelines de Ingestión, Particionamiento, Formatos Físicos |
| `analytics_engineer` | `ANALYTICS_ENGINEER` | `TECHNICAL` | Topología Kimball, Fórmulas Métricas, Definición de Granos |
| `bi_developer` | `BI_DEVELOPER` | `TECHNICAL` | Modelos TMDL Power BI, Medidas DAX, Formato Numérico |
| `data_governance_officer`| `DATA_GOVERNANCE_OFFICER`| `SUMMARY` | Propiedad de Datos, Sensibilidad PII, Linaje de Catálogo |
| `data_product_manager` | `DATA_PRODUCT_MANAGER` | `SUMMARY` | Ciclo de Vida de Data Products, Adopción, Contratos SLA |
| `finops_specialist` | `FINOPS_SPECIALIST` | `SUMMARY` | Costos de Consulta Analítica, Capacidad en Nube |
| `ai_systems_engineer` | `AI_SYSTEMS_ENGINEER` | `TECHNICAL` | Feature Store, Embeddings, Linaje de Datos de Entrenamiento |
| `business_consumer` | `BUSINESS_CONSUMER` | `EXECUTIVE` | Glosario de Negocio, Analítica Self-Service Simplificada |
| `compliance_auditor` | `COMPLIANCE_AUDITOR` | `EXHAUSTIVE` | Trazabilidad Regulatoria (GDPR/SOX), Auditoría de Procedencia |

### 4.1. Matriz de Clasificación de Seguridad para Overrides

- **`SAFE`**: Modificaciones cosméticas (`display_name`, `title`, `description`, `icon`, `aliases`). Aplicadas directamente.
- **`REVIEW_REQUIRED`**: Modificaciones de comportamiento (`technical_depth`, `visible_object_types`, `focus_areas`). Aplicadas con registro de auditoría.
- **`PROHIBITED`**: Invariantes inmutables (`persona_id`, `role`, reglas de seguridad). Rechazados con `ConfigurationValidationError`.

---

## 5. Referencia de Comandos CLI

```bash
# 1. Compilar esquema relacional a Power BI PBIP/TMDL
semanticflow compile -i schema.md -o output/PBIP

# 2. Proyectar perspectiva de una Persona Lens
semanticflow explain -i schema.md --persona executive
semanticflow explain -i schema.md --persona bi_engineer --format md
semanticflow explain -i schema.md --persona data_governance --format json

# 3. Listar las 10 Persona Lenses registradas
semanticflow personas list

# 4. Exportar las 10 Persona Lenses y el Leadership Cockpit
semanticflow personas export -i schema.md -o output/personas --formats md,json

# 5. Generar Cockpit de Liderazgo Ejecutivo C-Level
semanticflow cockpit -i schema.md
semanticflow cockpit -i schema.md -o output/cockpit
```

---

## 6. Benchmark de Verificación y Regresión

La suite de pruebas contiene 71 pruebas automatizadas que cubren unidades, integración, estrés masivo y archivos dorados deterministas:

```bash
.venv/Scripts/python.exe -m pytest tests/ -v
# 71 passed in 9.01s (100% PASS)
```

---

## 7. Citación BibTeX

```bibtex
@software{semanticflow2026,
  author = {SemanticFlow Engineering Team},
  title = {SemanticFlow: Declarative Semantic Compiler, Persona Lens Framework and Leadership Cockpit},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/SemanticFlow/SemanticFlow}}
}
```
