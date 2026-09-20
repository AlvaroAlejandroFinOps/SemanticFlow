"""
Parser de esquemas relacionales a partir de documentos Markdown y ERDs de Mermaid.
Especializado en extraer especificaciones analíticas como docs/architecture/esquema_relacional.md.
"""
import re
from pathlib import Path
from typing import Union

from src.core.ast.schema import (
    ColumnRaw,
    KeyType,
    RelationalSchemaRaw,
    RelationshipRaw,
    TableRaw,
)
from src.core.parsers.base import BaseSchemaParser


class MarkdownSchemaParser(BaseSchemaParser):
    """Extrae tablas, columnas, claves y relaciones desde documentos Markdown."""

    def parse(self, source: Union[str, Path]) -> RelationalSchemaRaw:
        if isinstance(source, Path):
            content = source.read_text(encoding="utf-8")
            schema_name = source.stem
        elif Path(source).is_file():
            path_obj = Path(source)
            content = path_obj.read_text(encoding="utf-8")
            schema_name = path_obj.stem
        else:
            content = source
            schema_name = "MarkdownSchema"

        tables: list[TableRaw] = []
        relationships: list[RelationshipRaw] = []

        # 1. Parsear el bloque Mermaid ERD si existe
        mermaid_rels = self._parse_mermaid_erd(content)

        # 2. Parsear secciones de tablas (### x.y. `TableName`)
        table_sections = self._split_table_sections(content)
        for t_name, t_body in table_sections:
            table = self._parse_table_section(t_name, t_body)
            tables.append(table)

        # 3. Resolver relaciones: primero desde FK references explícitas en las columnas/viñetas
        for table in tables:
            for col in table.columns:
                if col.is_foreign and col.foreign_target_table and col.foreign_target_column:
                    relationships.append(
                        RelationshipRaw(
                            from_table=table.name,
                            from_column=col.name,
                            to_table=col.foreign_target_table,
                            to_column=col.foreign_target_column,
                            description=f"FK: {table.name}.{col.name} -> {col.foreign_target_table}.{col.foreign_target_column}",
                        )
                    )

        # 4. Si faltasen relaciones que estaban en Mermaid y no se detectó destino en tabla:
        existing_pairs = {(r.from_table.lower(), r.to_table.lower()) for r in relationships}
        for parent, child in mermaid_rels:
            # En Mermaid Star Schema común: Dim ||--o{ Fact (Parent = Dim, Child = Fact)
            # from Fact to Dim
            if (child.lower(), parent.lower()) not in existing_pairs and (parent.lower(), child.lower()) not in existing_pairs:
                # Intentar buscar columna coincidente
                child_table = next((t for t in tables if t.name.lower() == child.lower()), None)
                parent_table = next((t for t in tables if t.name.lower() == parent.lower()), None)
                if child_table and parent_table:
                    # Buscar coincidencia de nombre de clave
                    parent_pk = parent_table.primary_keys[0].name if parent_table.primary_keys else None
                    if parent_pk:
                        child_fk = child_table.get_column(parent_pk)
                        if child_fk:
                            relationships.append(
                                RelationshipRaw(
                                    from_table=child_table.name,
                                    from_column=child_fk.name,
                                    to_table=parent_table.name,
                                    to_column=parent_pk,
                                    description=f"Mermaid: {child_table.name}.{child_fk.name} -> {parent_table.name}.{parent_pk}",
                                )
                            )

        return RelationalSchemaRaw(
            name=schema_name,
            description="Esquema extraído desde Markdown",
            tables=tables,
            relationships=relationships,
        )

    def _parse_mermaid_erd(self, content: str) -> list[tuple[str, str]]:
        """Extrae pares (Parent, Child) de bloques mermaid erDiagram."""
        erd_matches = re.search(r"```mermaid\s+erDiagram(.*?)```", content, re.DOTALL)
        if not erd_matches:
            return []

        body = erd_matches.group(1)
        # Buscar patrones como: TableA ||--o{ TableB : "..."
        rel_pattern = re.compile(
            r"(\w+)\s+\|\|--[o\|]\{\s+(\w+)",
            re.IGNORECASE,
        )
        return rel_pattern.findall(body)

    def _split_table_sections(self, content: str) -> list[tuple[str, str]]:
        """Divide el documento por encabezados de tabla tipo '### 2.1. `Dim_Linea`'."""
        header_regex = re.compile(r"^###\s+[\d\.]+\s+`?([A-Za-z0-9_]+)`?.*$", re.MULTILINE)
        matches = list(header_regex.finditer(content))
        sections: list[tuple[str, str]] = []

        for i, m in enumerate(matches):
            t_name = m.group(1)
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            body = content[start:end]
            sections.append((t_name, body))

        return sections

    def _parse_table_section(self, table_name: str, body: str) -> TableRaw:
        """Parsea metadatos y la tabla markdown de una sección."""
        # Extraer descripción inicial antes de las viñetas o tablas
        desc_match = re.search(r"^(.*?)(?=\n\s*\*|\n\s*\|)", body.strip(), re.DOTALL)
        table_desc = desc_match.group(1).strip() if desc_match else None

        # Diccionario temporal de FKs extraídas de las viñetas: col_name -> (target_table, target_col)
        fk_references = self._parse_fk_bullet_points(body)

        # Parsear filas de la tabla Markdown
        columns = self._parse_markdown_table(body, fk_references)

        return TableRaw(
            name=table_name,
            description=table_desc,
            columns=columns,
        )

    def _parse_fk_bullet_points(self, body: str) -> dict[str, tuple[str, str]]:
        """
        Extrae mapeos de claves foráneas desde viñetas como:
        `SK_Linea` referencia a `Dim_Linea(SK_Linea)`
        """
        fk_map: dict[str, tuple[str, str]] = {}
        # Patrón: `Columna` referencia a `Tabla(TargetCol)`
        pattern = re.compile(
            r"`([A-Za-z0-9_]+)`\s+referencia\s+a\s+`?([A-Za-z0-9_]+)\(([A-Za-z0-9_]+)\)`?",
            re.IGNORECASE,
        )
        for col, target_table, target_col in pattern.findall(body):
            fk_map[col.lower()] = (target_table, target_col)
        return fk_map

    def _parse_markdown_table(
        self, body: str, fk_references: dict[str, tuple[str, str]]
    ) -> list[ColumnRaw]:
        """Extrae columnas desde la tabla markdown (| Campo | Tipo de Dato | Tipo Clave | Descripción |)."""
        columns: list[ColumnRaw] = []
        lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]

        if len(lines) < 3:
            return columns

        # Header y separador
        # header = lines[0]
        data_rows = lines[2:]

        for row in data_rows:
            parts = [p.strip() for p in row.strip("|").split("|")]
            if len(parts) < 2:
                continue

            col_name_raw = parts[0]
            data_type_raw = parts[1]
            key_type_raw = parts[2] if len(parts) > 2 else ""
            desc_raw = parts[3] if len(parts) > 3 else ""

            # Limpiar nombre
            col_name = re.sub(r"[\*`]", "", col_name_raw).strip()
            # Limpiar tipo
            data_type = re.sub(r"[\*`]", "", data_type_raw).strip()
            # Limpiar clave
            key_clean = re.sub(r"[\*`]", "", key_type_raw).strip().upper()
            desc = desc_raw.strip()

            # Determinar KeyType
            key_type = KeyType.NONE
            if "PKEY" in key_clean and "FKEY" in key_clean:
                key_type = KeyType.PRIMARY_AND_FOREIGN
            elif "PKEY" in key_clean or "PRIMARY" in key_clean:
                key_type = KeyType.PRIMARY
            elif "FKEY" in key_clean or "FOREIGN" in key_clean:
                key_type = KeyType.FOREIGN

            # Asignar referencias FK si existen
            fk_target = fk_references.get(col_name.lower())
            target_t, target_c = (None, None)
            if fk_target:
                target_t, target_c = fk_target
                if key_type == KeyType.NONE:
                    key_type = KeyType.FOREIGN

            columns.append(
                ColumnRaw(
                    name=col_name,
                    raw_type=data_type,
                    key_type=key_type,
                    description=desc if desc else None,
                    foreign_target_table=target_t,
                    foreign_target_column=target_c,
                )
            )

        return columns
