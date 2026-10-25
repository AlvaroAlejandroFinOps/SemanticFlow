import sys
from pathlib import Path
import pandas as pd

current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from data_engine.generator import FalabellaDataGenerator


def test_generate_and_validate_falabella_data(tmp_path):
    data_dir = tmp_path / "data"
    generator = FalabellaDataGenerator(output_dir=data_dir, num_clientes=1000, num_productos=150)
    metrics = generator.generate_all()

    # 1. Validar que se generaron ventas
    assert metrics["total_transacciones"] > 1000, f"Transacciones: {metrics['total_transacciones']}"
    assert metrics["total_detalles"] > metrics["total_transacciones"], "Debe haber más items que transacciones"
    assert metrics["venta_neta_clp"] > 0

    # 2. Validar existencia de archivos CSV
    expected_files = [
        "Dim_Tiempo.csv",
        "Dim_Canal_Venta.csv",
        "Dim_Tienda_Sucursal.csv",
        "Dim_Categoria_Retail.csv",
        "Dim_Producto_Falabella.csv",
        "Dim_Cliente_CMR.csv",
        "Dim_Promocion_Cyber.csv",
        "Dim_Vendedor.csv",
        "Fact_Venta_Encabezado.csv",
        "Fact_Venta_Detalle.csv",
        "Fact_Inventario_Cierre.csv",
    ]
    for filename in expected_files:
        assert (data_dir / filename).exists(), f"Falta archivo {filename}"

    # 3. Validar continuidad de Dim_Tiempo (180 días exactos)
    df_tiempo = pd.read_csv(data_dir / "Dim_Tiempo.csv")
    assert len(df_tiempo) == 180, f"Se esperaban 180 días, encontrados {len(df_tiempo)}"

    # 4. Validar integridad referencial
    df_clientes = pd.read_csv(data_dir / "Dim_Cliente_CMR.csv")
    df_tiendas = pd.read_csv(data_dir / "Dim_Tienda_Sucursal.csv")
    df_productos = pd.read_csv(data_dir / "Dim_Producto_Falabella.csv")
    df_encabezado = pd.read_csv(data_dir / "Fact_Venta_Encabezado.csv")
    df_detalle = pd.read_csv(data_dir / "Fact_Venta_Detalle.csv")

    # Clientes de ventas existen en Dim_Cliente
    assert set(df_encabezado["SK_Cliente"]).issubset(set(df_clientes["SK_Cliente"]))
    # Tiendas de ventas existen en Dim_Tienda
    assert set(df_encabezado["SK_Tienda"]).issubset(set(df_tiendas["SK_Tienda"]))
    # Productos de detalles existen en Dim_Producto
    assert set(df_detalle["SK_Producto"]).issubset(set(df_productos["SK_Producto"]))
    # ID_Venta de detalles existen en Fact_Venta_Encabezado
    assert set(df_detalle["ID_Venta"]).issubset(set(df_encabezado["ID_Venta"]))

    # 5. Validar consistencia matemática contable (Suma Detalle == Encabezado)
    detalle_agregado = df_detalle.groupby("ID_Venta")["Subtotal_Neto_CLP"].sum().reset_index()
    merged = pd.merge(df_encabezado[["ID_Venta", "Monto_Neto_CLP"]], detalle_agregado, on="ID_Venta")
    # Tolerancia por redondeos
    diff = (merged["Monto_Neto_CLP"] - merged["Subtotal_Neto_CLP"]).abs()
    assert (diff < 1.0).all(), f"Discrepancia contable detectada entre encabezado y detalle: {diff.max()}"

    # 6. Validar impacto del CyberDay
    # CyberDay ocurre días 35-37 (fecha min + 35 días a fecha min + 37 días)
    fechas_cyber = df_tiempo.iloc[35:38]["Fecha_SK"].tolist()
    ventas_cyber_digital = df_encabezado[(df_encabezado["Fecha_SK"].isin(fechas_cyber)) & (df_encabezado["SK_Canal"].isin([2, 3]))]
    ventas_normal_digital = df_encabezado[(~df_encabezado["Fecha_SK"].isin(fechas_cyber)) & (df_encabezado["SK_Canal"].isin([2, 3]))]

    prom_cyber_diario = len(ventas_cyber_digital) / 3.0
    prom_normal_diario = len(ventas_normal_digital) / 177.0
    assert prom_cyber_diario > prom_normal_diario * 2.5, "El CyberDay debe mostrar un pico digital superior a 2.5x"
