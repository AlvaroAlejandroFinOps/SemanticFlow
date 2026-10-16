# Data Architect Lens - Enterprise Topology & Graph Standards

**Rol Organizacional:** Data Architect (`data_architect`)  
**Profundidad Técnica:** `EXHAUSTIVE`  
**Áreas de Foco:** `DATA_MODELING`, `STRATEGIC_ALIGNMENT`  
**Objetos Visibles:** `FACT`, `DIMENSION`, `BRIDGE`, `CALCULATED`, `RELATIONSHIP`  
**Tema de Color:** `#4A5568` | **Icono:** `layers`  

---

## 1. Propósito y Alcance

Este lente atiende a los arquitectos de datos y modeladores empresariales. Proporciona una vista exhaustiva del dígrafo relacional $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, la detección de componentes fuertemente conexos (algoritmo de Tarjan) y la función determinista de inferencia de roles $\mathcal{R}(v)$.

---

## 2. Visibilidad y Responsabilidades Técnicas

- **Grafo Relacional Completo:** Inspección de todas las aristas y dependencias topológicas.
- **Detección de Ciclos Acíclicos:** Asegurar que $\mathcal{C}(\mathcal{G}) = \emptyset$ para garantizar modelos resolubles.
- **Estándares Corporativos:** Gobernanza de claves subrogadas, nombres estandarizados y trazabilidad de entidades de negocio.
