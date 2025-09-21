# Sistema de control de Stock 
Pensamiento Computacional
**Grupo 2**


## Índice
- [Sistema de control de Stock](#sistema-de-control-de-stock)
  - [Índice](#índice)
- [Relevamiento del control de inventario](#relevamiento-del-control-de-inventario)
  - [Alcance](#alcance)
  - [Lo que no se contempla](#lo-que-no-se-contempla)
- [Diagrama Entidad Relación](#diagrama-entidad-relación)
- [Módulos](#módulos)
  - [Registro de entrada de mercancías](#registro-de-entrada-de-mercancías)
  - [Actualización de niveles de stock](#actualización-de-niveles-de-stock)
  - [Auditoría de inventario](#auditoría-de-inventario)
  - [Generación de alertas de stock bajo](#generación-de-alertas-de-stock-bajo)
  - [Reporte de inventario](#reporte-de-inventario)


# Relevamiento del control de inventario
Un almacén en el cual se reciben, almacenan y despachan productos de distintas características.  
Los problemas que buscará resolver el sistema son:

- Dificultad para llevar un control exacto de las entradas y salidas de mercancías.
- Riesgo de faltantes de stock al no detectar a tiempo cuando un producto baja de su nivel mínimo.
- Imposibilidad de obtener reportes en tiempo real que reflejen la situación del inventario.
- Alta probabilidad de errores humanos, duplicación de registros o pérdida de información.

## Alcance
El sistema abarcará las siguientes funcionalidades principales:
1. Registro de entrada de mercancías
   - Alta de productos y lotes.
   - Generación de movimientos de ingreso.
2. Actualización de niveles de stock
   - Recalcular stock en tiempo real en base a movimientos.
   - Mantener actualizado un inventario por producto y lote.
3. Auditoría de inventario
   - Registro histórico de todos los movimientos.
   - Identificación de fechas y cantidades.
   - Posibilidad de generar reportes de auditoría por periodo.
4. Generación de alertas de stock bajo
   - Comparación automática con stock mínimo definido.
   - Emisión de alertas cuando un producto alcanza nivel crítico.
   - Gestión de alertas activas y resolución cuando el stock se normaliza.
5. Reportes de inventario
   - Reportes generales y filtrados (por producto, categoría o lote).
   - Visualización de stock actual, movimientos y alertas.
   - Exportación de informes para toma de decisiones.

## Lo que no se contempla
- Gestión de compras ni órdenes automáticas a proveedores.
- No gestiona precios, facturación ni ventas, solo control físico de inventario.
- No cubre logística de transporte ni distribución fuera del almacén.
- No realiza una gestión de usuarios que puedan ingresar al sistema.

---

# Diagrama Entidad Relación
<img width="1045" height="491" alt="Diagrama ER" src="https://github.com/user-attachments/assets/b936f6cf-107e-4fb9-8868-8057b3e34467" />

---


# Módulos
- Registro de entrada de mercancías (Lautaro Stuve)
- Actualización de niveles de stock (Joaquín Terzano) 
- Auditoría de inventario (Priscila Della Vecchia)
- Generación de alertas de stock bajo (Matías Bonesi)
- Reporte de inventario (Agustín Sánchez)

---

## Registro de entrada de mercancías
- Una transacción es una entrada.
**Objetivo del módulo**
**Algoritmo**
**Niveles de refinamiento** 
**Pseudocódigo**

---

## Actualización de niveles de stock
- Hay un algoritmo que modifica la tabla stock a partir de una transacción.
**Objetivo del módulo**
**Algoritmo**
**Niveles de refinamiento** 
**Pseudocódigo**

---

## Auditoría de inventario
- a
**Objetivo del módulo**
**Algoritmo**
**Niveles de refinamiento** 
**Pseudocódigo**

---

## Generación de alertas de stock bajo 
- Cuando el stock de un producto sea menor a una cantidad establecida por el usuario, 
el sistema deberá alertar al usuario que hay productos en poca cantidad.  
Le deberá especificar qué producto está por debajo del límite y su cantidad actual.
**Objetivo del módulo**
**Algoritmo**
**Niveles de refinamiento** 
**Pseudocódigo**


**Algoritmo**
1. Chequear si se produjo un movimiento de egreso.  
   En caso afirmativo:  
   1. Obtener la cantidad actual del producto egresado.  
   2. Obtener el valor mínimo que debe haber del producto.  
   3. Comparar si la cantidad actual es menor al valor mínimo.  
      - En caso afirmativo:  
        1. Lanzar alerta.  

**Niveles de refinamiento**

**Nivel 1**
1. Si se utilizó el módulo de registro de mercancías:  
   i) Evaluar si el campo del movimiento está seteado como ingreso o egreso.  
   ii) En caso afirmativo pasar al siguiente paso.  
2. i) Del movimiento de egreso registrado, chequear el campo id del lote.  
   ii) Buscar el lote del producto por su id, devolver el valor del campo cantidad.  
3. i) Del lote del producto, chequear el campo id del producto.  
   ii) Buscar el producto por su id, devolver el valor del campo stock mínimo.  
4. i) Si `cantidad_actual < stock_minimo` entonces:  
5. i) Generar un registro con datos de la alerta.  
   ii) Mostrarla al usuario.  

**Nivel 2**
1. i) Del movimiento de egreso, chequear el campo id del lote.  
   ii) `buscar_lote(id_lote)`:  
   a) Establecer conexión con la base de datos.  
   b) Hacer una query consultando por el valor de cantidad.  
   c) Guardar el valor en la variable `cantidad_actual`.  

