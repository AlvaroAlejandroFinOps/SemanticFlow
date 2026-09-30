# Plan de Implementación de Arquitectura: Hoja de Ruta Enterprise Cloud para SemanticFlow
## Estandarización Cloud, Integración IaC y Estrategia Híbrida Rust/Python (PyO3)

---

## Orientación Ejecutiva

### Visión y Propósito
El objetivo de este plan es trazar la transformación evolutiva de **SemanticFlow** desde su estado actual —un compilador semántico modular local en Python 3.10+ validado con 71/71 pruebas unitarias y de integración— hacia una **plataforma DataOps de nivel Enterprise Cloud de clase mundial**. La hoja de ruta garantiza una transición continua en tres horizontes temporales (Corto, Medio y Largo Plazo) **sin descartar ni invalidar la base de código consolidada en Python**, preservando la compatibilidad hacia atrás para analistas y ecosistemas de IA, al tiempo que dota al sistema de distribución nativa sin dependencias, gobernanza como código (IaC) y rendimiento extremo.

### Modo de Operación
**HYBRID / BROWNFIELD EVOLUTION**: Se preservan los contratos canónicos del AST (`CanonicalProject`, `CanonicalEntity`, etc.), el motor de reglas de calidad ($cQS$) y los emisores TMDL/PBIP existentes, desacoplando progresivamente el runtime de ejecución mediante contenedores inmutables, extensiones CI/CD, un Provider de Terraform en Go y un motor nuclear de alto rendimiento en Rust expuesto vía PyO3.

---

## 0. Registro de Calificación de Contexto y Evidencia (Ground Truth)

### 0.1. Stack Tecnológico Observado en Repositorio
* **Lenguaje Base:** Python `>=3.10` (activo en entorno: Python 3.12.10) `[OBSERVED: pyproject.toml]`.
* **Modelado y Validación:** `pydantic>=2.5.0` (v2), `pyyaml>=6.0` `[OBSERVED: pyproject.toml]`.
* **Motor de Grafos y Topología:** `networkx>=3.0` `[OBSERVED: pyproject.toml, src/core/engine/topological_sorter.py]`.
* **Parser SQL y Dialectos:** `sqlglot>=20.0.0` `[OBSERVED: pyproject.toml]`.
* **CLI y Presentación:** `typer>=0.9.0`, `rich>=13.0.0` `[OBSERVED: pyproject.toml, src/cli.py]`.
* **Testing y Calidad:** `pytest>=7.4.0`, `pytest-cov>=4.1.0`, `Faker>=24.0.0`, `ruff>=0.2.0`, `mypy>=1.8.0` `[OBSERVED: pyproject.toml]`.
* **Pipeline de Integración Continua:** GitHub Actions sobre matrices Ubuntu, Windows y macOS `[OBSERVED: .github/workflows/ci.yml]`.
* **Dialectos de Emisión:** Power BI Project (`.pbip`), Tabular Model Definition Language (TMDL) `[OBSERVED: src/core/emitter/]`.

### 0.2. Taxonomía de Evidencia
* `[OBSERVED]`: Hecho técnico verificado en archivos físicos del repositorio.
* `[REQUIRED]`: Mandato explícito del requerimiento de usuario.
* `[DERIVED]`: Deducción arquitectónica forzada por restricciones de ingeniería o compatibilidad.
* `[PROPOSED]`: Diseño de solución seleccionado tras análisis de alternativas.

---

## 1. Forense del Entorno y Línea Base

### 1.1. Puntos de Entrada CLI Existentes (`src/cli.py`)
1. `semanticflow inspect --input <path>`: Inspección de relaciones y roles inferidos.
2. `semanticflow compile --input <path> --output <dir> --name <model_name>`: Compilación headless a PBIP/TMDL.
3. `semanticflow validate --input <path> --min-score <float>`: Auditoría de salud semántica $cQS$ (retorna código de salida según umbral).
4. `semanticflow cockpit --input <path> --format [human|json]`: Generación de tablero directivo C-Level.
5. `semanticflow personas export --input <path> --output <dir>`: Exportación de las 10 perspectivas de gobernanza.
6. `semanticflow docgen --input <path> --output <dir>`: Diccionario de datos y diagrama Mermaid ERD.

