import sys
from pathlib import Path
import time
from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.engine.compiler import SemanticCompiler
from src.core.emitter.pbip_writer import PbipWriter
from src.core.ast.semantic import TableRole

current_dir = Path(__file__).parent
data_engine_path = str(current_dir / "data_engine")
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from data_engine.generator import FalabellaDataGenerator


def test_massive_falabella_data_stress_pipeline():
    schema_path = Path("tests/Massive Data Stress/schemas/falabella_retail_schema.md")
    assert schema_path.exists(), "El esquema relacional de Falabella debe existir"

    data_dir = Path("tests/Massive Data Stress/data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generar los datos sintéticos de 6 meses (si no existen o para poblar)
    t0 = time.time()
    generator = FalabellaDataGenerator(output_dir=data_dir, num_clientes=2000, num_productos=200)
    data_metrics = generator.generate_all()
    t_gen = time.time() - t0

    # 2. Parsear el esquema relacional a AST
    t1 = time.time()
    parser = MarkdownSchemaParser()
    raw_schema = parser.parse(schema_path)
    raw_schema.name = "Falabella_Retail_Omnicanal"
    t_parse = time.time() - t1

    assert len(raw_schema.tables) == 11, f"Se esperaban 11 tablas, encontradas {len(raw_schema.tables)}"

    # 3. Compilar modelo semántico
    t2 = time.time()
    compiler = SemanticCompiler()
    semantic_model = compiler.compile(raw_schema, culture="es-CL")
    t_compile = time.time() - t2

    dim_count = sum(1 for t in semantic_model.tables if t.role == TableRole.DIMENSION)
    fact_count = sum(1 for t in semantic_model.tables if t.role == TableRole.FACT)
    assert dim_count == 8, f"Se esperaban 8 dimensiones, encontradas {dim_count}"
    assert fact_count == 3, f"Se esperaban 3 tablas de hechos, encontradas {fact_count}"

    # 4. Escribir bundle PBIP con particiones M conectadas a los CSVs locales
    t3 = time.time()
    output_dir = Path("output/SemanticFlow_Data/Falabella_Retail_PBIP")
    writer = PbipWriter()
    pbip_file = writer.write_bundle(semantic_model, output_dir, data_dir=data_dir)
    t_emit = time.time() - t3

    # 5. Validar existencia y consistencia de los artefactos PBIP
    assert pbip_file.exists()
    sem_model_dir = output_dir / f"{semantic_model.name}.SemanticModel"
    assert sem_model_dir.exists()
    assert (sem_model_dir / "definition.pbism").exists()

    def_dir = sem_model_dir / "definition"
    assert (def_dir / "database.tmdl").exists()
    assert (def_dir / "model.tmdl").exists()
    assert (def_dir / "relationships.tmdl").exists()

    # 6. Validar que las tablas TMDL contienen la partición M apuntando al CSV real
    tmdl_encabezado = (def_dir / "tables" / "Fact_Venta_Encabezado.tmdl").read_text(encoding="utf-8")
    assert 'Csv.Document(File.Contents(' in tmdl_encabezado, "Debe contener la función Csv.Document"
    assert 'Fact_Venta_Encabezado.csv' in tmdl_encabezado, "Debe referenciar el archivo CSV"
    assert 'Table.TransformColumnTypes' in tmdl_encabezado, "Debe tipar las columnas en Power Query"

    # Reporte
    print("\n" + "=" * 80)
    print("      FALABELLA RETAIL OMNICANAL - MASSIVE DATA STRESS RESULT REPORT       ")
    print("=" * 80)
    print(f"Período simulado:           6 Meses (Octubre 2025 - Marzo 2026, 180 días)")
    print(f"Total Transacciones (Boletas): {data_metrics['total_transacciones']:,}")
    print(f"Total Líneas de Detalle:       {data_metrics['total_detalles']:,}")
    print(f"Venta Neta Acumulada:          ${data_metrics['venta_neta_clp']:,.0f} CLP")
    print(f"Tablas del Modelo:             11 (8 Dimensiones, 3 Facts)")
    print(f"Relaciones 1:N Resueltas:      {len(semantic_model.relationships)}")
    print(f"Medidas DAX Sintetizadas:      {sum(len(t.measures) for t in semantic_model.tables)}")
    print("-" * 80)
    print(f"Tiempo Generación Datos:       {t_gen:.2f}s")
    print(f"Tiempo Compilación Semántica:  {(t_parse + t_compile + t_emit) * 1000:.2f} ms")
    print(f"Proyecto PBIP Listo en:        {pbip_file.resolve()}")
    print("=" * 80 + "\n")
