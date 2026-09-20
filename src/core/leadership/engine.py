"""
Autonomous Data Leadership Cockpit Engine.
Orchestrates the 8 specialized leadership modules and exports executive-grade telemetry.
"""
from pathlib import Path
from typing import Dict, List, Optional, Union

from src.core.ast.canonical.models import CanonicalSemanticProject
from src.core.leadership.capability_gaps import CapabilityGapsAnalyzer, CapabilityGapsReport
from src.core.leadership.delivery_flow import DeliveryFlowAnalyzer, DeliveryFlowReport
from src.core.leadership.health import HealthAnalyzer, PortfolioHealthReport
from src.core.leadership.ownership import OwnershipAnalyzer, OwnershipCoverageReport
from src.core.leadership.portfolio import PortfolioAnalyzer, PortfolioSummary
from src.core.leadership.risk import RiskAnalyzer, RiskOverviewReport
from src.core.leadership.team_dependencies import TeamDependenciesAnalyzer, TeamDependenciesReport
from src.core.leadership.value_indicators import ValueIndicatorsAnalyzer, ValueIndicatorsReport
from src.core.personas.models import LeadershipCockpit, PersonaProjection
from src.core.personas.projector import PersonaProjector
from src.core.personas.registry import PersonaRegistry
from src.core.personas.renderers import (
    JsonPersonaRenderer,
    LeadershipCockpitRenderer,
    MarkdownPersonaRenderer,
)


class DataLeadershipCockpit:
    """Consolidated Data Leadership Cockpit synthesized across all 8 specialized modules."""

    def __init__(
        self,
        portfolio: PortfolioSummary,
        health: PortfolioHealthReport,
        ownership: OwnershipCoverageReport,
        gaps: CapabilityGapsReport,
        dependencies: TeamDependenciesReport,
        delivery: DeliveryFlowReport,
        value: ValueIndicatorsReport,
        risk: RiskOverviewReport,
        legacy_cockpit: LeadershipCockpit,
    ):
        self.portfolio = portfolio
        self.health = health
        self.ownership = ownership
        self.gaps = gaps
        self.dependencies = dependencies
        self.delivery = delivery
        self.value = value
        self.risk = risk
        self.legacy_cockpit = legacy_cockpit


class LeadershipCockpitEngine:
    """Isolated engine responsible for synthesizing and exporting the C-Level Data Leadership Cockpit."""

    def __init__(
        self,
        project: CanonicalSemanticProject,
        registry: Optional[PersonaRegistry] = None,
    ):
        self._project = project
        self._projector = PersonaProjector(project, registry=registry)

    @property
    def project(self) -> CanonicalSemanticProject:
        return self._project

    @property
    def projector(self) -> PersonaProjector:
        return self._projector

    def synthesize(self) -> DataLeadershipCockpit:
        """Runs the 8 modular analyzers and synthesizes the full leadership telemetry model."""
        projections: Dict[str, PersonaProjection] = self._projector.project_all()

        portfolio = PortfolioAnalyzer.analyze(self._project)
        health = HealthAnalyzer.analyze(self._project, projections)
        ownership = OwnershipAnalyzer.analyze(self._project)
        gaps = CapabilityGapsAnalyzer.analyze(self._project)
        dependencies = TeamDependenciesAnalyzer.analyze(projections)
        delivery = DeliveryFlowAnalyzer.analyze(self._project)
        value = ValueIndicatorsAnalyzer.analyze(self._project)
        risk = RiskAnalyzer.analyze(self._project, projections)

        legacy_cockpit = self._projector.build_leadership_cockpit()

        return DataLeadershipCockpit(
            portfolio=portfolio,
            health=health,
            ownership=ownership,
            gaps=gaps,
            dependencies=dependencies,
            delivery=delivery,
            value=value,
            risk=risk,
            legacy_cockpit=legacy_cockpit,
        )

    def generate_cockpit(self) -> LeadershipCockpit:
        """Returns the canonical synthesized LeadershipCockpit model."""
        return self.synthesize().legacy_cockpit

    def export_all(
        self,
        output_dir: Union[str, Path],
        include_individual_lenses: bool = True,
        formats: Optional[List[str]] = None,
    ) -> Dict[str, str]:
        """
        Exports the leadership cockpit and optionally all individual persona lenses to disk.
        Returns mapping of artifact keys to exported file paths.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        if formats is None:
            formats = ["md", "json"]

        results: Dict[str, str] = {}
        cockpit_bundle = self.synthesize()
        legacy_cockpit = cockpit_bundle.legacy_cockpit

        # 1. Export Consolidated Cockpit Files
        if "md" in formats:
            cockpit_md_path = out_path / "data_leadership_cockpit.md"
            cockpit_md_content = LeadershipCockpitRenderer.render_markdown(legacy_cockpit)
            with open(cockpit_md_path, "w", encoding="utf-8") as f:
                f.write(cockpit_md_content)
            results["cockpit_markdown"] = str(cockpit_md_path)

        if "json" in formats:
            cockpit_json_path = out_path / "data_leadership_cockpit.json"
            cockpit_json_content = JsonPersonaRenderer.render_cockpit(legacy_cockpit)
            with open(cockpit_json_path, "w", encoding="utf-8") as f:
                f.write(cockpit_json_content)
            results["cockpit_json"] = str(cockpit_json_path)

        # 2. Export Individual Lenses
        if include_individual_lenses:
            lenses_dir = out_path / "lenses"
            lenses_dir.mkdir(parents=True, exist_ok=True)

            for pid, projection in legacy_cockpit.lens_projections.items():
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
