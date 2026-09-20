"""
Explainer engine for inspecting canonical model inferences and provenance.
"""
from rich import box
from rich.console import Console
from rich.table import Table

from src.core.ast.canonical.models import CanonicalSemanticProject, EntityRole


class SemanticExplainer:
    """Provides human-readable and structured JSON explanation of semantic inferences."""

    def __init__(self, project: CanonicalSemanticProject):
        self.project = project
        self.console = Console()

    def explain_entity_roles(self):
        table = Table(
            title=f"Inference Provenance: {self.project.name}",
            box=box.ROUNDED,
            header_style="bold cyan",
        )
        table.add_column("Entity", style="bold")
        table.add_column("Role", justify="center")
        table.add_column("Rule ID", justify="center", style="yellow")
        table.add_column("Description", style="dim")
        table.add_column("Confidence", justify="right")

        for entity in self.project.entities:
            role_style = "cyan" if entity.role == EntityRole.DIMENSION else "yellow"
            prov = entity.provenance[0] if entity.provenance else None
            rule_id = prov.rule_id if prov else "N/A"
            desc = prov.description if prov else "No provenance recorded"
            conf_str = str(prov.confidence) if prov else "N/A"
            role_val = entity.role.value
            role_colored = "[" + role_style + "]" + role_val + "[/" + role_style + "]"

            table.add_row(
                entity.name,
                role_colored,
                rule_id,
                desc,
                conf_str,
            )

        self.console.print(table)

    def to_dict(self) -> dict:
        return self.project.model_dump()