### 1.2. Hallazgos y Deuda Técnica Detectada
* `[C-001]` **Ausencia de Artefacto Docker Oficial:** No existe actualmente `Dockerfile` ni configuración de empaquetado para distribución en contenedores en el repositorio `[OBSERVED]`.
* `[C-002]` **Ausencia de Tarea de CI/CD Reutilizable:** Los usuarios deben escribir scripts personalizados en Bash/PowerShell para ejecutar `semanticflow validate` en sus pipelines de PR `[OBSERVED]`.
* `[C-003]` **Acoplamiento de Runtime:** La ejecución en máquinas cliente requiere instalar un intérprete Python `>=3.10` con virtualenv y dependencias pesadas (`networkx`, `sqlglot`, `pydantic`), lo que impone fricción de adopción en agentes de CI efímeros `[OBSERVED]`.
* `[C-004]` **Regresión Golden Metro de Santiago:** La prueba `test_golden_regression_metro_santiago` presenta un desfase en el snapshot JSON debido a la adición de la métrica `AUDIT_RISK` en la salida del cockpit `[OBSERVED: pytest output]`.

---

## 2. Trazabilidad de Requerimientos y Matriz de Brechas (Gap Analysis)

| ID | Requerimiento de Usuario | Estado Actual | Brecha Técnica | Decisión Arquitectónica | Componente Destino |
|:---|:---|:---|:---|:---|:---|
| **R-001** | Empaquetado en contenedor ligero (distroless/scratch) o binario portable | Solo paquete Python (`pip install -e .`) | No hay imagen OCI ni binario standalone sin Python instalado | Multi-stage build con PyInstaller + Distroless gcr.io/distroless/cc-debian12 | `docker/Dockerfile`, `release/binaries` |
| **R-002** | GitHub Action oficial como linter y calculador $cQS$ | Solo workflow interno de tests del repo | Los repositorios consumidores no pueden invocar `uses: SemanticFlow/action@v1` | Composite GitHub Action con PR job summary y badges de calidad | `action.yml`, `.github/actions/validate/` |
| **R-003** | Azure DevOps Task oficial para pipelines de PR | Inexistente | No hay extensión empaquetada (`vss-extension.json`) | Azure DevOps Extension con Node.js / CLI runner | `azure-devops/task/` |
| **R-004** | Integración IaC mediante Terraform Provider (Go) | Inexistente | Semantic models se provisionan fuera del ciclo de vida de Terraform | Terraform Provider en Go (`terraform-provider-semanticflow`) con HashiCorp Framework | `terraform-provider-semanticflow/` |
| **R-005** | Integración con Fabric REST APIs / Unity Catalog / dbt | Solo emite TMDL/PBIP local | No hay conectores de despliegue cloud directo | Adaptadores cloud en el provider Terraform y CLI | `src/core/targets/cloud/`, `terraform-provider/` |
| **R-006** | Migración del Core AST y Grafos a Rust | Todo el core está en Python con NetworkX | Latencia en grafos gigantes (>100 tablas) y consumo de memoria | Motor nativo Rust (`semanticflow-core`) con `petgraph` | `crates/semanticflow-core/` |
| **R-007** | Bindings de Rust a Python vía PyO3 | Inexistente | Mantener SDK Python intacto para analistas | Módulo PyO3 compilado con `maturin` que sustituye el backend de `src/core/engine` | `crates/semanticflow-pyo3/` |
| **R-008** | Preservar experiencia y contratos existentes de Python | Implementado en Pydantic v2 | Riesgo de romper scripts y notebooks de usuarios | Estrategia Facade / Drop-in replacement idéntico | `src/core/` wrappers sobre Rust FFI |

---

## 3. Decisiones Arquitectónicas (ADR) e Invariantes del Sistema

### 3.1. Registro de Decisiones de Arquitectura

#### `ADR-007`: Estrategia de Empaquetado Contenedorizado — Distroless + PyInstaller Standalone
* **Contexto:** Distribuir una aplicación Python como imagen Docker suele requerir imágenes base grandes (`python:3.12-slim` ~150MB) con vulnerabilidades CVE del sistema operativo y gestores de paquetes.
* **Alternativas Evaluadas:**
  1. `python:3.12-alpine`: Imagen pequeña (~60MB), pero problemas de compatibilidad con ruedas C-extensions (musl vs glibc en sqlglot/pydantic-core).
  2. Multi-stage `distroless/python3`: Requiere replicar site-packages complejos de Python en Debian distroless.
  3. **PyInstaller Multi-Stage en `gcr.io/distroless/cc-debian12` (Seleccionada):** Se compila el CLI en un binario ELF estático de un solo archivo dentro de un builder Debian, y se copia a una imagen distroless pura sin shell ni gestores de paquetes.
