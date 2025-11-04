# Actualización de niveles de stock

## Objetivo del módulo

Registrar movimientos y actualizar el stock.

## Algoritmo

Es llamado cada vez que se realiza un movimiento. Recibe como entrada los parámetros del movimiento.
Crea una entrada en la tabla de movimientos y crea o modifica una entrada en la tabla de stock.
Esto se realiza en una única transacción.

## Niveles de refinamiento

### Nivel 1

```
actualizar_stock(pid_movimiento, pid_lote, pid_usuario, ptipo, pcantidad, pfecha)

1.  Registrar el movimiento en la tabla de movimientos.
2.  Actualizar el stock del producto implicado.
```

### Nivel 2

```
actualizar_stock(pid_movimiento, pid_lote, pid_usuario, ptipo, pcantidad, pfecha)

2.1.  Seleccionar el id_producto del lote con id = pid_lote en la tabla de lotes.
2.2.  Si ptipo es ingreso,
    2.3.  Actualizar la entrada en la tabla de stock con ese id_producto, sumando pcantidad a la columna cantidad.
2.4.  Si ptipo es egreso,
    2.5.  Actualizar la entrada en la tabla de stock con ese id_producto, restando pcantidad a la columna cantidad.
```

## Pseudocódigo

```
PROCEDIMIENTO actualizar_stock(pid_movimiento, pid_lote, pid_usuario, ptipo, pcantidad, pfecha)

    INSERT INTO movimientos VALUES (pid_movimiento, pid_lote, pid_usuario, ptipo, pcantidad, pfecha)

    pid_producto ← SELECT id_producto FROM lotes WHERE id_lote = pid_lote

    SI ptipo = 1 ENTONCES
        UPDATE stock WHERE id_producto = pid_producto SET stock.cantidad = stock.cantidad + pcantidad
    FINSI

    SI ptipo = 0 ENTONCES
        UPDATE stock WHERE id_producto = pid_producto SET stock.cantidad = stock.cantidad - pcantidad
    FINSI

FIN PROCEDIMIENTO
```
