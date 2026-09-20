"""
Escritor del paquete PBIP nativo y orquestador de archivos TMDL en disco.
"""
import json
import shutil
from pathlib import Path
from typing import Optional

from src.core.ast.semantic import SemanticModel
from src.core.emitter.model_emitter import ModelEmitter
from src.core.emitter.relationship_emitter import RelationshipEmitter
from src.core.emitter.table_emitter import TableEmitter


class PbipWriter:
    """Escribe un proyecto Power BI (PBIP) completo con definición TMDL de manera atómica y segura."""

    def __init__(self):
        self.table_emitter = TableEmitter()
        self.rel_emitter = RelationshipEmitter()
        self.model_emitter = ModelEmitter()

    def write_bundle(
        self,
        model: SemanticModel,
        target_dir: Path,
        data_dir: Optional[Path] = None,
    ) -> Path:
        """
        Compila y escribe el árbol de directorios PBIP / TMDL en target_dir de forma atómica.
        Retorna la ruta al archivo .pbip generado.
        """
        import tempfile

        target_path = Path(target_dir).resolve()

        # Validación de seguridad: no permitir escribir directamente en raíces de sistema
        if target_path.parent == target_path or str(target_path) in ("/", "\\", "C:\\", "D:\\"):
            raise ValueError(f"Target directory '{target_path}' is a protected root path and cannot be overwritten.")

        sanitized_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in model.name)

        # Usar directorio temporal para garantizar atomicidad ante fallos
        with tempfile.TemporaryDirectory(prefix="semanticflow_stage_") as tmp_stage:
            stage_dir = Path(tmp_stage)

            # 1. Archivo raíz .pbip
            pbip_file = stage_dir / f"{sanitized_name}.pbip"
            pbip_content = {
                "version": "1.0",
                "artifacts": [
                    {
                        "report": {
                            "path": f"{sanitized_name}.Report"
                        }
                    }
                ],
                "settings": {
                    "enableAutoRecovery": True
                }
            }
            pbip_file.write_text(json.dumps(pbip_content, indent=2), encoding="utf-8")

            # 2. Directorio Report
            report_dir = stage_dir / f"{sanitized_name}.Report"
            report_dir.mkdir(parents=True, exist_ok=True)
            pbir_file = report_dir / "definition.pbir"
            pbir_content = {
                "version": "4.0",
                "datasetReference": {
                    "byPath": {
                        "path": f"../{sanitized_name}.SemanticModel"
                    },
                    "byConnection": None
                }
            }
            pbir_file.write_text(json.dumps(pbir_content, indent=2), encoding="utf-8")

            # 2.1. Definición completa del Reporte (PBIR)
            report_def_dir = report_dir / "definition"
            report_def_dir.mkdir(parents=True, exist_ok=True)

            report_json = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.2.0/schema.json",
                "activeSectionName": "ReportSection"
            }
            (report_def_dir / "report.json").write_text(json.dumps(report_json, indent=2), encoding="utf-8")

            version_json = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
                "version": "2.0.0"
            }
            (report_def_dir / "version.json").write_text(json.dumps(version_json, indent=2), encoding="utf-8")

            pages_dir = report_def_dir / "pages"
            pages_dir.mkdir(parents=True, exist_ok=True)
            pages_json = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
                "pageOrder": ["ReportSection"],
                "activePageName": "ReportSection"
            }
            (pages_dir / "pages.json").write_text(json.dumps(pages_json, indent=2), encoding="utf-8")

            page1_dir = pages_dir / "ReportSection"
            page1_dir.mkdir(parents=True, exist_ok=True)
            page1_json = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.2.0/schema.json",
                "name": "ReportSection",
                "displayName": "Página 1",
                "displayOption": "FitToPage",
                "height": 720,
                "width": 1280
            }
            (page1_dir / "page.json").write_text(json.dumps(page1_json, indent=2), encoding="utf-8")

            # 3. Directorio SemanticModel
            sem_model_dir = stage_dir / f"{sanitized_name}.SemanticModel"
            sem_model_dir.mkdir(parents=True, exist_ok=True)

            pbism_content = {
                "version": "4.0",
                "settings": {}
            }
            (sem_model_dir / "definition.pbism").write_text(json.dumps(pbism_content, indent=2), encoding="utf-8")

            # 3.1. definition/
            def_dir = sem_model_dir / "definition"
            def_dir.mkdir(parents=True, exist_ok=True)

            # database.tmdl
            db_content = self.model_emitter.emit_database(model)
            (def_dir / "database.tmdl").write_text(db_content, encoding="utf-8")

            # model.tmdl
            model_content = self.model_emitter.emit_model(model)
            (def_dir / "model.tmdl").write_text(model_content, encoding="utf-8")

            # relationships.tmdl
            rel_content = self.rel_emitter.emit_relationships(model.relationships)
            if rel_content:
                (def_dir / "relationships.tmdl").write_text(rel_content, encoding="utf-8")

            # cultures/<culture>.tmdl
            cult_dir = def_dir / "cultures"
            cult_dir.mkdir(parents=True, exist_ok=True)
            cult_content = self.model_emitter.emit_culture(model.culture)
            (cult_dir / f"{model.culture}.tmdl").write_text(cult_content, encoding="utf-8")

            # tables/<Table>.tmdl
            tables_dir = def_dir / "tables"
            tables_dir.mkdir(parents=True, exist_ok=True)
            for table in model.tables:
                data_file = None
                if data_dir and (data_dir / f"{table.name}.csv").exists():
                    data_file = data_dir / f"{table.name}.csv"
                table_content = self.table_emitter.emit_table(table, data_file_path=data_file)
                (tables_dir / f"{table.name}.tmdl").write_text(table_content, encoding="utf-8")

            # Paso final atómico: transferir desde stage al target_dir final
            target_path.mkdir(parents=True, exist_ok=True)
            shutil.copytree(stage_dir, target_path, dirs_exist_ok=True)

        return target_path / f"{sanitized_name}.pbip"

