from src.core.ast.schema import KeyType
from src.core.parsers.yaml_parser import YamlSchemaParser


def test_yaml_parser():
    sample_yaml = """
    name: SampleLakehouse
    description: Modelo de prueba en YAML
    tables:
      - name: Dim_Cliente
        description: Catalogo de clientes
        columns:
          - name: SK_Cliente
            type: int64
            key_type: PRIMARY
          - name: Nombre
            type: string
      - name: Fact_Ventas
        description: Ventas registradas
        columns:
          - name: ID_Venta
            type: int64
            key_type: PRIMARY
          - name: SK_Cliente
            type: int64
            key_type: FOREIGN
          - name: Monto_CLP
            type: float64
    relationships:
      - from_table: Fact_Ventas
        from_column: SK_Cliente
        to_table: Dim_Cliente
        to_column: SK_Cliente
    """
    parser = YamlSchemaParser()
    raw_schema = parser.parse(sample_yaml)

    assert raw_schema.name == "SampleLakehouse"
    assert len(raw_schema.tables) == 2
    dim_cli = raw_schema.get_table("Dim_Cliente")
    assert dim_cli is not None
    assert dim_cli.columns[0].key_type == KeyType.PRIMARY

    fact_v = raw_schema.get_table("Fact_Ventas")
    assert fact_v is not None
    assert len(raw_schema.relationships) == 1