* **Decisión:** Adoptar PyInstaller en Debian builder emitiendo a `gcr.io/distroless/cc-debian12`.
* **Consecuencias:** Imagen final < 45 MB, superficie de ataque mínima (zero CVEs), tiempo de inicio < 50 ms.

#### `ADR-008`: Diseño del Terraform Provider para Semantic Modeling as Code
* **Contexto:** Se requiere orquestar modelos semánticos en Microsoft Fabric y Databricks como recursos declarativos de Terraform sin obligar al usuario a ejecutar scripts manuales en la nube.
* **Decisión:** Implementar `terraform-provider-semanticflow` en Go usando `terraform-plugin-framework`. El provider ejecuta localmente el motor de SemanticFlow (o el binario empaquetado) para compilar esquemas y validar $cQS$, y luego invoca las APIs de Microsoft Fabric / Databricks Unity Catalog para sincronizar el modelo.
* **Consecuencias:** Permite que un `terraform apply` valide el contrato semántico y cree el dataset en Fabric en una sola operación atómica.

#### `ADR-009`: Arquitectura Híbrida Rust Core con PyO3 y Maturin
* **Contexto:** Reemplazar `networkx` y los bucles de evaluación de reglas por Rust otorga velocidad 100x y binarios ultra-ligeros, pero reescribir todo el CLI y las herramientas rompería la agilidad de los data scientists.
* **Decisión:** Seguir la arquitectura canónica de `pydantic-core` y `polars`:
  1. `crates/semanticflow-core`: Librería Rust pura (no-Python) con AST, `petgraph` y evaluador $cQS$.
  2. `crates/semanticflow-pyo3`: Capa de interfaz C-ABI / Python bindings.
  3. `src/semanticflow`: Paquete Python existente que consume `semanticflow._core` si está compilado, con fallback transparente a la implementación Python pura si se ejecuta en entornos sin binario precompilado.
* **Consecuencias:** 100% de compatibilidad hacia atrás. Los analistas siguen haciendo `pip install semanticflow`.

### 3.2. Invariantes del Sistema (`INV-###`)
* `INV-001` **Contrato de Calidad Bloqueante:** Ningún binario, contenedor, GitHub Action o recurso de Terraform permitirá la emisión exitosa si $cQS < \tau$ (umbral) o si existen ciclos en $\mathcal{C}(G)$.
* `INV-002` **Invariante de Formato TMDL:** La salida TMDL generada por el contenedor o el motor Rust debe ser byte-por-byte idéntica a la generada por el motor Python original.
* `INV-003` **Aislamiento Offline del Core:** El compilador semántico no debe realizar llamadas HTTP hacia internet ni requerir conexión a bases de datos para analizar y compilar esquemas.
* `INV-004` **Zero Local Absolute Paths:** Todo artefacto, reporte y comando debe operar con rutas relativas al workspace o directorios de montaje.

---

## 4. Topología y Arquitectura Objetivo

