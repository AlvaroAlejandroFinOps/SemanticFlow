import sys
from pathlib import Path
import time

current_dir = Path(__file__).parent
project_root = r"D:\0001 HyperScale Thinking\PROYECTOS CLOUD\Data & AI Strategy\SemanticFlow"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from src.core.parsers.markdown_parser import MarkdownSchemaParser
from src.core.engine.compiler import SemanticCompiler
from src.core.emitter.pbip_writer import PbipWriter
from src.core.ast.semantic import TableRole
from data_engine.generator import MetroDataGenerator

def test_massive_metro_santiago_data_stress_v2_pipeline():
    schema_path = Path(project_root) / "docs" / "architecture" / "esquema_relacional.md"
    assert schema_path.exists(), f"El esquema relacional de Metro de Santiago debe existir en la arquitectura. Path: {schema_path}"

    data_dir = current_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generar los datos sintéticos de 6 meses (si no existen o para poblar)
    t0 = time.time()
    generator = MetroDataGenerator(output_dir=data_dir, scale_factor=1)
    generator.generate_all()
    t_gen = time.time() - t0

    # 2. Parsear el esquema relacional a AST
    t1 = time.time()
    parser = MarkdownSchemaParser()
    raw_schema = parser.parse(schema_path)
    raw_schema.name = "Metro_Santiago_Lakehouse_V2"
    t_parse = time.time() - t1

    assert len(raw_schema.tables) == 20, f"Se esperaban 20 tablas, encontradas {len(raw_schema.tables)}"

    # 3. Compilar modelo semántico
    t2 = time.time()
    compiler = SemanticCompiler()
    semantic_model = compiler.compile(raw_schema, culture="es-CL")
    t_compile = time.time() - t2

    dim_count = sum(1 for t in semantic_model.tables if t.role == TableRole.DIMENSION)
    fact_count = sum(1 for t in semantic_model.tables if t.role == TableRole.FACT)
    assert dim_count == 10, f"Se esperaban 10 dimensiones, encontradas {dim_count}"
    assert fact_count == 10, f"Se esperaban 10 tablas de hechos, encontradas {fact_count}"

    # 4. Escribir bundle PBIP con particiones M conectadas a los CSVs locales
    t3 = time.time()
    output_dir = Path(project_root) / "Artefactos" / "SemanticFlow_Data" / "Massive_Stress_v2_PBIP"
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

    # Reporte
    print("\n" + "=" * 80)
    print("   METRO DE SANTIAGO LAKEHOUSE V2 - MASSIVE DATA STRESS RESULT REPORT       ")
    print("=" * 80)
    print(f"Tablas del Modelo:             20 (10 Dimensiones, 10 Facts)")
    print(f"Relaciones 1:N Resueltas:      {len(semantic_model.relationships)}")
    print(f"Medidas DAX Sintetizadas:      {sum(len(t.measures) for t in semantic_model.tables)}")
    print("-" * 80)
    print(f"Tiempo Generación Datos:       {t_gen:.2f}s")
    print(f"Tiempo Compilación Semántica:  {(t_parse + t_compile + t_emit) * 1000:.2f} ms")
    print(f"Proyecto PBIP Listo en:        {pbip_file.resolve()}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    test_massive_metro_santiago_data_stress_v2_pipeline()
