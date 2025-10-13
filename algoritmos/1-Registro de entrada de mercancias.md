# Registro de entrada de mercancías

## Objetivo del módulo
Diseñar e implementar un módulo que permita registrar de manera precisa y automatizada los movimientos de ingresos de mercancías en el almacén, garantizando su trazabilidad mediante el registro del usuario, fecha, lote, tipo de movimiento y cantidad.
El módulo deberá:
 * Asegurar la correcta captura de la información del producto (nombre, descripción y stock mínimo).
 * Registrar los datos del lote asociado (producto, fecha de vencimiento, cantidad).
 * Generar un movimiento inmutable para cada operación, que quedará como respaldo para auditorías.
 * Validar los datos y guardarlos en la base de datos.
Este módulo no modifica directamente la tabla stock.


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
                1.1.1. Ingresar datos del producto
                1.1.4. Verificar que los datos sean válidos y que no exista duplicado.
                1.1.5. Guardar producto en la base de datos.
    
        1.2. Si el usuario desea registrar un movimiento:
    
            Si es un ingreso:
                CrearMovimiento(tipo = ingreso):
            
            Si es un egreso:
                CrearMovimiento(tipo = egreso):
    
        1.4 Preguntar al usuario si desea continuar ingresando movimientos o creando productos.

### Nivel 2
    1- Repetir mientras el usuario quiera ingresar movimientos o crear productos:
    
        1.1. Si el usuario desea crear un producto:
            CrearProducto():
                1.1.1. Ingresar nombre del producto.
                    1.1.1.1 . Validar que no esté vacío, que no exceda 50 caracteres y que no exista ya en la base de datos.
                    
                1.1.2. Ingresar descripción del producto (texto opcional, máx. 100 caracteres).
                    1.1.2.1 . Validar que no exceda 100 caracteres.
                    
                1.1.3. Ingresar stock mínimo (entero mayor o igual a 0).
                    1.1.3.1 . Validar que sea un número entero >= 0.
                    
                1.1.5. Si todo es válido:
                    Guardar producto en la base de datos.
    
        1.2. Si el usuario desea registrar un movimiento:
    
            Si es un ingreso:
                RegistrarMovimiento(tipo = ingreso):
            
            Si es un egreso:
                RegistrarMovimiento(tipo = egreso):
    
        1.4 Preguntar al usuario si desea continuar ingresando movimientos o creando productos.
    
    
    
    Funcion RegistrarMovimiento(tipo):
        Si el tipo es ingreso:
            1.2.1. Seleccionar producto:
                - Si ya existe: elegir de la base de datos.
                - Si es nuevo: llamar a CrearProducto().
    
            1.2.2. Seleccionar o crear lote:
                - Si el lote ya existe: seleccionarlo.
                    - Ingresar cantidad a agregar al lote.
                    - Actualizar cantidad del lote sumando la cantidad ingresada.
                - Si no existe: 
                    CrearLote(id del producto):
                        1.2.2.1. Asociar ID del producto.
                        1.2.2.2. Ingresar fecha de ingreso:
                            1.2.2.2.1 . Validar formato dd/mm/aaaa y que no sea futura.
                        1.2.2.2. Ingresar fecha de vencimiento:
                            1.2.2.2.1 . Validar formato dd/mm/aaaa y que sea futura.
                        1.2.2.3. Ingresar cantidad inicial del lote:
                            1.2.2.2.3.1 . Validar que sea un número entero > 0.
                        1.2.2.4. Ingresar estado del lote = activo.
                        1.2.2.5. Guardar lote en la base de datos.
    
            1.2.3. Crear movimiento de ingreso:
                CrearMovimiento(id del lote, tipo, cantidad del ingreso, id del usuario)
                    
                    
                    
        Si el tipo es egreso:
            1.2.1. Seleccionar producto:
                - Elegir prodcuto de la base de datos.
    
            1.2.2. Seleccionar lote:
                - Elegir lote de la base de datos con stock suficiente.
                - ingresar cantidad a retirar del lote.
                - validar que la cantidad a retirar no supere el stock del lote.
                - Actualizar cantidad del lote restando la cantidad retirada.
    
            1.2.3. Crear movimiento de ingreso:
                CrearMovimiento(id del lote, tipo, cantidad del egreso del lote, id del usuario)
         
     
    Funcion CrearMovimiento(id del lote, tipo, cantidad del lote, id_usuario):
        1.2.3.1 Asociar ID del usuario
        1.2.3.1. Asociar ID del lote.
        1.2.3.2. Asociar tipo de movimiento (egreso o ingreso).
        1.2.3.3. Ingresar fecha del movimiento:
            1.2.3.3.1 . Validar formato dd/mm/aaaa y que no sea futura.
        1.2.3.4. Asociar cantidad del ingreso o egreso del lote
    
        1.2.3.5. Guardar movimiento en la base de datos.
        