2. i) Del lote del producto:  
   a) Hacer una query consultando el valor de `id_producto`.  
   ii) `buscar_producto(id_producto)`:  
   a) Hacer una query sobre la tabla producto consultando el valor de `stock_minimo`.  
   b) Guardar el valor en la variable `stock_minimo`.  

3. i) Generar un registro con datos de la alerta:  
   a) Almacenar en un campo el nombre del producto.  
   b) Almacenar en un campo la cantidad actual.  
   c) Hacer `stock_minimo - cantidad_actual` y guardarlo en un campo.  
   ii) Mostrarla al usuario mediante un pop-up:  
   a) Título: *Advertencia*.  
   b) Mostrar nombre del producto.  
   c) Mostrar cantidad actual.  
   d) Mostrar mensaje `"Debería comprar: {stock_minimo - cantidad_actual}"`.  

**Pseudocódigo**

```pseudo
MODULO generar_alerta_stock_bajo(movimiento)
    SI movimiento.tipo == "egreso" ENTONCES:
        id_lote <--- movimiento.id_lote
        cantidad_actual <--- buscar_lote(id_lote)

        id_producto <--- obtener_producto_de_lote(id_lote)
        stock_minimo <--- buscar_producto(id_producto)

        SI cantidad_actual < stock_minimo ENTONCES:
            alerta <--- crear_alerta(id_producto, cantidad_actual, stock_minimo)
            mostrar_pop_up(alerta)
        FIN SI
    FIN SI
FIN MODULO

FUNCION buscar_lote(id_lote)
    establecer_conexion_BD()
    query <--- "SELECT cantidad FROM Lote WHERE id_lote = id_lote"
    cantidad <--- ejecutar_query(query)
    RETORNAR cantidad
FIN FUNCION

FUNCION obtener_producto_de_lote(id_lote)
    query <--- "SELECT id_producto FROM Lote WHERE id_lote = id_lote"
    id_producto <--- ejecutar_query(query)
    RETORNAR id_producto
FIN FUNCION

FUNCION buscar_producto(id_producto)
    query <--- "SELECT stock_minimo FROM Producto WHERE id_producto = id_producto"
    stock_minimo <--- ejecutar_query(query)
    RETORNAR stock_minimo
FIN FUNCION

FUNCION crear_alerta(id_producto, cantidad_actual, stock_minimo)
    alerta <--- nuevo_registro()
    alerta.nombre_producto <--- obtener_nombre_producto(id_producto)
    alerta.cantidad_actual <--- cantidad_actual
    alerta.diferencia <--- stock_minimo - cantidad_actual
    alerta.mensaje <--- "Debería comprar: " + alerta.diferencia
    RETORNAR alerta
FIN FUNCION

PROCESO mostrar_pop_up(alerta)
    TITULO <--- "Advertencia"
    MOSTRAR TITULO
    MOSTRAR "Producto: " + alerta.nombre_producto
    MOSTRAR "Cantidad actual: " + alerta.cantidad_actual
    MOSTRAR alerta.mensaje
FIN PROCESO
```
---

## Reporte de inventario
- a
  **Objetivo del módulo**
**Algoritmo**
**Niveles de refinamiento** 
**Pseudocódigo**
