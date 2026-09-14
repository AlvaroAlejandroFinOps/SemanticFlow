# Data Dictionary: esquema_relacional

Esquema extraído desde Markdown

## Entities Overview

| Entity | Role | Attributes Count | Metrics Count | Source Table |
| --- | --- | --- | --- | --- |
| **Dim_Linea** | `DIMENSION` | 5 | 0 | `N/A` |
| **Dim_Estacion** | `DIMENSION` | 7 | 0 | `N/A` |
| **Dim_Tren_Coche** | `DIMENSION` | 6 | 0 | `N/A` |
| **Dim_Usuario_Bip** | `DIMENSION` | 3 | 0 | `N/A` |
| **Dim_Equipamiento** | `DIMENSION` | 5 | 0 | `N/A` |
| **Dim_Unidad_Negocio** | `DIMENSION` | 2 | 0 | `N/A` |
| **Dim_Espacio_Comercial** | `DIMENSION` | 3 | 0 | `N/A` |
| **Dim_Proyecto_Expansion** | `DIMENSION` | 3 | 0 | `N/A` |
| **Dim_Organizacion_ESG** | `DIMENSION` | 3 | 0 | `N/A` |
| **Dim_Tiempo** | `DIMENSION` | 7 | 0 | `N/A` |
| **Fact_Validacion** | `FACT` | 7 | 0 | `N/A` |
| **Fact_Simulacion_Flujo** | `FACT` | 7 | 0 | `N/A` |
| **Fact_Venta_Carga** | `FACT` | 6 | 0 | `N/A` |
| **Fact_Telemetria_Tren** | `FACT` | 8 | 0 | `N/A` |
| **Fact_Sensoraje_Via** | `FACT` | 6 | 0 | `N/A` |
| **Fact_Estado_Resultado** | `FACT` | 7 | 0 | `N/A` |
| **Fact_Ingresos_NNT** | `FACT` | 6 | 0 | `N/A` |
| **Fact_Consumo_ESG** | `FACT` | 6 | 0 | `N/A` |
| **Fact_Cumplimiento_Oferta** | `FACT` | 6 | 0 | `N/A` |
| **Fact_Seguridad_NPS** | `FACT` | 5 | 0 | `N/A` |

## Detailed Entities & Attributes

### Dim_Linea (`DIMENSION`)

*Representa las líneas de la red del Metro de Santiago.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `Codigo_Linea` | `DataType.STRING` | `-` | `-` |
| `Color` | `DataType.STRING` | `-` | `-` |
| `Tecnologia` | `DataType.STRING` | `-` | `-` |
| `Longitud_Km` | `DataType.STRING` | `-` | `-` |

### Dim_Estacion (`DIMENSION`)

*Representa cada una de las estaciones que componen las distintas líneas de metro.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Estacion` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `Codigo_Estacion` | `DataType.STRING` | `-` | `-` |
| `Nombre_Estacion` | `DataType.STRING` | `-` | `-` |
| `Comuna` | `DataType.STRING` | `-` | `-` |
| `Tipo_Estacion` | `DataType.STRING` | `-` | `-` |
| `Es_Combinacion` | `DataType.STRING` | `-` | `-` |

### Dim_Tren_Coche (`DIMENSION`)

*Representa la flota de trenes asignados a la red de metro.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Tren` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `ID_Formacion` | `DataType.STRING` | `-` | `-` |
| `Modelo` | `DataType.STRING` | `-` | `-` |
| `Cant_Coches` | `DataType.STRING` | `-` | `-` |
| `Capacidad_Pax` | `DataType.STRING` | `-` | `-` |

### Dim_Usuario_Bip (`DIMENSION`)

*Registro de tarjetas y usuarios del sistema Bip!*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Usuario` | `DataType.INT64` | `-` | `-` |
| `Numero_Tarjeta_Bip` | `DataType.STRING` | `-` | `-` |
| `Tipo_Usuario` | `DataType.STRING` | `-` | `-` |

### Dim_Equipamiento (`DIMENSION`)

*Contiene la jerarquía de activos e infraestructura crítica asociada a trenes o estaciones (módulo de mantenimiento/SAP PM).*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Equipo` | `DataType.INT64` | `-` | `-` |
| `SK_Tren` | `DataType.STRING` | `-` | `-` |
| `SK_Estacion` | `DataType.STRING` | `-` | `-` |
| `Sistema` | `DataType.STRING` | `-` | `-` |
| `Criticidad` | `DataType.STRING` | `-` | `-` |

