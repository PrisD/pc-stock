# Registro de movimientos de mercancías

## Objetivo del módulo
Módulo para gestionar el ciclo de vida del inventario, permitiendo el registro de todos los movimientos de ingreso y egreso, actualizando directamente la cantidad disponible por lote para mantener un control preciso.

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
                1.1.2. Verificar que los datos sean válidos y que no exista duplicado.
                1.1.3. Guardar producto en la base de datos.
    
        1.2. Si el usuario desea registrar un movimiento:
    
            Si es un ingreso:
                RegistrarMovimiento(tipo = ingreso):
            
            Si es un egreso:
                RegistrarMovimiento(tipo = egreso):
    
        1.4 Preguntar al usuario si desea continuar ingresando movimientos o creando productos.

    2- Actualizar niveles de stock

### Nivel 2
    1- Repetir mientras el usuario quiera ingresar movimientos:

    1.1. Si el usuario desea registrar un movimiento:

        Si es un ingreso:
            RegistrarMovimiento(tipo = ingreso):
        
        Si es un egreso:
            RegistrarMovimiento(tipo = egreso):

    1.1 Preguntar al usuario si desea continuar ingresando movimientos.

    2- Actualizarnivelesdestock()
    
    
    
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
            
            MIENTRAS Seguir:
                ESCRIBIR "--- MENU DE REGISTRO DE ENTRADAS Y SALIDAS ---"
                ESCRIBIR "1. Registrar Ingreso de Mercancia"
                ESCRIBIR "2. Registrar Egreso de Mercancia"
                ESCRIBIR "3. Salir"
                LEER opcion
        
                SEGUN opcion:
                    CASO 1:
                        LLAMAR RegistrarMovimiento("INGRESO")
                    CASO 2:
                        LLAMAR RegistrarMovimiento("EGRESO")
                    CASO 3:
                        ESCRIBIR "Saliendo del programa."
                        Seguir = Falso
                    DE OTRO MODO:
                        ESCRIBIR "Opcion no valida. Intente de nuevo."
    
            LLAMAR ActualizarNivelesDeStock()
        
        
        INICIO FUNCION RegistrarMovimiento(tipo)
            // 1. Seleccionar producto
            ESCRIBIR "Ingrese el codigo del producto para el movimiento:"
            LEER codigo_producto
            producto = BUSCAR_PRODUCTO_POR_CODIGO(codigo_producto)
        
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

    
            //2. Seleccionar lote
            
            SI tipo == "INGRESO" ENTONCES
                ESCRIBIR "Ingrese el código del lote o presione ENTER para cargar uno nuevo"
                LEER codigo_lote
                SI codigo_lote == "":
                    lote = LLAMAR CrearLote(producto.id)
                    cantidad_movimiento = lote.cantidad
                    SI lote == NULO ENTONCES
                        ESCRIBIR "Error creando el lote. Operacion cancelada."
                        RETORNAR

                SINO // Se ingreso un codigo de lote
                    lote = BUSCAR_LOTE_POR_CODIGO(codigo_lote)
                    SI lote != NULO ENTONCES // El lote ya existe
                        ESCRIBIR "Ingrese la cantidad a ingresar al lote (unidades):"
                        LEER cantidad_movimiento
                        nueva_cantidad = lote.cantidad + cantidad_movimiento
                        ACTUALIZAR_CANTIDAD_LOTE_EN_BD(lote.id, nueva_cantidad)
                        ESCRIBIR "Stock del lote existente actualizado."
                    
                    SINO
                        ESCRIBIR "Error en el ingreso del codigo, lote no existente"
                        
            SINO // tipo es EGRESO
                ESCRIBIR "Ingrese el código del lote"
                LEER codigo_lote
                lote = BUSCAR_LOTE_POR_CODIGO(codigo_lote)
                SI lote == NULO ENTONCES
                    ESCRIBIR "Error: El lote no existe. No se puede registrar el egreso."
                    RETORNAR

                // Si llega hasta aca, es porque encontro el lote
                ESCRIBIR "Ingrese la cantidad a retirar del lote (unidades):"
                LEER cantidad_movimiento
                
                SI cantidad_movimiento > lote.cantidad ENTONCES
                    ESCRIBIR "Error: Stock insuficiente en el lote. Disponible: ", lote.cantidad
                    RETORNAR
                SINO
                    nueva_cantidad = lote.cantidad - cantidad_movimiento
                    ACTUALIZAR_CANTIDAD_LOTE_EN_BD(lote.id, nueva_cantidad)
                    ESCRIBIR "Stock del lote actualizado."
            
        
            //3. Crear el registro del movimiento
            LLAMAR CrearMovimiento(lote.id, tipo, cantidad_movimiento, ID_USUARIO_LOGUEADO)
        
        
        INICIO FUNCION CrearMovimiento(id_lote, tipo, cantidad, id_usuario)
            // 1. Ingresar fecha del movimiento
            ESCRIBIR "Ingrese fecha del movimiento (dd/mm/aaaa) o presione Enter para usar la fecha actual:"
            LEER fecha_movimiento // Validar formato y que no sea futura
            SI fecha_movimiento == "" ENTONCES
                fecha_movimiento = FECHA_ACTUAL()
            
            // 1.2.3.5. Guardar movimiento en la base de datos
            GUARDAR_MOVIMIENTO_EN_BD(id_lote, id_usuario, tipo, fecha_movimiento, cantidad)
            ESCRIBIR "Movimiento registrado correctamente en el historial."
