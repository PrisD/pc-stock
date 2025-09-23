# MAIN

## Objetivo del módulo
Menu principal

## Algoritmo
        1. Iniciar sesion
        2. Despliegue del menu con las opciones:
                2.1. Registrar Movimientos
                2.2. Consultar Stock Actual 
                2.3. Consultar movimientos (Auditoria)
                2.4. Consultar alertas de stock bajo.
                2.5. Visualizar Reporte
                2.6. Cerrar sesión
## Niveles de refinamiento 

### Nivel 1
        1. Iniciar sesion
            1.1. Pedir usuario y contraseña.
            1.2. Validar credenciales.
            1.3. Si son correctas, continuar al menú.
        
        Repetir mientras el usuario no elija cerrar sesión:
            2. Despliegue del menú con las opciones:
                    2.1. Registrar Movimientos
                    2.2. Consultar Stock Actual
                    2.3. Consultar movimientos (Auditoria)
                    2.4. Consultar alertas de stock bajo.
                    2.5. Visualizar Reporte
                    2.6. Cerrar sesión
        
            3. Pedir opción al usuario.
            
            4. Ejecutar la función correspondiente a la opción seleccionada.

### Nivel 2

        1. Iniciar sesion
            1.1. Pedir usuario y contraseña.
            1.2. Validar credenciales.
            1.3. Si son correctas, continuar al menú.
        
        Repetir mientras el usuario no elija cerrar sesión:
            2. Despliegue del menú con las opciones:
                    2.1. Registrar Movimientos
                    2.2. Consultar Stock Actual
                    2.3. Consultar movimientos (Auditoria)
                    2.4. Consultar alertas de stock bajo.
                    2.5. Visualizar Reporte
                    2.6. Cerrar sesión
        
            3. Pedir opción al usuario.
            
            4. Ejecutar la función correspondiente a la opción seleccionada:
                4.1. Si opción == 1:
                    4.1.1. llamar a RegistrarMovimientos()
                    4.1.2. llamar a ConsultarStockActual() para mostrar stock actualizado.
                    4.1.3. llamar a ConsultarAlertasStockBajo() para mostrar alertas actualizadas.
                
                4.2. Si opción == 2:
                    4.2.1. llamar a ConsultarStockActual()
                
                4.3. Si opción == 3:
                    4.3.1. llamar a ConsultarMovimientosAuditoria()
                    
                4.4. Si opción == 4:
                    4.4.1. llamar a ConsultarAlertasStockBajo()
                
                4.5. Si opción == 5:
                    4.5.1.  llamar a VisualizarReporte()
                    
                4.6. Si opción = 6:
                    4.6.1 cerrar sesión.
                    
                4.7. Si opción no es válida:
                    4.7.1 mostrar mensaje de error.
        
## Pseudocódigo
