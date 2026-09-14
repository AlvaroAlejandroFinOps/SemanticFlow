import csv
from datetime import date, timedelta
from pathlib import Path
import random

try:
    from faker import Faker
    fake = Faker("es_CL")
except Exception:
    fake = None


class MetroDataGenerator:
    """Genera 6 meses de datos sintéticos estacionales para Metro de Santiago (Lakehouse)."""

    def __init__(self, output_dir: Path, scale_factor: int = 1):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scale_factor = scale_factor
        self.start_date = date(2025, 10, 1)  # 6 meses
        self.num_days = 180
        
        self.lineas = [
            (1, "L1", "Rojo", "CBTC", 19.3),
            (2, "L2", "Amarillo", "ASFA", 20.7),
            (3, "L3", "Cafe", "CBTC-UTO", 21.7),
            (4, "L4", "Azul", "ASFA", 24.7),
            (5, "L4A", "Celeste", "ASFA", 4.6),
            (6, "L5", "Verde", "ASFA", 30.0),
            (7, "L6", "Morado", "CBTC-UTO", 15.3),
        ]

    def generate_all(self):
        print("[1/5] Generando Dimensiones Maestras...")
        self._generate_dim_tiempo()
        self._generate_dim_linea()
        estaciones = self._generate_dim_estacion()
        trenes = self._generate_dim_tren_coche()
        usuarios = self._generate_dim_usuario_bip()
        equipos = self._generate_dim_equipamiento(estaciones, trenes)
        unidades = self._generate_dim_unidad_negocio()
        espacios = self._generate_dim_espacio_comercial(estaciones)
        self._generate_dim_proyecto_expansion()
        self._generate_dim_organizacion_esg()

        print("[2/5] Generando Hechos Operacionales Diarios (Validaciones, Flujo)...")
        self._generate_fact_validacion(estaciones, usuarios)
        self._generate_fact_simulacion_flujo(estaciones)
        
        print("[3/5] Generando Hechos Comerciales y Telemetría...")
        self._generate_fact_venta_carga(estaciones, usuarios)
        self._generate_fact_telemetria_tren(trenes)
        self._generate_fact_sensoraje_via()

        print("[4/5] Generando Hechos Agregados Mensuales (Resultados, ESG, Oferta, Seguridad)...")
        self._generate_fact_estado_resultado(unidades)
        self._generate_fact_ingresos_nnt(unidades)
        self._generate_fact_consumo_esg()
        self._generate_fact_cumplimiento_oferta()
        self._generate_fact_seguridad_nps()

        print("[5/5] Generación masiva finalizada.")
        
        return {"status": "success", "scale_factor": self.scale_factor}

    def _generate_dim_tiempo(self):
        with open(self.output_dir / "Dim_Tiempo.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Fecha_SK", "Fecha", "Dia", "Mes", "Año", "Dia_Semana", "Es_Fin_Semana"])
            for i in range(self.num_days):
                curr = self.start_date + timedelta(days=i)
                w.writerow([
                    int(curr.strftime("%Y%m%d")), curr.isoformat(), curr.day, curr.month, curr.year,
                    curr.weekday(), 1 if curr.weekday() >= 5 else 0
                ])

    def _generate_dim_linea(self):
        with open(self.output_dir / "Dim_Linea.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Linea", "Codigo_Linea", "Color", "Tecnologia", "Longitud_Km"])
            for l in self.lineas:
                w.writerow(l)

    def _generate_dim_estacion(self):
        estaciones = []
        with open(self.output_dir / "Dim_Estacion.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Estacion", "SK_Linea", "Codigo_Estacion", "Nombre_Estacion", "Comuna", "Tipo_Estacion", "Es_Combinacion"])
            sk = 1
            for sk_linea, cod_l, _, _, _ in self.lineas:
                for i in range(1, 15):
                    nom = f"Estacion_{cod_l}_{i}"
                    est = [sk, sk_linea, f"EST-{cod_l}-{i:02d}", nom, "Santiago", random.choice(["Subterránea", "Viaducto"]), random.choice([0, 1])]
                    w.writerow(est)
                    estaciones.append(sk)
                    sk += 1
        return estaciones

    def _generate_dim_tren_coche(self):
        trenes = []
        with open(self.output_dir / "Dim_Tren_Coche.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Tren", "SK_Linea", "ID_Formacion", "Modelo", "Cant_Coches", "Capacidad_Pax"])
            sk = 1
            for sk_linea, _, _, _, _ in self.lineas:
                for i in range(1, 10):
                    tr = [sk, sk_linea, f"TRN-{sk_linea}-{i:03d}", random.choice(["NS-74", "NS-93", "AS-14"]), random.choice([5, 6, 7]), random.randint(1200, 1500)]
                    w.writerow(tr)
                    trenes.append(sk)
                    sk += 1
        return trenes

    def _generate_dim_usuario_bip(self):
        usuarios = []
        with open(self.output_dir / "Dim_Usuario_Bip.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Usuario", "Numero_Tarjeta_Bip", "Tipo_Usuario"])
            for i in range(1, 1000 * self.scale_factor + 1):
                u = [i, random.randint(10000000, 99999999), random.choice(["Adulto", "Estudiante_TNE", "Adulto_Mayor"])]
                w.writerow(u)
                usuarios.append(i)
        return usuarios

    def _generate_dim_equipamiento(self, estaciones, trenes):
        equipos = []
        with open(self.output_dir / "Dim_Equipamiento.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Equipo", "SK_Tren", "SK_Estacion", "Sistema", "Criticidad"])
            sk = 1
            for tr in trenes[:50]:
                w.writerow([sk, tr, -1, "Tracción", "Alta"])
                equipos.append(sk)
                sk += 1
            for est in estaciones[:50]:
                w.writerow([sk, -1, est, "Escaleras Mecánicas", "Media"])
                equipos.append(sk)
                sk += 1
        return equipos

    def _generate_dim_unidad_negocio(self):
        unidades = [1, 2]
        with open(self.output_dir / "Dim_Unidad_Negocio.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Unidad", "Nombre"])
            w.writerow([1, "Transporte Pasajeros"])
            w.writerow([2, "Negocios No Tarifarios"])
        return unidades

    def _generate_dim_espacio_comercial(self, estaciones):
        espacios = []
        with open(self.output_dir / "Dim_Espacio_Comercial.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Espacio", "SK_Estacion", "Tipo"])
            sk = 1
            for est in estaciones:
                if random.random() < 0.3:
                    w.writerow([sk, est, "Local Comercial"])
                    espacios.append(sk)
                    sk += 1
        return espacios

    def _generate_dim_proyecto_expansion(self):
        with open(self.output_dir / "Dim_Proyecto_Expansion.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Proyecto", "Nombre", "Presupuesto_USD"])
            w.writerow([1, "Línea 7", 2500.0])

    def _generate_dim_organizacion_esg(self):
        with open(self.output_dir / "Dim_Organizacion_ESG.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["SK_Iniciativa", "Categoria", "Meta"])
            w.writerow([1, "Energía Renovable", "100% ERNC 2025"])

    # FACTS (Samples heavily reduced for testing speed, controlled by scale_factor)
    def _generate_fact_validacion(self, estaciones, usuarios):
        with open(self.output_dir / "Fact_Validacion.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID_Validacion", "Fecha_SK", "Segundo_Dia", "SK_Estacion", "SK_Usuario", "Tarifa_Cobrada_CLP", "Canal_Validacion"])
            id_v = 1
            for i in range(self.num_days):
                fecha = int((self.start_date + timedelta(days=i)).strftime("%Y%m%d"))
                for _ in range(500 * self.scale_factor):
                    w.writerow([id_v, fecha, random.randint(0, 86399), random.choice(estaciones), random.choice(usuarios), random.choice([0, 240, 730, 830]), random.choice(["Torniquete Físico", "QR"])])
                    id_v += 1

    def _generate_fact_simulacion_flujo(self, estaciones):
        with open(self.output_dir / "Fact_Simulacion_Flujo.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID_Agente_Flujo", "Fecha_SK", "Segundo_Dia", "SK_Estacion", "Posicion_X", "Posicion_Y", "Estado"])
            id_a = 1
            for i in range(self.num_days):
                fecha = int((self.start_date + timedelta(days=i)).strftime("%Y%m%d"))
                for _ in range(50 * self.scale_factor):
                    w.writerow([id_a, fecha, random.randint(0, 86399), random.choice(estaciones), random.uniform(0, 100), random.uniform(0, 100), random.choice(["Esperando Tren", "Transito Pasillo"])])
                    id_a += 1

    def _generate_fact_venta_carga(self, estaciones, usuarios):
        with open(self.output_dir / "Fact_Venta_Carga.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID_Venta_Carga", "Fecha_SK", "SK_Estacion", "SK_Usuario", "Monto_Carga_CLP", "Metodo_Pago"])
            id_vc = 1
            for i in range(self.num_days):
                fecha = int((self.start_date + timedelta(days=i)).strftime("%Y%m%d"))
                for _ in range(100 * self.scale_factor):
                    w.writerow([id_vc, fecha, random.choice(estaciones), random.choice(usuarios), random.choice([1000, 2000, 5000]), random.choice(["Efectivo", "Débito"])])
                    id_vc += 1

    def _generate_fact_telemetria_tren(self, trenes):
        with open(self.output_dir / "Fact_Telemetria_Tren.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID_Log", "Fecha_SK", "Segundo_Dia", "SK_Tren", "Velocidad_KmH", "Temp_Motor_C", "Voltaje_Linea_V", "Estado_ATP"])
            id_log = 1
            for i in range(self.num_days):
                fecha = int((self.start_date + timedelta(days=i)).strftime("%Y%m%d"))
                for _ in range(50 * self.scale_factor):
                    w.writerow([id_log, fecha, random.randint(0, 86399), random.choice(trenes), random.uniform(0, 80), random.uniform(60, 90), 750.0, 1])
                    id_log += 1

    def _generate_fact_sensoraje_via(self):
        with open(self.output_dir / "Fact_Sensoraje_Via.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID_Sensoraje", "Fecha_SK", "SK_Linea", "Vibracion_RMS_G", "Desgaste_Riel_mm", "Temp_Riel_C"])
            id_sens = 1
            for i in range(self.num_days):
                fecha = int((self.start_date + timedelta(days=i)).strftime("%Y%m%d"))
                for sk_l, _, _, _, _ in self.lineas:
                    w.writerow([id_sens, fecha, sk_l, random.uniform(0.1, 0.5), random.uniform(0.01, 0.1), random.uniform(15, 35)])
                    id_sens += 1

    # Hechos Mensuales (Iteran sobre 6 meses)
    def _generate_mensual(self, file_name, headers, row_generator):
        with open(self.output_dir / file_name, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            for m in [10, 11, 12, 1, 2, 3]:
                anio = 2025 if m >= 10 else 2026
                sk_periodo = int(f"{anio}{m:02d}")
                for sk_l, _, _, _, _ in self.lineas:
                    row_generator(w, sk_periodo, sk_l)

    def _generate_fact_estado_resultado(self, unidades):
        def row_gen(w, sk_p, sk_l):
            for u in unidades:
                w.writerow([sk_p, sk_l, u, random.uniform(1e8, 5e8), random.uniform(1e7, 5e7), random.uniform(8e7, 4e8), random.uniform(1e7, 1e8)])
        self._generate_mensual("Fact_Estado_Resultado.csv", ["SK_Periodo", "SK_Linea", "SK_Unidad", "Ingresos_Tarifarios_CLP", "Ingresos_NNT_CLP", "Costos_Operacionales_CLP", "EBITDA_CLP"], row_gen)

    def _generate_fact_ingresos_nnt(self, unidades):
        def row_gen(w, sk_p, sk_l):
            w.writerow([sk_p, sk_l, 2, random.uniform(1e6, 5e6), random.uniform(1e6, 5e6), random.uniform(1e5, 5e5)])
        self._generate_mensual("Fact_Ingresos_NNT.csv", ["SK_Periodo", "SK_Linea", "SK_Unidad", "Ingreso_Arriendos_Comerciales_CLP", "Ingreso_Publicidad_CLP", "Ingreso_Cajeros_Telecom_CLP"], row_gen)

    def _generate_fact_consumo_esg(self):
        def row_gen(w, sk_p, sk_l):
            w.writerow([sk_p, sk_l, random.uniform(1e5, 5e5), random.uniform(1.0, 5.0), random.uniform(1000, 5000), random.uniform(50000, 100000)])
        self._generate_mensual("Fact_Consumo_ESG.csv", ["SK_Periodo", "SK_Linea", "Consumo_Traccion_KWh", "Indicador_KWh_CKm", "Ahorro_Emisiones_CO2_Ton", "Horas_Ahorradas_Viajeros"], row_gen)

    def _generate_fact_cumplimiento_oferta(self):
        def row_gen(w, sk_p, sk_l):
            w.writerow([sk_p, sk_l, random.uniform(0.9, 0.99), random.uniform(10000, 50000), random.uniform(0.7, 0.95), random.randint(0, 10)])
        self._generate_mensual("Fact_Cumplimiento_Oferta.csv", ["SK_Periodo", "SK_Linea", "Cumplimiento_Frecuencia_Pct", "MKBF_Km", "Factor_Ocupacion_Pct", "Demanda_Buses_Respaldo"], row_gen)

    def _generate_fact_seguridad_nps(self):
        def row_gen(w, sk_p, sk_l):
            w.writerow([sk_p, sk_l, random.uniform(30, 80), random.uniform(0.1, 1.5), random.randint(0, 50)])
        self._generate_mensual("Fact_Seguridad_NPS.csv", ["SK_Periodo", "SK_Linea", "NPS_Satisfaccion", "Tasa_Delitos_MillonPax", "Eventos_Seguridad_Averias"], row_gen)

if __name__ == "__main__":
    out = Path(__file__).parent.parent / "data"
    g = MetroDataGenerator(output_dir=out)
    g.generate_all()
