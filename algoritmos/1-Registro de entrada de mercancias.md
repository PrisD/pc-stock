# Registro de entrada de mercancías
- Una transacción es una entrada.

## Objetivo del módulo
Diseñar e implementar un módulo que permita registrar de manera precisa y automatizada la entrada de mercancías al almacén, generando un movimiento de ingreso con su respectiva trazabilidad (usuario, fecha, lote, tipo (ingreso o egreso) y cantidad). Estos movimientos serán inmutables, se utilizarán para auditoria. El módulo deberá garantizar la correcta captura de la información del producto (nombre, descripción y stock mínimo) y del lote asociado (producto, fecha de vencimiento, cantidad), de manera que dichos datos puedan ser enviados posteriormente al módulo de actualización de stock para su validación e incorporación en el inventario, manteniendo la integridad de la información y dejando un registro inmutable de cada movimiento para fines de auditoría.
El módulo no toca el stock directamente, solo se encarga de registrar el movimiento de entrada y de preparar la información necesaria (producto, lote, cantidad, vencimiento, etc.) para que después el módulo de Actualización de stock haga su parte

## Algoritmo
1- Repetir mientras el usuario quiera ingresar movimientos:

    1.1- Solicitar y registrar datos del producto asociado.
    
    1.2- Solicitar y registrar datos del lote asociado.

    1.3- Solicitar y registrar datos del movimiento.

    1.5- Si los datos son correctos:
    
        1.5.1- Guardar los datos registrados en la base de datos.

## Niveles de refinamiento 

### Nivel 1
### Nivel 2

## Pseudocódigo
