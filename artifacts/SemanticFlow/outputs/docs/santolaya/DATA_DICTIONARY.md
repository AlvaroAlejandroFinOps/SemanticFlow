# Data Dictionary: esquema_estrella_unificado_santolaya

Santolaya es una destacada empresa chilena de ingeniería, construcción y desarrollo inmobiliario con más de cuatro décadas de liderazgo y excelencia en el mercado nacional. Su modelo integrado abarca desde la prospección, compra de terrenos y estructuración financiera de proyectos, hasta la ejecución integral de obras civiles, comercialización de viviendas y servicio técnico de postventa.

## Entities Overview

| Entity | Role | Attributes Count | Metrics Count | Source Table |
| --- | --- | --- | --- | --- |
| **dim_proyecto_obra** | `DIMENSION` | 15 | 0 | `N/A` |
| **dim_tiempo** | `DIMENSION` | 10 | 0 | `N/A` |
| **dim_tercero** | `DIMENSION` | 7 | 0 | `N/A` |
| **dim_centro_costo** | `DIMENSION` | 4 | 0 | `N/A` |
| **dim_partida_edt** | `DIMENSION` | 5 | 0 | `N/A` |
| **dim_unidad_inmobiliaria** | `DIMENSION` | 11 | 0 | `N/A` |
| **fact_evm_avance_obra** | `FACT` | 10 | 0 | `N/A` |
| **fact_compras_compromisos** | `FACT` | 11 | 0 | `N/A` |
| **fact_recepciones_bodega** | `FACT` | 10 | 0 | `N/A` |
| **fact_facturacion_contratista** | `FACT` | 11 | 0 | `N/A` |
| **fact_ventas_inmobiliarias** | `FACT` | 14 | 0 | `N/A` |
| **fact_postventa_servicio** | `FACT` | 12 | 0 | `N/A` |
| **seguridad_usuarios_obra** | `DIMENSION` | 4 | 0 | `N/A` |
| **DIM_EMPRESA_SOCIEDAD** | `DIMENSION` | 4 | 0 | `N/A` |

## Detailed Entities & Attributes

### dim_proyecto_obra (`DIMENSION`)

*Conecta la visión de obra física con la visión de estructuración societaria e inmobiliaria.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `codigo_obra_sap` | `DataType.STRING` | `-` | `-` |
| `nombre_proyecto` | `DataType.STRING` | `-` | `-` |
| `tipo_negocio` | `DataType.STRING` | `-` | `-` |
| `sk_empresa_sociedad` | `DataType.INT64` | `PK` | `-` |
| `comuna` | `DataType.STRING` | `-` | `-` |
| `region` | `DataType.STRING` | `-` | `-` |
| `direccion_obra` | `DataType.STRING` | `-` | `-` |
| `superficie_construida_m2` | `DataType.DECIMAL` | `-` | `-` |
| `cantidad_unidades_totales` | `DataType.INT64` | `-` | `-` |
| `fecha_inicio_programada` | `DataType.DATE` | `-` | `-` |
| `fecha_termino_contractual` | `DataType.DATE` | `-` | `-` |
| `jefe_obra_email` | `DataType.STRING` | `-` | `-` |
| `administrador_obra_email` | `DataType.STRING` | `-` | `-` |
| `estado_proyecto` | `DataType.STRING` | `-` | `-` |

### dim_tiempo (`DIMENSION`)

** **Granularidad:** Un registro por día calendario (1990 - 2040).*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_fecha` | `DataType.INT64` | `PK` | `-` |
| `fecha` | `DataType.DATE` | `-` | `-` |
| `anio` | `DataType.INT64` | `-` | `-` |
| `mes_numero` | `DataType.INT64` | `-` | `-` |
| `mes_nombre` | `DataType.STRING` | `-` | `-` |
| `anio_mes` | `DataType.STRING` | `-` | `-` |
| `trimestre` | `DataType.STRING` | `-` | `-` |
| `semana_anio` | `DataType.INT64` | `-` | `-` |
| `dia_habil_construccion` | `DataType.BOOLEAN` | `-` | `-` |
| `valor_uf_cierre` | `DataType.DECIMAL` | `-` | `-` |

### dim_tercero (`DIMENSION`)

** **Granularidad:** Un registro por persona natural o jurídica que interactúa con la compañía.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_tercero` | `DataType.INT64` | `PK` | `-` |
| `codigo_socio_sap` | `DataType.STRING` | `-` | `-` |
| `rut_dni` | `DataType.STRING` | `-` | `-` |
| `razon_social_nombre` | `DataType.STRING` | `-` | `-` |
| `tipo_tercero` | `DataType.STRING` | `-` | `-` |
| `calificacion_riesgo` | `DataType.STRING` | `-` | `-` |
| `cuenta_bancaria_asociada` | `DataType.STRING` | `-` | `-` |

