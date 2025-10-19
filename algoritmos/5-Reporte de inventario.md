# Reporte de inventario

## Objetivo del modulo
El objetivo principal del modulo es transformar los datos operativos del inventario en conocimiento estrategico para la toma de decisiones.

Permite el analisis de rendimiento de los productos. Facilita la identificacion de tendencias de venta. Su finalidad es ofrecer metricas claras que soporten la planificacion futura, asegurando la disponibilidad de informacion consolidada sin afectar el rendimiento del sistema transaccional principal.



## Algoritmo
1. INICIO
2. Presentar al usuario las opciones de reportes disponibles.
3. Recibir la seleccion del usuario y los parametros necesarios (ej. rango de fechas).
4. Consultar el Data Warehouse para generar el reporte seleccionado.
5. Generar y presentar el reporte al usuario.
6. FIN

## Refinamientos

### Nivel 1
1. INICIO
2. Mostrar opciones de reportes
    1. Ingresos por fecha por producto
    2. Vencimientos proximos
    3. Evolucion de stock de un producto por periodo
3. Pedir parametros necesarios segun reporte elegido
    1. fecha
    2. periodo
    3. producto
4. Validar datos ingresados
5. Iniciar conexion con el dw.
6. Obtener datos.
7. Generar reporte.
8. Cerrar conexion con el dw.
9. Mostrar reporte.
10. Ofrecer exportar reporte.
11. FIN

### Nivel 2
1. INICIO
2. Presentar un menú con tres opciones de reportes:
    1. Opción 1: Reporte de ingresos por fecha por producto.
    2. Opción 2: Reporte de vencimientos proximos.
    3. Opción 3: Reporte de evolucion de stock de un producto por periodo.
3. Esperar a que el usuario seleccione una opción ingresando un numero.
4. Según la opción seleccionada, solicitar los siguientes parametros:
    1. Para opción 1 (ingresos por fecha por producto):
        1. Fecha de inicio.
        2. Fecha de fin.
        3. Producto.
    2. Para opción 2 (vencimientos próximos):
        1. Rango de dias hacia adelante (por ejemplo, "15 dias")
    3. Para opción 3 (evolucion de stock):
        1. Tipo periodo (semana, mes, trimestre, anio).
        2. Fecha de inicio del periodo.
        3. Producto.
5. Validar datos.
6. Establecer conexion con el dw.
7. Enviar la consulta con los parámetros correspondientes.
8. Procesar los datos y construir el reporte en una estructura clara (tabla, grafico, etc.).
9. Cerrar conexion con el dw.
10. Mostrar el resultado al usuario.
11. Preguntar al usuario si desea exportar el reporte.
    1. Si la respuesta es si, pedir el formato deseado (PDF, Excel, etc.)
        1. Generar y descargar el archivo
12. FIN.



## Pseudocódigo
```
INICIO


PROCEDIMIENTO Generar_Reporte()
    IMPRIMIR "Seleccione el tipo de reporte que desea:"
    IMPRIMIR "Opción 1: Reporte de ingresos por fecha por producto."
    IMPRIMIR "Opción 2: Reporte de vencimientos próximos."
    IMPRIMIR "Opción 3: Reporte de evolucion de stock de un producto por periodo."

    PEDIR eleccion

    SEGUN eleccion
        CASO 1
            PEDIR fecha_inicio
            PEDIR fecha_fin
            PEDIR producto
            Validar_Fechas(fecha_inicio, fecha_fin)
        CASO 2
            PEDIR rango_dias
        CASO 3
            PEDIR tipo_periodo
            PEDIR fecha_inicio
            PEDIR producto
    
    Iniciar_Conexion_DW()

    SEGUN eleccion
        CASO 1
            Validar_Producto(producto)
            Reporte_Ingresos_Producto(fecha_inicio, fecha_fin, producto)
        CASO 2
            Reporte_Vencimientos(rango_dias)
        CASO 3
            Validar_Producto(producto)
            Reporte_Evolucion_Stock(tipo_periodo, fecha_inicio, producto)

    Cerrar_Conexion_DW()

    IMPRIMIR "En que formato desea el reporte?"
    IMPRIMIR "1. CSV"
    IMPRIMIR "2. PDF"
    IMPRIMIR "3. ..."
    PEDIR formato

    Exportar_Reporte(formato)

FIN PROCEDIMIENTO

    
// SUB-PROCEDIMIENTOS

PROCEDIMIENTO Validar_Fechas(fecha_inicio, fecha_fin)
    SI fecha_inicio > fecha_fin
        ERROR "La fecha de inicio no puede ser superior a la fecha de fin"
FIN PROCEDIMIENTO


PROCEDIMIENTO Validar_Producto(producto)
    SI producto no existe en DW
        ERROR "El producto no existe"
FIN PROCEDIMIENTO


PROCEDIMIENTO Iniciar_conexion_DW()
    VARIABLE GLOBAL conexion_dw = Conectar("cadena de conexion al dw")
    SI conexion_dw ES NULO
        ERROR "No se pudo establecer conexion"
    FIN SI
FIN PROCEDIMIENTO


PROCEDIMIENTO Cerrar_Conexion_DW()
    SI conexion_dw NO ES NULO
        conexion_dw.Cerrar()
    FIN SI   
FIN PROCEDIMIENTO


PROCEDIMIENTO Reporte_Ingresos_Producto(fecha_inicio, fecha_fin, producto)
    sql = "query"
    VARIABLE GLOBAL ultimo_reporte_generado = Ejecutar_consulta(conexion_dw, sql)
FIN PROCEDIMIENTO


PROCEDIMIENTO Reporte_Vencimientos(rango_dias)
    sql = "query"
    VARIABLE GLOBAL ultimo_reporte_generado = Ejecutar_consulta(conexion_dw, sql)
FIN PROCEDIMIENTO


PROCEDIMIENTO Reporte_Evolucion_Stock(tipo_periodo, fecha_inicio, producto)
    sql = "query"
    VARIABLE GLOBAL ultimo_reporte_generado = Ejecutar_consulta(conexion_dw, sql)
FIN PROCEDIMIENTO


PROCEDIMIENTO Exportar_Reporte(formato)
    SEGUN formato
    CASO "CSV"
        Convertir_A_CSV(ultimo_reporte_generado)
        Guardar_Archivo("reporte.csv")
    CASO "PDF"
        Convertir_A_PDF(ultimo_reporte_generado)
        Guardar_Archivo("reporte.pdf")
    DE OTRO MODO
        IMPRIMIR "Formato no válido."
    FIN SEGUN
FIN PROCEDIMIENTO
    

FIN
```