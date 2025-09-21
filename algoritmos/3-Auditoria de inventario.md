# Auditoría de inventario

## Objetivo del módulo

Registrar en un historial todos los movimientos (entradas y salidas) del inventario, incluyendo datos de producto, lote, usuario, fecha y cantidad.

## Algoritmo

1. Obtener los datos del `Movimiento` realizado (id_lote, id_usuario, tipo, fecha, cantidad)
2. Guardar los datos del `Movimiento`
3. Asociar el Lote con el Producto
4. Permitir la visualización de Movimientos con la adición de filtros (rango de fechas, tipo, producto)

## Niveles de refinamiento 

### Nivel 1
1. Se genera una `ENTRADA/SALIDA`
   1. Se obtienen los datos de `id_lote`, `id_usuario`, `tipo`, `fecha`, `cantidad`
   2. Si el lote no existe se rechaza movimiento
   3. Si el usuario no existe rechaza movimiento
2. Se relaciona el `Movimiento` con un `Lote` y `Usuario`
3. Se guardan los datos en la tabla `Movimiento`
4. En la tabla de `Movimiento` tendrá consultas de auditoría por:
   1. Producto
   2. Tipo de movimiento
   3. Rango de fechas

### Nivel 2
1. `capturar_movimiento(Movimiento)`
   1. Elegir el `Lote` por su `id_lote`
   2. Elegir el `Usuario` por su `id_usuario`
   3. Recibir el `tipo` (ingreso/egreso)
   4. Recibir la `cantidad`
2. `registrar_movimiento(Movimiento)`
   1. Guardar la información del `Movimiento` en la tabla de movimientos
3.  `consultar_auditoria()`
   1.  Permitir la consulta de movimientos con filtros:
      1. `id_producto`
      2. `tipo`
      3. `fecha_inicio` y `fecha_fin`
   2. Retornar los movimientos que cumplan con los filtros


## Pseudocódigo

```pseudo
MODULO capturar_movimiento()
   movimiento.id_lote <--- seleccionar_lote()
   movimiento.id_usuario <--- seleccionar_usuario()
   movimiento.tipo <--- recibir_tipo()  // "ingreso" o "egreso"
   movimiento.cantidad <--- recibir_cantidad()
   movimiento.fecha <--- obtener_fecha_actual()
   registrar_movimiento(movimiento)
FIN MODULO

FUNCION registrar_movimiento(movimiento)
   conexion <--- conectar_BD()
   query <--- "INSERT INTO Movimiento (id_lote, id_usuario, fecha, tipo, cantidad)
               VALUES (movimiento.id_lote, movimiento.id_usuario, 
                     movimiento.fecha, movimiento.tipo, movimiento.cantidad)"
   ejecutar_query(query, conexion)
   cerrar_conexion(conexion)
FIN FUNCION


FUNCION consultar_auditoria(filtros)
   conexion <--- conectar_BD()
   query <--- "SELECT M.id_movimiento, P.Nombre, M.tipo, M.cantidad, M.fecha, M.id_usuario
               FROM Movimiento M
               JOIN Lote L ON M.id_lote = L.id_lote
               JOIN Producto P ON L.id_producto = P.id_producto
               WHERE filtros"
   resultados <--- ejecutar_query(query, conexion)
   cerrar_conexion(conexion)
   RETORNAR resultados
FIN FUNCION

```

---
