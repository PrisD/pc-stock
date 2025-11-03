import threading
from datetime import date


def iniciar_actualizacion_stock(conn, cursor):
    actualizar_stock(conn, cursor)
    # Se ejecuta cada hora en modo background
    t = threading.Timer(3600, iniciar_actualizacion_stock)
    t.daemon = True
    t.start()


def actualizar_stock(conn, cursor):
    print("Actualizando stock...")
    revisar_vencimiento(conn, cursor)
    calcular_stock(conn, cursor)
    print("Niveles de stock actualizados.")


def revisar_vencimiento(conn, cursor):
    """Marcar lotes vencidos para cada producto"""
    fecha_hoy = date.today()

    # 1.1 Seleccionar la tabla de lotes en orden ascendente por fecha de vencimiento
    cursor.execute("""
        SELECT DISTINCT id_producto FROM lotes ORDER BY fecha_vencimiento ASC
    """)
    productos = [row[0] for row in cursor.fetchall()]

    # 1.2 Para cada producto
    for producto in productos:
        while True:
            # 1.4 Filtrar los lotes sin marcar del producto
            cursor.execute("""
                SELECT id_lote, fecha_vencimiento 
                FROM lotes 
                WHERE id_producto = ? AND estado = 'activo' 
                ORDER BY fecha_vencimiento ASC 
                LIMIT 1
            """, (producto,))
            lote = cursor.fetchone()

            # Si no hay más lotes sin marcar, salir del bucle
            if lote is None:
                break

            id_lote, fecha_vencimiento = lote

            # 1.5 Seleccionar el lote con menor fecha (ya lo tenemos)
            # 1.6 Comparar con la fecha actual
            fecha_vencimiento = date.fromisoformat(fecha_vencimiento)

            if fecha_hoy > fecha_vencimiento:
                # 1.7 Marcar el lote
                cursor.execute("""
                    UPDATE lotes SET estado = 'vencido' WHERE id = ?
                """, (id_lote,))
                conn.commit()
                print(
                    f"Lote {id_lote} del producto {producto} marcado como vencido ({fecha_vencimiento}).")
            else:
                # 1.8 Si la fecha actual es menor, detener el ciclo para este producto
                break


def calcular_stock(conn, cursor):
    """Calcular stock para cada producto"""
    # 2.1 Seleccionar movimientos con lotes sin marcar
    cursor.execute("""
        SELECT m.id_producto, m.cantidad 
        FROM movimientos AS m 
        JOIN lotes AS l ON m.id_lote = l.id_lote 
        WHERE l.estado = 'activo'
    """)
    movimientos = cursor.fetchall()

    # Agrupar acumulados por producto
    acumulados = {}
    for producto, cantidad in movimientos:
        acumulados[producto] = acumulados.get(producto, 0) + cantidad

    # 2.2 Para cada producto con movimientos válidos
    for producto, cantidad_total in acumulados.items():
        # 2.5 Actualizar o insertar el stock acumulado
        cursor.execute("""
            INSERT INTO stock (id_producto, cantidad)
            VALUES (?, ?)
            ON CONFLICT(id_producto) DO UPDATE SET cantidad = excluded.cantidad;
        """, (producto, cantidad_total))
        print(f"Stock actualizado: {producto} = {cantidad_total}")

    conn.commit()
