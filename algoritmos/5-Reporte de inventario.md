# Reporte de inventario

## Objetivo del módulo
Generar reportes generales por periodo (dia, semana, mes, etc.) sobre el estado y movimientos del inventario para controlar existencias, analizar tendencias y apoyar la toma de decisiones para optimizar las compras, almacenamiento y distribucion.


## Algoritmo
1. Solicitar al usuario el periodo del que desea obtener el reporte. (dia, semana o mes)
2. Consultar los datos requeridos de la base de datos
3. Procesar la informacion para cada producto: stock actual, ingresos, egresos, vencimientos y comparaciones con ciclo anterior.
4. Generar el reporte con todos los indicadores.
5. Mostrar el reporte al usuario.


## Niveles de refinamiento 

### Nivel 1
1. Entrada de datos
    - Determinar tipo de periodo y su fecha inicial y final
2. Obtencion de informacion
    - Consultar productos
    - Consultar lotes
    - Consultar movimientos
3. Procesamiento de datos
    - Obtener stock actual
    - Procesar ingresos y egresos, actuales y del periodo anterior
    - Encontrar lote con vencimiento mas proximo
4. Generacion del reporte
    - Crear tabla de resultados con columnas | Producto | Inventario actual | Ingresos | Egresos | % Ingresos vs ciclo anterior | % Egresos vs ciclo anterior | Vencido | Lote más próximo a vencer | Fecha más próxima de vencimiento |
5. Salida
    - Mostrar reporte por pantalla
    - Dar opcion a exportar el reporte a otro formato (.txt, excel, etc)


### Nivel 2
1. Entrada de datos
    - Pedir tipo de ciclo (dia, semana o mes)
    - Pedir fecha inicial
    - Calcular fecha final segun fecha inicial y tipo de ciclo
2. Obtencion de informacion
    - Obtener id de todos los productos via tabla de productos
    - Con id de productos obtener los stock actuales via tabla de stock actual
    - Con id de productos obtener los lotes via tabla de lotes
    - Con id de productos obtener los movimientos del periodo actual
    - Con id de productos obtener los movimientos del periodo anterior
3. Procesamiento de datos
    - Obtener stock actual
    - Calcular ingresos = sumar todas las ingresos del periodo
    - Calcular egresos = sumar todos los egresos del periodo
    - Calcular relacion de ingresos respecto al periodo anterior (%)
    - Calcular relacion de egresos respecto al periodo anterior (%)
    - Identificar productos vencidos en el periodo
    - Calcular relacion de vencimientos respecto al periodo anterior (%)
    - Calcular lote con vencimiento mas proximo
    - Obtener fecha de vencimiento mas proxima
4. Generacion del reporte
    - Crear tabla de resultados con columnas | Producto | Inventario actual | Ingresos | Egresos | % Ingresos vs ciclo anterior | % Egresos vs ciclo anterior | Vencido | Lote más próximo a vencer | Fecha más próxima de vencimiento |
5. Salida
    - Mostrar reporte por pantalla
    - Dar opcion a exportar el reporte a otro formato (.txt, excel, etc)

## Pseudocódigo
INICIO

    // 1. Entrada de datos
    PEDIR tipo_ciclo (día, semana, mes)
    PEDIR fecha_inicial
    fecha_final ← CALCULAR_FECHA_FINAL(fecha_inicial, tipo_ciclo)
    fecha_inicial_ca ← CALCULAR_CICLO_ANTERIOR(fecha_inicial, tipo_ciclo)   // ca = ciclo anterior
    fecha_final_ca ← CALCULAR_CICLO_ANTERIOR(fecha_final, tipo_ciclo)       // ca = ciclo anterior

    // 2. Obtención de información
    productos ← CONSULTAR tabla_productos
    stock_actual ← CONSULTAR tabla_stock(productos)
    lotes ← CONSULTAR tabla_lotes(productos)
    movimientos_actual ← CONSULTAR tabla_movimientos(productos, fecha_inicial, fecha_final)
    movimientos_anterior ← CONSULTAR tabla_movimientos(productos, fecha_inicial_ca, fecha_final_ca)

    // 3. Procesamiento de datos
    PARA cada producto EN productos HACER
        stock ← stock_actual[producto]

        ingresos ← SUMAR movimientos_actual.ingresos(producto)
        egresos ← SUMAR movimientos_actual.egresos(producto)

        ingresos_anteriores ← SUMAR movimientos_anterior.ingresos(producto)
        egresos_anteriores ← SUMAR movimientos_anterior.egresos(producto)

        porcentaje_ingresos ← CALCULAR % (ingresos, ingresos_anteriores)
        porcentaje_egresos ← CALCULAR % (egresos, egresos_anteriores)

        vencidos ← IDENTIFICAR lotes vencidos(producto, fecha_inicial, fecha_final)
        lote_proximo ← ENCONTRAR lote con vencimiento más cercano(producto)
        fecha_proxima ← OBTENER fecha de vencimiento más próxima(producto)

        AGREGAR fila a tabla_resultados con:
            Producto, inventario, ingresos, egresos,
            porcentaje_ingresos, porcentaje_egresos,
            vencidos, lote_proximo, fecha_proxima
    FIN PARA

    // 4. Generación del reporte
    CREAR tabla_resultados con las filas de cada producto

    // 5. Salida
    MOSTRAR tabla_resultados en pantalla
    PREGUNTAR si se desea exportar
    SI respuesta = si ENTONCES
        PEDIR formato de exportación
        EXPORTAR reporte en formato seleccionado (.txt, .xls, etc)

FIN
