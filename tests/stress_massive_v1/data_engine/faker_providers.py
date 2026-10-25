"""
Proveedores de datos sintéticos especializados en Retail Chileno / Falabella.
"""
import random


def generate_rut() -> str:
    """Genera un RUT chileno sintético válido con dígito verificador."""
    num = random.randint(5000000, 25000000)
    # Cálculo DV Módulo 11
    digits = [int(d) for d in str(num)][::-1]
    factors = [2, 3, 4, 5, 6, 7]
    total = sum(d * factors[i % len(factors)] for i, d in enumerate(digits))
    remainder = 11 - (total % 11)
    if remainder == 11:
        dv = "0"
    elif remainder == 10:
        dv = "K"
    else:
        dv = str(remainder)
    return f"{num}-{dv}"


TIENDAS_FALABELLA = [
    ("SUC-001", "Falabella Parque Arauco", "Metropolitana", "Las Condes", 18500.0),
    ("SUC-002", "Falabella Costanera Center", "Metropolitana", "Providencia", 22000.0),
    ("SUC-003", "Falabella Alto Las Condes", "Metropolitana", "Las Condes", 15200.0),
    ("SUC-004", "Falabella Plaza Vespucio", "Metropolitana", "La Florida", 16800.0),
    ("SUC-005", "Falabella Plaza Oeste", "Metropolitana", "Cerrillos", 14500.0),
    ("SUC-006", "Falabella Ahumada Centro", "Metropolitana", "Santiago", 12000.0),
    ("SUC-007", "Falabella Mall Plaza Trébol", "Biobío", "Talcahuano", 14200.0),
    ("SUC-008", "Falabella Mall Marina Arauco", "Valparaíso", "Viña del Mar", 13800.0),
    ("SUC-009", "Falabella Mall Plaza La Serena", "Coquimbo", "La Serena", 11500.0),
    ("SUC-010", "Falabella Mall Plaza Antofagasta", "Antofagasta", "Antofagasta", 13000.0),
    ("SUC-011", "Falabella Portal Temuco", "La Araucanía", "Temuco", 11200.0),
    ("SUC-012", "Falabella Mall Plaza Los Ángeles", "Biobío", "Los Ángeles", 9800.0),
    ("SUC-013", "Falabella Portal Rancagua", "O'Higgins", "Rancagua", 10500.0),
    ("SUC-014", "Falabella Mall Plaza Iquique", "Tarapacá", "Iquique", 10200.0),
    ("SUC-015", "Falabella Portal Osorno", "Los Lagos", "Osorno", 8900.0),
]

CATEGORIAS_FALABELLA = [
    ("CAT-MOD-MUJ", "Mujer & Vestuario", "Moda"),
    ("CAT-MOD-HOM", "Hombre & Juvenil", "Moda"),
    ("CAT-CAL-ZAP", "Calzado & Zapatillas", "Calzado"),
    ("CAT-TEC-TEL", "Telefonía & Smartphones", "Tecnología"),
    ("CAT-TEC-TV", "Smart TVs & Audio", "Tecnología"),
    ("CAT-TEC-COM", "Computación & Gaming", "Tecnología"),
    ("CAT-HOG-MUE", "Muebles & Terrazas", "Hogar"),
    ("CAT-HOG-DEC", "Decohogar & Cama", "Hogar"),
    ("CAT-BEL-PER", "Perfumería & Fragancias", "Belleza"),
    ("CAT-DEP-FIT", "Deportes & Fitness", "Deportes"),
    ("CAT-ELE-BLA", "Línea Blanca & Cocina", "Electro"),
]

MARCAS_POR_DEPTO = {
    "Moda": ["Basement", "Sybilla", "Mango", "Americanino", "Reiss", "Mossimo", "University Club"],
    "Calzado": ["Nike", "Adidas", "Converse", "Gacel", "Clarks", "Puma", "Vans"],
    "Tecnología": ["Samsung", "Apple", "Sony", "LG", "Lenovo", "Asus", "Xiaomi"],
    "Hogar": ["Crate&Barrel", "Casaideas", "Rosen", "CIC", "Mica", "Basement Home"],
    "Belleza": ["MAC Cosmetics", "Dior", "Chanel", "Lancôme", "Clinique", "Estée Lauder"],
    "Deportes": ["Under Armour", "Columbia", "The North Face", "Lippi", "Garmin"],
    "Electro": ["Whirlpool", "Bosch", "Electrolux", "Fensa", "Mademsa", "Nespresso"],
}

CANALES_VENTA = [
    ("CAN-POS", "Tienda Física (POS)", 0),
    ("CAN-WEB", "Falabella.com (Web Desktop)", 1),
    ("CAN-APP", "Falabella App Móvil", 1),
    ("CAN-PICK", "Click & Collect (Retiro Tienda)", 1),
]

PROMOCIONES = [
    ("PROMO-NONE", "Sin Promoción", 0.0, 0),
    ("PROMO-CMR-20", "20% Dcto Tarjeta CMR", 0.20, 0),
    ("PROMO-CYBER-40", "CyberDay Falabella 40% OFF", 0.40, 1),
    ("PROMO-CYBER-BOMBA", "Cyber Bombazo Exclusivo 50%", 0.50, 1),
    ("PROMO-LIQUID-VER", "Liquidación Temporada Verano", 0.30, 0),
    ("PROMO-VENTA-NOCT", "Venta Nocturna Falabella", 0.25, 0),
]
