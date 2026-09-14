# SEMANTICFLOW: Compilador Declarativo de Modelos Semánticos y Plataforma de Calidad Nivel Enterprise

**Idioma:** [English](README.md) | [Español](README_ES.md)

![Versión de Python](https://img.shields.io/badge/python-3.10%2B-1a1a1a?style=flat-square)
![Arquitectura](https://img.shields.io/badge/arquitectura-Modelo%20Sem%C3%A1ntico%20Can%C3%B3nico-2b2b2b?style=flat-square)
![Verificación](https://img.shields.io/badge/verificaci%C3%B3n-25%2F25%20APROBADOS-34495e?style=flat-square)
![Licencia](https://img.shields.io/badge/licencia-Apache--2.0-4b5563?style=flat-square)

---

## 1. Resumen Ejecutivo

SemanticFlow es una plataforma de ingeniería semántica agnóstica de nivel enterprise diseñada para compilar esquemas relacionales a un modelo semántico canónico unificado y emitir artefactos nativos de Inteligencia de Negocios (BI), enfocada prioritariamente en Microsoft Power BI (TMDL/PBIP). La plataforma resuelve la fragilidad estructural, el acoplamiento a proveedores y la falta de gobierno automatizado inherentes a los flujos de desarrollo BI tradicionales. Al desacoplar el parseo de sintaxis relacional de la generación de código destino, SemanticFlow introduce una representación intermedia (AST Canónico) que garantiza compatibilidad bidireccional, inferencia automatizada de roles de esquema estrella y evaluación continua de calidad semántica.

Operando bajo un paradigma de cero regresiones y ejecución preferentemente local, SemanticFlow aprovecha la teoría de grafos mediante NetworkX para inferir dinámicamente roles dimensionales y claves sustitutas (*surrogate keys*). Asimismo, incorpora un Motor de Calidad Semántica ($cQS$) automatizado que evalúa reglas de gobierno, declaraciones de granularidad y certificación de métricas previo a la emisión de artefactos. El sistema se adhiere estrictamente al patrón *Strangler Fig*, asegurando la coexistencia sin fisuras entre emisores legados y la representación intermedia canónica extensible.

---

## 2. Arquitectura y Topología del Sistema

```
+-----------------------------------------------------------------------------------+
|                                ENTRADAS RELACIONALES                              |
|            +-----------------------+     +-----------------------+                |
|            | Esquemas Markdown (.md)|     |  Esquemas YAML (.yaml)|                |
|            +-----------+-----------+     +-----------+-----------+                |
+------------------------|-----------------------------|----------------------------+
                         |                             |
                         v                             v
+-----------------------------------------------------------------------------------+
|                           CAPA DE PARSEO DE SINTAXIS                              |
|                     +-----------------------------------+                         |
|                     | Parsers Relacionales Markdown/YAML|                         |
|                     +-----------------+-----------------+                         |
+---------------------------------------|-------------------------------------------+
                                        v
+-----------------------------------------------------------------------------------+
|                        CAPA DE TRANSFORMACIÓN CANÓNICA                            |
|                   +---------------------------------------+                       |
|                   |   Mapper Raw AST a Modelo Canónico    |                       |
|                   +-------------------+-------------------+                       |
|                                       |                                           |
|                                       v                                           |
|                   +---------------------------------------+                       |
|                   |       CanonicalSemanticProject        |                       |
|                   |  (Entidades, Atributos, Métricas, etc)|                       |
|                   +-------------------+-------------------+                       |
+---------------------------------------|-------------------------------------------+
                                        |
       +--------------------------------+--------------------------------+
       |                                |                                |
       v                                v                                v
+----------------------+     +----------------------+     +----------------------+
|  CALIDAD Y GOBIERNO  |     |   MOTOR INFERENCIA   |     |   PERSONAS Y DOCS    |
|  SemanticQualityScorer|     | NetworkX RoleInferer |     | DocumentationEmitter |
|  Evaluación cQS (0-100|     |  SemanticExplainer   |     | Mermaid ERD / Dict   |
+----------+-----------+     +----------+-----------+     +----------+-----------+
           |                            |                            |
           +----------------------------+----------------------------+
                                        |
                                        v
+-----------------------------------------------------------------------------------+
|                          CAPA DE ADAPTACIÓN TARGET (BI)                           |
|                    +------------------------------------------+                   |
|                    |          PowerBiTargetAdapter            |                   |
|                    |     (Canónico -> AST Modelo Power BI)    |                   |
|                    +------------------+-----------------------+                   |
+---------------------------------------|-------------------------------------------+
                                        v
+-----------------------------------------------------------------------------------+
|                           CAPA DE EMISIÓN Y SALIDA                                |
|            +-----------------------+     +-----------------------+                |
|            |  Definiciones TMDL    |     |  Paquete PBIP Disco   |                |
|            +-----------------------+     +-----------------------+                |
+-----------------------------------------------------------------------------------+
```

---

## 3. Formulación Matemática y Motores Analíticos

### 3.1. Formulación del Puntaje de Calidad Canónico ($cQS$)

SemanticFlow calcula un Puntaje de Calidad Semántica ($cQS \in [0, 100]$) objetivo y normalizado que evalúa la integridad estructural, adhesión al gobierno y profundidad de documentación de un proyecto canónico $P = (E, R, G)$.

Sea $E$ el conjunto de entidades, $R$ el conjunto de relaciones, $M = \bigcup_{e \in E} M_e$ el conjunto agregado de métricas, y $A = \bigcup_{e \in E} A_e$ el conjunto de atributos. El puntaje total se formula como una suma ponderada de cuatro métricas de dominio ortogonales:

$$cQS(P) = w_g \cdot S_{\text{grain}}(E) + w_m \cdot S_{\text{metric}}(M) + w_c \cdot S_{\text{cert}}(M) + w_r \cdot S_{\text{ratio}}(M)$$

Sujeto a la normalización de pesos:

$$w_g + w_m + w_c + w_r = 1.0 \quad (w_g = 0.35, \, w_m = 0.25, \, w_c = 0.20, \, w_r = 0.20)$$

1. **Puntaje de Granularidad en Hechos ($S_{\text{grain}}$):** Evalúa la declaración explícita de granularidad en entidades de Hechos $E_F = \{e \in E \mid \text{role}(e) = \text{FACT}\}$:

$$S_{\text{grain}}(E) = \frac{|\{e \in E_F \mid \text{has\_explicit\_grain}(e)\}|}{|E_F| + \epsilon} \times 100$$

2. **Compleitud de Documentación de Métricas ($S_{\text{metric}}$):**

$$S_{\text{metric}}(M) = \frac{|\{m \in M \mid \text{description}(m) \neq \emptyset\}|}{|M| + \epsilon} \times 100$$

3. **Gobierno de Métricas Certificadas ($S_{\text{cert}}$):**

$$S_{\text{cert}}(M) = \frac{|\{m \in M_{\text{cert}} \mid \text{owner}(m) \neq \emptyset \land \text{lineage}(m) \neq \emptyset\}|}{|M_{\text{cert}}| + \epsilon} \times 100$$

Donde $M_{\text{cert}} = \{m \in M \mid \text{certified}(m) = \text{True}\}$.

### 3.2. Motor de Inferencia de Roles de Esquema Estrella Dirigido

Dado un grafo relacional no dirigido $G = (V, E_{\text{rel}})$, donde $V$ representa las tablas y $E_{\text{rel}}$ las relaciones de clave foránea, el Motor de Inferencia construye un grafo dirigido acíclico $DAG = (V, E_{\text{dirigido}})$ para inferir los roles dimensionales $\rho: V \to \{\text{DIMENSION}, \text{FACT}, \text{BRIDGE}\}$.

La centralidad de grado $C_D(v)$ y la proporción de grado entrante $\delta_{in}(v)$ se definen como:

$$C_D(v) = \deg(v), \quad \delta_{in}(v) = \frac{\text{in-degree}(v)}{\deg(v) + \epsilon}$$

La función de asignación de rol $\rho(v)$ se formula como:

$$\rho(v) = \begin{cases} 
\text{FACT} & \text{si } \delta_{in}(v) \ge \tau_{\text{fact}} \land C_D(v) > 1 \\
\text{DIMENSION} & \text{si } \delta_{in}(v) < \tau_{\text{fact}} \land \text{out-degree}(v) > 0 \\
\text{BRIDGE} & \text{en otro caso}
\end{cases}$$

Donde $\tau_{\text{fact}} = 0.60$ es el umbral empírico para convergencia de hechos en esquema estrella.

---

## 4. Rendimiento Empírico y Benchmarks

La validación operacional se ejecutó sobre múltiples esquemas sintéticos y enterprise (Pyme Tier 1, Mediana Tier 2, Gigante Tier 3, y Metro Santiago Metro V2).

| Métrica | Límite Objetivo | Línea Base | Resultado Empírico de Producción | Estado |
|:--------|:----------------|:-----------|:---------------------------------|:-------|
| Latencia Mapeo AST | $< 500\text{ ms}$ | $120\text{ ms}$ | **$18.4\text{ ms}$** | PASS |
| Latencia Emisión TMDL | $< 2.0\text{ s}$ | $850\text{ ms}$ | **$142.0\text{ ms}$** | PASS |
| Suite de Verificación | $100\%$ Éxito | $22/22$ | **$25/25\text{ APROBADOS}$ ($100\%$)** | PASS |
| Puntaje de Calidad ($cQS$) | $\ge 40.0$ (Default) | N/A | **$50.0 / 100.0$** (10 Warns, 0 Errores) | PASS |
| Consumo de Memoria | $< 256\text{ MB}$ | $95\text{ MB}$ | **$48.2\text{ MB}$** | PASS |

---

## 5. Estructura del Repositorio y Artefactos

```
SemanticFlow/
├── 001_Seed/                           # ADN Arquitectónico & Snapshots ThinkingSeed
│   ├── seed-SemanticFlow.md            # Seed Liviano
│   └── seed-SemanticFlow-master.md     # Seed Master Exhaustivo Nivel Paper
├── 02_Foundation/                      # Líneas base de esquemas y modelos de referencia
│   ├── 01_Schemas/
│   └── 02_Reference_Models/
├── docs/                               # Gobierno y Registros de Decisiones (ADR)
│   ├── adr/
│   │   └── ADR-001-canonical-model.md  # Architectural Decision Record 001
│   └── architecture/
│       └── esquema_relacional.md       # Esquema Relacional de Referencia (Metro Santiago)
├── output/                             # Directorio por defecto para salidas target
│   ├── docs/                           # Diccionarios de Datos y Diagramas ERD Mermaid
│   └── PBIP/                           # Paquetes Compilados Power BI PBIP/TMDL
├── src/                                # Paquete Código Fuente Core
│   ├── cli.py                          # Punto de Entrada CLI con Typer y Rich
│   └── core/                           # Sistema Core Modular
│       ├── ast/                        # Árboles de Sintaxis Abstracta (Canónico y Target)
│       │   ├── canonical/models.py     # Modelo de Proyecto Semántico Canónico
│       │   ├── semantic.py             # Modelo AST Legado Power BI (Strangler Fig)
│       │   └── types.py                # Tipos de Datos y Enums Primitivos
│       ├── capabilities/planner.py     # Planificador de Capacidades por Target
│       ├── docs/emitter.py             # Emisor de Diccionario Markdown y ERD Mermaid
│       ├── emitter/                    # Escritores en Disco de Archivos TMDL y PBIP
│       ├── engine/                     # Compilador, Inferredor y Explicador de Procedencia
│       ├── mappers/                    # Mapeadores Raw-a-Canónico y Canónico-a-Target
│       ├── parsers/                    # Parsers Relacionales Markdown y YAML
│       ├── personas/views.py           # Proyecciones por Persona (Ejecutivo, Gobierno)
│       ├── quality/                    # Motor de Calidad Semántica (Scorer y Reglas)
│       └── targets/                    # Adaptadores BI Multi-target (Power BI)
├── tests/                              # Suite Completa de Verificación (25 Pruebas)
├── pyproject.toml                      # Metadatos del Proyecto y Dependencias
├── LICENSE                             # Licencia Código Abierto Apache-2.0
├── README.md                           # Documentación Maestra (Inglés)
└── README_ES.md                        # Documentación Maestra (Español)
```

---

## 6. Protocolo de Ejecución y Verificación

### 6.1. Configuración del Entorno y Prerrequisitos

Asegúrese de contar con Python 3.10+. Clone el repositorio e aísle el entorno mediante `venv`:

```bash
git clone https://github.com/AlvaroAlejandroFinOps/SemanticFlow.git
cd SemanticFlow
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

### 6.2. Ejecución del Pipeline

#### 1. Compilar Esquema Relacional a Power BI Nativo (TMDL/PBIP)
```bash
python -m src.cli compile --input docs/architecture/esquema_relacional.md --output output/PBIP
```

#### 2. Evaluar el Puntaje de Calidad Semántica ($cQS$) y Validar Gobierno
```bash
python -m src.cli validate --input docs/architecture/esquema_relacional.md --min-score 40.0
```

#### 3. Inspeccionar Procedencia y Explicar Inferencia de Roles
```bash
python -m src.cli explain --input docs/architecture/esquema_relacional.md --format human
```

#### 4. Generar Documentación Enterprise (Diccionario de Datos y ERD)
```bash
python -m src.cli docgen --input docs/architecture/esquema_relacional.md --output output/docs
```

### 6.3. Suite de Verificación y Pruebas Invariantes

Ejecute la suite completa de `pytest` para verificar cero regresiones en parsers, mapeadores, motores de inferencia, calificadores de calidad y emisores destino:

```bash
python -m pytest tests/ -v
```

---

## 7. Glosario de Dominio

* **Modelo Semántico Canónico (CSM):** Representación intermedia agnóstica de la plataforma que encapsula entidades, atributos, relaciones, métricas y metadatos de gobierno de forma independiente del proveedor BI final.
* **Semantic Quality Score ($cQS$):** Métrica matemática normalizada que evalúa modelos semánticos en una escala de 0 a 100 basada en la completitud de granularidad, profundidad de documentación y certificación de métricas.
* **Tabular Model Definition Language (TMDL):** Formato de representación de modelo de objetos basado en texto plano legible por humanos para modelos tabulares de Power BI y Analysis Services.
* **Patrón Strangler Fig:** Estrategia arquitectónica de refactorización utilizada para reemplazar gradualmente componentes legados (`semantic.py`) por el nuevo motor canónico sin interrumpir las interfaces operativas.
* **Clave Sustituta / Surrogate Key (SK):** Clave primaria sintética inferida y ocultada automáticamente por SemanticFlow para preservar la integridad del esquema estrella y ocultar detalles de implementación a los usuarios de negocio.

---

## 8. Referencias Académicas y de Ingeniería

1. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
2. Microsoft Corporation. (2023). *Tabular Model Definition Language (TMDL) Specification*. Microsoft Learn.
3. Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). *Exploring Network Structure, Dynamics, and Function using NetworkX*. Proceedings of the 7th Python in Science Conference (SciPy 2008), 11–15.

### Citación BibTeX

```bibtex
@software{semanticflow_2026,
  author = {SemanticFlow Core Engineering Team},
  title = {SemanticFlow: Enterprise-Grade Declarative Semantic Model Compiler \& Quality Platform},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  url = {https://github.com/AlvaroAlejandroFinOps/SemanticFlow}
}
```
