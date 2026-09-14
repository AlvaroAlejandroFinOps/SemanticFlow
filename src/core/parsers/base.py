"""
Interfaz base para extractores/parsers de esquemas relacionales a AST Canónico.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from src.core.ast.schema import RelationalSchemaRaw


class BaseSchemaParser(ABC):
    """Clase base abstracta para parsers de esquemas."""

    @abstractmethod
    def parse(self, source: Union[str, Path]) -> RelationalSchemaRaw:
        """Parsea la fuente (ruta o contenido string) y retorna un RelationalSchemaRaw."""
        pass
