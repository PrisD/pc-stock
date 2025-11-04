# Generación de alertas de stock bajo 

## Objetivo del módulo

- Cuando el stock de un producto sea menor a una cantidad establecida, el sistema deberá alertar al usuario que hay productos en poca cantidad.Le deberá especificar qué producto está por debajo del límite y su cantidad actual. Además, deberá mostrar si es un tipo de alerta de stock bajo, stock en nivel crítico (que ya se encuentra por debajo del nivel establecido como crítico) o stock completamente agotado. Finalmente, se registra la alerta en la base de datos.

## Algoritmo
```pseudo
Para cada producto en la base de datos:
   1) Obtener la cantidad actual de cada producto.
   2) Obtener el valor mínimo que debe haber del producto.
   3) Según la cantidad actual hacer:
      Caso igual 0 :
            4) Lanzar alerta stock agotado.
      Caso cantidad actual < nivel critico:
            5) Lanzar alerta stock crítico.
      Caso cantidad actual < nivel bajo:
            6) Lanzar alerta de stock bajo.
      Otro caso:
            7) No se genera alerta.
   
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
        i) Según la cantidad actual hacer:
            Caso == 0:
                4)
                    i) Generar registro de alerta tipo “STOCK AGOTADO”.
                    ii) Mostrar mensaje al usuario.
                    iii) Guardar alerta en la base de datos.
            Caso < stock_critico:
                5)
                    i) Generar registro de alerta tipo “STOCK CRITICO”.
                    ii) Mostrar mensaje al usuario.
                    iii) Guardar alerta en la base de datos.
            Caso < stock_bajo:
                6)
                    i) Generar registro de alerta tipo “STOCK BAJO”.
                    ii) Mostrar mensaje al usuario.
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
         i) Según cantidad_actual hacer:
            Caso == 0:
             4)
               i) Generar un registro con datos de la alerta:
                tipo_alerta ← "AGOTADO"
                alerta ← crear_alerta(id_producto, cantidad_actual, tipo_alerta)
                mostrar_alerta(alerta)
                guardar_alerta(alerta)
            Caso cantidad_actual < stock_critico:
                tipo_alerta ← "CRITICO"
                alerta ← crear_alerta(id_producto, cantidad_actual, tipo_alerta)
                mostrar_alerta(alerta)
                guardar_alerta(alerta)
            Caso cantidad_actual < stock_bajo:
                tipo_alerta ← "BAJO"
                alerta ← crear_alerta(id_producto, cantidad_actual, tipo_alerta)
                mostrar_alerta(alerta)
                guardar_alerta(alerta)

```
## Pseudocódigo

```pseudo
MODULO verificar_stock()
    productos <--traer_productos() 
    PARA CADA producto EN productos HACER
        cantidad_actual <--- buscar_stock(producto.id)
        (stock_bajo, stock_critico) <--- buscar_limites_stock(producto.id)

        SEGUN cantidad_actual HACER
            CASO 0:
                tipo_alerta <--- "AGOTADO"
                lanzar_alerta(producto,tipo_alerta)
            CASO CUANDO cantidad_actual < stock_critico:
                tipo_alerta <--- "CRITICO"
                lanzar_alerta(producto,tipo_alerta)
            CASO CUANDO cantidad_actual < stock_bajo:
                tipo_alerta <--- "BAJO"
                lanzar_alerta(producto,tipo_alerta)
        FIN SEGUN
        FIN SI
    FIN PARA
FIN MODULO

FUNCION traer_productos()
    establecer_conexion_BD()
    query <--- "SELECT * FROM Productos"
    lista_productos <--- ejecutar_query(query)
    RETORNAR lista_productos

FUNCION buscar_stock(id_producto)
    establecer_conexion_BD()
    query <--- "SELECT cantidad FROM stock WHERE id_producto = id_producto"
    cantidad_actual <--- ejecutar_query(query)
    RETORNAR cantidad_actual
FIN FUNCION


FUNCION buscar_limites_stock(id_producto)
    establecer_conexion_BD()
    query <--- "SELECT stock_bajo, stock_critico FROM Producto WHERE id_producto = id_producto"
    (stock_bajo, stock_critico) <--- ejecutar_query(query)
    RETORNAR (stock_bajo, stock_critico)
FIN FUNCION

PROCESO lanzar_alerta()
   alerta <--- crear_alerta(producto.id, cantidad_actual, tipo_alerta)
   mostrar_alerta(alerta)
   guardar_alerta(alerta)

FUNCION crear_alerta(id_producto, cantidad_actual, tipo_alerta)
    alerta <--- nuevo_registro()
    alerta.id_producto <--- id_producto
    alerta.nombre_producto <--- obtener_nombre_producto(id_producto)
    alerta.cantidad_actual <--- cantidad_actual
    alerta.tipo_alerta <--- tipo_alerta
    alerta.mensaje <--- "Alerta de stock " + tipo_alerta + 
                        ": cantidad actual " + cantidad_actual
    RETORNAR alerta
FIN FUNCION


PROCESO mostrar_alerta(alerta)
    IMPRIMIR "Alerta de Stock " + alerta.tipo_alerta
    IMPRIMIR "Producto: " + alerta.nombre_producto
    IMPRIMIR "Cantidad actual: " + alerta.cantidad_actual
    IMPRIMIR alerta.mensaje
FIN PROCESO


PROCESO guardar_alerta(alerta)
    establecer_conexion_BD()
    query <--- "INSERT INTO Alerta (id_producto, fecha, cantidad, tipo_alerta, descripcion) " +
               "VALUES (alerta.id_producto, alerta.fecha, alerta.cantidad_actual, alerta.tipo_alerta, alerta.mensaje)"
    ejecutar_query(query)
FIN PROCESO


```
---
