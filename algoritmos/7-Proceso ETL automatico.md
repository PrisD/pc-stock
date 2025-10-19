# Proceso ETL para Data-Warehouse

## Objetivo

El objetivo del modulo ETL es alimentar el Data Warehouse con datos fiables, consistentes y listos para el analisis.

Su funcion es automatizar el proceso de mover la informacion desde la base de datos transaccional hacia la base analitica. Este proceso convierte los registros de operaciones diarias en una estructura optimizada para la consulta historica. Procesa los datos crudos para limpiarlos, agregarlos y enriquecerlos, asegurando que el modulo de reportes siempre consulte una fuente de informacion coherente y actualizada hasta el ultimo ciclo de carga.

La idea es que este modulo se ejecute una vez al dia en horarios de baja actividad (ej 02:00hs), para evitar sobrecargas sobre la db transaccional cuando los usuarios estan operando en el sistema. Todos los reportes que seran posibles de generar en el dw tendran datos de como minimo fecha del dia anterior a la del reporte.

## Algoritmo

1. INICIO
2. Establecer conexiones (fuente y destino)
3. Extraer todos los datos nuevos o modificados desde la ultima ejecucion.
4. Transformar los datos (limpiar, agregar, calcular).
5. Cargar los datos transformados en el Data Warehouse.
6. Registrar el éxito de la operación y la fecha/hora.
7. Cerrar conexiones.
8. FIN


## Niveles de refinamiento

### Nivel 1
1. INICIO
2. Se establencen las conexiones
    1. Se establece conexion con la base de datos fuente
    2. Se establece conexion con el data-warhouse
3. Se determina la fecha de la ultima ejecucion
4. Se ejecuta consulta para obtener los registros nuevos o modificados desde la ultima fecha.
5. Transformar los datos
6. Cargar los datos al data-warehouse
    1. Si el dato ya existe se actualziza.
    2. Si el dato no existe se inserta.
7. Se guarda un registro de la ejecucion
    1. Fecha
    2. Hora de inicio
    3. Hora fin
    4. Cantidad de registros procesados
8. Se cierran las conexiones
9. FIN

### Nivel 2
1. INICIO
2. Se establencen las conexiones
    1. Se establece conexion con la base de datos fuente
    2. Se establece conexion con el data-warhouse
3. Se determina la fecha de la ultima ejecucion
4. Se ejecuta consulta para obtener los registros nuevos o modificados desde la ultima fecha.
5. Transformar los datos
    1. 
6. Cargar los datos al data-warehouse
    1. Si el dato ya existe se actualziza.
    2. Si el dato no existe se inserta.
7. Se guarda un registro de la ejecucion
    1. Fecha
    2. Hora de inicio
    3. Hora fin
    4. Cantidad de registros procesados
8. Se cierran las conexiones
9. FIN

## Pseudocodigo

```
PROCEDIMIENTO Iniciar_ETL()

    Establecer_Conexion(db_origen)
    Establecer_Conexion(dw_destino)
    
    fecha_ultima_ejecucion = Obtener_Fecha_Ultima_Ejecucion_Exitosa()
    fecha_actual = Obtener_Fecha_Actual()
    
    Procesar_Dimension_Tiempo(fecha_actual)
    Procesar_Dimension_Producto()
    Procesar_Dimension_Lote()
    
    Procesar_Hechos_Movimientos(fecha_ultima_ejecucion)
    
    Procesar_Hechos_Stock_Diario(fecha_actual - 1 día)

    Guardar_Fecha_Ejecucion_Exitosa(fecha_actual)

FIN PROCEDIMIENTO

// Sub-procedimientos detallados

PROCEDIMIENTO Procesar_Dimension_Tiempo(fecha)
    id_fecha_numerico = Convertir_Fecha_A_Entero(fecha) 
    SI NO Existe_En_DW("DimTiempo", "id_fecha", id_fecha_numerico) ENTONCES
        dia = Obtener_Dia(fecha)
        mes = Obtener_Mes(fecha)
        anio = Obtener_Anio(fecha)
        trimestre = Obtener_Trimestre(fecha)
        nombre_dia = Calcular_Nombre_Dia(fecha)
        nombre_mes = Calcular_Nombre_Mes(fecha)
        
        Insertar_En_DW("DimTiempo", [id_fecha_numerico, fecha, dia, mes, anio, trimestre, nombre_dia, nombre_mes])
    FIN SI
FIN PROCEDIMIENTO

PROCEDIMIENTO Procesar_Dimension_Producto()
    productos_origen = Consultar_En_Origen()
    
    PARA CADA p_origen EN productos_origen
        registro_dw = Buscar_En_DW("DimProducto", "id_producto", p_origen.id_producto)
        
        SI registro_dw ES NULO ENTONCES
            Insertar_En_DW("DimProducto", [p_origen.id_producto, p_origen.nombre, p_origen.descripcion, p_origen.stock_minimo])
        SINO SI (cambio algun campo) ENTONCES
            Actualizar_En_DW("DimProducto", "id_producto", p_origen.id_producto, [nombre_producto=p_origen.nombre, ...])
        FIN SI
    FIN PARA
FIN PROCEDIMIENTO

PROCEDIMIENTO Procesar_Dimension_Lote()
    // Lógica idéntica a Procesar_Dimension_Producto pero con la tabla Lote
FIN PROCEDIMIENTO

PROCEDIMIENTO Procesar_Hechos_Movimientos(fecha_desde)
    movimientos_nuevos = Consultar_En_Origen()
    
    PARA CADA mov EN movimientos_nuevos
        id_fecha_dw = Buscar_En_DW("DimTiempo", "fecha_completa", mov.fecha).id_fecha
        
        cantidad_ingreso = 0
        cantidad_egreso = 0
        SI mov.tipo == 'ingreso' ENTONCES
            cantidad_ingreso = mov.cantidad
        SINO
            cantidad_egreso = mov.cantidad
        FIN SI
        
        Insertar_En_DW("HechosMovimientos", [mov.id_producto,...])
    FIN PARA
FIN PROCEDIMIENTO

PROCEDIMIENTO Procesar_Hechos_Stock_Diario(fecha_stock)
    id_fecha_stock = Buscar_En_DW("DimTiempo", "fecha_completa", fecha_stock).id_fecha
    
    // Se elimina la foto del día por si el proceso se re-ejecuta
    Eliminar_De_DW("HechosStockDiario", "id_fecha", id_fecha_stock)
    
    stock_por_producto = Consultar_En_Origen()
    
    PARA CADA item_stock EN stock_por_producto
        Insertar_En_DW("HechosStockDiario", [item_stock.id_producto,...])
    FIN PARA
FIN PROCEDIMIENTO
```