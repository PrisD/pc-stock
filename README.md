# Pensamiento Computacional

**Grupo 2**


## Índice
- [Sistema de control de Stock](#sistema-de-control-de-stock)
  - [Índice](#índice)
- [Relevamiento del control de inventario](#relevamiento-del-control-de-inventario)
  - [Alcance](#alcance)
  - [Lo que no se contempla](#lo-que-no-se-contempla)
- [Diagrama Entidad Relación](#diagrama-entidad-relación)
- [Módulos](#módulos)


# Objetivo General
Mantener un registro del inventario asegurando la disponibilidad de productos, mientras se facilita la auditoria por generacion de alertas y reportes

# Relevamiento del control de inventario
Un almacén en el cual se reciben, almacenan y despachan productos de distintas características.  
Los problemas que buscará resolver el sistema son:

- Dificultad para llevar un control exacto de las entradas y salidas de mercancías.
- Riesgo de faltantes de stock al no detectar a tiempo cuando un producto baja de su nivel mínimo.
- Imposibilidad de obtener reportes en tiempo real que reflejen la situación del inventario.
- Realizar anotaciones o controles del inventario en papel.

## Alcance
El sistema abarcará las siguientes funcionalidades principales:
1. Registro de entrada y salidas de mercancías
   - Generación de movimientos de ingreso y egreso.
2. Actualización de niveles de stock
   - Recalcular stock en tiempo real en base a movimientos.
   - Mantener actualizado un inventario detectando si un lote se encuentra vencido.
3. Auditoría de inventario
   - Conocer el acceso y la salida del usuario.
   - Monitorear que acciones realiza un usuario.
   - Ver acciones de un determinado usuario en un período.
   - Auditar los movimientos realizados por usuarios.
4. Generación de alertas de stock bajo
   - Comparación automática con stock mínimo definido.
   - Emisión de alertas cuando un producto se encuentra por debajo de su stock mínimo.
   - Registro de las alertas en la base de datos.
5. Reportes de inventario
   - Generarcion de reportes por fechas, productos y mas.
   - Exportación de informes para toma de decisiones.

## Lo que no se contempla
- Gestión de compras ni órdenes automáticas a proveedores.
- Gestionar precios, facturación ni ventas, solo control físico de inventario.
- Logística de transporte ni distribución fuera del almacén.
- Realizar una gestión o validación de usuarios por contraseña.

---

# Diagrama Entidad Relación
<img width="1077" height="695" alt="image" src="https://github.com/user-attachments/assets/1473b125-a12b-4cc3-beea-0c320e2df867" />

# Diagrama Data Warehouse
<img width="954" height="498" alt="imagen" src="https://github.com/user-attachments/assets/7745d2d1-248a-4114-92bd-835fcf8c6bf9" />

# Diagrama de Flujo
<img width="1571" height="727" alt="image" src="https://github.com/user-attachments/assets/0cb31fcd-9dfe-4e62-8bb9-bb3610ec9ab1" />





---


# Módulos
- [Main](algoritmos/0-Main.md)
- [Registro de entrada de mercancías (Lautaro Stuve)](algoritmos/1-Registro%20de%20entrada%20de%20mercancias.md)
- [Actualización de niveles de stock (Joaquín Terzano)](algoritmos/2-Actualización%20de%20niveles%20de%20Stock.md) 
- [Auditoría de inventario (Priscila Della Vecchia)](algoritmos/3-Auditoria%20de%20inventario.md)
- [Generación de alertas de stock bajo (Matías Bonesi)](algoritmos/4-Generacion%20de%20alertas%20de%20stock%20bajo.md)
- [Reporte de inventario (Agustín Sánchez)](algoritmos/5-Reporte%20de%20inventario.md)

---
