# Crear Producto

## Objetivo del módulo
Crear productos a traves de un formulario para luego guardarlos en la base de datos

## Algoritmo
    1.  Mientas que el usuario no haya enviado el formulario:
        1.1. Mostrar un formulario al usuario (con los campos de nombre, descripcion y stock).
        2.1. Esperar a que el usuario presione el botón "Enviar".
        3.1. Al recibir la accion "Enviar":
            3.1. Obtener los datos ingresados por el usuario en los campos.
            3.2. Validar los datos.
            3.3. Si los datos son correctos, guardar en la base de datos, si no mostrar errores.

## Niveles de refinamiento 

### Nivel 1
    1.  Mostrar el formulario "Nuevo Producto" (campos: nombre, descripcion, stock minimo).
    2.  Esperar a que el usuario presione el boton "Enviar".
    3.  Al recibir la accion "Enviar":
            3.1. Obtener 'nombre', 'descripcion' y 'stock_min' del formulario.
            
            3.2. Realizar validaciones del 'nombre':
                 (Debe tener < 50 caracteres, no estar vacio y no existir en la BD).
            3.3. Realizar validaciones de la 'descripcion':
                 (Debe tener < 100 caracteres).
            3.4. Realizar validaciones del 'stock_min':
                 (Debe ser un numero entero >= 0).
        
            3.5. Si (las validaciones 3.2, 3.3 y 3.4 son todas correctas):
                3.5.1. Guardar el producto en la base de datos.
                3.5.2. Mostrar mensaje de "Producto creado".
            3.6. Si no:
                3.6.1. Mostrar mensaje de error indicando que campos deben corregirse.

### Nivel 2
    1.  Mostrar el formulario "Nuevo Producto" (campos: nombre, descripción, stock mínimo).
    2.  Esperar a que el usuario presione el boton "Enviar".
    3.  Al recibir la accion "Enviar":
        3.1. Obtener 'nombre' ingresado.
        3.2. Obtener 'descripcion' ingresada.
        3.3. Obtener 'stock_min' ingresado.
        3.4. Inicializar una lista de 'errores' (vacía).
        
    
        3.5. Validar 'nombre':
            3.5.1. Si 'nombre' está vacío:
                   Añadir "El nombre no puede estar vacio" a 'errores'.
            3.5.2. Si la longitud de 'nombre' > 50 caracteres:
                   Añadir "El nombre no debe exceder los 50 caracteres" a 'errores'.
            3.5.3. Si 'nombre' ya existe en la Base de Datos:
                   Añadir "El producto ya existe" a 'errores'.
                   
        3.6. Validar 'descripcion':
            3.6.1. Si la longitud de 'descripcion' > 100 caracteres:
                   Añadir "La descripcion no debe exceder los 100 caracteres" a 'errores'.
                   
        3.7. Validar 'stock_min':
            3.7.1. Si 'stock_min' no es un numero entero:
                   Añadir "El stock minimo debe ser un numero entero" a 'errores'.
            3.7.2. Si 'stock_min' es < 0:
                   Añadir "El stock minimo debe ser mayor o igual a 0" a 'errores'.
        
        
        3.8. Si la lista de 'errores' esta vacia:
            3.8.1. Guardar (nombre, descripcion, stock_min) en la Base de Datos.
            3.8.2. Mostrar mensaje: "Producto creado exitosamente".
            3.8.3. Limpiar los campos del formulario.
        3.9. Si la lista de 'errores' NO está vacía:
            3.9.1. Mostrar los 'errores' al usuario (detallando que campos fallaron).
        
## Pseudocódigo

    1. MostrarFormularioProducto("Nuevo Producto", ["campo_nombre", "campo_descripcion", "campo_stock_min"], "boton_enviar")
    
    2. Esperar a que el usuario presione el boton "Enviar".
    
    3. AlPresionar("boton_enviar")
            
        3.1 nombre = Leer("campo_nombre")
        3.2 descripcion = Leer("campo_descripcion")
        3.3 stock_min_texto = Leer("campo_stock_min")

        3.4 Inicializar errores = [] 

        3.5 Validar 'nombre'
            3.5.1 Si EstaVacio(nombre):
                Agregar "El nombre no puede estar vacio" a errores
            
            3.5.2 Si Longitud(nombre) > 50:
                Agregar "El nombre no debe exceder los 50 caracteres" a errores
        
        3.5.3 Si ExisteEnBaseDeDatos(nombre):
                Agregar "El producto ya existe" a errores
            

        3.6: Validar 'descripcion'
            3.6.1 Si Longitud(descripcion) > 100 :
                Agregar "La descripcion no debe exceder los 100 caracteres" a errores

        3.7: Validar 'stock_min'

            3.7.1 Si No EsNumeroEntero(stock_min_texto) :
                    Agregar "El stock minimo debe ser un numero entero" a errores
                Sino
                    stock_min_num = ConvertirAEntero(stock_min_texto)
                    es_valido_entero = Verdadero
        
            3.7.2 Si es_valido_entero Y stock_min_num < 0 :
                    Agregar "El stock minimo debe ser mayor o igual a 0" a errores



        3.8 Si EstaVacia(errores) :
            3.8.1 GuardarEnBaseDeDatos(nombre, descripcion, stock_min_num)
            3.8.2 MostrarMensaje("Producto creado exitosamente")
            3.8.3 LimpiarCamposDelFormulario()
             
        3.9 Sino
            3.9.1 MostrarErroresEnFormulario(errores)
