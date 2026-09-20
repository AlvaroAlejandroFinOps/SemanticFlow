"""
Mapeo de tipos de datos relacionales a tipos nativos de Power BI TMDL.
"""
from enum import Enum


class PbiDataType(str, Enum):
    INT64 = "int64"
    DOUBLE = "double"
    DECIMAL = "decimal"
    STRING = "string"
    DATETIME = "dateTime"
    BOOLEAN = "boolean"
    BINARY = "binary"


# Mapeo normalizado desde tipos SQL/Lakehouse/Markdown a Power BI TMDL
SQL_TO_PBI_TYPE_MAP: dict[str, PbiDataType] = {
    # Enteros
    "int8": PbiDataType.INT64,
    "int16": PbiDataType.INT64,
    "int32": PbiDataType.INT64,
    "int64": PbiDataType.INT64,
    "int": PbiDataType.INT64,
    "integer": PbiDataType.INT64,
    "bigint": PbiDataType.INT64,
    "smallint": PbiDataType.INT64,
    "tinyint": PbiDataType.INT64,

    # Flotantes y decimales
    "float32": PbiDataType.DOUBLE,
    "float64": PbiDataType.DOUBLE,
    "float": PbiDataType.DOUBLE,
    "real": PbiDataType.DOUBLE,
    "double": PbiDataType.DOUBLE,
    "decimal": PbiDataType.DECIMAL,
    "numeric": PbiDataType.DECIMAL,
    "money": PbiDataType.DECIMAL,

    # Texto / Strings
    "string": PbiDataType.STRING,
    "varchar": PbiDataType.STRING,
    "nvarchar": PbiDataType.STRING,
    "text": PbiDataType.STRING,
    "char": PbiDataType.STRING,

    # Temporales
    "datetime": PbiDataType.DATETIME,
    "timestamp": PbiDataType.DATETIME,
    "date": PbiDataType.DATETIME,
    "time": PbiDataType.STRING,

    # Booleanos
    "bool": PbiDataType.BOOLEAN,
    "boolean": PbiDataType.BOOLEAN,
}


def normalize_data_type(raw_type: str) -> PbiDataType:
    """Normaliza un tipo de dato arbitrario al tipo PBI DataType correspondiente."""
    cleaned = raw_type.strip().lower()
    # Eliminar longitud o precisión tipo varchar(50) o decimal(18,2)
    if "(" in cleaned:
        cleaned = cleaned.split("(")[0].strip()
    return SQL_TO_PBI_TYPE_MAP.get(cleaned, PbiDataType.STRING)
