# Especificación de Inputs - SemanticFlow (SMaC Ingestion)

Este directorio centraliza las especificaciones de esquemas relacionales que alimentan el compilador **SemanticFlow**.

---

## 1. Estructura de Directorios

```
inputs/
├── README.md               # Este documento de especificación
├── templates/              # Plantillas canónicas para copiar y completar
│   ├── schema_template.md  # Plantilla en formato Markdown estructurado
│   └── schema_template.yaml# Plantilla en formato YAML estructurado
└── companies/              # Espacio de trabajo particionado por empresa/cliente
    ├── metro_santiago/     # Ejemplo de referencia corporativa (20 tablas)
    │   └── schema.md
    └── [nombre_empresa]/   # Espacio para nuevos clientes
        └── schema.md
```

---

## 2. Contrato de Esquema en Markdown (`.md`)

SemanticFlow analiza archivos Markdown estructurados mediante `MarkdownSchemaParser`. Para que una tabla y sus relaciones sean ingeridas con 100% de precisión, se deben respetar las siguientes directrices:

### 2.1 Encabezado de Tabla
Cada tabla debe declararse con un título de nivel 2 o 3 (`##` o `###`):
```markdown
### `Dim_Cliente`
Descripción opcional del propósito de la entidad.

* **Clave Primaria:** `SK_Cliente`
```

### 2.2 Tabla de Atributos
La tabla Markdown debe incluir los campos estándar:
| Campo | Tipo de Dato | Tipo Clave | Descripción |
| :--- | :--- | :--- | :--- |
| **SK_Cliente** | `int64` | **PKey** | Identificador subrogado único del cliente. |
| **RUT** | `string` | | RUT o identificación nacional (PII: True). |
| **Nombre_Completo** | `string` | | Nombre y apellido del cliente (PII: True). |
| **SK_Comuna** | `int32` | **FKey (`Dim_Comuna.SK_Comuna`)** | Clave foránea a la comuna de residencia. |

### 2.3 Tipos de Datos Soportados
- **Enteros:** `int32`, `int64`, `integer`, `bigint`
- **Numéricos / Decimales:** `float32`, `float64`, `decimal`, `double`, `currency`
- **Texto:** `string`, `varchar`, `text`
- **Temporales:** `datetime`, `date`, `timestamp`
- **Booleanos:** `boolean`, `bool`

### 2.4 Declaración de Claves y Relaciones
- **Clave Primaria:** Debe contener `PKey`, `PK` o `Primary Key`.
- **Clave Foránea:** Debe declarar explícitamente el destino entre paréntesis:
  - Formato: `FKey (TablaDestino.ColumnaDestino)` o `FK: TablaDestino.ColumnaDestino`.
  - Ejemplo: `FKey (Dim_Estacion.SK_Estacion)`

---

## 3. Contrato de Esquema en YAML (`.yaml`)

Para integraciones de catálogo automatizadas o canalizaciones CI/CD:

```yaml
version: "1.0"
name: "Retail_Omnicanal"
culture: "es-CL"
tables:
  - name: "Fact_Ventas"
    role: "FACT"
    description: "Transacciones de venta física y digital"
    columns:
      - name: "SK_Venta"
        data_type: "int64"
        is_primary_key: true
      - name: "SK_Cliente"
        data_type: "int64"
        foreign_key: "Dim_Cliente.SK_Cliente"
      - name: "Monto_Neto"
        data_type: "decimal"
      - name: "Fecha_Venta"
        data_type: "datetime"
```

---

## 4. Checklist para Ingestar una Nueva Empresa

1. Crear la carpeta en `artifacts/SemanticFlow/inputs/companies/<slug_empresa>/`.
2. Copiar `templates/schema_template.md` a `companies/<slug_empresa>/schema.md`.
3. Especificar todas las tablas de hechos (`Fact_*`) y dimensiones (`Dim_*`).
4. Verificar que cada tabla de hechos tenga sus `FKey` apuntando a las dimensiones correspondientes.
5. Ejecutar la validación previa:
   ```bash
   python -m src.cli inspect -i artifacts/SemanticFlow/inputs/companies/<slug_empresa>/schema.md
   python -m src.cli validate -i artifacts/SemanticFlow/inputs/companies/<slug_empresa>/schema.md --min-score 75
   ```
