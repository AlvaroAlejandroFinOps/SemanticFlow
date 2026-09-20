"""
Data Leadership Cockpit Legacy Adapter.
Delegates to the autonomous src.core.leadership package while preserving backwards compatibility.
"""
from pathlib import Path
from typing import Dict, List, Optional, Union

from src.core.ast.canonical.models import CanonicalSemanticProject
from src.core.leadership.engine import LeadershipCockpitEngine
from src.core.personas.models import LeadershipCockpit
from src.core.personas.projector import PersonaProjector
from src.core.personas.registry import PersonaRegistry


class DataLeadershipCockpitEngine:
    """Legacy adapter delegating to the isolated src.core.leadership.LeadershipCockpitEngine."""

    def __init__(
        self,
        project: CanonicalSemanticProject,
        registry: Optional[PersonaRegistry] = None,
    ):
        self._engine = LeadershipCockpitEngine(project, registry=registry)

    @property
    def projector(self) -> PersonaProjector:
        return self._engine.projector

    def generate_cockpit(self) -> LeadershipCockpit:
        """Generates the full synthesized LeadershipCockpit model."""
        return self._engine.generate_cockpit()

    def export_all(
        self,
        output_dir: Union[str, Path],
        include_individual_lenses: bool = True,
        formats: Optional[List[str]] = None,
    ) -> Dict[str, str]:
        """Exports the leadership cockpit and lenses via the autonomous leadership engine."""
        return self._engine.export_all(
            output_dir=output_dir,
            include_individual_lenses=include_individual_lenses,
            formats=formats,
        )

