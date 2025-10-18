# Generación de alertas de stock bajo 

## Objetivo del módulo

- Cuando el stock de un producto sea menor a una cantidad establecida, el sistema deberá alertar al usuario que hay productos en poca cantidad.Le deberá especificar qué producto está por debajo del límite y su cantidad actual. Además, deberá mostrar si es un tipo de alerta de stock bajo o stock en nivel crítico (que ya se encuentra agotado o por debajo del nivel establecido como crítico) registrar la alerta en la base de datos.

## Algoritmo
```pseudo
Para cada producto en la base de datos:
   1) Obtener la cantidad actual de cada producto.
   2) Obtener el valor mínimo que debe haber del producto.
   3) Comparar si la cantidad actual es menor al valor critico.
      - En caso afirmativo:
      4)  Lanzar alerta.
      -Sino:
      5) Comparar si la cantidad actual es menor al valor bajo.
         -En caso afirmativo:
      6) Lanzar alerta.
```
## Niveles de refinamiento

### Nivel 1
```pseudo
 Para cada producto en la base de datos:
   1)
    i) Consultar la cantidad actual en los lotes asociados.
    ii) Guardar la suma de cantidades como cantidad_actual.
    2) 
       i) Tomar el valor del campo stock_minimo del producto.
    3) 
        i) Si cantidad_actual < stock_minimo entonces:
            4)
                i) Generar un registro con los datos de la alerta.
                ii) Mostrar la alerta.
               iii) Guardar alerta en la base de datos.
```
### Nivel 2
```pseudo
 Para cada producto en la base de datos:
      1)
        i) Buscar_lotes(id_producto):
            a) Establecer conexión con la base de datos.
            b) Hacer una query: SELECT cantidad FROM Lote WHERE id_producto = id_producto.
        ii) Guardar resultado en la variable cantidad_actual.

    2)Buscar_producto(id_producto):
        i) Hacer una query: SELECT stock_minimo FROM Producto WHERE id_producto = id_producto.
        ii) Guardar el valor en la variable stock_minimo.

    3)
        i) Si cantidad_actual < stock_minimo entonces:
            4)
                i) Generar un registro con datos de la alerta:
                    a) Nombre del producto.
                    b) Cantidad actual.
                    c) Diferencia = {stock_minimo - cantidad_actual}.
                ii) Mostrar la alerta.
               iii) Guardar alerta en la base de datos.
```
## Pseudocódigo

```pseudo
MODULO verificar_stock()
            PARA CADA producto EN productos HACER
                cantidad_actual <--- buscar_lotes(producto.id)
                stock_minimo <--- buscar_stock_minimo(producto.id)

                SI cantidad_actual < stock_minimo ENTONCES
                    alerta <--- crear_alerta(producto.id, cantidad_actual, stock_minimo)
                    mostrar_alerta(alerta)
                    guardar_alerta(alerta)
                FIN SI
        FIN SI
    FIN MIENTRAS
FIN MODULO



FUNCION buscar_lotes(id_producto)
    establecer_conexion_BD()
    query <--- "SELECT cantidad FROM Lote WHERE id_producto = id_producto"
    cantidad_actual <--- ejecutar_query(query)
    RETORNAR cantidad_actual
FIN FUNCION


FUNCION buscar_stock_minimo(id_producto)
    establecer_conexion_BD()
    query <--- "SELECT stock_minimo FROM Producto WHERE id_producto = id_producto"
    stock_minimo <--- ejecutar_query(query)
    RETORNAR stock_minimo
FIN FUNCION


FUNCION crear_alerta(id_producto, cantidad_actual, stock_minimo)
    alerta <--- nuevo_registro()
    alerta.id_producto <--- id_producto
    alerta.nombre_producto <--- obtener_nombre_producto(id_producto)
    alerta.cantidad_actual <--- cantidad_actual
    alerta.diferencia <--- stock_minimo - cantidad_actual
    alerta.mensaje <--- "Stock bajo: Debería comprar " + alerta.diferencia
    RETORNAR alerta
FIN FUNCION


PROCESO mostrar_alerta(alerta)
    IMPRIMIR "Advertencia: Stock Bajo"
    IMPRIMIR "Producto: " + alerta.nombre_producto
    IMPRIMIR "Cantidad actual: " + alerta.cantidad_actual
    IMPRIMIR alerta.mensaje
FIN PROCESO

PROCESO guardar_alerta(alerta)
    establecer_conexion_BD()
    query <--- " INSERT INTO Alerta (id_producto, fecha, cantidad, descripcion) VALUES ( alerta.id_producto, alerta.fecha, alerta.cantidad_actual, alerta.mensaje)"
    ejecutar_query(query)
FIN PROCESO

```
---
