"""
Power BI target adapter leveraging TMDL and PBIP emitters.
"""
from pathlib import Path
from typing import Any, Dict

from src.core.ast.canonical.models import CanonicalSemanticProject
from src.core.emitter.pbip_writer import PbipWriter
from src.core.mappers.canonical_to_pbi import CanonicalToPbiMapper
from src.core.targets.base import BaseTargetAdapter


class PowerBiTargetAdapter(BaseTargetAdapter):
    """Adapter for generating Power BI TMDL / PBIP semantic projects."""

    @property
    def target_name(self) -> str:
        return "powerbi"

    def export(self, project: CanonicalSemanticProject, output_path: str) -> Dict[str, Any]:
        pbi_project = CanonicalToPbiMapper.to_pbi_model(project)
        writer = PbipWriter()
        output_dir = writer.write_bundle(pbi_project, target_dir=Path(output_path))

        return {
            "target": self.target_name,
            "status": "SUCCESS",
            "output_dir": output_dir,
            "entities_count": len(project.entities),
            "relationships_count": len(project.relationships)
        }
