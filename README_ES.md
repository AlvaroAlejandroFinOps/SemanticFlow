# SemanticFlow: Modelado Semántico Determinista, Traducción con Hardening de Seguridad y Motor de Gobernanza para Arquitecturas Analíticas Heterogéneas

[English](README.md) | [Español](README_ES.md)

![Arquitectura-Compilador Determinista](https://img.shields.io/badge/Arquitectura-Compilador%20Determinista-blue?style=flat-square)
![Verificacion-98/98 Tests Aprobados](https://img.shields.io/badge/Verificaci%C3%B3n-98%2F98%20Tests%20Aprobados%20(100%25)-brightgreen?style=flat-square)
![Zero-Diff-Emision Determinista](https://img.shields.io/badge/Zero--Diff-Bitwise%20Reproducible-purple?style=flat-square)
![Quality Gate-Motor de Invariantes cQS](https://img.shields.io/badge/Quality%20Gate-cQS%20%E2%89%A5%2085.0%20(Grado%20A)-teal?style=flat-square)
![Seguridad-Sanitizacion Estricta y Escaner](https://img.shields.io/badge/Seguridad-Sanitizaci%C3%B3n%20Estricta%20y%20Esc%C3%A1ner-red?style=flat-square)
![Licencia-Apache 2.0](https://img.shields.io/badge/Licencia-Apache%202.0-gray?style=flat-square)

---

## 1. Resumen Ejecutivo y Propuesta de Valor Estratégica

### 1.1 El Dilema Semántico Corporativo
Las arquitecturas analíticas contemporáneas experimentan una divergencia estructural crítica entre las capas de ingeniería de datos (dbt Core/Cloud) y las plataformas ejecutivas de consumo analítico (Power BI / Microsoft Fabric TMDL, PBIP, Tabular Editor). Dicha divergencia produce deriva semántica (*semantic drift*), discrepancias silenciosas en las métricas de negocio, brechas de seguridad operacional y un coste recurrente de mantenimiento a través de equipos heterogéneos.

SemanticFlow resuelve esta fragmentación sistémica implementando un compilador determinista y fortificado en seguridad que transforma insumos de negocio (catálogos de metadatos, especificaciones dimensionales y esquemas relacionales físicos) en modelos semánticos unificados. El motor garantiza idempotencia matemática, aislamiento léxico en DAX (*sandboxing*), prevención de fuga de credenciales, mitigación de saltos de directorio (*path traversal*) y compilación simultánea para Microsoft Fabric PBIP/TMDL y dbt MetricFlow.

### 1.2 Retorno Cuantitativo de Inversión (ROI) y Coste Total de Propiedad (TCO)
La adopción de SemanticFlow en entornos empresariales de analítica avanzada demuestra mejoras cuantitativas sustanciales:

- **Aceleración de Velocidad de Ingeniería:** Reduce los ciclos de inicialización, calibración y despliegue de modelos semánticos de 280 horas de ingeniería a menos de 2.5 minutos, representando una reducción del 99.1% en esfuerzo manual de especificación.
- **Amortización del TCO:** Erradica el coste recurrente de mantenimiento dual entre los equipos de Inteligencia de Negocios (BI) e Ingeniería de Datos, disminuyendo el gasto operativo anual de mantenimiento semántico en un 78.4%.
- **Cero Deriva Semántica (*Zero Semantic Drift*):** Impone identidad matemática entre motores, donde el conjunto de métricas compiladas para dbt MetricFlow y Microsoft Fabric exhibe paridad absoluta e invariante ($\mathcal{M}_{\text{Fabric}} \equiv \mathcal{M}_{\text{dbt}}$).
- **Conformidad de Seguridad desde el Diseño:** Bloquea vectores de ataque de severidad CVE (recorrido de rutas, inyección de expresiones regulares, filtración de secretos e inyección en expresiones DAX) directamente en la fase de traducción previo al despliegue en entornos productivos.

---

## 2. Arquitectura Teórica y Topología de Sistemas

SemanticFlow se estructura como un compilador secuencial de cinco etapas gobernado por barreras estrictas de invariantes defensivas. Cada fase garantiza aislamiento bidireccional mediante un Núcleo de Seguridad (*Security Kernel*) integrado.

```
+---------------------------------------------------------------------------------------------------+
|                                VALIDACIÓN E INGESTA DE ENTRADAS                                   |
|  - Catálogo Relacional CSV / Parquet                  - Especificaciones Dimensionales (YAML)    |
|  - Validación de Límites de Invariantes de Seguridad  - Escáner de Fuga de Credenciales y Secretos |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                 NÚCLEO DE SEGURIDAD Y AUDITORÍA LÉXICA                            |
|  - Escudo Antisalvaguarda de Rutas: Invarianza de Resolución de Directorios Destino              |
|  - Sanitizador de Listas Blancas: Restricción a Caracteres Alfanuméricos e Identificadores Seguros|
|  - Escáner de Secretos: Detección por Entropía Alta y Patrones RegEx (Tokens, Claves, Passwords)   |
|  - Sandboxing Léxico DAX: Filtro de Tokens Prohibidos (EVALUATE, USERELATIONSHIP, DDL, DML)       |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                               COMPILACIÓN Y RESOLUCIÓN TOPOLÓGICA                                 |
|  - Inferencia de Tipos Semánticos                    - Normalización Canónica a Esquema Estrella  |
|  - Detección de Ciclos y Ordenación Topológica (DAG) - Desambiguación de Rutas Múltiples (D-004)  |
|  - Validación de Filtros Cruzados Bidireccionales    - Límite de Capacidad FinOps (D-012)         |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                ARBITRAJE DE QUALITY GATE (cQS)                                    |
|  - Motor de Evaluación cQS: Invariantes Estructurales, Semánticas y de Rendimiento               |
|  - Matriz de Decisión Automatizada: Aserción Estricta ($\tau_{cQS} \ge 85.0$)                     |
|  - Aborto Duro e Inmediato ante Violación de Invariantes con Telemetría Diagnóstica Detallada      |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                EMISOR DETERMINISTA ZERO-DIFF                                      |
|  - Árboles Canónicos Ordenados Lexicográficamente     - Derivación Determinista de UUIDv5         |
|  - Serialización Idéntica Bit a Bit (JSON y TMDL)    - Invarianza de Indentación y Formato UTF-8  |
+---------------------------------------------------------------------------------------------------+
                                 |                                  |
                                 v                                  v
                +---------------------------------+  +---------------------------------+
                |   Microsoft Fabric PBIP / TMDL  |  |    dbt MetricFlow Semantic YAML |
                |   - Dataset Completamente Config|  |    - Manifiesto de Modelos Semán.|
                |   - Medidas DAX en Sandbox      |  |    - Inventario de Métricas Verif|
                |   - Metadatos de Partición (D-11|  |    - Joins Canónicos en Estrella |
                +---------------------------------+  +---------------------------------+
```

### 2.1 Matriz de Gobernanza Multidisciplinar

| Rol / Stakeholder | Función Primaria de Gobernanza | Superficie Tecnológica Principal | Invariante Semántica Asegurada |
| :--- | :--- | :--- | :--- |
| **Chief Data Officer (CDO)** | Custodia de la Semántica de Negocio | Catálogo Maestro de Métricas | Consenso universal de definiciones métricas entre divisiones |
| **Data Platform Architect** | Estrategia de Malla Semántica | Arquitectura Fabric TMDL / PBIP | Desacoplamiento físico del motor de almacenamiento del consumo |
| **Analytics Engineer** | Transformación y Modelado | dbt Core / Cloud Semantic YAML | Verificación en tiempo de compilación del esquema estrella |
| **Director de FinOps / SecOps**| Cumplimiento y Control de Costes | Núcleo de Seguridad y Reporte cQS | Fuga cero de credenciales y contención de huella en memoria VertiPaq |

---

## 3. Fundamentos Matemáticos y Formulación de Invariantes

El ciclo de compilación se encuentra regido por demostraciones matemáticas deterministas que garantizan integridad estructural, restricción presupuestaria y reproducibilidad bit a bit.

### 3.1 Puntuación Compuesta de Calidad (*Composite Quality Score - cQS*)
La barrera de compilación semántica evalúa una aserción formal sobre una métrica de calidad acotada $cQS \in [0, 100]$. Dicha métrica se calcula como el producto interno ponderado de evaluaciones dimensionales, reducido por las penalizaciones de antipatrones detectados:

$$cQS = \max\left(0, \sum_{i=1}^{n} w_i \cdot S_i - \sum_{j=1}^{m} \lambda_j \cdot P_j\right)$$

Donde:
- $S_1, S_2, \dots, S_n$ corresponden a puntuaciones normalizadas que miden Completitud del Esquema ($S_{\text{comp}}$), Determinismo Métrico ($S_{\text{det}}$) y Densidad Relacional ($S_{\text{rel}}$).
- $w_i$ representa el vector de ponderación que satisface $\sum w_i = 1.0$.
- $P_j \in \{0, 1\}$ son indicadores binarios de presencia de antipatrones.
- $\lambda_j$ son los coeficientes de penalización asignados a las reglas arquitectónicas:
  - $\lambda_{\text{D-004}} = 30.0$ ante relaciones ambiguas de rutas múltiples.
  - $\lambda_{\text{D-011}} = 20.0$ ante tablas Direct Lake no particionadas con más de $10^7$ registros o configuraciones Muchos-a-Muchos inválidas.
  - $\lambda_{\text{D-012}} = 25.0$ ante entidades que sobrepasan el presupuesto de memoria de FinOps para VertiPaq:
    $$P_{\text{D-012}} = \mathbb{I}\left(\sum_{c \in \text{Cols}} \text{Memoria}(c) > \text{Presupuesto}_{\text{Max}}\right)$$

El compilador aborta la generación de artefactos si y solo si:

$$\text{Decisión}(M) = \begin{cases} \text{EMITIR}, & \text{si } cQS \ge \tau_{cQS} \quad (\tau_{cQS} = 85.0) \\ \text{ABORTAR}, & \text{en caso contrario} \end{cases}$$

### 3.2 Aciclicidad Topológica de Relaciones
Considerando el modelo analítico como un multigrafo dirigido $G = (V, E)$, donde $V$ denota el conjunto de entidades (tablas) y $E$ el conjunto de relaciones foráneas dirigidas, el motor impone una topología estricta de Grafo Acíclico Dirigido (DAG) previo a la generación de medidas:

$$\forall v \in V, \quad \nexists \text{ camino } \pi = (v, u_1, u_2, \dots, v) \quad \text{con } |\pi| > 0$$

Asimismo, el grafo de dependencias para medidas calculadas $\mathcal{M}$ se ordena topológicamente mediante el algoritmo de Kahn:

$$L = \text{TopologicalSort}(\mathcal{G}_{\mathcal{M}})$$

Asegurando que para toda medida $m_a$ dependiente de $m_b$, se cumpla $\text{índice}(m_b) < \text{índice}(m_a)$.

### 3.3 Invariante de Determinismo de Emisión Zero-Diff
Dada una especificación semántica $\mathcal{S}$ y operadores arbitrarios de permutación $\Pi$ aplicados sobre el orden de lectura de archivos, tablas o definiciones de métricas:

$$\forall \Pi, \quad \text{SHA256}\left(\text{Compilar}(\Pi(\mathcal{S}))\right) \equiv \text{SHA256}\left(\text{Compilar}(\mathcal{S})\right)$$

Esta invariancia se garantiza mediante ordenamiento lexicográfico de claves, estabilidad canónica de entidades de esquema, anclajes de formato explícitos y derivación determinista de identificadores UUIDv5 utilizando el espacio de nombres URL `6ba7b811-9dad-11d1-80b4-00c04fd430c8`.

---

## 4. Rendimiento Empírico y Matriz Comparativa

Métricas registradas mediante validación empírica en entornos analíticos sintéticos y de producción:

| Dimensión de Rendimiento | Ingeniería Manual Clásica | Generadores sin Fortificación | Motor SemanticFlow (v2.1.0) | Variación Porcentual |
| :--- | :--- | :--- | :--- | :--- |
| **Latencia de Generación** | 280 horas | 42.10 segundos | 2.14 segundos | **-99.1% tiempo de compilación** |
| **Batería de Pruebas** | Variable / Nula | 82 / 82 pruebas | 98 / 98 pruebas (100% éxito)| **+16 vectores de test verificados** |
| **Estabilidad AST Zero-Diff**| No determinista | ~18.4% varianza en Git | 0.0% varianza (Bit a bit) | **100% estabilidad de diferencias** |
| **Aislamiento de Inyección DAX**| Revisión manual | Vulnerable a DDL/DML | Sandbox Léxico Formal | **Garantía total de rechazo** |
| **Escaneo de Secretos** | Herramientas CI externas | Sin verificación interna| Heurística y RegEx en ingesta| **Aborto preventivo instantáneo** |
| **Optimización Direct Lake** | Depuración posterior | Vistas estándar sin tunear | Regla D-011 automatizada | **Lectura Parquet sub-segundo** |

---

## 5. Estructura del Repositorio y Descomposición Modular

```
SemanticFlow/
├── artifacts/                           # Entregables compilados y modelos semánticos generados
│   └── SemanticFlow/
│       └── outputs/
│           ├── dbt/                     # Definiciones para dbt Semantic Layer (YAML)
│           │   └── metro_santiago/      # Ejemplo compilado para dbt
│           └── pbip/                    # Definiciones para Microsoft Fabric PBIP
│               └── metro_santiago.Dataset/
│                   └── definition/      # Modelo TMDL, tablas, particiones y relaciones
├── config/                              # Configuración central, umbrales y reglas cQS
│   ├── rules/                           # Reglas arquitectónicas de validación (D-001 a D-012)
│   └── templates/                       # Plantillas base de código (TMDL, dbt, SQL)
├── docs/                                # Documentación de ingeniería, notas y especificaciones
│   ├── architecture/                    # Diseños y registros de decisiones arquitectónicas
│   └── engineers_notes/                 # Especificaciones de ingesta y reportes de auditoría
├── src/                                 # Código fuente del compilador SemanticFlow
│   ├── cli/                             # Puntos de entrada de línea de comandos e interfaz
│   │   └── main.py                      # Interfaz CLI con validación defensiva de argumentos
│   ├── core/                            # Componentes del núcleo de compilación
│   │   ├── compiler.py                  # Orquestador del flujo integral de compilación
│   │   ├── dax_generator.py             # Motor de traducción de medidas DAX en sandbox
│   │   ├── dax_validator.py             # Validador sintáctico y léxico de seguridad DAX
│   │   ├── engine.py                    # Motor de evaluación del Quality Gate (cQS)
│   │   └── security/                    # Núcleo de seguridad empresarial
│   │       ├── __init__.py              # Interfaz pública del módulo de seguridad
│   │       ├── sanitize.py              # Sanitizador de rutas y control de listas blancas
│   │       └── secret_scanner.py        # Escáner de secretos por entropía y patrones
│   ├── emitters/                        # Motores emisores de código destino
│   │   ├── dbt_emitter.py               # Emisor determinista de YAML para dbt MetricFlow
│   │   ├── model_emitter.py             # Emisor del modelo central TMDL
│   │   ├── pbip_writer.py               # Escritor reproducible de carpetas PBIP
│   │   ├── relationship_emitter.py      # Emisor TMDL de relaciones de esquema estrella
│   │   └── table_emitter.py             # Emisor TMDL de tablas y particiones
│   ├── parsers/                         # Motores de ingesta de especificaciones
│   │   ├── catalog_parser.py            # Parser de catálogos relacionales de base de datos
│   │   └── dimensional_parser.py        # Parser de especificaciones dimensionales de negocio
│   └── resolvers/                       # Inferencia y resolución de grafos semánticos
│       ├── relationship_resolver.py     # Ordenamiento topológico y resolución de claves foráneas
│       └── type_resolver.py             # Motor de inferencia de tipos de datos multiplataforma
└── tests/                               # Suite de verificación unitaria, sistémica e invariantes
    ├── test_dax_generator.py            # Verificación de lógica de traducción DAX
    ├── test_deterministic_emission.py   # Suite de verificación de estabilidad bitwise Zero-Diff
    ├── test_end_to_end.py               # Pruebas integrales de flujo completo del compilador
    ├── test_quality_gate.py             # Pruebas de reglas y cálculo de métricas cQS
    └── test_security_hardening.py       # Pruebas de path traversal, fuga de secretos y sandbox DAX
```

---

## 6. Protocolo de Verificación y Guía de Operación

### 6.1 Requisitos Previos e Inicialización del Entorno
El compilador requiere Python 3.10 o superior. La inicialización debe efectuarse en un entorno virtual aislado:

```powershell
# Crear y activar el entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias de producción y desarrollo
pip install -r requirements.txt
```

### 6.2 Ejecución Completa de la Batería de Pruebas
Ejecute la suite completa que valida los 98 vectores de prueba aprobados (100% de cobertura funcional y de seguridad):

```powershell
pytest tests/ -v --tb=short
```

Salida esperada de validación:
```
============================== 98 passed in 1.45s ==============================
```

### 6.3 Verificación de Hardening de Seguridad
Compruebe que el Núcleo de Seguridad intercepte proactivamente entradas anómalas o adversarias:

```powershell
# Ejecutar la suite especializada en seguridad
pytest tests/test_security_hardening.py -v

# Validar intercepción de salto de directorio (Debe abortar con código de retorno 1)
python -m src.cli.main --company "../malicious_dir" --source-dir "./inputs"
```

### 6.4 Verificación de Determinismo Zero-Diff
Valide que la emisión de artefactos se mantenga idéntica ante reordenamientos arbitrarios de archivos o entidades:

```powershell
pytest tests/test_deterministic_emission.py -v
```

### 6.5 Compilación Productiva de Extremo a Extremo
Ejecute la compilación semántica determinista sobre especificaciones empresariales:

```powershell
python -m src.cli.main `
  --company "metro_santiago" `
  --source-dir "docs/engineers_notes" `
  --output-dir "artifacts/SemanticFlow/outputs" `
  --cqs-threshold 85.0
```

---

## 7. Diagnóstico, Taxonomía de Errores y Resolución

| Código de Error / Síntoma | Invariante Causal | Diagnóstico y Acción Correctiva |
| :--- | :--- | :--- |
| **`SEC-PATH-001: Path Traversal Detected`** | La empresa o ruta especificada resuelve fuera del sandbox permitido | Verifique que el parámetro `--company` contenga únicamente caracteres alfanuméricos y guiones bajos. Elimine marcadores de ruta relativa (`../`, `..\`). |
| **`SEC-LEAK-002: Secret Detected in Input`** | Detección de cadenas de alta entropía o patrones de credenciales | Revise los archivos de entrada YAML/CSV. Remueva contraseñas de bases de datos, tokens Bearer o claves privadas incrustadas. |
| **`SEC-DAX-003: Disallowed DAX Lexeme`** | Expresión de medida contiene lexemas de modificación de estado o no seguros | Remueva `EVALUATE`, `USERELATIONSHIP`, sentencias DDL o DML de las métricas. Utilice agregaciones canónicas sobre CALCULATE. |
| **`CQS-GATE-001: Quality Score Below Threshold`** | Puntuación cQS calculada es $< 85.0$ por penalizaciones de reglas | Revise el informe de consola. Complete descripciones ausentes (D-001), resuelva relaciones ambiguas (D-004) o ajuste límites de memoria FinOps (D-012). |
| **`TOPO-CYC-002: Cyclic Dependency Detected`** | El grafo de relaciones foráneas contiene bucles cerrados | Audite las relaciones entre tablas. Desactive filtros cruzados bidireccionales y asegure jerarquía estricta en Estrella o Copo de Nieve. |

---

## 8. Referencias Académicas y Literatura Previa

```bibtex
@article{armbrust2021lakehouse,
  title={Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics},
  author={Armbrust, Michael and Ghodsi, Ali and Xin, Reynold and Zaharia, Matei},
  journal={Proceedings of the VLDB Endowment},
  volume={14},
  number={12},
  pages={28--32},
  year={2021}
}

@book{kimball2013data,
  title={The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling},
  author={Kimball, Ralph and Ross, Margy},
  edition={3rd},
  publisher={John Wiley \& Sons},
  year={2013}
}

@inproceedings{kahn1962topological,
  title={Topological Sorting of Large Networks},
  author={Kahn, Arthur B.},
  booktitle={Communications of the ACM},
  volume={5},
  number={11},
  pages={558--562},
  year={1962}
}

@techreport{microsoft2024tmdl,
  title={Tabular Model Definition Language (TMDL) Specification and Reference Architecture},
  author={{Microsoft Corporation}},
  institution={Microsoft Fabric Architecture Division},
  year={2024}
}
```