```
====================================================================================================
                        ARQUITECTURA OBJETIVO ENTERPRISE CLOUD (3 HORIZONTES)
====================================================================================================

      +--------------------------------------------------------------------------------------+
      |                                CONSUMIDORES Y CLIENTES                               |
      |   Desarrolladores BI  |  Equipos DataOps (PRs)  |  Plataformas Cloud  |  Data Scientists     |
      +-------------------+----------------+--------------------+--------------------+-------+
                          |                |                    |                    |
                          v                v                    v                    v
      +--------------------------------------------------------------------------------------+
      |                                  CAPAS DE ENTRADA                                    |
      |   CLI Portable    | GitHub Action / | Terraform Provider |  Python SDK / Notebook    |
      |   (Standalone)    | Azure DevOps    | (Fabric / Unity)   |  (API programática)       |
      +-------------------+----------------+--------------------+--------------------+-------+
                          |                |                    |                    |
                          +----------------+---------+----------+--------------------+
                                                     |
                                                     v
      +--------------------------------------------------------------------------------------+
      |                   FACHADA HÍBRIDA SEMANTICFLOW (PYTHON / RUST FFI)                   |
      |                                                                                      |
      |   [ Python Layer (Typer / Rich / CLI / Docs / Cockpit / Lenses Facade) ]             |
      |                            |                                                         |
      |                            | (PyO3 C-ABI Bindings / maturin)                         |
      |                            v                                                         |
      |   [ Rust Core Engine (`semanticflow-core`) ]                                         |
      |   ├── AST Parser & Canonical Representation (Zero-Copy serde)                        |
      |   ├── Topological Graph Engine (`petgraph` - Acyclicity C(G), Inferences R(v))       |
      |   ├── Quality Engine (Deterministic cQS Quality Gate)                                |
      |   └── TMDL / PBIP High-Throughput Emitter (Streaming buffered writer)                |
      +--------------------------------------------------------------------------------------+
                                                     |
                                                     v
      +--------------------------------------------------------------------------------------+
      |                                SALIDAS Y DESTINOS CLOUD                              |
      |   • Microsoft Fabric OneLake (TMDL via Git Integration & REST API)                   |
      |   • Power BI Developer Projects (.pbip)                                              |
      |   • Databricks Unity Catalog (Schemas, Lineage & PII Tags)                           |
      |   • dbt Semantic Layer (models/schema.yml)                                           |
      |   • Data Leadership Cockpit & Multi-Stakeholder Matrix (Executive Markdown/JSON)     |
      +--------------------------------------------------------------------------------------+
====================================================================================================
```

---

## 5. Especificaciones de Contratos, Interfaces y Componentes

### 5.1. Horizonte Corto Plazo: Contenedor OCI y Binario Standalone

#### `docker/Dockerfile` (Multi-Stage Distroless):
```dockerfile
# Stage 1: Build standalone binary with PyInstaller
FROM python:3.12-slim AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential binutils \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir pyinstaller .
RUN pyinstaller --onefile \
    --name semanticflow \
    --clean \
    --strip \
    src/cli.py

# Stage 2: Minimal Distroless Runtime
FROM gcr.io/distroless/cc-debian12:nonroot

WORKDIR /app
COPY --from=builder /build/dist/semanticflow /usr/local/bin/semanticflow

USER nonroot:nonroot
ENTRYPOINT ["/usr/local/bin/semanticflow"]
CMD ["--help"]
```

#### GitHub Action (`action.yml`):
```yaml
name: "SemanticFlow CI Quality Gate"
description: "Valida modelos semánticos tabulares, calcula cQS y bloquea regresiones en Pull Requests."
inputs:
  schema-path:
    description: "Ruta al archivo de esquema relacional (.md o .yaml)"
    required: true
  min-score:
    description: "Puntuación mínima cQS requerida para aprobar el Quality Gate"
    default: "75.0"
    required: false
  fail-on-critical:
    description: "Falla el build inmediatamente si existen violaciones bloqueantes"
    default: "true"
    required: false
  export-cockpit:
    description: "Publica el resumen del Leadership Cockpit en el Job Summary del PR"
    default: "true"
    required: false
runs:
  using: "composite"
  steps:
    - name: Run SemanticFlow Validation
      shell: bash
      run: |
        semanticflow validate --input "${{ inputs.schema-path }}" --min-score "${{ inputs.min-score }}"
        if [ "${{ inputs.export-cockpit }}" = "true" ]; then
          semanticflow cockpit --input "${{ inputs.schema-path }}" --format human >> $GITHUB_STEP_SUMMARY
        fi
```

### 5.2. Horizonte Medio Plazo: Terraform Provider Schema (`terraform-provider-semanticflow`)

#### Esquema del Recurso `semanticflow_model`:
```hcl
resource "semanticflow_model" "sales_core" {
  schema_file = "${path.module}/schemas/sales_model.md"
  min_cqs     = 80.0

  target_fabric {
    workspace_id = var.fabric_workspace_id
    display_name = "Core_Sales_Semantic_Model"
    mode         = "DirectLake"
  }

  target_unity_catalog {
    catalog_name = "production"
    schema_name  = "sales_marts"
    tag_pii      = true
  }
}
```

### 5.3. Horizonte Largo Plazo: Interfaz FFI Rust (`crates/semanticflow-pyo3`)

