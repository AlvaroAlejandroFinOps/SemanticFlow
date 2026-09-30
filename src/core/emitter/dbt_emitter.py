"""
dbt Semantic Layer Emitter.
Transforms CanonicalProject into dbt MetricFlow semantic_models.yml specifications.
"""
from typing import Any, Dict, List
import yaml

from src.core.ast.canonical.models import CanonicalSemanticProject, DataType, EntityRole


class DbtSemanticEmitter:
    """Emits dbt MetricFlow semantic layer specifications from CanonicalSemanticProject."""

    def __init__(self, project: CanonicalSemanticProject):
        self.project = project

    def generate_spec(self) -> Dict[str, Any]:
        """Generates dbt semantic layer dictionary representation."""
        semantic_models: List[Dict[str, Any]] = []

        for entity in self.project.entities:
            model_def: Dict[str, Any] = {
                "name": entity.name.lower(),
                "description": entity.description or f"Semantic model for {entity.name}",
                "model": f"ref('{entity.name.lower()}')",
                "entities": [],
                "dimensions": [],
                "measures": [],
            }

            # 1. Process Attributes into Entities and Dimensions
            for attr in entity.attributes:
                if attr.is_key:
                    entity_type = "primary" if entity.role in (EntityRole.DIMENSION, EntityRole.BRIDGE) else "foreign"
                    model_def["entities"].append({
                        "name": attr.name.lower(),
                        "type": entity_type,
                        "description": attr.description or f"Identifier for {attr.name}",
                    })
                else:
                    is_time = attr.data_type in (DataType.DATETIME, DataType.DATE)
                    dim_entry = {
                        "name": attr.name.lower(),
                        "type": "time" if is_time else "categorical",
                        "description": attr.description or f"Dimension {attr.name}",
                    }
                    if is_time:
                        dim_entry["type_params"] = {
                            "time_granularity": "day"
                        }
                    model_def["dimensions"].append(dim_entry)

            # 2. Process Metrics into Measures
            for metric in entity.metrics:
                model_def["measures"].append({
                    "name": metric.name.lower(),
                    "description": metric.description or f"Metric {metric.name}",
                    "agg": "sum",
                    "expr": metric.expression or "1",
                })

            # Add default count measure if none present
            if not model_def["measures"]:
                model_def["measures"].append({
                    "name": f"{entity.name.lower()}_count",
                    "description": f"Total count of {entity.name}",
                    "agg": "count",
                    "expr": "1",
                })

            semantic_models.append(model_def)

        return {
            "version": 2,
            "semantic_models": semantic_models,
        }

    def to_yaml(self) -> str:
        """Serializes the dbt specification to formatted YAML."""
        data = self.generate_spec()
        return yaml.dump(data, sort_keys=False, indent=2)

    def write_to_file(self, output_path: str) -> str:
        """Writes the semantic_models.yml file to destination."""
        yaml_content = self.to_yaml()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        return output_path
