# pc-stock

### Modulos
- Registro de entrada de mercancias ()
- Actualización de niveles de stock () 
- Audotoría de inventario ()
- Generación de alertas de stock bajo ()
- Reporte de inventario ()

## Relevamiento del control de inventario
Un almacén en el cual se reciben, almacenan y despachan productos de distintas características. 
Los problemas que buscará resolver el sistema son:
- Dificultad para llevar un control exacto de las entradas y salidas de mercancías.
- Riesgo de faltantes de stock al no detectar a tiempo cuando un producto baja de su nivel mínimo.
- Imposibilidad de obtener reportes en tiempo real que reflejen la situación del inventario.
- Alta probabilidad de errores humanos, duplicación de registros o pérdida de información.

 **Alcance**
El sistema abarcará las siguientes funcionalidades principales:
1. Registro de entrada de mercancías
  - Alta de productos y lotes.
  - Generación de movimientos de ingreso
2. Actualización de niveles de stock
 - Recalcular stock en tiempo real en base a movimientos.
 - Mantener actualizado un inventario por producto y lote.
3. Auditoría de inventario
 - Registro histórico de todos los movimientos.
 - Identificación de fechas y cantidades.
 - Posibilidad de generar reportes de auditoría por periodo.
4. Generación de alertas de stock bajo
 - Comparación automática con stock mínimo definido.
 - Emisión de alertas cuando un producto alcanza nivel crítico.
 - Gestión de alertas activas y resolución cuando el stock se normaliza.
5. Reportes de inventario
 - Reportes generales y filtrados (por producto, categoría o lote).
 - Visualización de stock actual, movimientos y alertas.
 - Exportación de informes para toma de decisiones.

Lo que no se contempla:
- Gestión de compras ni órdenes automáticas a proveedores.
- No gestiona precios, facturación ni ventas, solo control físico de inventario.
- No cubre logística de transporte ni distribución fuera del almacén.
- No realiza una gestión de usuarios que puedan ingresar al sistema.

## Diagrama Entidad Relación

**Producto**
- codigo de producto
- descripcion
- dimension
- peso

**Transacción**
- codigo
- codigo de producto
- ingreso/egreso
- cantidad
- fecha
- fecha vencimiento

**Stock**
- codigo
- codigo de producto
- cantidad

## Registro de entrada de mercancias
 - Una transacción es una entrada
## Actualización de niveles de stock
 - Hay un algoritmo que modifica la tabla stock a partir de una transacción
## Audotoría de inventario
## Generación de alertas de stock bajo 
## Reporte de inventario




 
