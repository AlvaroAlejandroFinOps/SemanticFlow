"""
Renderers for Persona Projections and the Data Leadership Cockpit.
Generates Markdown, JSON, and Mermaid outputs deterministically.
"""
from typing import List

from src.core.personas.models import (
    LeadershipCockpit,
    PersonaProjection,
    TechnicalDepth,
)


class MermaidPersonaRenderer:
    """Generates Mermaid diagrams for persona perspectives and team interactions."""

    @staticmethod
    def render_erd_subgraph(projection: PersonaProjection, max_entities: int = 10) -> str:
        """Generates a Mermaid ERD focusing on primary entities for this persona."""
        lines = ["```mermaid", "erDiagram"]
        entities = projection.primary_entities[:max_entities]
        if not entities:
            lines.append("    NO_DATA ||--o{ EMPTY : \"No primary entities\"")
        else:
            for ent in entities:
                lines.append(f"    {ent} {{")
                lines.append("        string role \"Primary Asset\"")
                lines.append("    }")
        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def render_team_interactions(projection: PersonaProjection) -> str:
        """Generates a Mermaid sequence diagram of team handoffs and interactions."""
        if not projection.interactions:
            return ""

        lines = ["```mermaid", "sequenceDiagram", f"    actor Current as {projection.role.value}"]
        for idx, inter in enumerate(projection.interactions):
            target_alias = f"Target{idx}"
            lines.append(f"    actor {target_alias} as {inter.target_persona.value}")
            lines.append(f"    Current->>{target_alias}: [{inter.interaction_type.upper()}] {inter.interface_artifact} ({inter.frequency})")
            if inter.sla_or_expectation:
                lines.append(f"    Note over Current,{target_alias}: SLA: {inter.sla_or_expectation}")
        lines.append("```")
        return "\n".join(lines)


