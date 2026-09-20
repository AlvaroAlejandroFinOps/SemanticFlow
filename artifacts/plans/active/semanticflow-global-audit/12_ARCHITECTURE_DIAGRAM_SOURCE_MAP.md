# 12. MAPA DE FUENTES Y DIAGRAMA DE ARQUITECTURA (ARCHITECTURE SOURCE MAP)

**Proyecto:** SemanticFlow  
**Fecha de Auditoría:** 2026-09-19  
**Commit:** `59f3c929b3e7a2d52ceb3553b9285388a52eee52`  

---

## 1. MAPA DE CORRESPONDENCIA FUENTE-ARQUITECTURA

| Capa Arquitectónica | Módulo / Paquete | Archivos Fuente Clave | Rol y Responsabilidad |
|---|---|---|---|
| **Frontend / Ingesta** | `src/core/parsers/` | `markdown_parser.py`, `yaml_parser.py`, `base.py` | Parsea esquemas de entrada a `RelationalSchemaRaw` |
| **AST Canónico (SST)** | `src/core/ast/canonical/` | `models.py` | Modela `CanonicalSemanticProject`, `SemanticEntity`, `SemanticMetric`, `ProjectGovernance` |
| **AST Relacional Crudo** | `src/core/ast/` | `schema.py`, `semantic.py`, `types.py` | Modela tablas, columnas y relaciones crudas |
| **Mappers de Adaptación**| `src/core/mappers/` | `raw_to_canonical.py`, `canonical_to_pbi.py` | Normaliza el AST crudo a canónico y canónico a PBI |
| **Motor de Inferencia** | `src/core/engine/` | `role_inferer.py`, `relationship_resolver.py`, `graph.py` | Infiere hechos/dimensiones y resuelve grafo NetworkX |
| **Generador DAX** | `src/core/engine/` | `dax_generator.py` | Sintetiza expresiones DAX agregadas canónicas |
| **Gobierno y Explicabilidad** | `src/core/engine/` | `governance.py`, `explainer.py` | Oculta claves foráneas y provee trazabilidad de evidencia |
| **Evaluador de Calidad cQS** | `src/core/quality/` | `scorer.py`, `rules.py` | Evalúa reglas de gobernanza, grano y penalizaciones |
| **Planificador de Destino** | `src/core/capabilities/` | `planner.py` | Evalúa soporte del dialecto target (`SUPPORTED`, `UNSUPPORTED`) |
| **Adaptador Power BI** | `src/core/targets/powerbi/`| `adapter.py` | Adapta el modelo canónico al backend Power BI |
| **Emisores TMDL / PBIP** | `src/core/emitter/` | `pbip_writer.py`, `table_emitter.py`, `relationship_emitter.py`, `model_emitter.py`, `tmdl_formatter.py` | Emite carpetas y archivos `.tmdl` y `.pbip` |
| **Documentación** | `src/core/docs/` | `emitter.py` | Genera `DATA_DICTIONARY.md` y `ARCHITECTURE_ERD.mmd` |
| **Framework Persona Lens** | `src/core/personas/` | `models.py`, `registry.py`, `config_loader.py`, `projector.py`, `renderers.py`, `lenses/*.py` | Proyecta perspectivas por rol sin mutar el AST canónico |
| **Leadership Cockpit** | `src/core/personas/` | `cockpit.py` (actual) -> `src/core/leadership/` (destino) | Sintetiza radar de madurez y telemetría C-Level |
| **CLI Typer + Rich** | `src/` | `cli.py` | Comandos `compile`, `inspect`, `explain`, `validate`, `docgen`, `personas`, `cockpit` |

---

## 2. DIAGRAMA DE ARQUITECTURA AS-IS (ESTADO ACTUAL)

