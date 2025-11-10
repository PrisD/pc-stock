import os
from datetime import datetime
import sqlite3

stockdb_path = os.path.join(os.path.dirname(__file__), "stock.db")


def validar_fecha_dw(fecha):
    """
    Validar que el formato de fecha es yyyy-mm-dd
    """
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validar_rango_fechas_dw(fecha_inicio, fecha_fin):
    """
    Validar que fecha_inicio es menor que fecha_fin
    """
    try:
        dt_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        dt_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        return dt_inicio <= dt_fin
    except ValueError:
        return False


def pedir_fecha(mensaje="Ingrese una fecha (dd/mm/aaaa): ", permitir_hoy=True, formato="%d/%m/%Y", permitir_futuras=False):
    """
    Pide al usuario una fecha, valida el formato y opcionalmente impide fechas futuras.
    Devuelve un objeto datetime.
    """
    while True:
        entrada = input(mensaje).strip()

        # Si se permite usar la fecha actual
        if permitir_hoy and (entrada.upper() == "HOY" or entrada == ""):
            return datetime.today()

        try:
            fecha = datetime.strptime(entrada, formato)

            # Validar si se permiten fechas futuras
            if not permitir_futuras and fecha > datetime.today():
                print(" Error: La fecha no puede ser futura.")
                continue

            return fecha

        except ValueError:
            print(f" Error: Ingrese una fecha válida en el formato {formato}.")
            
            

def listarStock(conn, cursor):
    print("\n--- STOCK ACTUAL ---\n")

    cursor.execute("""
        SELECT s.id_producto, p.nombre, s.cantidad
        FROM stock s
        INNER JOIN productos p ON s.id_producto = p.id_producto
        ORDER BY p.nombre DESC;
    """)

    filas = cursor.fetchall()

    if not filas:
        print("No hay productos registrados en stock.\n")
        return

    # Encabezado
    print(f"{'ID':<6} {'Producto':<30} {'Cantidad':>10}")
    print("-" * 50)

    for id_prod, nombre, cantidad in filas:
        print(f"{id_prod:<6} {nombre:<30} {cantidad:>10}")

    print()

