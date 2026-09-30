use std::collections::HashMap;
use petgraph::algo::tarjan_scc;
use petgraph::graph::{DiGraph, NodeIndex};
use crate::models::{CanonicalProject, EntityRole};

pub struct TopologicalAnalysis {
    pub has_cycles: bool,
    pub cycle_nodes: Vec<Vec<String>>,
    pub inferred_roles: HashMap<String, EntityRole>,
}

pub struct GraphEngine<'a> {
    project: &'a CanonicalProject,
}

impl<'a> GraphEngine<'a> {
    pub fn new(project: &'a CanonicalProject) -> Self {
        Self { project }
    }

    pub fn analyze(&self) -> TopologicalAnalysis {
        let mut graph = DiGraph::<&str, &str>::new();
        let mut node_indices: HashMap<&str, NodeIndex> = HashMap::new();
        let mut reverse_indices: HashMap<NodeIndex, &str> = HashMap::new();

        // 1. Add Vertices
        for entity in &self.project.entities {
            let idx = graph.add_node(entity.name.as_str());
            node_indices.insert(entity.name.as_str(), idx);
            reverse_indices.insert(idx, entity.name.as_str());
        }

        // 2. Add Directed Edges from dependent (child) to referenced (parent)
        for rel in &self.project.relationships {
            if let (Some(&from_idx), Some(&to_idx)) = (
                node_indices.get(rel.from_entity_id.as_str()),
                node_indices.get(rel.to_entity_id.as_str()),
            ) {
                graph.add_edge(from_idx, to_idx, rel.name.as_str());
            }
        }

        // 3. Cycle Detection with Tarjan's SCC
        let sccs = tarjan_scc(&graph);
        let mut has_cycles = false;
        let mut cycle_nodes = Vec::new();

        for scc in sccs {
            if scc.len() > 1 {
                has_cycles = true;
                let names: Vec<String> = scc
                    .into_iter()
                    .filter_map(|idx| reverse_indices.get(&idx).map(|s| s.to_string()))
                    .collect();
                cycle_nodes.push(names);
            }
        }

        // 4. Role Assignment Function R(v) based on In-Degree and Out-Degree
        let mut inferred_roles = HashMap::new();

        for entity in &self.project.entities {
            if let Some(&node_idx) = node_indices.get(entity.name.as_str()) {
                let out_degree = graph.neighbors(node_idx).count();
                let in_degree = graph
                    .neighbors_directed(node_idx, petgraph::Direction::Incoming)
                    .count();

                let role = if out_degree >= 1 && in_degree == 0 {
                    EntityRole::Fact
                } else if out_degree == 0 && in_degree >= 1 {
                    EntityRole::Dimension
                } else if out_degree >= 2 && in_degree >= 1 {
                    EntityRole::Bridge
                } else if out_degree >= 1 && in_degree >= 1 && entity.attributes.len() <= 5 {
                    EntityRole::Outrigger
                } else {
                    EntityRole::Dimension
                };

                inferred_roles.insert(entity.name.clone(), role);
            }
        }

        TopologicalAnalysis {
            has_cycles,
            cycle_nodes,
            inferred_roles,
        }
    }
}
