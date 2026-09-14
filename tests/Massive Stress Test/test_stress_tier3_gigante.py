from pathlib import Path
import tempfile
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.engine.compiler import SemanticCompiler
from src.core.emitter.pbip_writer import PbipWriter
from src.core.ast.semantic import TableRole


def get_tier3_schemas():
    base_path = Path("tests/Massive Stress Test/schemas/tier3_gigante")
    return list(base_path.glob("*.md"))


def test_tier3_schemas_exist():
    schemas = get_tier3_schemas()
    assert len(schemas) == 4, f"Se esperaban 4 esquemas en Tier 3, se encontraron {len(schemas)}"


def test_compile_tier3_gigantes():
    schemas = get_tier3_schemas()
    parser = MarkdownSchemaParser()
    compiler = SemanticCompiler()
    writer = PbipWriter()

    for schema_file in schemas:
        raw_schema = parser.parse(schema_file)
        assert len(raw_schema.tables) >= 14, f"Esquema {schema_file.name} debe tener al menos 14 tablas"

        semantic_model = compiler.compile(raw_schema)
        assert len(semantic_model.tables) == len(raw_schema.tables)

        dim_count = sum(1 for t in semantic_model.tables if t.role == TableRole.DIMENSION)
        fact_count = sum(1 for t in semantic_model.tables if t.role == TableRole.FACT)
        assert dim_count >= 6, f"Esquema {schema_file.name} requiere al menos 6 dimensiones"
        assert fact_count >= 6, f"Esquema {schema_file.name} requiere al menos 6 tablas de hechos"

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_path = Path(tmp_dir) / "output"
            pbip_file = writer.write_bundle(semantic_model, out_path)
            assert pbip_file.exists()
            assert (out_path / f"{semantic_model.name}.SemanticModel" / "definition" / "database.tmdl").exists()
