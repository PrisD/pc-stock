# Actualización de niveles de stock

## Objetivo del módulo
Este módulo se ejecuta de forma periódica (por ejemplo una vez al día) para detectar si un lote ha vencido.

(Opcional). Calcula el stock actual de cada producto. Requiere una tabla de stock.

## Algoritmo
El algoritmo encuentra todos los lotes no marcados que, en la fecha de su ejecución, están vencidos y los marca (cómo?).

(Opcional). Calcula el stock actual de cada producto y actualiza la tabla de stock.

## Niveles de refinamiento 

### Nivel 1
```
1.  Marcar lotes vencidos para cada producto.
2.  (Opcional). Calcular stock para cada producto.
```

### Nivel 2
```
1.  Marcar lotes vencidos para cada producto.
  1.1.  Seleccionar la tabla de lotes en orden ascendente respecto de la fecha de vencimiento.
  1.2.  Para cada producto,
    1.3.  Repetir
      1.4.  Filtrar la tabla seleccionada para que muestre los lotes sin marcar del producto.
      1.5.  Seleccionar el lote con la menor fecha de vencimiento en la tabla (la primera entrada).
      1.6.  Si la fecha actual es menor que la fecha de vencimiento del lote (el lote está vencido),
        1.7.  Marcar el lote.
    1.8.  Hasta que la fecha actual sea mayor o igual a la fecha de vencimiento.

2.  (Opcional). Calcular stock para cada producto.
  2.1.  Seleccionar la tabla de movimientos filtrada para que muestre los movimientos con lotes sin marcar.
  2.2.  Para cada producto,
    2.3.  Filtrar la tabla seleccionada para que muestre los movimientos del producto.
    2.4.  Acumular en una variable la cantidad de todos los movimientos de la tabla.
    2.5.  Actualizar la entrada del producto en tabla de stock con la cantidad acumulada.
```

## Pseudocódigo
```
PROCEDIMIENTO ActualizarNivelesDeStock()

    // Marcar lotes vencidos
    listaLotes ← SeleccionarTodos("Lote", ordenPor = "fecha_vencimiento ASC")

    PARA CADA producto EN Tabla("Producto") HACER
        lotesProducto ← Filtrar(listaLotes, 
                                condicion = (lote.idProducto = producto.id) 
                                            Y (lote.vencido = FALSO))

        PARA CADA lote EN lotesProducto HACER
            SI FechaActual() >= lote.fecha_vencimiento ENTONCES
                lote.vencido ← VERDADERO
                Actualizar("Lote", lote)
                RegistrarAuditoria("Lote vencido", producto.id, lote.id)
            FIN SI
        FIN PARA
    FIN PARA


    //  Calcular stock actual de cada producto 
    SI CalcularStock = VERDADERO ENTONCES
        movimientos ← SeleccionarTodos("Movimiento", 
                                       condicion = (lote.vencido = FALSO))

        PARA CADA producto EN Tabla("Producto") HACER
            movimientosProducto ← Filtrar(movimientos, 
                                           condicion = (movimiento.idProducto = producto.id))

            cantidadTotal ← 0

            PARA CADA mov EN movimientosProducto HACER
                cantidadTotal ← cantidadTotal + mov.cantidad
            FIN PARA

            registroStock ← Buscar("Stock", condicion = (stock.idProducto = producto.id))

            SI registroStock EXISTE ENTONCES
                registroStock.cantidad_actual ← cantidadTotal
                Actualizar("Stock", registroStock)
            SINO
                nuevoStock ← CrearRegistro("Stock", {
                    idProducto: producto.id,
                    cantidad_actual: cantidadTotal
                })
                Insertar("Stock", nuevoStock)
            FIN SI

            RegistrarAuditoria("Stock actualizado", producto.id, NULL)
        FIN PARA
    FIN SI

FIN PROCEDIMIENTO
```
