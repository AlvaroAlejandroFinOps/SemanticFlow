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
        mermaid_entities = self._parse_mermaid_entities(content)
        mermaid_entity_map = {e.name.lower(): e for e in mermaid_entities}

        # 2. Parsear secciones de tablas (### x.y. `TableName` o #### A. `fact_name`)
        table_sections = self._split_table_sections(content)
        for t_name, t_body in table_sections:
            table = self._parse_table_section(t_name, t_body)
            # Enriquecer claves desde Mermaid si en Markdown no se especificaron
            m_entity = mermaid_entity_map.get(table.name.lower())
            if m_entity:
                m_cols = {c.name.lower(): c for c in m_entity.columns}
                for col in table.columns:
                    m_col = m_cols.get(col.name.lower())
                    if m_col:
                        if col.key_type == KeyType.NONE and m_col.key_type != KeyType.NONE:
                            col.key_type = m_col.key_type
            tables.append(table)

        # 2b. Parsear entidades del bloque Mermaid que no tengan sección Markdown (ej: DIM_EMPRESA_SOCIEDAD)
        existing_table_names = {t.name.lower() for t in tables}
        for me in mermaid_entities:
            if me.name.lower() not in existing_table_names:
                tables.append(me)
                existing_table_names.add(me.name.lower())

        # 3. Resolver relaciones: primero desde FK references explícitas en las columnas/viñetas
        for table in tables:
            for col in table.columns:
                if (
                    col.is_foreign
                    and col.foreign_target_table
                    and col.foreign_target_column
                    and col.foreign_target_table.lower() in existing_table_names
                ):
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
                child_table = next((t for t in tables if t.name.lower() == child.lower()), None)
                parent_table = next((t for t in tables if t.name.lower() == parent.lower()), None)
                if child_table and parent_table:
                    parent_pk = parent_table.primary_keys[0].name if parent_table.primary_keys else None
                    if parent_pk:
                        child_fk = child_table.get_column(parent_pk)
                        if not child_fk:
                            pk_root = parent_pk.lower().replace("sk_", "").replace("id_", "")
                            candidates = [
                                c for c in child_table.columns
                                if parent_pk.lower() in c.name.lower()
                                or (pk_root and pk_root in c.name.lower())
                            ]
                            if candidates:
                                child_fk = candidates[0]
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
                            existing_pairs.add((child_table.name.lower(), parent_table.name.lower()))
                        else:
                            # Caso puente o relación por clave de negocio común (ej: codigo_obra_sap)
                            common_cols = [c.name for c in child_table.columns if parent_table.get_column(c.name)]
                            if common_cols:
                                c_col = common_cols[0]
                                relationships.append(
                                    RelationshipRaw(
                                        from_table=child_table.name,
                                        from_column=c_col,
                                        to_table=parent_table.name,
                                        to_column=c_col,
                                        description=f"Mermaid: {child_table.name}.{c_col} -> {parent_table.name}.{c_col}",
                                    )
                                )
                                existing_pairs.add((child_table.name.lower(), parent_table.name.lower()))

        return RelationalSchemaRaw(
            name=schema_name,
            description="Esquema extraído desde Markdown",
            tables=tables,
            relationships=relationships,
        )

    def _parse_mermaid_entities(self, content: str) -> list[TableRaw]:
        """Extrae entidades con columnas declaradas dentro del bloque mermaid erDiagram."""
        erd_matches = re.search(r"```mermaid\s+erDiagram(.*?)```", content, re.DOTALL)
        if not erd_matches:
            return []
        body = erd_matches.group(1)
        entity_pattern = re.compile(r"([A-Za-z0-9_]+)\s*\{([^}]+)\}", re.MULTILINE)
        tables = []
        for t_name, fields_block in entity_pattern.findall(body):
            columns = []
            for line in fields_block.strip().splitlines():
                parts = line.strip().split()
                if len(parts) >= 2:
                    raw_type = parts[0]
                    col_name = parts[1]
                    key_tag = parts[2].upper() if len(parts) > 2 else ""
                    key_type = KeyType.NONE
                    if "PK" in key_tag:
                        key_type = KeyType.PRIMARY
                    elif "FK" in key_tag:
                        key_type = KeyType.FOREIGN
                    columns.append(ColumnRaw(name=col_name, raw_type=raw_type, key_type=key_type))
            if columns:
                tables.append(TableRaw(name=t_name, description="Extraída de Mermaid ERD", columns=columns))
        return tables

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
        """Divide el documento por encabezados de tabla tipo '### 2.1. `Dim_Linea`' o '#### A. `fact_name`'."""
        header_regex = re.compile(
            r"^#{2,4}\s+(?:[A-Za-z\d\.]+\s+)?(?:`([A-Za-z0-9_]+)`|((?:dim|fact|bridge)_[A-Za-z0-9_]+)).*$",
            re.MULTILINE | re.IGNORECASE,
        )
        matches = list(header_regex.finditer(content))
        sections: list[tuple[str, str]] = []

        for i, m in enumerate(matches):
            t_name = m.group(1) or m.group(2)
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            body = content[start:end]
            # Truncar si hay un encabezado de nivel 1 o 2 (ej: ## 6 o ## 7)
            sec_end = re.search(r"\n#{1,2}\s+[^\n]+", body)
            if sec_end:
                body = body[:sec_end.start()]
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
        """Extrae columnas desde la primera tabla markdown contigua."""
        columns: list[ColumnRaw] = []
        raw_lines = body.splitlines()

        # Encontrar el primer bloque contiguo de tabla Markdown
        table_lines = []
        in_table = False
        for line in raw_lines:
            s_line = line.strip()
            if s_line.startswith("|"):
                in_table = True
                table_lines.append(s_line)
            elif in_table:
                break

        if len(table_lines) < 3:
            return columns

        # Mapeo dinámico de cabeceras
        headers = [h.strip().lower() for h in table_lines[0].strip("|").split("|")]
        col_idx = 0
        type_idx = 1
        key_idx = None
        desc_idx = None

        for idx, h in enumerate(headers):
            h_clean = re.sub(r"[^a-záéíóúñ0-9]", "", h)
            if any(k in h_clean for k in ["restriccion", "naturaleza", "clave", "key", "constraint"]):
                key_idx = idx
            elif any(k in h_clean for k in ["campo", "columna", "column"]):
                col_idx = idx
            elif any(k in h_clean for k in ["tipo", "datatype", "type"]) and "clave" not in h_clean:
                type_idx = idx
            elif any(k in h_clean for k in ["descripcion", "desc", "glosa", "detalle", "notes", "origen"]):
                if desc_idx is None:
                    desc_idx = idx

        if key_idx is None and desc_idx is None and len(headers) >= 3:
            desc_idx = 2

        data_rows = table_lines[2:]

        for row in data_rows:
            parts = [p.strip() for p in row.strip("|").split("|")]
            if len(parts) <= max(col_idx, type_idx):
                continue

            col_name_raw = parts[col_idx]
            data_type_raw = parts[type_idx]
            key_type_raw = parts[key_idx] if (key_idx is not None and key_idx < len(parts)) else ""
            desc_raw = parts[desc_idx] if (desc_idx is not None and desc_idx < len(parts)) else ""

            col_name = re.sub(r"[\*`]", "", col_name_raw).strip()
            data_type = re.sub(r"[\*`]", "", data_type_raw).strip()
            key_clean = re.sub(r"[\*`]", "", key_type_raw).strip().upper()
            desc = desc_raw.strip()

            is_pk = bool(re.search(r"\b(PK|PKEY|PRIMARY)\b", key_clean, re.I))
            is_fk = bool(re.search(r"\b(FK|FKEY|FOREIGN)\b", key_clean, re.I))

            if is_pk and is_fk:
                key_type = KeyType.PRIMARY_AND_FOREIGN
            elif is_pk:
                key_type = KeyType.PRIMARY
            elif is_fk:
                key_type = KeyType.FOREIGN
            else:
                key_type = KeyType.NONE

            if key_type == KeyType.NONE and desc:
                if re.search(r"\b(PRIMARY KEY|CLAVE PRIMARIA|CLAVE SURROGADA)\b", desc, re.I) and (
                    col_name.lower().startswith("sk_") or col_name.lower().startswith("id_")
                ):
                    key_type = KeyType.PRIMARY

            fk_target = fk_references.get(col_name.lower())
            target_t, target_c = (None, None)
            if fk_target:
                target_t, target_c = fk_target
                if key_type == KeyType.NONE:
                    key_type = KeyType.FOREIGN
            else:
                # Buscar FK en formato FKEY (Table:Col)
                fk_match = re.search(
                    r"(?:FKEY|FK)[^\(]*\(\s*`?([A-Za-z0-9_]+)`?[\.:]`?([A-Za-z0-9_]+)`?\s*\)",
                    f"{key_type_raw} {desc_raw}",
                    re.IGNORECASE,
                )
                if fk_match:
                    target_t, target_c = fk_match.group(1), fk_match.group(2)
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