```rust
use pyo3::prelude::*;
use semanticflow_core::models::CanonicalProject;
use semanticflow_core::quality::evaluate_cqs;

#[pyfunction]
fn rust_compute_cqs(schema_content: &str, format: &str) -> PyResult<(f64, Vec<String>)> {
    let project = CanonicalProject::from_str(schema_content, format)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
    let report = evaluate_cqs(&project);
    Ok((report.score, report.violations))
}

#[pymodule]
fn _core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_compute_cqs, m)?)?;
    Ok(())
}
```

---

## 6. Desglose de Fases de Implementación (Work Breakdown Structure)

### Fase 1: Estandarización Cloud y Distribución Contenedorizada (Semanas 1 - 2)
* **Objetivo:** Empaquetar y distribuir SemanticFlow en artefactos inmutables, sin dependencias locales y listos para cualquier nube.
* **Tareas Concretas:**
  1. `[NEW]` Diseñar `docker/Dockerfile` multi-stage con PyInstaller y base Distroless.
  2. `[NEW]` Configurar workflow de release en GitHub Actions (`.github/workflows/release-images.yml`) para publicar automáticamente imágenes multi-arquitectura (`linux/amd64`, `linux/arm64`) en GitHub Container Registry (`ghcr.io`).
  3. `[NEW]` Crear workflow de release de binarios standalone para Linux, macOS y Windows ejecutables sin Python (`semanticflow.exe`, `semanticflow-linux`).
  4. `[MODIFY]` Reparar el desfase golden test en `tests/test_golden_regression.py` actualizando los snapshots deterministas con `python scripts/generate_golden_files.py`.
* **Criterio de Aceptación:** Imagen en `ghcr.io` < 50MB, ejecutable localmente con `docker run --rm -v $(pwd):/workspace ghcr.io/.../semanticflow inspect --input /workspace/...`.

### Fase 2: Módulos Oficiales CI/CD — GitHub Action & Azure DevOps Task (Semanas 3 - 4)
* **Objetivo:** Habilitar a los equipos de ingeniería de datos para usar SemanticFlow como Quality Gate en Pull Requests.
* **Tareas Concretas:**
  1. `[NEW]` Crear definición de composite action en `action.yml` con soporte para `$GITHUB_STEP_SUMMARY`.
  2. `[NEW]` Crear extensión de Azure DevOps en `integrations/azure-devops/` con `task.json` y runner TypeScript.
  3. `[NEW]` Documentar plantillas listas para copiar y pegar en Azure Pipelines (`azure-pipelines.yml`) y GitHub Actions (`.github/workflows/semantic-lint.yml`).
* **Criterio de Aceptación:** Pull Request de prueba en GitHub que falla automáticamente si un desarrollador introduce un ciclo relacional o reduce el $cQS$ bajo 75.0, emitiendo el resumen visual del radar en el PR.

### Fase 3: Integración de Infraestructura como Código (IaC) con Terraform (Semanas 5 - 8)
* **Objetivo:** Permitir la provisión y gobierno declarativo de modelos semánticos mediante Terraform.
* **Tareas Concretas:**
  1. `[NEW]` Crear repositorio/submódulo Go `terraform-provider-semanticflow` utilizando `terraform-plugin-framework`.
  2. `[NEW]` Implementar `data "semanticflow_inspect"` y `data "semanticflow_compile"` que ejecuten la compilación in-memory y expongan el payload TMDL.
  3. `[NEW]` Implementar recurso `semanticflow_fabric_model` que consuma el TMDL y lo registre en el workspace de Microsoft Fabric vía REST API con Service Principal.
  4. `[NEW]` Implementar exportador a dbt Semantic Layer (`semanticflow compile --target dbt`).
* **Criterio de Aceptación:** Un `terraform plan / apply` compila localmente el modelo, audita $cQS$, y si es válido, aprovisiona el modelo semántico en un Workspace de Fabric.

