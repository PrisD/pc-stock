# Registro de entrada de mercancías

## Objetivo del módulo
Diseñar e implementar un módulo que permita registrar de manera precisa y automatizada los movimientos de ingresos de mercancías en el almacén, garantizando su trazabilidad mediante el registro del usuario, fecha, lote, tipo de movimiento y cantidad.
El módulo deberá:
    Asegurar la correcta captura de la información del producto (nombre, descripción y stock mínimo).
    Registrar los datos del lote asociado (producto, fecha de vencimiento, cantidad).
    Generar un movimiento inmutable para cada operación, que quedará como respaldo para auditorías.
    Preparar y enviar la información registrada al módulo de actualización de stock, encargado de validar y reflejar los cambios en el inventario.
Este módulo no modifica directamente el stock, sino que se centra en garantizar la integridad de la información registrada, la inmutabilidad de los movimientos y la disponibilidad de datos consistentes para la gestión posterior del inventario.


## Algoritmo
    1- Repetir mientras el usuario quiera ingresar movimientos o crear productos:
    
        1.1 Si desea crear un producto:
    
            1.1- Solicitar y registrar datos del producto asociado.
        
        1.2- Si desea ingresar un movimiento:
        
            1.2.1- Seleccionar producto existente en el sistema o solicitar los datos y crear uno nuevo.
            
            1.2.2- Seleccionar un lote existente en el sistema o solicitar los datos y crear uno nuevo.
    
            1.2.3- Solicitar y registrar datos del movimiento.

## Niveles de refinamiento 

### Nivel 1
    1- Repetir mientras el usuario quiera ingresar movimientos o crear productos:
    
        1.1. Si el usuario desea crear un producto:
            CrearProducto():
                1.1.1. Ingresar nombre del producto.
                1.1.2. Ingresar descripción del producto.
                1.1.3. Ingresar cantidad de stock mínimo.
                1.1.4. Verificar que los datos sean válidos y que no exista duplicado.
                1.1.5. Guardar producto en la base de datos.
    
        1.2. Si el usuario desea registrar un movimiento de ingreso:
    
            CrearIngreso():
            
                1.2.1. Seleccionar producto:
                    - Si ya existe: elegir de la base de datos.
                    - Si es nuevo: llamar a CrearProducto().
    
                1.2.2. Seleccionar o crear lote:
                    - Si el lote ya existe: seleccionarlo.
                    - Si no existe: 
                        CrearLote():
                            1.2.2.1. Asociar ID del producto.
                            1.2.2.2. Ingresar fecha de vencimiento.
                            1.2.2.3. Ingresar cantidad inicial del lote.
                            1.2.2.4. Validar datos.
                            1.2.2.5. Guardar lote en la base de datos.
    
                1.2.3. Crear movimiento de ingreso:
                    CrearMovimiento():
                        1.2.3.1. Asociar ID del lote.
                        1.2.3.2. Asociar tipo de movimiento = "ingreso".
                        1.2.3.3. Ingresar fecha del movimiento.
                        1.2.3.4. Ingresar cantidad del movimiento (no forzar a que sea igual a la del lote).
                        1.2.3.5. Guardar movimiento en la base de datos.
    
        1.3. Si el usuario desea registrar un movimiento de egreso:
            RegistrarSalidasDeMercancia()

        1.4 Preguntar al usuario si desea continuar ingresando movimientos o creando productos.

### Nivel 2
Nivel  2 refinamiento

    Repetir mientras el usuario desee crear productos o registrar movimientos:

    Si desea crear un producto:
    1.1. CrearProducto():
    
        1.1.1. Ingresar nombre del producto.
            1.1.1.1 . Validar que no esté vacío, que no exceda 30 caracteres y que no exista ya en la base de datos.
            
        1.1.2. Ingresar descripción del producto (texto opcional, máx. 100 caracteres).
            1.1.2.1 . Validar que no exceda 100 caracteres.
            
        1.1.3. Ingresar stock mínimo (entero mayor o igual a 0).
            1.1.3.1 . Validar que sea un número entero >= 0.
            
        1.1.5. Si todo es válido:
            Guardar producto en la base de datos.

    Si desea registrar un movimiento:
    1.2. CrearIngreso():
    
        1.2.1. Seleccionar producto:

            Si existe: elegirlo de la base de datos.
            Si no existe: ejecutar CrearProducto (1.1).
        
        1.2.2. Seleccionar o crear lote:

            Si existe: elegirlo de la base de datos.
                1.2.5. Ingresar cantidad a agregar al lote.
                1.2.4. Actualizar cantidad del lote sumando la cantidad ingresada.
                
            Si no existe: CrearLote(id del producto):

                1.2.2.1. Asociar ID del producto.

                1.2.2.2. Ingresar fecha de vencimiento:
                    1.2.2.2.1 . Validar formato dd/mm/aaaa y que sea futura.

                1.2.2.3. Ingresar cantidad inicial del lote:
                    1.2.2.2.3.1 . Validar que sea un número entero > 0.

                1.2.2.5. Guardar lote en la base de datos.
                
        1.2.3. CrearMovimiento(id del lote, ingreso):

            1.2.3.1. Asociar ID del lote.

            1.2.3.2. Tipo = ingreso.

            1.2.3.3. Ingresar fecha del movimiento:
                1.2.3.3.1 . Validar formato dd/mm/aaaa y que no sea futura.

            1.2.3.4. Ingresar cantidad del movimiento:
                1.2.3.4.1 . Validar que sea un número entero > 0.

            1.2.3.5. Guardar movimiento en la base de datos.
            

    1.3. Registrar Movimiento de Egreso:
        1.3.1. Seleccionar producto desde la base de datos.
        1.3.2. Seleccionar lote disponible (con stock suficiente).
        1.3.3. Crear movimiento de egreso:

            1.3.3.1. Asociar ID del lote.

            1.3.3.2. Tipo = "egreso".

            1.3.3.3. Ingresar fecha del movimiento (formato dd/mm/aaaa, no futura).

            1.3.3.4. Ingresar cantidad del movimiento (entero > 0, no mayor al stock del lote).

            1.3.3.5. Guardar movimiento en la base de datos.
            
        1.3.4. Actualizar cantidad del lote restando la cantidad egresada.
        
    1.4 Preguntar al usuario si desea continuar ingresando movimientos o creando productos.
        
