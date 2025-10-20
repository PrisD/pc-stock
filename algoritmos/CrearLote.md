# Crear Lote

## Objetivo del módulo
Crear Lotes a traves de un formulario para luego guardarlos en la base de datos

## Algoritmo
    1.  Ingresar y validar la fecha de ingreso del lote.
    2.  Ingresar y validar la fecha de vencimiento del lote.
    3.  Ingresar y validar la cantidad inicial del lote.
    4.  Si todas las validaciones son correctas:
        4.1. Asignar estado "activo".
        4.2. Guardar el nuevo lote en la base de datos (asociado al ID_Producto).
        4.3. retornar exito.
    5.  Si alguna validacion falla:
        5.1. Informar error.

## Niveles de refinamiento 

### Nivel 1
    1.  Mientras que el usuario no haya enviado el formulario de lote:
        1.1. Mostrar un formulario al usuario (con los campos: fecha de ingreso, fecha de vencimiento y cantidad inicial).
        2.1. Esperar a que el usuario presione el boton "Guardar Lote".
        3.1. Al recibir la accion "Guardar Lote":
            3.1. Obtener los datos ingresados (fecha_ingreso, fecha_vencimiento, cantidad).
            3.2. Validar los datos (formato y reglas de fechas, y que la cantidad sea > 0).
            3.3. Si los datos son correctos:
                3.3.1. Asignar 'estado' = "activo".
                3.3.2. Guardar el nuevo lote en la base de datos (asociándolo al ID_Producto).
                3.3.3. Retornar mensaje: "Lote creado exitosamente".
            3.4. Si los datos NO son correctos:
                3.4.1. Mostrar errores de validacion al usuario.

### Nivel 2
    1.  Mientras que el usuario no haya enviado el formulario de lote:

      1.  Mostrar el formulario "Nuevo Lote" (campos: fecha ingreso, fecha vencimiento, cantidad).
      2.  Esperar a que el usuario presione el boton "Guardar Lote".
      3.  Al recibir la accion "Guardar Lote":
          3.1. Obtener 'fecha_ingreso' ingresada.
          3.2. Obtener 'fecha_vencimiento' ingresada.
          3.3. Obtener 'cantidad' ingresada.
          3.4. Inicializar una lista de 'errores' (vacia).
          
          3.5. errorFecha = ValidarFecha(fecha_ingreso,fecha_vencimiento)
          3.6 Si errorFecha <> NULO:
              Anadir errorFecha a 'errores'.
                  
          3.7. Validar 'cantidad':
              3.7.1. Si 'cantidad' no es un numero entero:
                  Anadir "La cantidad debe ser un numero entero" a 'errores'.
              3.7.2. Si (ConvertirAEntero(cantidad) <= 0):
                  Anadir "La cantidad debe ser un numero mayor a 0" a 'errores'.
          
          3.8. Si la lista de 'errores' esta vacia:
              3.8.1. Asignar 'estado' = "activo".
              3.8.2. Guardar (ID_Producto, fecha_ingreso, fecha_vencimiento, ConvertirAEntero(cantidad), estado) en la Base de Datos.
              3.8.3. Mostrar mensaje: "Lote creado exitosamente".
              3.8.4. Limpiar los campos del formulario.
          3.9. Si la lista de 'errores' NO esta vacia:
              3.9.1. Mostrar los 'errores' al usuario (detallando que campos fallaron).
        
## Pseudocódigo

    1. MostrarFormulario("Nuevo Lote", ["campo_fecha_ingreso", "campo_fecha_vencimiento", "campo_cantidad"], "boton_guardar_lote")

    2. Esperar a que el usuario presione el boton "Guardar Lote".

    3. AlPresionar("boton_guardar_lote")
        
        3.1 fecha_ingreso = Leer("campo_fecha_ingreso")
        3.2 fecha_vencimiento = Leer("campo_fecha_vencimiento")
        3.3 cantidad = Leer("campo_cantidad")

        3.4 Inicializar errores = [] 

        3.5 errorFecha = ValidarFecha(fecha_ingreso, fecha_vencimiento)
        3.6 Si errorFecha <> NULO:
            Agregar errorFecha a errores
            
        3.7: Validar 'cantidad'
            3.7.1 Si No EsNumeroEntero(cantidad):
                    Agregar "La cantidad debe ser un número entero" a errores
                Sino
                    es_valido_entero = Verdadero
            
            3.7.2 Si es_valido_entero Y cantidad_num <= 0:
                    Agregar "La cantidad debe ser un número mayor a 0" a errores

        3.8 Si EstaVacia(errores):
            3.8.1 estado = "activo"
            3.8.2 GuardarLoteEnBaseDeDatos(ID_Producto, fecha_ingreso, fecha_vencimiento, cantidad_num, estado)
            3.8.3 MostrarMensaje("Lote creado exitosamente")
            3.8.4 LimpiarCamposDelFormulario()
            
        3.9 Sino
            3.9.1 MostrarErroresEnFormulario(errores)
