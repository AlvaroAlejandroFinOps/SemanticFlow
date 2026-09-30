use crate::graph::GraphEngine;
use crate::models::CanonicalProject;

pub struct QualityReport {
    pub score: f64,
    pub is_passing: bool,
    pub blocking_violations: Vec<String>,
    pub governance_warnings: Vec<String>,
}

pub struct QualityEngine<'a> {
    project: &'a CanonicalProject,
}

impl<'a> QualityEngine<'a> {
    pub fn new(project: &'a CanonicalProject) -> Self {
        Self { project }
    }

    pub fn evaluate(&self, min_threshold: f64) -> QualityReport {
        let mut score: f64 = 100.0;
        let mut blocking_violations = Vec::new();
        let mut governance_warnings = Vec::new();

        // 1. Evaluate Topological Invariants (Cycles)
        let graph_engine = GraphEngine::new(self.project);
        let topo = graph_engine.analyze();

        if topo.has_cycles {
            score -= 40.0;
            blocking_violations.push(format!(
                "Invariante bloqueante: Ciclos relacionales detectados en el grafo: {:?}",
                topo.cycle_nodes
            ));
        }

        // 2. Evaluate Primary Keys & Entities
        for entity in &self.project.entities {
            let has_pk = entity.attributes.iter().any(|a| a.is_key);
            if !has_pk {
                score -= 15.0;
                blocking_violations.push(format!(
                    "Invariante bloqueante: Entidad '{}' carece de Primary Key.",
                    entity.name
                ));
            }

            // Governance: Undocumented entities or attributes
            if entity.description.is_none() {
                score -= 2.0;
                governance_warnings.push(format!(
                    "Gobernanza: Entidad '{}' no posee descripción formal.",
                    entity.name
                ));
            }

            for attr in &entity.attributes {
                if attr.is_pii && !attr.is_hidden {
                    score -= 5.0;
                    governance_warnings.push(format!(
                        "Seguridad: Atributo sensible PII '{}.{}' no está marcado como oculto o enmascarado.",
                        entity.name, attr.name
                    ));
                }
            }
        }

        let final_score = score.max(0.0).min(100.0);
        let is_passing = final_score >= min_threshold && blocking_violations.is_empty();

        QualityReport {
            score: final_score,
            is_passing,
            blocking_violations,
            governance_warnings,
        }
    }
}
