"""
Base interface for BI target adapters.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.core.ast.canonical.models import CanonicalSemanticProject


class BaseTargetAdapter(ABC):
    """Abstract Base Class for target BI platform code generators / exporters."""

    @property
    @abstractmethod
    def target_name(self) -> str:
        """Returns the canonical name of the target platform (e.g., 'powerbi', 'dbt', 'cube')."""
        pass

    @abstractmethod
    def export(self, project: CanonicalSemanticProject, output_path: str) -> Dict[str, Any]:
        """
        Exports the CanonicalSemanticProject to the target platform artifacts.
        
        Returns execution summary metadata.
        """
        pass
