"""
DAX Symbol Table Validator.
Performs semantic and symbol table validation of DAX measures against the Canonical AST:
- QUAL_DAX_REF_001: Missing entity, column, or measure references.
- QUAL_DAX_TYPE_001: Aggregation functions on non-numeric attributes.
- QUAL_DAX_CYCLE_001: Cyclic dependencies among DAX measures.
"""
import re
from typing import Dict, List, Optional, Set, Tuple

import networkx as nx

from src.core.ast.canonical.models import (
    CanonicalSemanticProject,
    DataType,
    Diagnostic,
    DiagnosticCategory,
    DiagnosticSeverity,
    SemanticAttribute,
    SemanticEntity,
    SemanticMetric,
)

# Common DAX built-in terms or keywords that appear inside brackets or expressions
_KNOWN_DAX_KEYWORDS = {
    "date", "year", "month", "day", "value", "total", "blank", "true", "false",
}


def _strip_dax_string_literals(expr: str) -> str:
    """Replaces string literals between double quotes with spaces."""
    in_string = False
    clean = []
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c == '"':
            if in_string and i + 1 < n and expr[i + 1] == '"':
                i += 2
                continue
            in_string = not in_string
            clean.append(" ")
            i += 1
            continue
        if in_string:
            clean.append(" ")
        else:
            clean.append(c)
        i += 1
    return "".join(clean)


def _extract_local_variables(expr: str) -> Set[str]:
    """Extracts local variables declared as 'VAR <id> ='."""
    var_re = re.compile(r"\bVAR\s+([a-zA-Z0-9_]+)\s*=", re.IGNORECASE)
    return {m.group(1).lower() for m in var_re.finditer(expr)}


