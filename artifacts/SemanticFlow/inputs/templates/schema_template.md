# Esquema Relacional: [Nombre de la Empresa / Proyecto]

**Dominio de Negocio:** [Retail / Finanzas / Logística / Salud / Telecomunicaciones]  
**Arquitectura:** Star Schema / Snowflake Schema  
**Motor Analítico Destino:** Microsoft Fabric OneLake / Power BI (Direct Lake & Import)  
**Versión:** 1.0.0  

---

## 1. Dimensiones (Dim)

### `Dim_Cliente`
Entidad que centraliza la información demográfica y maestra de clientes.

* **Clave Primaria:** `SK_Cliente`

| Campo | Tipo de Dato | Tipo Clave | Descripción |
| :--- | :--- | :--- | :--- |
| **SK_Cliente** | `int64` | **PKey** | Identificador único subrogado del cliente. |
| **Codigo_Cliente** | `string` | | Código natural de negocio del cliente. |
| **Nombre_Completo** | `string` | | Nombre de la persona o razón social (PII: True). |
| **Email** | `string` | | Correo electrónico de contacto (PII: True). |
| **Segmento** | `string` | | Categoría de cliente (ej: Premium, Estándar, Corporativo). |
| **Estado_Activo** | `boolean` | | Indicador de si el cliente permanece activo. |

---

### `Dim_Producto`
Catálogo maestro de productos y servicios comercializados.

* **Clave Primaria:** `SK_Producto`

| Campo | Tipo de Dato | Tipo Clave | Descripción |
| :--- | :--- | :--- | :--- |
| **SK_Producto** | `int64` | **PKey** | Clave primaria subrogada del producto. |
| **SKU** | `string` | | Código identificador de inventario. |
| **Nombre_Producto** | `string` | | Descripción comercial del artículo. |
| **Categoria** | `string` | | Categoría superior de negocio. |
| **Subcategoria** | `string` | | Subcategoría de producto. |
| **Precio_Lista** | `decimal` | | Precio unitario base de lista. |

---

### `Dim_Tiempo`
Dimensión temporal con calendario corporativo pre-calculado.

* **Clave Primaria:** `SK_Fecha`

| Campo | Tipo de Dato | Tipo Clave | Descripción |
| :--- | :--- | :--- | :--- |
| **SK_Fecha** | `int32` | **PKey** | Clave fecha en formato numérico (YYYYMMDD). |
| **Fecha** | `date` | | Fecha estándar en formato YYYY-MM-DD. |
| **Anio** | `int32` | | Año del calendario. |
| **Mes** | `int32` | | Número de mes (1 al 12). |
| **Nombre_Mes** | `string` | | Nombre completo del mes. |
| **Trimestre** | `string` | | Trimestre del año (Q1, Q2, Q3, Q4). |
| **Es_Dia_Habil** | `boolean` | | Flag indicador de día laborable. |

---

## 2. Tablas de Hechos (Fact)

### `Fact_Ventas`
Transacciones comerciales a nivel de línea de detalle de boleta o factura.

* **Clave Primaria:** `SK_Venta`

| Campo | Tipo de Dato | Tipo Clave | Descripción |
| :--- | :--- | :--- | :--- |
| **SK_Venta** | `int64` | **PKey** | Identificador único de la transacción. |
| **SK_Cliente** | `int64` | **FKey (`Dim_Cliente.SK_Cliente`)** | Enlace a la dimensión cliente. |
| **SK_Producto** | `int64` | **FKey (`Dim_Producto.SK_Producto`)** | Enlace a la dimensión producto. |
| **SK_Fecha** | `int32` | **FKey (`Dim_Tiempo.SK_Fecha`)** | Enlace al calendario dimensional. |
| **Cantidad** | `int32` | | Unidades vendidas en la transacción. |
| **Precio_Unitario** | `decimal` | | Precio real transado por unidad. |
| **Monto_Bruto** | `decimal` | | Monto monetario antes de descuentos e impuestos. |
| **Monto_Descuento** | `decimal` | | Descuento total aplicado. |
| **Monto_Neto** | `decimal` | | Monto final percibido por la venta. |
| **Costo_Total** | `decimal` | | Costo de adquisición o manufactura asociado. |
| **Margen_Bruto** | `decimal` | | Margen bruto calculado (`Monto_Neto - Costo_Total`). |
