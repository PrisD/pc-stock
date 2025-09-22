# Registro de entrada de mercancías
- Una transacción es una entrada.

## Objetivo del módulo
Diseñar e implementar un módulo que permita registrar de manera precisa y automatizada la entrada de mercancías al almacén, generando un movimiento de ingreso con su respectiva trazabilidad (usuario, fecha, lote, tipo (ingreso o egreso) y cantidad). Estos movimientos serán inmutables, se utilizarán para auditoria. El módulo deberá garantizar la correcta captura de la información del producto (nombre, descripción y stock mínimo) y del lote asociado (producto, fecha de vencimiento, cantidad), de manera que dichos datos puedan ser enviados posteriormente al módulo de actualización de stock para su validación e incorporación en el inventario, manteniendo la integridad de la información y dejando un registro inmutable de cada movimiento para fines de auditoría.
El módulo no toca el stock directamente, solo se encarga de registrar el movimiento de entrada y de preparar la información necesaria (producto, lote, cantidad, vencimiento, etc.) para que después el módulo de Actualización de stock haga su parte.

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

### Nivel 2

## Pseudocódigo
