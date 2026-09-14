"""
Data Leadership Cockpit Engine.
Aggregates, synthesizes, and exports C-Level telemetry across all 10 Persona Lenses.
"""
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from src.core.ast.canonical.models import CanonicalSemanticProject, MetricType
from src.core.personas.models import (
    LeadershipCockpit,
    PersonaProjection,
    PersonaRecommendation,
    RecommendationPriority,
)
from src.core.personas.projector import PersonaProjector
from src.core.personas.registry import PersonaRegistry
from src.core.personas.renderers import (
    JsonPersonaRenderer,
    LeadershipCockpitRenderer,
    MarkdownPersonaRenderer,
)


class DataLeadershipCockpitEngine:
    """Engine responsible for building and exporting the Executive Data Leadership Cockpit."""

    def __init__(
        self,
        project: CanonicalSemanticProject,
        registry: Optional[PersonaRegistry] = None,
    ):
        self._project = project
        self._projector = PersonaProjector(project, registry=registry)

    @property
    def projector(self) -> PersonaProjector:
        return self._projector

    def generate_cockpit(self) -> LeadershipCockpit:
        """Generates the full synthesized LeadershipCockpit model."""
        return self._projector.build_leadership_cockpit()

    def export_all(
        self,
        output_dir: Union[str, Path],
        include_individual_lenses: bool = True,
        formats: Optional[List[str]] = None,
    ) -> Dict[str, str]:
        """
        Exports the leadership cockpit and optionally all individual persona lenses
        to disk in Markdown and JSON formats. Returns mapping of artifact names to file paths.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        if formats is None:
            formats = ["md", "json"]

        results: Dict[str, str] = {}
        cockpit = self.generate_cockpit()

        # 1. Export Cockpit
        if "md" in formats:
            cockpit_md_path = out_path / "data_leadership_cockpit.md"
            cockpit_md_content = LeadershipCockpitRenderer.render_markdown(cockpit)
            with open(cockpit_md_path, "w", encoding="utf-8") as f:
                f.write(cockpit_md_content)
            results["cockpit_markdown"] = str(cockpit_md_path)

        if "json" in formats:
            cockpit_json_path = out_path / "data_leadership_cockpit.json"
            cockpit_json_content = JsonPersonaRenderer.render_cockpit(cockpit)
            with open(cockpit_json_path, "w", encoding="utf-8") as f:
                f.write(cockpit_json_content)
            results["cockpit_json"] = str(cockpit_json_path)

        # 2. Export Individual Lenses
        if include_individual_lenses:
            lenses_dir = out_path / "lenses"
            lenses_dir.mkdir(parents=True, exist_ok=True)

            for pid, projection in cockpit.lens_projections.items():
                if "md" in formats:
                    lens_md_path = lenses_dir / f"{pid}_lens.md"
                    lens_md_content = MarkdownPersonaRenderer.render(projection)
                    with open(lens_md_path, "w", encoding="utf-8") as f:
                        f.write(lens_md_content)
                    results[f"lens_{pid}_md"] = str(lens_md_path)

                if "json" in formats:
                    lens_json_path = lenses_dir / f"{pid}_lens.json"
                    lens_json_content = JsonPersonaRenderer.render_projection(projection)
                    with open(lens_json_path, "w", encoding="utf-8") as f:
                        f.write(lens_json_content)
                    results[f"lens_{pid}_json"] = str(lens_json_path)

        return results
