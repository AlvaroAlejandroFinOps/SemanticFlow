"""
Parser de esquemas declarativos estructurados en formato YAML o JSON.
"""
from pathlib import Path
from typing import Union
import yaml
from src.core.parsers.base import BaseSchemaParser
from src.core.ast.schema import (
    KeyType,
    ColumnRaw,
    TableRaw,
    RelationshipRaw,
    RelationalSchemaRaw,
)


class YamlSchemaParser(BaseSchemaParser):
    """Parsea archivos de esquema declarativo YAML o JSON."""

    def parse(self, source: Union[str, Path]) -> RelationalSchemaRaw:
        if isinstance(source, Path):
            content = source.read_text(encoding="utf-8")
            default_name = source.stem
        elif Path(source).is_file():
            path_obj = Path(source)
            content = path_obj.read_text(encoding="utf-8")
            default_name = path_obj.stem
        else:
            content = source
            default_name = "DeclarativeSchema"

        data = yaml.safe_load(content) or {}
        schema_name = data.get("name", default_name)
        schema_desc = data.get("description")

        tables: list[TableRaw] = []
        for t_dict in data.get("tables", []):
            columns: list[ColumnRaw] = []
            for c_dict in t_dict.get("columns", []):
                ktype_str = str(c_dict.get("key_type", "NONE")).upper()
                try:
                    ktype = KeyType(ktype_str)
                except ValueError:
                    ktype = KeyType.NONE

                columns.append(
                    ColumnRaw(
                        name=c_dict["name"],
                        raw_type=c_dict.get("type", "string"),
                        key_type=ktype,
                        description=c_dict.get("description"),
                        foreign_target_table=c_dict.get("foreign_target_table"),
                        foreign_target_column=c_dict.get("foreign_target_column"),
                    )
                )

            tables.append(
                TableRaw(
                    name=t_dict["name"],
                    description=t_dict.get("description"),
                    columns=columns,
                )
            )

        relationships: list[RelationshipRaw] = []
        for r_dict in data.get("relationships", []):
            relationships.append(
                RelationshipRaw(
                    from_table=r_dict["from_table"],
                    from_column=r_dict["from_column"],
                    to_table=r_dict["to_table"],
                    to_column=r_dict["to_column"],
                    description=r_dict.get("description"),
                )
            )

        return RelationalSchemaRaw(
            name=schema_name,
            description=schema_desc,
            tables=tables,
            relationships=relationships,
        )