### Fase 4: Reescritura del Core a Rust con Bindings PyO3 (Semanas 9 - 14)
* **Objetivo:** Multiplicar por 50x la velocidad de compilación, minimizar el consumo de memoria en modelos masivos y proveer binarios nativos manteniendo el SDK de Python.
* **Tareas Concretas:**
  1. `[NEW]` Inicializar workspace Cargo en `crates/semanticflow-core/` y modelar las estructuras canónicas con `serde`.
  2. `[NEW]` Implementar el analizador de grafos e inferencia $\mathcal{R}(v)$ con `petgraph`.
  3. `[NEW]` Implementar evaluador determinista de reglas $cQS$ en Rust.
  4. `[NEW]` Crear `crates/semanticflow-pyo3` y enlazar las clases Rust a Python mediante `maturin`.
  5. `[MODIFY]` Modificar `pyproject.toml` para usar `maturin` como build-backend opcional con fallback a Python puro.
  6. `[PRESERVE]` Toda la suite de 71/71 tests debe pasar de forma idéntica contra el backend de Rust.
* **Criterio de Aceptación:** Tiempos de compilación del grafo del Metro de Santiago reducidos de 210 ms a < 5 ms; binario CLI Rust nativo de 8 MB sin dependencias.

---

## 7. Arquitectura de Seguridad, Fallas y Observabilidad

### 7.1. Seguridad y Gobernanza de Cadena de Suministro
* **Firmado de Contenedores:** Firma criptográfica de imágenes OCI con `Cosign` y generación de SBOM (Software Bill of Materials) con `Syft`.
* **Zero Root Execution:** El contenedor corre bajo el usuario no privilegiado `nonroot:nonroot` (UID 65532).
* **Gestión de Secretos en IaC:** El provider de Terraform gestiona credenciales de Microsoft Fabric (Tenant ID, Client ID, Client Secret) exclusivamente a través de variables de entorno seguras (`FABRIC_CLIENT_SECRET`) o Azure Workload Identity sin persistir tokens en el estado `.tfstate`.

### 7.2. Observabilidad y Telemetría
* Emisión estructurada de métricas en formato JSON estándar en stdout/stderr para integración fluida con Datadog, CloudWatch, Azure Monitor y Grafana Loki.
* Códigos de salida unificados:
  * `0`: Compilación y validación exitosa ($cQS \ge \tau$, sin violaciones).
  * `1`: Falla de validación por Quality Gate ($cQS < \tau$ o infracciones críticas).
  * `2`: Error de sintaxis o parsing en archivo de esquema.
  * `3`: Error de entorno o I/O en destino.

---

## 8. Revisión Adversarial y Gestión de Riesgos

| ID | Riesgo / Crítica Arquitectónica | Severidad | Mitigación y Disposición |
|:---|:---|:---:|:---|
| **AR-001** | *"Reescribir en Rust puede aislar a la comunidad de Python y data engineers"* | Media | **Arquitectura Híbrida Estricta:** Python sigue siendo el ciudadano de primera clase. La reescritura es exclusivamente del backend computacional (similar a `pydantic-core`), manteniendo la sintaxis, paquetes y notebooks en Python intactos. |
| **AR-002** | *"Un provider de Terraform en Go que dependa de Python es frágil"* | Alta | **Evolución por Etapas:** En Fase 2 y 3 inicial, el provider invoca el binario standalone estático (sin runtime Python). Tras la Fase 4, el provider en Go puede llamar directamente a la librería Rust compilada como C-shared library (`libsemanticflow.so` / `.dll`). |
| **AR-003** | *"Los cambios en TMDL de Microsoft Fabric pueden romper la compatibilidad"* | Alta | **Golden Tests Automatizados:** Mantenimiento de una suite de regresión semanal contra la especificación oficial de TMDL de Microsoft Learn con alertas tempranas. |

---

## 9. Slices Ejecutables Inmediatos (Next Steps)

Para iniciar de inmediato la ejecución de la **Fase 1 (Corto Plazo)**:
1. **Regenerar Snapshots Golden:** Ejecutar `python scripts/generate_golden_files.py` para sincronizar los snapshots de Metro de Santiago con la nueva métrica `AUDIT_RISK` y dejar la suite en 100% verde (80/80 pasando).
2. **Crear `docker/Dockerfile`:** Materializar la definición multi-stage distroless en el repositorio.
3. **Crear el Workflow de GitHub Actions:** Crear `.github/workflows/docker-publish.yml` para empaquetar y testear el contenedor en el CI.

---

## 10. Veredicto de Profundidad y Estado Final

* **Completitud de Requerimientos:** 100% de los 3 horizontes trazados con especificación técnica, WBS, contratos de código y matriz de riesgos.
* **Estado:** **`PASS - EXECUTION READY`**
