use std::collections::HashMap;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use semanticflow_core::models::CanonicalProject;
use semanticflow_core::graph::GraphEngine;
use semanticflow_core::quality::QualityEngine;

#[pyfunction]
fn rust_compute_cqs(project_json: &str, min_score: f64) -> PyResult<(f64, bool, Vec<String>, Vec<String>)> {
    let project: CanonicalProject = serde_json::from_str(project_json)
        .map_err(|e| PyValueError::new_err(format!("Error al deserializar CanonicalProject en Rust: {}", e)))?;
    
    let engine = QualityEngine::new(&project);
    let report = engine.evaluate(min_score);

    Ok((
        report.score,
        report.is_passing,
        report.blocking_violations,
        report.governance_warnings,
    ))
}

#[pyfunction]
fn rust_detect_cycles(project_json: &str) -> PyResult<(bool, Vec<Vec<String>>)> {
    let project: CanonicalProject = serde_json::from_str(project_json)
        .map_err(|e| PyValueError::new_err(format!("Error deserializando JSON en Rust: {}", e)))?;
    
    let engine = GraphEngine::new(&project);
    let topo = engine.analyze();

    Ok((topo.has_cycles, topo.cycle_nodes))
}

#[pyfunction]
fn rust_infer_roles(project_json: &str) -> PyResult<HashMap<String, String>> {
    let project: CanonicalProject = serde_json::from_str(project_json)
        .map_err(|e| PyValueError::new_err(format!("Error deserializando JSON en Rust: {}", e)))?;
    
    let engine = GraphEngine::new(&project);
    let topo = engine.analyze();

    let mut result = HashMap::new();
    for (name, role) in topo.inferred_roles {
        result.insert(name, format!("{:?}", role).to_uppercase());
    }

    Ok(result)
}

#[pymodule]
fn _core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_compute_cqs, m)?)?;
    m.add_function(wrap_pyfunction!(rust_detect_cycles, m)?)?;
    m.add_function(wrap_pyfunction!(rust_infer_roles, m)?)?;
    Ok(())
}
