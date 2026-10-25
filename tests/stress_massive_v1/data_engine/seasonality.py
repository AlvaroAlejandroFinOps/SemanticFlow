"""
Motor matemático de estacionalidad y shocks de demanda para retail chileno.
"""
from datetime import date


class SeasonalityEngine:
    """Calcula multiplicadores de volumen y ticket según fecha y canal."""

    def get_demand_multiplier(self, day_index: int, dt: date, is_digital: bool) -> tuple[float, float]:
        """
        Retorna (multiplicador_transacciones, multiplicador_descuento).
        day_index: 0 a 179 (días desde el inicio de los 6 meses).
        """
        # 1. Factor día de la semana (Lunes=0, Domingo=6)
        weekday = dt.weekday()
        if is_digital:
            # En digital, compras se distribuyen más parejas, con picos jueves-domingo
            weekday_mult = 1.25 if weekday in (3, 4, 6) else 0.90
        else:
            # En tiendas físicas, el sábado y domingo explotan
            if weekday == 5:  # Sábado
                weekday_mult = 1.75
            elif weekday == 6:  # Domingo
                weekday_mult = 1.45
            elif weekday == 4:  # Viernes
                weekday_mult = 1.25
            else:
                weekday_mult = 0.80

        # 2. Factor Quincena / Pago de Sueldos (Días 1-5 y 15-18)
        day_of_month = dt.day
        if 1 <= day_of_month <= 5 or 15 <= day_of_month <= 18:
            payday_mult = 1.35
        else:
            payday_mult = 1.0

        # 3. Shocks y Campañas Masivas
        event_mult = 1.0
        discount_boost = 0.0

        # Evento A: CyberDay Falabella (Días 35 a 37 del periodo de 6 meses)
        if 35 <= day_index <= 37:
            if is_digital:
                event_mult = 4.8  # Boom digital 4.8x
                discount_boost = 0.25
            else:
                event_mult = 0.85  # Tienda física baja ligeramente

        # Evento B: Campaña Navideña (Días 75 a 85)
        elif 75 <= day_index <= 85:
            # Intensidad creciente hasta el día 84 (24 Dic)
            climax = 1.0 + (day_index - 74) * 0.15
            event_mult = 2.4 * climax
            discount_boost = 0.10

        # Evento C: Gran Liquidación Verano Falabella (Días 110 a 120)
        elif 110 <= day_index <= 120:
            event_mult = 1.4
            discount_boost = 0.20

        total_tx_mult = weekday_mult * payday_mult * event_mult
        return total_tx_mult, discount_boost