```mermaid
flowchart TD
    subgraph Ingestion["Capa de Ingesta"]
        MD[Markdown Schema]
        YAML[YAML/JSON Schema]
        MP[MarkdownSchemaParser]
        YP[YamlSchemaParser]
    end

    subgraph CanonicalCore["Núcleo Semántico Canónico"]
        R2C[RawToCanonicalMapper]
        CSP["CanonicalSemanticProject (AST Único)"]
        RI[RoleInferer]
        RR[RelationshipResolver / NetworkX]
        DG[DaxGenerator]
        QS[SemanticQualityScorer / cQS]
    end

    subgraph TargetPlanning["Planificación y Adaptación Target"]
        TCP[TargetCapabilityPlanner]
        PBI_A[PowerBiTargetAdapter]
        C2P[CanonicalToPbiMapper]
    end

    subgraph Emission["Emisión de Artefactos"]
        PW[PbipWriter]
        TE[TmdlEmitters]
        DOC[DocumentationEmitter]
    end

    subgraph PersonaFramework["Framework de Personas (Dimensión B)"]
        REG[PersonaRegistry]
        PRJ[PersonaProjector]
        LENSES["10 Lenses (5 Core + 5 Ext)"]
        CPT["cockpit.py (Monolítico en personas)"]
        REND[Markdown/JSON Renderers]
    end

    MD --> MP --> R2C
    YAML --> YP --> R2C
    R2C --> CSP

    CSP --> RI --> CSP
    CSP --> RR --> CSP
    CSP --> DG --> CSP
    CSP --> QS --> CSP

    CSP --> TCP --> PBI_A --> C2P --> TE --> PW
    CSP --> DOC

    CSP --> PRJ
    REG --> PRJ
    PRJ --> LENSES --> REND
    PRJ --> CPT --> REND
```

---

## 3. DIAGRAMA DE ARQUITECTURA TO-BE (ESTADO OBJETIVO ENTERPRISE)

```mermaid
flowchart TD
    subgraph IngestionLayer["1. Ingesta Declarativa Multifuente"]
        MD_In[Markdown]
        YAML_In[YAML/JSON]
        SQL_In[SQL DDL - sqlglot]
        Parsers[Unified Parser Frontends]
    end

    subgraph CanonicalTruth["2. Canonical Semantic Model (SSOT)"]
        RawAST[Raw Metadata AST]
        CanModel["CanonicalSemanticProject + ProjectGovernance"]
        InfEngine["Inference & Topology Engine (DAG/Cycles)"]
        GovEngine["Governance & Attribute Policies"]
        MetricEngine["Metric Compiler & DAX Synthesis"]
        QualityEngine["Semantic Quality Scorer (cQS Profiles)"]
    end

    subgraph TargetEcosystem["3. Target Adapters & Capability Matrix"]
        CapPlanner["Target Capability Planner (Versioned Matrix)"]
        PBI_Target["Power BI Target Adapter (TMDL/PBIP Reference)"]
        Future_Targets["Looker / Qlik / dbt Adapters (Future)"]
    end

    subgraph PersonaEcosystem["4. Persona Lens Framework (Dimensión B)"]
        PersonaReg["Configurable Persona Registry (YAML Overrides)"]
        CoreLenses["10 Core Persona Lenses (Read-Only Projections)"]
        ExtLenses["6 Extension Persona Lenses"]
        PolicyEngine["Visibility & Privacy Policy Engine"]
    end

    subgraph LeadershipPackage["5. Isolated Data Leadership Cockpit"]
        LC_Core["src/core/leadership/ (Autonomous Package)"]
        LC_Mods["Portfolio | Health | Ownership | Gaps | Deps | Delivery | Value | Risk"]
        LC_Renderers["Multi-Artifact Exporter (9 JSON/MD/MMD files)"]
    end

    subgraph OutputSafeguards["6. Safe Atomic Output Delivery"]
        SafetyGate["Path Traversal & Root Protection Gate"]
        AtomicWriter["Atomic Staging & Rollback Writer"]
        ArtifactsDir["/output/PBIP/ | /output/personas/ | /output/leadership/ | /output/docs/"]
    end

    MD_In & YAML_In & SQL_In --> Parsers --> RawAST --> CanModel
    CanModel <--> InfEngine & GovEngine & MetricEngine & QualityEngine
    
    CanModel --> CapPlanner
    CapPlanner --> PBI_Target & Future_Targets
    PBI_Target --> SafetyGate

    CanModel --> PolicyEngine --> PersonaReg --> CoreLenses & ExtLenses
    CoreLenses & ExtLenses --> LC_Core
    CanModel --> LC_Core
    LC_Core --> LC_Mods --> LC_Renderers --> SafetyGate

    SafetyGate --> AtomicWriter --> ArtifactsDir
```