### dim_centro_costo (`DIMENSION`)

** **Granularidad:** Un registro por centro de costo analítico definido en las dimensiones contables de SAP B1.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_centro_costo` | `DataType.INT64` | `PK` | `-` |
| `codigo_norma_reparto` | `DataType.STRING` | `-` | `-` |
| `nombre_centro_costo` | `DataType.STRING` | `-` | `-` |
| `dimension_contable` | `DataType.INT64` | `-` | `-` |

### dim_partida_edt (`DIMENSION`)

** **Granularidad:** Registro por ítem de presupuesto de obra o partida analítica.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_partida_edt` | `DataType.INT64` | `PK` | `-` |
| `codigo_partida` | `DataType.STRING` | `-` | `-` |
| `nombre_partida` | `DataType.STRING` | `-` | `-` |
| `capitulo_edt` | `DataType.STRING` | `-` | `-` |
| `unidad_medida` | `DataType.STRING` | `-` | `-` |

### dim_unidad_inmobiliaria (`DIMENSION`)

** **Granularidad:** Un registro por cada departamento, local, bodega o estacionamiento de cada desarrollo.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_unidad_inmobiliaria` | `DataType.INT64` | `PK` | `-` |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `codigo_unidad` | `DataType.STRING` | `-` | `-` |
| `tipo_unidad` | `DataType.STRING` | `-` | `-` |
| `modelo_tipologia` | `DataType.STRING` | `-` | `-` |
| `numero_piso` | `DataType.INT64` | `-` | `-` |
| `orientacion` | `DataType.STRING` | `-` | `-` |
| `superficie_util_m2` | `DataType.DECIMAL` | `-` | `-` |
| `superficie_terraza_m2` | `DataType.DECIMAL` | `-` | `-` |
| `superficie_total_m2` | `DataType.DECIMAL` | `-` | `-` |
| `estado_comercial_actual` | `DataType.STRING` | `-` | `-` |

### fact_evm_avance_obra (`FACT`)

** **Granularidad:** Snapshot semanal por proyecto/obra y por partida presupuestaria de control.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_evm` | `DataType.INT64` | `PK` | `-` |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `sk_fecha` | `DataType.INT64` | `PK` | `-` |
| `sk_partida_edt` | `DataType.INT64` | `PK` | `-` |
| `monto_bac_presupuesto_base` | `DataType.DECIMAL` | `-` | `-` |
| `monto_pv_planificado` | `DataType.DECIMAL` | `-` | `-` |
| `monto_ev_ganado` | `DataType.DECIMAL` | `-` | `-` |
| `monto_ac_costo_real` | `DataType.DECIMAL` | `-` | `-` |
| `porcentaje_avance_fisico` | `DataType.DECIMAL` | `-` | `-` |
| `porcentaje_avance_financiero` | `DataType.DECIMAL` | `-` | `-` |

### fact_compras_compromisos (`FACT`)

** **Granularidad:** Línea individual de detalle de cada Orden de Compra emitida en SAP B1.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_compra` | `DataType.INT64` | `PK` | `-` |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `sk_tercero_proveedor` | `DataType.INT64` | `PK` | `-` |
| `sk_centro_costo` | `DataType.INT64` | `PK` | `-` |
| `sk_partida_edt` | `DataType.INT64` | `PK` | `-` |
| `sk_fecha_emision` | `DataType.INT64` | `PK` | `-` |
| `num_oc_sap` | `DataType.STRING` | `-` | `-` |
| `cantidad_ordenada` | `DataType.DECIMAL` | `-` | `-` |
| `monto_comprometido_neto_clp` | `DataType.DECIMAL` | `-` | `-` |
| `monto_comprometido_uf` | `DataType.DECIMAL` | `-` | `-` |
| `estado_aprobacion` | `DataType.STRING` | `-` | `-` |

### fact_recepciones_bodega (`FACT`)

** **Granularidad:** Línea de entrada física de material recepcionado en la bodega de faena.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_recepcion` | `DataType.INT64` | `PK` | `-` |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `sk_tercero_proveedor` | `DataType.INT64` | `PK` | `-` |
| `sk_partida_edt` | `DataType.INT64` | `PK` | `-` |
| `sk_fecha_recepcion` | `DataType.INT64` | `PK` | `-` |
| `num_guia_despacho` | `DataType.STRING` | `-` | `-` |
| `num_entrada_sap` | `DataType.STRING` | `-` | `-` |
| `cantidad_recibida` | `DataType.DECIMAL` | `-` | `-` |
| `monto_recepcionado_clp` | `DataType.DECIMAL` | `-` | `-` |
| `indicador_conforme` | `DataType.BOOLEAN` | `-` | `-` |