### Dim_Unidad_Negocio (`DIMENSION`)

*Estructura organizacional interna para reporte financiero.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Unidad` | `DataType.STRING` | `-` | `-` |
| `Nombre` | `DataType.STRING` | `-` | `-` |

### Dim_Espacio_Comercial (`DIMENSION`)

*Detalle de locales y publicidad en las estaciones.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Espacio` | `DataType.INT64` | `-` | `-` |
| `SK_Estacion` | `DataType.STRING` | `-` | `-` |
| `Tipo` | `DataType.STRING` | `-` | `-` |

### Dim_Proyecto_Expansion (`DIMENSION`)

*Registro de iniciativas de infraestructura y crecimiento de la red.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Proyecto` | `DataType.STRING` | `-` | `-` |
| `Nombre` | `DataType.STRING` | `-` | `-` |
| `Presupuesto_USD` | `DataType.STRING` | `-` | `-` |

### Dim_Organizacion_ESG (`DIMENSION`)

*Catálogo de iniciativas y compromisos ESG (Ambiental, Social y Gobernanza).*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Iniciativa` | `DataType.STRING` | `-` | `-` |
| `Categoria` | `DataType.STRING` | `-` | `-` |
| `Meta` | `DataType.STRING` | `-` | `-` |

### Dim_Tiempo (`DIMENSION`)

*Dimensión temporal detallada para análisis de tendencias cronológicas.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `Fecha_SK` | `DataType.STRING` | `-` | `-` |
| `Fecha` | `DataType.DATETIME` | `-` | `-` |
| `Dia` | `DataType.STRING` | `-` | `-` |
| `Mes` | `DataType.STRING` | `-` | `-` |
| `Año` | `DataType.STRING` | `-` | `-` |
| `Dia_Semana` | `DataType.STRING` | `-` | `-` |
| `Es_Fin_Semana` | `DataType.STRING` | `-` | `-` |

### Fact_Validacion (`FACT`)

*Registra cada uno de los accesos y validaciones de pasajeros en los torniquetes de la red.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `ID_Validacion` | `DataType.INT64` | `-` | `-` |
| `Fecha_SK` | `DataType.STRING` | `-` | `-` |
| `Segundo_Dia` | `DataType.STRING` | `-` | `-` |
| `SK_Estacion` | `DataType.STRING` | `-` | `-` |
| `SK_Usuario` | `DataType.INT64` | `-` | `-` |
| `Tarifa_Cobrada_CLP` | `DataType.STRING` | `-` | `-` |
| `Canal_Validacion` | `DataType.STRING` | `-` | `-` |

### Fact_Simulacion_Flujo (`FACT`)

*Resultados de modelos de simulación basados en agentes en el andén y pasillos de estaciones.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `ID_Agente_Flujo` | `DataType.INT64` | `-` | `-` |
| `Fecha_SK` | `DataType.STRING` | `-` | `-` |
| `Segundo_Dia` | `DataType.STRING` | `-` | `-` |
| `SK_Estacion` | `DataType.STRING` | `-` | `-` |
| `Posicion_X` | `DataType.STRING` | `-` | `-` |
| `Posicion_Y` | `DataType.STRING` | `-` | `-` |
| `Estado` | `DataType.STRING` | `-` | `-` |

### Fact_Venta_Carga (`FACT`)

*Registra las transacciones de carga monetaria en tarjetas Bip!*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `ID_Venta_Carga` | `DataType.INT64` | `-` | `-` |
| `Fecha_SK` | `DataType.STRING` | `-` | `-` |
| `SK_Estacion` | `DataType.STRING` | `-` | `-` |
| `SK_Usuario` | `DataType.INT64` | `-` | `-` |
| `Monto_Carga_CLP` | `DataType.STRING` | `-` | `-` |
| `Metodo_Pago` | `DataType.STRING` | `-` | `-` |

