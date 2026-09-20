from pathlib import Path

from typer.testing import CliRunner

from src.cli import app

runner = CliRunner()


def test_cli_inspect():
    schema_path = Path("docs/architecture/esquema_relacional.md")
    result = runner.invoke(app, ["inspect", "--input", str(schema_path)])
    assert result.exit_code == 0
    assert "Dim_Linea" in result.output
    assert "Fact_Validacion" in result.output
    assert "DIMENSION" in result.output
    assert "FACT" in result.output


def test_cli_compile(tmp_path):
    schema_path = Path("docs/architecture/esquema_relacional.md")
    out_dir = tmp_path / "pbi_out"
    result = runner.invoke(
        app,
        [
            "compile",
            "--input",
            str(schema_path),
            "--output",
            str(out_dir),
            "--name",
            "Test_Metro",
        ],
    )
    assert result.exit_code == 0
    pbip_file = out_dir / "Test_Metro.pbip"
    assert pbip_file.exists()
    assert (out_dir / "Test_Metro.SemanticModel" / "definition" / "database.tmdl").exists()