class MarkdownPersonaRenderer:
    """Renders rich, paper-grade GitHub Flavored Markdown for a PersonaProjection."""

    @classmethod
    def render(cls, projection: PersonaProjection, include_diagrams: bool = True) -> str:
        """Produces a complete Markdown document for a single persona projection."""
        lines: List[str] = []

        # 1. Header & Badges
        lines.append(f"# {projection.title}")
        lines.append("")
        lines.append(f"**Persona Role**: `{projection.role.value}` | **Technical Depth**: `{projection.technical_depth.value}`")
        if projection.rendered_at:
            lines.append(f"**Generated At**: `{projection.rendered_at}`")
        lines.append("")

        # 2. Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        lines.append("> [!NOTE]")
        lines.append(f"> {projection.summary}")
        lines.append("")

        # 3. Focus Areas & Strategic Objectives
        if projection.focus_areas:
            lines.append("### Focus Areas")
            for fa in projection.focus_areas:
                lines.append(f"- **{fa.value.replace('_', ' ').title()}**")
            lines.append("")

        # 4. Certified KPIs & Metrics
        lines.append("## Metrics & KPIs Portfolio")
        lines.append("")
        if projection.certified_metrics:
            lines.append("### Certified Metrics")
            lines.append("| Metric Name | Status | Type |")
            lines.append("| :--- | :--- | :--- |")
            for m in projection.certified_metrics:
                lines.append(f"| **{m}** | Certified | KPI / Core Metric |")
            lines.append("")
        else:
            lines.append("_No certified metrics assigned to this primary scope._\n")

        if projection.secondary_metrics and projection.technical_depth in (TechnicalDepth.TECHNICAL, TechnicalDepth.EXHAUSTIVE):
            lines.append("### Supporting / Operational Metrics")
            for sm in projection.secondary_metrics:
                lines.append(f"- `{sm}`")
            lines.append("")

        # 5. Entity Scope & Modeling Topology
        lines.append("## Entity Scope")
        lines.append("")
        lines.append(f"- **Primary Entities ({len(projection.primary_entities)})**: {', '.join([f'`{e}`' for e in projection.primary_entities]) if projection.primary_entities else 'None'}")
        if projection.secondary_entities:
            lines.append(f"- **Secondary Entities ({len(projection.secondary_entities)})**: {', '.join([f'`{e}`' for e in projection.secondary_entities])}")
        lines.append(f"- **Active Relationships**: {projection.relationships_count}")
        lines.append("")

        if include_diagrams and projection.primary_entities:
            lines.append("### Entity Topology Diagram")
            lines.append(MermaidPersonaRenderer.render_erd_subgraph(projection))
            lines.append("")

        # 6. Governance & RACI Responsibilities
        if projection.responsibilities:
            lines.append("## RACI Responsibility Matrix")
            lines.append("")
            lines.append("| Task / Artifact | RACI Role | Description | Collaborators |")
            lines.append("| :--- | :--- | :--- | :--- |")
            for r in projection.responsibilities:
                collabs = ", ".join([c.value for c in r.collaborator_roles]) if r.collaborator_roles else "-"
                desc = r.description or "-"
                lines.append(f"| {r.task_or_artifact} | **{r.role.value}** | {desc} | {collabs} |")
            lines.append("")

        # 7. Cross-Functional Team Interactions
        if projection.interactions:
            lines.append("## Cross-Functional Team Interactions")
            lines.append("")
            lines.append("| Target Persona | Interaction Type | Frequency | Artifact / Interface | SLA / Expectation |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for inter in projection.interactions:
                sla = inter.sla_or_expectation or "-"
                lines.append(f"| **{inter.target_persona.value}** | {inter.interaction_type} | {inter.frequency} | `{inter.interface_artifact}` | {sla} |")
            lines.append("")
            if include_diagrams:
                diagram = MermaidPersonaRenderer.render_team_interactions(projection)
                if diagram:
                    lines.append("### Interaction Flow")
                    lines.append(diagram)
                    lines.append("")

        # 8. Actionable Persona Recommendations
        if projection.recommendations:
            lines.append("## Actionable Recommendations")
            lines.append("")
            lines.append("| ID | Priority | Title | Impact | Effort | Suggested Action |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for rec in projection.recommendations:
                action = rec.suggested_action or rec.description
                lines.append(f"| `{rec.id}` | **{rec.priority.value}** | {rec.title} | {rec.impact} | {rec.effort} | {action} |")
            lines.append("")

        # 9. Maturity Assessment
        if projection.maturity_assessment:
            mat = projection.maturity_assessment
            lines.append("## Domain Maturity Assessment")
            lines.append("")
            lines.append(f"**Overall Score**: `{mat.overall_score:.1f}/100.0` ({mat.maturity_level})")
            lines.append("")
            if mat.dimensions:
                lines.append("| Maturity Dimension | Score | Level | Findings |")
                lines.append("| :--- | :--- | :--- | :--- |")
                for dim in mat.dimensions:
                    findings_str = "; ".join(dim.findings) if dim.findings else "Nominal"
                    lines.append(f"| {dim.dimension_name} | {dim.score:.1f}% | {dim.level} | {findings_str} |")
                lines.append("")
            if mat.strengths:
                lines.append("### Strengths")
                for s in mat.strengths:
                    lines.append(f"- {s}")
                lines.append("")
            if mat.gaps:
                lines.append("### Areas for Improvement")
                for g in mat.gaps:
                    lines.append(f"- {g}")
                lines.append("")

        # 10. Diagnostics
        if projection.diagnostics and projection.technical_depth in (TechnicalDepth.TECHNICAL, TechnicalDepth.EXHAUSTIVE):
            lines.append("## Diagnostics & Audit Traces")
            lines.append("")
            for diag in projection.diagnostics:
                lines.append(f"- `[{diag.severity.value}]` **{diag.code}** ({diag.category.value}): {diag.message}")
            lines.append("")

        return "\n".join(lines)


class JsonPersonaRenderer:
    """Renders PersonaProjections and Cockpits as formatted JSON."""

    @staticmethod
    def render_projection(projection: PersonaProjection, indent: int = 2) -> str:
        """Serializes PersonaProjection to JSON string."""
        return projection.model_dump_json(indent=indent)

    @staticmethod
    def render_cockpit(cockpit: LeadershipCockpit, indent: int = 2) -> str:
        """Serializes LeadershipCockpit to JSON string."""
        return cockpit.model_dump_json(indent=indent)


class LeadershipCockpitRenderer:
    """Renders the executive Data Leadership Cockpit in Markdown."""

    @classmethod
    def render_markdown(cls, cockpit: LeadershipCockpit) -> str:
        """Generates comprehensive C-Level Data Leadership Cockpit Markdown."""
        lines: List[str] = [
            f"# Data Leadership Cockpit: {cockpit.project_name}",
            f"**Version**: `{cockpit.project_version}` | **Generated At**: `{cockpit.generated_at}`",
            "",
            "## Executive Overview",
            "> [!IMPORTANT]",
            f"> {cockpit.executive_summary}",
            "",
            "## Governance & Portfolio Health",
            "",
            "| Metric | Value |",
            "| :--- | :--- |",
        ]

        for k, v in cockpit.governance_overview.items():
            metric_label = k.replace("_", " ").title()
            lines.append(f"| {metric_label} | **{v}** |")
        lines.append("")

        if cockpit.maturity_radar:
            lines.append("## Domain Maturity Radar")
            lines.append("")
            lines.append("| Persona / Domain | Maturity Score | Target Band |")
            lines.append("| :--- | :--- | :--- |")
            for persona_name, score in cockpit.maturity_radar.items():
                band = "Optimal (>=80%)" if score >= 80 else ("Satisfactory (>=60%)" if score >= 60 else "Attention Required (<60%)")
                lines.append(f"| **{persona_name}** | `{score:.1f}%` | {band} |")
            lines.append("")

        if cockpit.priority_action_matrix:
            lines.append("## Executive Priority Action Matrix")
            lines.append("")
            lines.append("| ID | Priority | Title | Impact | Effort | Owner Persona |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for act in cockpit.priority_action_matrix:
                owner = act.target_objects[0] if act.target_objects else "Enterprise Leadership"
                lines.append(f"| `{act.id}` | **{act.priority.value}** | {act.title} | {act.impact} | {act.effort} | {owner} |")
            lines.append("")

        lines.append("## Registered Persona Lens Perspectives")
        lines.append("")
        for pid, proj in cockpit.lens_projections.items():
            lines.append(f"- **[{proj.title}](#{pid})**: {proj.summary[:120]}...")
        lines.append("")

        return "\n".join(lines)