class SymbolTableDaxValidator:
    """
    Validates DAX expressions against the project's canonical symbol table.
    """

    def __init__(self, project: CanonicalSemanticProject):
        self.project = project
        self.entity_map: Dict[str, SemanticEntity] = {
            e.name.lower(): e for e in project.entities
        }
        self.column_map: Dict[str, Dict[str, SemanticAttribute]] = {
            e.name.lower(): {a.name.lower(): a for a in e.attributes}
            for e in project.entities
        }
        self.metric_map: Dict[str, SemanticMetric] = {}
        for e in project.entities:
            for m in e.metrics:
                self.metric_map[m.name.lower()] = m

    def validate_project(self) -> List[Diagnostic]:
        """Runs symbol validation across all metrics in the project."""
        diagnostics: List[Diagnostic] = []
        dep_graph = nx.DiGraph()

        # Populate measure nodes in dependency graph
        for m_name in self.metric_map:
            dep_graph.add_node(m_name)

        for entity in self.project.entities:
            for metric in entity.metrics:
                if not metric.expression:
                    continue
                d_refs, d_types = self._validate_metric_symbols(entity, metric, dep_graph)
                diagnostics.extend(d_refs)
                diagnostics.extend(d_types)

        # Detect cyclic dependencies among measures
        cycles = list(nx.simple_cycles(dep_graph))
        for cycle in cycles:
            cycle_str = " -> ".join(cycle + [cycle[0]])
            diagnostics.append(
                Diagnostic(
                    code="QUAL_DAX_CYCLE_001",
                    severity=DiagnosticSeverity.ERROR,
                    category=DiagnosticCategory.QUALITY,
                    message=f"Dependencia cíclica detectada entre medidas DAX: {cycle_str}.",
                    object_id=f"metric.{cycle[0]}",
                    suggested_action="Romper la recursión o dependencia circular entre las medidas identificadas.",
                    penalty=15.0,
                )
            )

        return diagnostics

    def _validate_metric_symbols(
        self,
        entity: SemanticEntity,
        metric: SemanticMetric,
        dep_graph: nx.DiGraph,
    ) -> Tuple[List[Diagnostic], List[Diagnostic]]:
        ref_diags: List[Diagnostic] = []
        type_diags: List[Diagnostic] = []

        clean_expr = _strip_dax_string_literals(metric.expression)
        local_vars = _extract_local_variables(clean_expr)
        curr_metric_name = metric.name.lower()

        # 1. Check for Qualified References: 'Table'[Column] or Table[Column]
        qual_pattern = re.compile(
            r"(?:'(?P<tab_q>[^']+)'|(?P<tab_b>\b[a-zA-Z0-9_]+))\[(?P<col>[^\]]+)\]"
        )
        for match in qual_pattern.finditer(clean_expr):
            tab_name = (match.group("tab_q") or match.group("tab_b") or "").strip()
            col_name = match.group("col").strip()

            tab_key = tab_name.lower()
            col_key = col_name.lower()

            # Ignore if table name matches a local variable or DAX keyword
            if tab_key in local_vars:
                continue

            target_entity = self.entity_map.get(tab_key)
            if not target_entity:
                ref_diags.append(
                    Diagnostic(
                        code="QUAL_DAX_REF_001",
                        severity=DiagnosticSeverity.ERROR,
                        category=DiagnosticCategory.QUALITY,
                        message=(
                            f"La tabla '{tab_name}' referenciada en la expresión de '{entity.name}.{metric.name}' "
                            "no existe en el proyecto semántico."
                        ),
                        object_id=metric.id,
                        suggested_action="Verificar el nombre de la tabla referenciada o agregarla al esquema.",
                        penalty=5.0,
                    )
                )
            else:
                # Table exists, verify column or measure inside table
                cols = self.column_map.get(tab_key, {})
                table_metrics = {m.name.lower() for m in target_entity.metrics}

                if col_key not in cols and col_key not in table_metrics and col_key not in _KNOWN_DAX_KEYWORDS:
                    ref_diags.append(
                        Diagnostic(
                            code="QUAL_DAX_REF_001",
                            severity=DiagnosticSeverity.ERROR,
                            category=DiagnosticCategory.QUALITY,
                            message=(
                                f"La columna o medida '{col_name}' referenciada en '{entity.name}.{metric.name}' "
                                f"no existe en la tabla '{target_entity.name}'."
                            ),
                            object_id=metric.id,
                            suggested_action=f"Verificar los atributos de '{target_entity.name}'.",
                            penalty=5.0,
                        )
                    )
                elif col_key in table_metrics:
                    dep_graph.add_edge(curr_metric_name, col_key)

        # 2. Check for Unqualified References: [Identifier]
        # Must not be preceded by a table name or quote
        unqual_pattern = re.compile(r"(?<![a-zA-Z0-9_'])\[(?P<id>[a-zA-Z0-9_ -]+)\]")
        for match in unqual_pattern.finditer(clean_expr):
            ident = match.group("id").strip()
            ident_key = ident.lower()

            if ident_key in local_vars or ident_key in _KNOWN_DAX_KEYWORDS:
                continue

            # If it's a measure, register dependency
            if ident_key in self.metric_map:
                if ident_key != curr_metric_name:
                    dep_graph.add_edge(curr_metric_name, ident_key)
                else:
                    # Self-reference cycle
                    dep_graph.add_edge(curr_metric_name, curr_metric_name)
                continue

            # Check if it's an attribute in current entity
            curr_cols = self.column_map.get(entity.name.lower(), {})
            if ident_key in curr_cols:
                continue

            # Check if it exists in any entity attribute
            found_anywhere = any(
                ident_key in cols for cols in self.column_map.values()
            )
            if not found_anywhere:
                ref_diags.append(
                    Diagnostic(
                        code="QUAL_DAX_REF_001",
                        severity=DiagnosticSeverity.ERROR,
                        category=DiagnosticCategory.QUALITY,
                        message=(
                            f"El símbolo o medida '{ident}' referenciado en '{entity.name}.{metric.name}' "
                            "no existe en el proyecto semántico ni en el alcance local."
                        ),
                        object_id=metric.id,
                        suggested_action="Verificar la definición de la medida o declarar la columna en la entidad.",
                        penalty=5.0,
                    )
                )

        # 3. Numeric Aggregation on Non-Numeric Types (QUAL_DAX_TYPE_001)
        agg_pattern = re.compile(
            r"\b(?P<fn>SUM|AVERAGE)\s*\(\s*(?:'(?P<tab_q>[^']+)'|(?P<tab_b>[a-zA-Z0-9_]+))?\[(?P<col>[^\]]+)\]",
            re.IGNORECASE,
        )
        non_numeric_types = {DataType.STRING, DataType.BOOLEAN, DataType.DATE, DataType.DATETIME}

        for match in agg_pattern.finditer(clean_expr):
            fn_name = match.group("fn").upper()
            tab_name = (match.group("tab_q") or match.group("tab_b") or entity.name).strip()
            col_name = match.group("col").strip()

            target_entity = self.entity_map.get(tab_name.lower())
            if target_entity:
                col_attr = self.column_map.get(tab_name.lower(), {}).get(col_name.lower())
                if col_attr and col_attr.data_type in non_numeric_types:
                    type_diags.append(
                        Diagnostic(
                            code="QUAL_DAX_TYPE_001",
                            severity=DiagnosticSeverity.ERROR,
                            category=DiagnosticCategory.QUALITY,
                            message=(
                                f"Agregación numérica {fn_name}() sobre la columna no numérica '{col_name}' "
                                f"de tipo '{col_attr.data_type.value}' en '{entity.name}.{metric.name}'."
                            ),
                            object_id=metric.id,
                            suggested_action="Utilizar funciones de agregación textuales (ej. CONCATENATEX) o convertir el tipo de dato a numérico.",
                            penalty=10.0,
                        )
                    )

        return ref_diags, type_diags