### Fact_Telemetria_Tren (`FACT`)

*Muestreo de sensores en tiempo real de cada uno de los trenes en circulación.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `ID_Log` | `DataType.INT64` | `-` | `-` |
| `Fecha_SK` | `DataType.STRING` | `-` | `-` |
| `Segundo_Dia` | `DataType.STRING` | `-` | `-` |
| `SK_Tren` | `DataType.STRING` | `-` | `-` |
| `Velocidad_KmH` | `DataType.STRING` | `-` | `-` |
| `Temp_Motor_C` | `DataType.STRING` | `-` | `-` |
| `Voltaje_Linea_V` | `DataType.STRING` | `-` | `-` |
| `Estado_ATP` | `DataType.STRING` | `-` | `-` |

### Fact_Sensoraje_Via (`FACT`)

*Monitoreo de telemetría sobre el desgaste físico y vibración de las vías férreas de la red.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `ID_Sensoraje` | `DataType.INT64` | `-` | `-` |
| `Fecha_SK` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `Vibracion_RMS_G` | `DataType.STRING` | `-` | `-` |
| `Desgaste_Riel_mm` | `DataType.STRING` | `-` | `-` |
| `Temp_Riel_C` | `DataType.STRING` | `-` | `-` |

### Fact_Estado_Resultado (`FACT`)

*Consolidación financiera mensual por línea y unidad de negocio.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Periodo` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `SK_Unidad` | `DataType.STRING` | `-` | `-` |
| `Ingresos_Tarifarios_CLP` | `DataType.STRING` | `-` | `-` |
| `Ingresos_NNT_CLP` | `DataType.STRING` | `-` | `-` |
| `Costos_Operacionales_CLP` | `DataType.STRING` | `-` | `-` |
| `EBITDA_CLP` | `DataType.STRING` | `-` | `-` |

### Fact_Ingresos_NNT (`FACT`)

*Detalle analítico mensual de los ingresos de Negocios No Tarifarios (NNT).*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Periodo` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `SK_Unidad` | `DataType.STRING` | `-` | `-` |
| `Ingreso_Arriendos_Comerciales_CLP` | `DataType.STRING` | `-` | `-` |
| `Ingreso_Publicidad_CLP` | `DataType.STRING` | `-` | `-` |
| `Ingreso_Cajeros_Telecom_CLP` | `DataType.STRING` | `-` | `-` |

### Fact_Consumo_ESG (`FACT`)

*KPIs ambientales y de rentabilidad social corporativa mensuales por línea.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Periodo` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `Consumo_Traccion_KWh` | `DataType.STRING` | `-` | `-` |
| `Indicador_KWh_CKm` | `DataType.STRING` | `-` | `-` |
| `Ahorro_Emisiones_CO2_Ton` | `DataType.STRING` | `-` | `-` |
| `Horas_Ahorradas_Viajeros` | `DataType.STRING` | `-` | `-` |

### Fact_Cumplimiento_Oferta (`FACT`)

*Consolidación mensual de la oferta y la regularidad del servicio por línea.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Periodo` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `Cumplimiento_Frecuencia_Pct` | `DataType.STRING` | `-` | `-` |
| `MKBF_Km` | `DataType.STRING` | `-` | `-` |
| `Factor_Ocupacion_Pct` | `DataType.STRING` | `-` | `-` |
| `Demanda_Buses_Respaldo` | `DataType.STRING` | `-` | `-` |

### Fact_Seguridad_NPS (`FACT`)

*Indicadores de percepción de usuario y eventos de seguridad reportados por mes.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `SK_Periodo` | `DataType.STRING` | `-` | `-` |
| `SK_Linea` | `DataType.STRING` | `-` | `-` |
| `NPS_Satisfaccion` | `DataType.STRING` | `-` | `-` |
| `Tasa_Delitos_MillonPax` | `DataType.STRING` | `-` | `-` |
| `Eventos_Seguridad_Averias` | `DataType.STRING` | `-` | `-` |
