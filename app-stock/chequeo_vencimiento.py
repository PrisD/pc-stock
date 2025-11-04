import sqlite3
import threading
from datetime import date
from utils import stockdb_path


def programar_chequear_vencimiento(periodo=86400):
    t = threading.Timer(periodo, chequear_vencimiento)
    t.daemon = True
    t.start()


def chequear_vencimiento():
    """
    Se ejecuta de forma periódica una vez al día.
    Encuentra todos los lotes activos que están vencidos.
    Por cada lote vencido, modifica una entrada en la tabla de lotes para registrar el hecho.
    """
    print("\nIniciando chequeo de vencimiento...")
    conn = sqlite3.connect(stockdb_path)
    cursor = conn.cursor()
    fecha_actual = date.today()

    while True:
        cursor.execute("""
            SELECT id_lote, fecha_vencimiento
            FROM lotes
            WHERE estado = 'activo'
            ORDER BY fecha_vencimiento ASC
            LIMIT 1
        """)
        lote = cursor.fetchone()

        if lote is None:
            break

        id_lote, fecha_vencimiento = lote

        if isinstance(fecha_vencimiento, str):
            fecha_vencimiento = date.fromisoformat(fecha_vencimiento)

        if fecha_actual > fecha_vencimiento:
            cursor.execute("""
                UPDATE lotes
                SET estado = 'vencido'
                WHERE id_lote = ?
            """, (id_lote,))
            conn.commit()
        else:
            break

    conn.close()
    print("\nChequeo finalizado.")
