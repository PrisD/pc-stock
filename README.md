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
   - Conocer el acceso y la salida del usuario
   - Monitorear que acciones realiza un usuario
   - Ver acciones de un determinado usuario en un período
   - Auditar los movimientos realizados por usuarios 
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
- [Registro de entrada de mercancías (Lautaro Stuve)](algoritmos/1-Registro%20de%20entrada%20de%20mercancias.md)
- [Actualización de niveles de stock (Joaquín Terzano)](algoritmos/2-Actualización%20de%20niveles%20de%20Stock.md) 
- [Auditoría de inventario (Priscila Della Vecchia)](algoritmos/3-Auditoria%20de%20inventario.md)
- [Generación de alertas de stock bajo (Matías Bonesi)](algoritmos/4-Generacion%20de%20alertas%20de%20stock%20bajo.md)
- [Reporte de inventario (Agustín Sánchez)](algoritmos/5-Reporte%20de%20inventario.md)

---
