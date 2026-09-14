"""
Generador del archivo relationships.tmdl en sintaxis nativa TMDL.
"""
from src.core.ast.semantic import SemanticRelationship, CrossFilteringBehavior
from src.core.emitter.tmdl_formatter import escape_tmdl_identifier


class RelationshipEmitter:
    """Genera la lista de relaciones en sintaxis TMDL."""

    def emit_relationships(self, relationships: list[SemanticRelationship]) -> str:
        blocks: list[str] = []

        for rel in relationships:
            rel_id = escape_tmdl_identifier(rel.name)
            lines: list[str] = [f"relationship {rel_id}"]

            # Columnas de origen y destino
            from_ref = f"{escape_tmdl_identifier(rel.from_table)}.{escape_tmdl_identifier(rel.from_column)}"
            to_ref = f"{escape_tmdl_identifier(rel.to_table)}.{escape_tmdl_identifier(rel.to_column)}"

            lines.append(f"\tfromColumn: {from_ref}")
            lines.append(f"\ttoColumn: {to_ref}")

            if rel.cross_filtering_behavior != CrossFilteringBehavior.ONE_DIRECTION:
                lines.append(f"\tcrossFilteringBehavior: {rel.cross_filtering_behavior.value}")

            if not rel.is_active:
                lines.append("\tisActive: false")

            blocks.append("\n".join(lines))

        return "\n\n".join(blocks) + "\n" if blocks else ""
