# Chequeo de vencimiento de mercaderías

## Objetivo del módulo

Registrar los lotes vencidos en cada día.

## Algoritmo

Se ejecuta de forma periódica una vez al día.
Encuentra todos los lotes activos que están vencidos.
Por cada lote vencido, modifica una entrada en la tabla de lotes para registrar el hecho.

## Niveles de refinamiento

### Nivel 1

```
1.  Registrar los lotes vencidos desde su última ejecución.
```

### Nivel 2

```
      Repetir
    1.1.  Seleccionar la tabla de lotes.
    1.2.  Filtrar la tabla seleccionada para que muestre los lotes activos.
    1.3.  Ordenar la tabla respecto de la fecha de vencimiento en orden ascendente.
    1.4.  Seleccionar el lote con la menor fecha de vencimiento en la tabla (la primera entrada).
    1.5.  Si la fecha actual es mayor que la fecha de vencimiento del lote (el lote está vencido),
        1.6.  Cambiar el estado del lote de activo a vencido.
1.7.  Hasta que la fecha actual sea menor o igual a la fecha de vencimiento.
```

## Pseudocódigo

```
PROCEDIMIENTO chequear_vencimiento()

    fecha_actual ← obtener_fecha_actual()

    REPETIR
        vid_lote, vfecha_vencimiento ← SELECT id_lote, fecha_vencimiento FROM lotes WHERE estado = 'activo' ORDER BY fecha_vencimiento ASC LIMIT 1
        SI fecha_actual > vfecha_vencimiento ENTONCES
            UPDATE lotes WHERE id_lote = vid_lote SET estado = 'vencido'
        FINSI
    HASTA fecha_actual <= vfecha_vencimiento

FIN PROCEDIMIENTO
```