### fact_facturacion_contratista (`FACT`)

** **Granularidad:** Detalle de factura de proveedor o subcontrato / Estado de Pago liquidado.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_factura_contratista` | `DataType.INT64` | `PK` | `-` |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `sk_tercero_contratista` | `DataType.INT64` | `PK` | `-` |
| `sk_centro_costo` | `DataType.INT64` | `PK` | `-` |
| `sk_fecha_contable` | `DataType.INT64` | `PK` | `-` |
| `num_factura_tributaria` | `DataType.STRING` | `-` | `-` |
| `num_estado_pago_ep` | `DataType.STRING` | `-` | `-` |
| `monto_bruto_clp` | `DataType.DECIMAL` | `-` | `-` |
| `monto_retencion_garantia_clp` | `DataType.DECIMAL` | `-` | `-` |
| `monto_liquido_a_pago_clp` | `DataType.DECIMAL` | `-` | `-` |
| `certificacion_laboral_f30` | `DataType.STRING` | `-` | `-` |

### fact_ventas_inmobiliarias (`FACT`)

** **Granularidad:** Evento o hito de cambio de estado sobre una unidad inmobiliaria (Reserva, Promesa, Escritura, Desistimiento).*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_venta` | `DataType.INT64` | `PK` | `-` |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `sk_unidad_inmobiliaria` | `DataType.INT64` | `PK` | `-` |
| `sk_tercero_cliente` | `DataType.INT64` | `PK` | `-` |
| `sk_tercero_broker` | `DataType.INT64` | `PK` | `-` |
| `sk_fecha_operacion` | `DataType.INT64` | `PK` | `-` |
| `etapa_comercial` | `DataType.STRING` | `-` | `-` |
| `precio_lista_uf` | `DataType.DECIMAL` | `-` | `-` |
| `precio_cierre_uf` | `DataType.DECIMAL` | `-` | `-` |
| `monto_pie_uf` | `DataType.DECIMAL` | `-` | `-` |
| `monto_credito_hipotecario_uf` | `DataType.DECIMAL` | `-` | `-` |
| `monto_subsidio_uf` | `DataType.DECIMAL` | `-` | `-` |
| `monto_desistimiento_uf` | `DataType.DECIMAL` | `-` | `-` |
| `dias_ciclo_promesa_escritura` | `DataType.INT64` | `-` | `-` |

### fact_postventa_servicio (`FACT`)

** **Granularidad:** Ticket o solicitud de servicio técnico de clientes de departamentos entregados.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_postventa` | `DataType.INT64` | `PK` | `-` |
| `sk_proyecto_obra` | `DataType.INT64` | `PK` | `-` |
| `sk_unidad_inmobiliaria` | `DataType.INT64` | `PK` | `-` |
| `sk_tercero_cliente` | `DataType.INT64` | `PK` | `-` |
| `sk_fecha_apertura` | `DataType.INT64` | `PK` | `-` |
| `sk_fecha_cierre` | `DataType.INT64` | `PK` | `-` |
| `ticket_servicio_sap` | `DataType.STRING` | `-` | `-` |
| `recinto_afectado` | `DataType.STRING` | `-` | `-` |
| `tipologia_falla` | `DataType.STRING` | `-` | `-` |
| `costo_reparacion_clp` | `DataType.DECIMAL` | `-` | `-` |
| `dias_resolucion` | `DataType.INT64` | `-` | `-` |
| `estado_ticket` | `DataType.STRING` | `-` | `-` |

### seguridad_usuarios_obra (`DIMENSION`)

** **Granularidad:** Relación N a M entre usuarios de Microsoft Entra ID (M365) y proyectos.*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `user_email` | `DataType.STRING` | `-` | `-` |
| `codigo_obra_sap` | `DataType.STRING` | `-` | `-` |
| `rol_usuario` | `DataType.STRING` | `-` | `-` |
| `acceso_total` | `DataType.BOOLEAN` | `-` | `-` |

### DIM_EMPRESA_SOCIEDAD (`DIMENSION`)

*Extraída de Mermaid ERD*

#### Attributes
| Attribute | Data Type | Key Type | Classification |
| --- | --- | --- | --- |
| `sk_empresa_sociedad` | `DataType.INT64` | `PK` | `-` |
| `rut_sociedad` | `DataType.STRING` | `-` | `-` |
| `razon_social` | `DataType.STRING` | `-` | `-` |
| `codigo_sociedad_sap` | `DataType.STRING` | `-` | `-` |
