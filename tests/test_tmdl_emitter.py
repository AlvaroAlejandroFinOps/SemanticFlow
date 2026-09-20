import json
import tempfile
from pathlib import Path

from src.core.emitter.pbip_writer import PbipWriter
from src.core.engine.compiler import SemanticCompiler
from src.core.parsers.markdown_parser import MarkdownSchemaParser


def test_tmdl_pbip_emission_metro_santiago():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    raw_schema = MarkdownSchemaParser().parse(schema_path)
    semantic_model = SemanticCompiler().compile(raw_schema)

    with tempfile.TemporaryDirectory() as tmp_dir:
        target_path = Path(tmp_dir) / "output"
        writer = PbipWriter()
        pbip_file = writer.write_bundle(semantic_model, target_path)

        # 1. Validar existencia del .pbip
        assert pbip_file.exists()
        pbip_data = json.loads(pbip_file.read_text(encoding="utf-8"))
        assert pbip_data["version"] == "1.0"
        assert pbip_data["artifacts"][0]["report"]["path"] == "esquema_relacional.Report"

        # 2. Validar estructura del Report y SemanticModel
        report_dir = target_path / "esquema_relacional.Report"
        assert report_dir.exists()
        assert (report_dir / "definition.pbir").exists()

        sem_model_dir = target_path / "esquema_relacional.SemanticModel"
        assert sem_model_dir.exists()
        assert (sem_model_dir / "definition.pbism").exists()

        def_dir = sem_model_dir / "definition"
        assert (def_dir / "database.tmdl").exists()
        assert (def_dir / "model.tmdl").exists()
        assert (def_dir / "relationships.tmdl").exists()
        assert (def_dir / "cultures" / "es-CL.tmdl").exists()

        # 3. Validar contenido de database.tmdl
        db_content = (def_dir / "database.tmdl").read_text(encoding="utf-8")
        assert "database esquema_relacional" in db_content
        assert "\tcompatibilityLevel: 1567" in db_content

        # 4. Validar tablas emitidas
        tables_dir = def_dir / "tables"
        assert tables_dir.exists()
        table_files = list(tables_dir.glob("*.tmdl"))
        assert len(table_files) == 20

        # Validar Dim_Linea.tmdl
        dim_linea_content = (tables_dir / "Dim_Linea.tmdl").read_text(encoding="utf-8")
        assert "table Dim_Linea" in dim_linea_content
        assert "\tcolumn SK_Linea" in dim_linea_content
        assert "\t\tdataType: int64" in dim_linea_content
        assert "\t\tisHidden" in dim_linea_content
        assert "\tpartition Dim_Linea = m" in dim_linea_content

        # Validar Fact_Validacion.tmdl
        fact_val_content = (tables_dir / "Fact_Validacion.tmdl").read_text(encoding="utf-8")
        assert "table Fact_Validacion" in fact_val_content
        assert "\tmeasure '# Registros Validacion' = COUNTROWS('Fact_Validacion')" in fact_val_content
        assert "\tcolumn SK_Estacion" in fact_val_content
        assert "\t\tisHidden" in fact_val_content

        # Validar relationships.tmdl
        rel_content = (def_dir / "relationships.tmdl").read_text(encoding="utf-8")
        assert "relationship AutoRel_Fact_Validacion_SK_Estacion_Dim_Estacion_SK_Estacion" in rel_content
        assert "\tfromColumn: Fact_Validacion.SK_Estacion" in rel_content
        assert "\ttoColumn: Dim_Estacion.SK_Estacion" in rel_content
