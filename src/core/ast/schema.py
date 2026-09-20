"""
Modelos AST canónicos para esquemas relacionales brutos ingeridos.
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.core.ast.types import PbiDataType, normalize_data_type


class KeyType(str, Enum):
    NONE = "NONE"
    PRIMARY = "PRIMARY"
    FOREIGN = "FOREIGN"
    PRIMARY_AND_FOREIGN = "PRIMARY_AND_FOREIGN"


class ColumnRaw(BaseModel):
    name: str
    raw_type: str
    key_type: KeyType = KeyType.NONE
    description: Optional[str] = None
    foreign_target_table: Optional[str] = None
    foreign_target_column: Optional[str] = None

    @property
    def pbi_type(self) -> PbiDataType:
        return normalize_data_type(self.raw_type)

    @property
    def is_primary(self) -> bool:
        return self.key_type in (KeyType.PRIMARY, KeyType.PRIMARY_AND_FOREIGN)

    @property
    def is_foreign(self) -> bool:
        return self.key_type in (KeyType.FOREIGN, KeyType.PRIMARY_AND_FOREIGN)


class TableRaw(BaseModel):
    name: str
    description: Optional[str] = None
    columns: list[ColumnRaw] = Field(default_factory=list)

    def get_column(self, col_name: str) -> Optional[ColumnRaw]:
        for col in self.columns:
            if col.name.lower() == col_name.lower():
                return col
        return None

    @property
    def primary_keys(self) -> list[ColumnRaw]:
        return [c for c in self.columns if c.is_primary]

    @property
    def foreign_keys(self) -> list[ColumnRaw]:
        return [c for c in self.columns if c.is_foreign]


class RelationshipRaw(BaseModel):
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    description: Optional[str] = None


class RelationalSchemaRaw(BaseModel):
    name: str
    description: Optional[str] = None
    tables: list[TableRaw] = Field(default_factory=list)
    relationships: list[RelationshipRaw] = Field(default_factory=list)

    def get_table(self, table_name: str) -> Optional[TableRaw]:
        for t in self.tables:
            if t.name.lower() == table_name.lower():
                return t
        return None
