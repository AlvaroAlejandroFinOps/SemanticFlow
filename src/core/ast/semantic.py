"""
Modelos AST canónicos para el Modelo Semántico enriquecido listo para emitir TMDL/PBIP.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from src.core.ast.types import PbiDataType


class TableRole(str, Enum):
    DIMENSION = "DIMENSION"
    FACT = "FACT"
    BRIDGE = "BRIDGE"
    CALCULATED = "CALCULATED"


class CrossFilteringBehavior(str, Enum):
    ONE_DIRECTION = "oneDirection"
    BOTH_DIRECTIONS = "bothDirections"
    AUTOMATIC = "automatic"


class SummarizeBy(str, Enum):
    NONE = "none"
    SUM = "sum"
    COUNT = "count"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    DISTINCT_COUNT = "distinctCount"


class SemanticColumn(BaseModel):
    name: str
    data_type: PbiDataType
    is_hidden: bool = False
    summarize_by: SummarizeBy = SummarizeBy.NONE
    format_string: Optional[str] = None
    description: Optional[str] = None
    display_folder: Optional[str] = None
    source_column: Optional[str] = None


class SemanticMeasure(BaseModel):
    name: str
    expression: str
    format_string: Optional[str] = None
    display_folder: Optional[str] = None
    description: Optional[str] = None
    is_hidden: bool = False


class SemanticTable(BaseModel):
    name: str
    role: TableRole = TableRole.DIMENSION
    description: Optional[str] = None
    columns: list[SemanticColumn] = Field(default_factory=list)
    measures: list[SemanticMeasure] = Field(default_factory=list)
    m_partition_expression: Optional[str] = None

    def get_column(self, col_name: str) -> Optional[SemanticColumn]:
        for c in self.columns:
            if c.name.lower() == col_name.lower():
                return c
        return None


class SemanticRelationship(BaseModel):
    name: str
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    cross_filtering_behavior: CrossFilteringBehavior = CrossFilteringBehavior.ONE_DIRECTION
    is_active: bool = True
    security_filtering_behavior: str = "oneDirection"


class SemanticModel(BaseModel):
    name: str
    compatibility_level: int = 1567
    culture: str = "es-CL"
    tables: list[SemanticTable] = Field(default_factory=list)
    relationships: list[SemanticRelationship] = Field(default_factory=list)
    description: Optional[str] = None

    def get_table(self, name: str) -> Optional[SemanticTable]:
        for t in self.tables:
            if t.name.lower() == name.lower():
                return t
        return None
