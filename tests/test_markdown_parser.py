from pathlib import Path
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.ast.schema import KeyType


def test_parse_metro_santiago_markdown():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    assert schema_path.exists(), "El archivo de esquema relacional debe existir"

    parser = MarkdownSchemaParser()
    raw_schema = parser.parse(schema_path)

    # 1. Validar nombre de esquema
    assert raw_schema.name == "esquema_relacional"

    # 2. Validar que se hayan parseado las 20 tablas (10 Dim + 10 Fact)
    assert len(raw_schema.tables) == 20, f"Se esperaban 20 tablas, se encontraron {len(raw_schema.tables)}"

    dim_tables = [t for t in raw_schema.tables if t.name.startswith("Dim_")]
    fact_tables = [t for t in raw_schema.tables if t.name.startswith("Fact_")]
    assert len(dim_tables) == 10, f"Se esperaban 10 dimensiones, se encontraron {len(dim_tables)}"
    assert len(fact_tables) == 10, f"Se esperaban 10 facts, se encontraron {len(fact_tables)}"

    # 3. Validar columnas y claves de Dim_Linea
    dim_linea = raw_schema.get_table("Dim_Linea")
    assert dim_linea is not None
    assert len(dim_linea.columns) == 5
    sk_linea = dim_linea.get_column("SK_Linea")
    assert sk_linea is not None
    assert sk_linea.key_type == KeyType.PRIMARY
    assert sk_linea.raw_type == "int32"

    # 4. Validar columnas y claves foráneas de Fact_Validacion
    fact_val = raw_schema.get_table("Fact_Validacion")
    assert fact_val is not None
    assert len(fact_val.columns) == 7
    pk_val = fact_val.get_column("ID_Validacion")
    assert pk_val is not None
    assert pk_val.key_type == KeyType.PRIMARY
    fk_estacion = fact_val.get_column("SK_Estacion")
    assert fk_estacion is not None
    assert fk_estacion.is_foreign
    assert fk_estacion.foreign_target_table == "Dim_Estacion"
    assert fk_estacion.foreign_target_column == "SK_Estacion"

    # 5. Validar relaciones
    assert len(raw_schema.relationships) >= 20, f"Relaciones extraídas: {len(raw_schema.relationships)}"
