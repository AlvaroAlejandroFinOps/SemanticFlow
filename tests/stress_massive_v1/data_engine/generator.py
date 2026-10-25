"""
Generador masivo de datasets sintéticos con estacionalidad para Retail Falabella (6 meses).
Produce archivos CSV locales con consistencia referencial estricta.
"""
import csv
from datetime import date, timedelta
from pathlib import Path
import random
from .faker_providers import (
    generate_rut,
    TIENDAS_FALABELLA,
    CATEGORIAS_FALABELLA,
    MARCAS_POR_DEPTO,
    CANALES_VENTA,
    PROMOCIONES,
)
from .seasonality import SeasonalityEngine

try:
    from faker import Faker
    fake = Faker("es_CL")
except Exception:
    fake = None


class FalabellaDataGenerator:
    """Genera 6 meses de datos sintéticos estacionales para Retail Falabella."""

    def __init__(self, output_dir: Path, num_clientes: int = 5000, num_productos: int = 500):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.num_clientes = num_clientes
        self.num_productos = num_productos
        self.seasonality = SeasonalityEngine()
        self.start_date = date(2025, 10, 1)  # 6 meses: Octubre 2025 a Marzo 2026
        self.num_days = 180

    def generate_all(self):
        """Orquesta la creación de todas las dimensiones y hechos."""
        print("[1/5] Generando dimensiones fijas y catálogos...")
        self._generate_dim_tiempo()
        self._generate_dim_canales()
        self._generate_dim_tiendas()
        self._generate_dim_categorias()
        self._generate_dim_promociones()
        self._generate_dim_vendedores()

        print("[2/5] Generando catálogo de productos y clientes CMR...")
        productos = self._generate_dim_productos()
        clientes = self._generate_dim_clientes()

        print("[3/5] Simulando 6 meses de ventas estacionales (Encabezados y Detalles)...")
        ventas_res = self._generate_fact_ventas(productos, clientes)

        print("[4/5] Simulando snapshots de inventario de cierre...")
        self._generate_fact_inventario(productos)

        print("[5/5] Generación completa de datos en CSV.")
        return ventas_res

    def _generate_dim_tiempo(self):
        csv_file = self.output_dir / "Dim_Tiempo.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Fecha_SK", "Fecha", "Dia", "Mes", "Año", "Trimestre", "Dia_Semana", "Es_Fin_Semana"])
            for i in range(self.num_days):
                curr = self.start_date + timedelta(days=i)
                fecha_sk = int(curr.strftime("%Y%m%d"))
                dia = curr.day
                mes = curr.month
                anio = curr.year
                trim = (mes - 1) // 3 + 1
                dia_sem = curr.weekday()
                es_finde = 1 if dia_sem in (5, 6) else 0
                writer.writerow([fecha_sk, curr.isoformat(), dia, mes, anio, trim, dia_sem, es_finde])

    def _generate_dim_canales(self):
        csv_file = self.output_dir / "Dim_Canal_Venta.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["SK_Canal", "Codigo_Canal", "Nombre_Canal", "Es_Digital"])
            for i, (cod, nom, dig) in enumerate(CANALES_VENTA, start=1):
                writer.writerow([i, cod, nom, dig])

    def _generate_dim_tiendas(self):
        csv_file = self.output_dir / "Dim_Tienda_Sucursal.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["SK_Tienda", "Codigo_Tienda", "Nombre_Tienda", "Region", "Comuna", "Metros_Cuadrados"])
            for i, (cod, nom, reg, com, m2) in enumerate(TIENDAS_FALABELLA, start=1):
                writer.writerow([i, cod, nom, reg, com, m2])

    def _generate_dim_categorias(self):
        csv_file = self.output_dir / "Dim_Categoria_Retail.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["SK_Categoria", "Codigo_Categoria", "Nombre_Categoria", "Departamento"])
            for i, (cod, nom, depto) in enumerate(CATEGORIAS_FALABELLA, start=1):
                writer.writerow([i, cod, nom, depto])

    def _generate_dim_promociones(self):
        csv_file = self.output_dir / "Dim_Promocion_Cyber.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["SK_Promocion", "Codigo_Promo", "Nombre_Promo", "Descuento_Pct", "Es_Cyber"])
            for i, (cod, nom, dcto, cyber) in enumerate(PROMOCIONES, start=1):
                writer.writerow([i, cod, nom, dcto, cyber])

    def _generate_dim_vendedores(self):
        csv_file = self.output_dir / "Dim_Vendedor.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["SK_Vendedor", "Codigo_Vendedor", "Nombre_Vendedor", "Sucursal_Base"])
            for i in range(1, 101):
                suc = random.choice(TIENDAS_FALABELLA)[1]
                nom = f"Vendedor {i:03d} Falabella"
                writer.writerow([i, f"VEND-{i:03d}", nom, suc])

    def _generate_dim_productos(self) -> list[dict]:
        productos = []
        csv_file = self.output_dir / "Dim_Producto_Falabella.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["SK_Producto", "SK_Categoria", "Codigo_SKU", "Nombre_Producto", "Marca", "Precio_Lista_CLP", "Costo_Reposicion_CLP"])
            
            for i in range(1, self.num_productos + 1):
                cat_idx = random.randint(1, len(CATEGORIAS_FALABELLA))
                cat_data = CATEGORIAS_FALABELLA[cat_idx - 1]
                depto = cat_data[2]
                marca = random.choice(MARCAS_POR_DEPTO.get(depto, ["Falabella Basics"]))
                sku = f"FAL-{cat_data[0][:7]}-{i:04d}"
                nom = f"{cat_data[1]} {marca} Mod-{i}"
                
                # Precios coherentes según departamento
                if depto == "Tecnología":
                    precio = random.choice([199990, 299990, 499990, 799990, 1199990])
                    costo = round(precio * random.uniform(0.65, 0.80), 0)
                elif depto in ("Moda", "Calzado"):
                    precio = random.choice([19990, 29990, 39990, 59990, 89990])
                    costo = round(precio * random.uniform(0.35, 0.50), 0)
                elif depto == "Hogar":
                    precio = random.choice([49990, 99990, 199990, 349990, 599990])
                    costo = round(precio * random.uniform(0.45, 0.60), 0)
                else:
                    precio = random.choice([14990, 24990, 49990, 79990])
                    costo = round(precio * random.uniform(0.40, 0.55), 0)

                writer.writerow([i, cat_idx, sku, nom, marca, precio, costo])
                productos.append({
                    "sk": i,
                    "cat": cat_idx,
                    "precio": precio,
                    "costo": costo,
                    "depto": depto,
                })
        return productos

    def _generate_dim_clientes(self) -> list[dict]:
        clientes = []
        csv_file = self.output_dir / "Dim_Cliente_CMR.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["SK_Cliente", "RUT", "Nombre_Completo", "Segmento_CMR", "Tiene_CMR", "Email"])
            
            segmentos = [("Elite", 1, 0.15), ("Premium", 1, 0.30), ("Puntos", 1, 0.35), ("Sin Tarjeta", 0, 0.20)]
            seg_choices = [s[0] for s in segmentos]
            seg_weights = [s[2] for s in segmentos]

            for i in range(1, self.num_clientes + 1):
                rut = generate_rut()
                seg = random.choices(seg_choices, weights=seg_weights, k=1)[0]
                tiene_cmr = 0 if seg == "Sin Tarjeta" else 1
                nom = f"Cliente {i:05d}"
                mail = f"cliente_{i}@falabella.cl"
                writer.writerow([i, rut, nom, seg, tiene_cmr, mail])
                clientes.append({"sk": i, "tiene_cmr": tiene_cmr, "seg": seg})
        return clientes

    def _generate_fact_ventas(self, productos: list[dict], clientes: list[dict]) -> dict:
        encabezado_file = self.output_dir / "Fact_Venta_Encabezado.csv"
        detalle_file = self.output_dir / "Fact_Venta_Detalle.csv"

        total_tx = 0
        total_items = 0
        venta_neta_global = 0.0

        with open(encabezado_file, mode="w", newline="", encoding="utf-8") as f_enc, \
             open(detalle_file, mode="w", newline="", encoding="utf-8") as f_det:

            w_enc = csv.writer(f_enc)
            w_det = csv.writer(f_det)

            w_enc.writerow([
                "ID_Venta", "Fecha_SK", "SK_Tienda", "SK_Canal", "SK_Cliente",
                "SK_Promocion", "SK_Vendedor", "Monto_Bruto_CLP", "Monto_Descuento_CLP",
                "Monto_Neto_CLP", "Es_CMR_Pago"
            ])

            w_det.writerow([
                "ID_Detalle", "ID_Venta", "SK_Producto", "Cantidad",
                "Precio_Unitario_CLP", "Costo_Unitario_CLP", "Subtotal_Bruto_CLP",
                "Descuento_Linea_CLP", "Subtotal_Neto_CLP", "Costo_Total_CLP",
                "Margen_Bruto_CLP"
            ])

            id_venta = 1
            id_detalle = 1

            for day_idx in range(self.num_days):
                curr_date = self.start_date + timedelta(days=day_idx)
                fecha_sk = int(curr_date.strftime("%Y%m%d"))

                # Base diaria de transacciones (~150 tx promedio por día para balancear tamaño/velocidad)
                for canal_id in [1, 2, 3, 4]:
                    is_digital = canal_id in (2, 3)
                    mult_tx, boost_dcto = self.seasonality.get_demand_multiplier(day_idx, curr_date, is_digital)
                    
                    # Cantidad de ventas en este canal hoy
                    base_canal = 50 if is_digital else 70
                    num_ventas = int(base_canal * mult_tx)

                    for _ in range(num_ventas):
                        tienda_id = random.randint(1, len(TIENDAS_FALABELLA))
                        cliente = random.choice(clientes)
                        vendedor_id = random.randint(1, 100) if not is_digital else 100

                        # Determinar si es Cyber o promoción
                        if 35 <= day_idx <= 37:
                            promo_id = 3 if random.random() < 0.70 else 4  # Promo Cyber
                            dcto_pct = 0.40 + boost_dcto
                        elif cliente["tiene_cmr"] and random.random() < 0.60:
                            promo_id = 2  # Promo CMR 20%
                            dcto_pct = 0.20
                        else:
                            promo_id = 1  # Sin Promo
                            dcto_pct = 0.0

                        es_cmr_pago = 1 if (cliente["tiene_cmr"] and random.random() < 0.85) else 0

                        # Generar entre 1 y 3 artículos en la boleta
                        num_articulos = random.choices([1, 2, 3], weights=[0.60, 0.30, 0.10], k=1)[0]
                        monto_bruto_boleta = 0.0
                        monto_dcto_boleta = 0.0
                        monto_neto_boleta = 0.0

                        for _ in range(num_articulos):
                            prod = random.choice(productos)
                            cant = random.choices([1, 2], weights=[0.85, 0.15], k=1)[0]
                            precio_u = prod["precio"]
                            costo_u = prod["costo"]

                            sub_bruto = cant * precio_u
                            dcto_linea = round(sub_bruto * dcto_pct, 0)
                            sub_neto = sub_bruto - dcto_linea
                            costo_total = cant * costo_u
                            margen_linea = sub_neto - costo_total

                            w_det.writerow([
                                id_detalle, id_venta, prod["sk"], cant,
                                precio_u, costo_u, sub_bruto, dcto_linea,
                                sub_neto, costo_total, margen_linea
                            ])

                            id_detalle += 1
                            total_items += 1
                            monto_bruto_boleta += sub_bruto
                            monto_dcto_boleta += dcto_linea
                            monto_neto_boleta += sub_neto

                        w_enc.writerow([
                            id_venta, fecha_sk, tienda_id, canal_id, cliente["sk"],
                            promo_id, vendedor_id, monto_bruto_boleta, monto_dcto_boleta,
                            monto_neto_boleta, es_cmr_pago
                        ])

                        venta_neta_global += monto_neto_boleta
                        id_venta += 1
                        total_tx += 1

        return {
            "total_transacciones": total_tx,
            "total_detalles": total_items,
            "venta_neta_clp": venta_neta_global,
        }

    def _generate_fact_inventario(self, productos: list[dict]):
        csv_file = self.output_dir / "Fact_Inventario_Cierre.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID_Inventario", "Fecha_SK", "SK_Tienda", "SK_Producto", "Stock_Unidades", "Valor_Inventario_CLP"])
            
            # Muestreo representativo de cierre mensual (6 cierres)
            id_inv = 1
            for m in [10, 11, 12, 1, 2, 3]:
                anio = 2025 if m >= 10 else 2026
                dia_cierre = 30 if m in (11,) else (28 if m == 2 else 31)
                fecha_sk = int(f"{anio}{m:02d}{dia_cierre:02d}")

                for tienda_id in range(1, len(TIENDAS_FALABELLA) + 1):
                    # Muestra de productos por tienda
                    for prod in productos[:50]:
                        stock = random.randint(5, 120)
                        valor = stock * prod["costo"]
                        writer.writerow([id_inv, fecha_sk, tienda_id, prod["sk"], stock, valor])
                        id_inv += 1
