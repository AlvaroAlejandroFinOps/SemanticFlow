"""
Enterprise Documentation emitters (Markdown Data Dictionary & Mermaid ERD).
"""
import os
from typing import Dict, Any
from src.core.ast.canonical.models import CanonicalSemanticProject


class DocumentationEmitter:
    """Generates automated enterprise documentation from Canonical Semantic Projects."""

    def __init__(self, project: CanonicalSemanticProject):
        self.project = project

    def generate_markdown_dictionary(self) -> str:
        """Generates a complete Markdown Data Dictionary."""
        md = [f"# Data Dictionary: {self.project.name}\n"]
        if self.project.description:
            md.append(f"{self.project.description}\n")

        md.append("## Entities Overview\n")
        md.append("| Entity | Role | Attributes Count | Metrics Count | Source Table |")
        md.append("| --- | --- | --- | --- | --- |")
        for e in self.project.entities:
            source_tbl = getattr(e, 'source_table', 'N/A')
            md.append(f"| **{e.name}** | `{e.role.value}` | {len(e.attributes)} | {len(e.metrics)} | `{source_tbl}` |")
        
        md.append("\n## Detailed Entities & Attributes\n")
        for e in self.project.entities:
            md.append(f"### {e.name} (`{e.role.value}`)\n")
            if e.description:
                md.append(f"*{e.description}*\n")

            if e.attributes:
                md.append("#### Attributes")
                md.append("| Attribute | Data Type | Key Type | Classification |")
                md.append("| --- | --- | --- | --- |")
                for attr in e.attributes:
                    key_val = getattr(attr, 'key_type', None)
                    key_str = key_val.value if hasattr(key_val, 'value') else str(key_val or '-')
                    class_str = getattr(attr, 'classification', '-') or '-'
                    md.append(f"| `{attr.name}` | `{attr.data_type}` | `{key_str}` | `{class_str}` |")
                md.append("")

            if e.metrics:
                md.append("#### Metrics")
                md.append("| Metric | Expression | Certified | Owner |")
                md.append("| --- | --- | --- | --- |")
                for m in e.metrics:
                    cert = "Yes" if m.governance and m.governance.certified else "No"
                    owner = m.governance.owner if m.governance and m.governance.owner else "-"
                    md.append(f"| **{m.name}** | `{m.expression}` | {cert} | {owner} |")
                md.append("")

        return "\n".join(md)

    def generate_mermaid_erd(self) -> str:
        """Generates a Mermaid ERD diagram string."""
        mermaid = ["erDiagram"]
        for r in self.project.relationships:
            rel_type = "||--o{"
            from_e = getattr(r, 'from_entity_id', 'EntityA')
            to_e = getattr(r, 'to_entity_id', 'EntityB')
            from_a = getattr(r, 'from_attribute_id', 'attrA')
            to_a = getattr(r, 'to_attribute_id', 'attrB')
            mermaid.append(f'    "{from_e}" {rel_type} "{to_e}" : "{from_a} -> {to_a}"')
        return "\n".join(mermaid)

    def export_all(self, output_dir: str) -> Dict[str, str]:
        """Writes dictionary and Mermaid diagram to output_dir."""
        os.makedirs(output_dir, exist_ok=True)
        
        dict_path = os.path.join(output_dir, "DATA_DICTIONARY.md")
        dict_content = self.generate_markdown_dictionary()
        with open(dict_path, "w", encoding="utf-8") as f:
            f.write(dict_content)

        erd_path = os.path.join(output_dir, "ARCHITECTURE_ERD.mmd")
        erd_content = self.generate_mermaid_erd()
        with open(erd_path, "w", encoding="utf-8") as f:
            f.write(erd_content)

        return {
            "dictionary": dict_path,
            "erd": erd_path
        }
