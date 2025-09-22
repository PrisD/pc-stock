# Actualización de niveles de stock

## Objetivo del módulo
Este módulo se ejecuta de forma periódica para detectar si un lote ha vencido.

## Algoritmo
El algoritmo encuentra todos los lotes no marcados que, en la fecha de su ejecución, están vencidos y los marca.

## Niveles de refinamiento 

### Nivel 1
```
1.  Seleccionar la tabla de lotes en orden ascendente respecto de la fecha de vencimiento.
2.  Comprobar vencimiento para cada producto.
```

### Nivel 2
```
2.  Comprobar vencimiento para cada producto.
  2.1.  Para cada producto,
    2.2.  Repetir
      2.3.  Filtrar la tabla seleccionada para que muestre los lotes sin marcar del producto.
      2.4.  Seleccionar el lote con la menor fecha de vencimiento en la tabla.
      2.5.  Si la fecha actual es menor que la fecha de vencimiento del lote (el lote está vencido),
        2.6.  Marcar el lote.
    2.7.  Hasta que la fecha actual sea mayor o igual a la fecha de vencimiento.
```

## Pseudocódigo