## Pseudocódigo

    INICIO MóduloRegistro
    
        seguir = VERDADERO
    
        MIENTRAS seguir == VERDADERO:
    
            MOSTRAR "Selecciona una opcion:"
            MOSTRAR "1 - Crear Producto"
            MOSTRAR "2 - Registrar Movimiento de Ingreso"
            MOSTRAR "3 - Registrar Movimiento de Egreso"
            MOSTRAR "4 - Salir"
            opcion = INGRESAR()
    
            CASE:
    
                CASO 1:
                    CrearProducto()
    
                CASO 2:
                    CrearIngreso()
    
                CASO 3:
                    CrearEgreso()
    
                CASO 4:
                    seguir = FALSO
    
                OTRO:
                    MOSTRAR "Opcion invalida."
    
            
    
    FUNCION CrearProducto()
        INGRESAR nombre_producto
        MIENTRAS nombre_producto = "" O LONG(nombre_producto) > 30 O existeProducto(nombre_producto)
            MOSTRAR "Nombre invalido o ya existente."
            INGRESAR nombre_producto
    
        INGRESAR descripcion_producto
        MIENTRAS LONG(descripcion_producto) > 100
            MOSTRAR "Descripcion demasiado larga."
            INGRESAR descripcion_producto
    
        INGRESAR stock_minimo
        MIENTRAS stock_minimo < 0
            MOSTRAR "El stock minimo debe ser ≥ 0."
            INGRESAR stock_minimo
    
        GuardarProducto(nombre_producto, descripcion_producto, stock_minimo)
        
        MOSTRAR "Producto guardado correctamente."
        
        RETORNAR id_producto
    
    
    
    FUNCION CrearIngreso()
        id_producto = SeleccionarProducto()
        SI id_producto == NULO ENTONCES
            id_producto = CrearProducto()
    
        id_lote = SeleccionarLote(id_producto)
        SI id_lote == NULO ENTONCES
            id_lote = CrearLote(id_producto)
        SINO
            INGRESAR cantidad_a_agregar
            MIENTRAS cantidad_a_agregar ≤ 0
                MOSTRAR "Debe ingresar una cantidad valida."
                INGRESAR cantidad_a_agregar
            ActualizarCantidadLote(id_lote, cantidad_a_agregar)
    
        CrearMovimiento(id_lote, 1)  # 1 para ingreso
    
    
    FUNCION CrearLote(id_producto)
        INGRESAR fecha_vencimiento
        MIENTRAS no FormatoValido(fecha_vencimiento) O fecha_vencimiento ≤ FechaActual()
            MOSTRAR "Fecha invalida. Debe ser futura."
            INGRESAR fecha_vencimiento
    
        INGRESAR cantidad_inicial
        MIENTRAS cantidad_inicial ≤ 0
            MOSTRAR "Cantidad invalida."
            INGRESAR cantidad_inicial
    
        id_lote = GuardarLote(id_producto, fecha_vencimiento, cantidad_inicial)
        RETORNAR id_lote
    
    
    
    FUNCION CrearMovimiento(id_lote, tipo)
        INGRESAR fecha_movimiento
        MIENTRAS no formatoValido(fecha_movimiento) O fecha_movimiento > FechaActual()
            MOSTRAR "Fecha invalida."
            INGRESAR fecha_movimiento
    
        INGRESAR cantidad_movimiento
        MIENTRAS cantidad_movimiento ≤ 0 O (tipo = 0 Y cantidad_movimiento > stockLote(id_lote))
            MOSTRAR "Cantidad invalida."
            INGRESAR cantidad_movimiento
    
        GuardarMovimiento(id_lote, tipo, fecha_movimiento, cantidad_movimiento)
    
        SI tipo == 0 ENTONCES
            ActualizarCantidadLote(id_lote, -cantidad_movimiento)
        SINO SI tipo = 1 ENTONCES
            ActualizarCantidadLote(id_lote, cantidad_movimiento)
    
    
        MOSTRAR "Movimiento registrado correctamente."
        RETORNAR id_movimiento
    
    
    
    FUNCION CrearEgreso()
        id_producto = SeleccionarProducto()
        id_lote = SeleccionarLoteDisponible(id_producto)
    
        CrearMovimiento(id_lote, 0)  # 0 para egreso


