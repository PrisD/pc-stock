import sqlite3
from utils import stockdb_path


def actualizar_stock(id_lote, id_usuario, tipo, cantidad, fecha, auditoria):
    """
    Es llamado cada vez que se realiza un movimiento. Recibe como entrada los parámetros del movimiento.
    Crea una entrada en la tabla de movimientos y crea o modifica una entrada en la tabla de stock.
    Esto se realiza en una única transacción.
    """
    conn = sqlite3.connect(stockdb_path)
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO movimientos (id_lote, id_usuario, tipo, cantidad, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (id_lote, id_usuario[0], tipo, cantidad, fecha.strftime("%Y-%m-%d")))

    cursor.execute("""
        SELECT id_producto
        FROM lotes
        WHERE id_lote = ?
    """, (id_lote,))
    fila = cursor.fetchone()

    if fila is None:
        conn.rollback()
        conn.close()
        raise ValueError(f"No se encontró el lote con id {id_lote}")

    id_producto = fila[0]

    # Asegurarse de que exista una entrada en la tabla de stock para el producto
    cursor.execute("""
        INSERT OR IGNORE INTO stock (id_producto, cantidad)
        VALUES (?, 0)
    """, (id_producto,))
    
    
    # ingreso
    if tipo == 1:
        cursor.execute("""
            UPDATE stock
            SET cantidad = cantidad + ?
            WHERE id_producto = ?
        """, (cantidad, id_producto))
    # egreso
    elif tipo == 0:
        cursor.execute("""
            UPDATE stock
            SET cantidad = cantidad - ?
            WHERE id_producto = ?
        """, (cantidad, id_producto))
    else:
        conn.rollback()
        conn.close()
        raise ValueError(f"Tipo de movimiento inválido: {tipo}")

    conn.commit()
    conn.close()
    print(f"Movimiento registrado correctamente. Stock actualizado con exito.")
    auditoria.registrar_auditoria(id_usuario[0], "REGISTRAR_MOVIMIENTO", "MOVIMIENTOS", f"Usuario {id_usuario[1]} registró un {'INGRESO' if tipo == 1 else 'EGRESO'} de {cantidad} unidades para el lote ID: {id_lote} del producto ID: {id_producto} en la fecha {fecha.strftime('%d/%m/%Y')}")
    return 