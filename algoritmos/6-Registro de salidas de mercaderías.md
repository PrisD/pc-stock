# Registro de entrada de mercancías

## Objetivo del módulo
Registrar en la tabla de movimientos las salidas de mercaderías y actualizar la tabla de lotes.

## Algoritmo
Recibe como parámetro el ID del producto vendido, la cantidad y la fecha.

Selecciona los lotes con la menor fecha de vencimiento para descontar la cantidad vendida y generar los movimientos correspondientes.

## Niveles de refinamiento

### Nivel 1
```
1.  Actualiza la tabla de lotes para descontar la mercadería que sale.
2.  Añade las entradas en la tabla de movimientos con la salida de mercaderías.
```

### Nivel 2
```
1.  Actualiza la tabla de lotes para descontar la mercadería que sale.
  1.1.  Selecciona la tabla de lotes filtrada para mostrar los lotes sin marcar del producto vendido en orden ascendente respecto de la fecha de vencimiento.
  1.2.  Poner la bandera de salida del bucle en falso.
  1.3.  Repetir
    1.4.  Acumular en una variable la cantidad en el lote con la menor fecha de vencimiento.
    1.5.  Si esta cantidad es menor que la cantidad vendida,
      1.6.  Marcar el lote como vendido.
    1.7.  Si no,
      1.8.  Actualizar la cantidad en el lote como la cantidad acumulada menos la cantidad vendida.
      1.9.  Poner la bandera de salida del bucle en verdadero.
  1.10. Hasta que la bandera de salida del bucle así lo determine.

2.  Añade las entradas en la tabla de movimientos con la salida de mercaderías.
```

## Pseudocódigo
