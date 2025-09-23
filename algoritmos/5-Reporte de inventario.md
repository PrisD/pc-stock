# Reporte de inventario

## Objetivo del módulo
Generar reportes generales por periodo (dia, semana, mes, etc.) sobre el estado y movimientos del inventario para controlar existencias, analizar tendencias y apoyar la toma de decisiones para optimizar las compras, almacenamiento y distribucion.


## Algoritmo
1. Solicitar al usuario el periodo del que desea obtener el reporte. (dia, semana o mes)
2. Consultar los datos de inventario y movimientos del periodo elegido.
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
    - Consultar movimientos periodo actual
    - Consultar movimientos periodo anterior para comparacion
3. Procesamiento de datos
    - Obtener stock actual
    - Obtener ingresos y egresos del periodo actual
    - Otener ingresos y egresos del periodo anterior
    - Obtener cantidad de producto vencido del periodo actual
    - Obtener cantidad de producto vencido del periodo anterior
    - Encontrar lote con vencimiento mas proximo
    - Mostrar fecha de vencimiento mas proxima
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
    - Mostrar fecha de vencimiento mas proxima
4. Generacion del reporte
    - Crear tabla de resultados con columnas | Producto | Inventario actual | Ingresos | Egresos | % Ingresos vs ciclo anterior | % Egresos vs ciclo anterior | Vencido | Lote más próximo a vencer | Fecha más próxima de vencimiento |
5. Salida
    - Mostrar reporte por pantalla
    - Dar opcion a exportar el reporte a otro formato (.txt, excel, etc)

## Pseudocódigo