## Pseudocódigo

    INICIO RegistroEntradasySalidas
        
        MIENTRAS VERDADERO HACER
            ESCRIBIR "--- MENU DE REGISTRO DE ENTRADAS Y SALIDAS ---"
            ESCRIBIR "1. Crear Nuevo Producto"
            ESCRIBIR "2. Registrar Ingreso de Mercancia"
            ESCRIBIR "3. Registrar Egreso de Mercancia"
            ESCRIBIR "4. Salir"
            LEER opcion
    
            SEGUN opcion HACER
                CASO 1:
                    LLAMAR CrearProducto()
                CASO 2:
                    LLAMAR RegistrarMovimiento("INGRESO")
                CASO 3:
                    LLAMAR RegistrarMovimiento("EGRESO")
                CASO 4:
                    ESCRIBIR "Saliendo del programa."
                    SALIR_DEL_BUCLE
                DE OTRO MODO:
                    ESCRIBIR "Opcion no valida. Intente de nuevo."
            
    
            
    
    INICIO FUNCION CrearProducto()
        // 1.1.1. Ingresar datos del producto
        ESCRIBIR "Ingrese nombre del nuevo producto:"
        LEER nombre
        ESCRIBIR "Ingrese descripcion:"
        LEER descripcion
        ESCRIBIR "Ingrese stock mínimo:"
        LEER stock_minimo
    
        // 1.1.4. Verificar que los datos sean validos y que no exista duplicado
        SI nombre == "" O stock_minimo < 0 ENTONCES
            ESCRIBIR "Error: El nombre no puede estar vacío y el stock minimo debe ser positivo."
            RETORNAR NULO
    
    
        SI BUSCAR_PRODUCTO_POR_NOMBRE(nombre) != NULO ENTONCES
            ESCRIBIR "Error: Ya existe un producto con ese nombre."
            RETORNAR NULO
        
    
        // 1.1.5. Guardar producto en la base de datos
        nuevo_producto = GUARDAR_PRODUCTO_EN_BD(nombre, descripcion, stock_minimo)
        ESCRIBIR "Producto creado con exito."
        RETORNAR nuevo_producto
    
    
    
    INICIO FUNCION RegistrarMovimiento(tipo)
        // 1.2.1. Seleccionar producto
        ESCRIBIR "Ingrese el nombre del producto para el movimiento:"
        LEER nombre_producto
        producto = BUSCAR_PRODUCTO_POR_NOMBRE(nombre_producto)
    
        SI producto == NULO ENTONCES
            SI tipo == "INGRESO" ENTONCES
                ESCRIBIR "Producto no encontrado. Desea crearlo ahora? (S/N)"
                LEER respuesta
                SI respuesta == "S" ENTONCES
                    producto = LLAMAR CrearProducto()
                    SI producto == NULO ENTONCES
                        ESCRIBIR "Error al crear producto. Operacion cancelada."
                        RETORNAR
                    
                SINO
                    ESCRIBIR "Operación cancelada."
                    RETORNAR
                
            SINO // Es un EGRESO
                ESCRIBIR "Error: No se puede dar salida a un producto que no existe."
                RETORNAR
            
    
        // 1.2.2. Seleccionar lote
        ESCRIBIR "Ingrese el código del lote:"
        LEER codigo_lote
        lote = BUSCAR_LOTE_POR_CODIGO(producto.id, codigo_lote)
    
        ESCRIBIR "Ingrese la cantidad (unidades):"
        LEER cantidad_movimiento
    
        SI tipo == "INGRESO" ENTONCES
            SI lote != NULO ENTONCES // El lote ya existe
                nueva_cantidad = lote.cantidad + cantidad_movimiento
                ACTUALIZAR_CANTIDAD_LOTE_EN_BD(lote.id, nueva_cantidad)
                ESCRIBIR "Stock del lote existente actualizado."
                
            SINO // El lote es nuevo
                lote = LLAMAR CrearLote(producto.id, codigo_lote, cantidad_movimiento)
                SI lote == NULO ENTONCES
                    ESCRIBIR "Error creando el lote. Operacion cancelada."
                    RETORNAR
                
        SINO // tipo es EGRESO
            SI lote == NULO ENTONCES
                ESCRIBIR "Error: El lote no existe. No se puede registrar el egreso."
                RETORNAR
            
            SI cantidad_movimiento > lote.cantidad ENTONCES
                ESCRIBIR "Error: Stock insuficiente en el lote. Disponible: ", lote.cantidad
                RETORNAR
            
            nueva_cantidad = lote.cantidad - cantidad_movimiento
            ACTUALIZAR_CANTIDAD_LOTE_EN_BD(lote.id, nueva_cantidad)
            ESCRIBIR "Stock del lote actualizado."
        
    
        // 1.2.3. Crear el registro del movimiento
        LLAMAR CrearMovimiento(lote.id, tipo, cantidad_movimiento, ID_USUARIO_LOGUEADO)
        
    
    
    INICIO FUNCION CrearLote(id_producto, codigo_lote, cantidad_inicial)
        // 1.2.2.2. Ingresar fechas
        ESCRIBIR "Ingrese fecha de ingreso (dd/mm/aaaa):"
        LEER fecha_ingreso // Validar formato y que no sea futura
        ESCRIBIR "Ingrese fecha de vencimiento (dd/mm/aaaa):"
        LEER fecha_vencimiento // Validar formato y que sea futura
        
        // 1.2.2.3. Validar cantidad
        SI cantidad_inicial <= 0 ENTONCES
            ESCRIBIR "Error: la cantidad inicial debe ser mayor a 0."
            RETORNAR NULO  
    
        // 1.2.2.5. Guardar lote en la base de datos
        nuevo_lote = GUARDAR_LOTE_EN_BD(id_producto, codigo_lote, fecha_ingreso, fecha_vencimiento, cantidad_inicial, "activo")
        ESCRIBIR "Lote nuevo creado."
        RETORNAR nuevo_lote
    
    
    
    INICIO FUNCION CrearMovimiento(id_lote, tipo, cantidad, id_usuario)
        // 1.2.3.3. Ingresar fecha del movimiento
        ESCRIBIR "Ingrese fecha del movimiento (dd/mm/aaaa) o presione Enter para usar la fecha actual:"
        LEER fecha_movimiento // Validar formato y que no sea futura
        SI fecha_movimiento == "" ENTONCES
            fecha_movimiento = FECHA_ACTUAL()
        
        // 1.2.3.5. Guardar movimiento en la base de datos
        GUARDAR_MOVIMIENTO_EN_BD(id_lote, id_usuario, tipo, fecha_movimiento, cantidad)
        ESCRIBIR "Movimiento registrado correctamente en el historial."
