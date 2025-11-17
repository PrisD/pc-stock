from datetime import datetime
from utils import pedir_fecha
import sqlite3


def CrearLote(conn, cursor, id_producto, usuario, auditoria):
    print("\n--- CREAR LOTE (SIN GUARDAR AÚN) ---")

    # ---------------- INGRESAR Y VALIDAR FECHA DE INGRESO ----------------
    fecha_ingreso = pedir_fecha(
        mensaje="Fecha de ingreso (dd/mm/aaaa) o Enter para hoy: ",
        permitir_hoy=True,
        formato="%d/%m/%Y",
        permitir_futuras=False
    )

    # ---------------- INGRESAR Y VALIDAR FECHA DE VENCIMIENTO ----------------
    while True:
        fecha_venc = pedir_fecha(
            mensaje="Fecha de vencimiento (dd/mm/aaaa): ",
            permitir_hoy=False,
            formato="%d/%m/%Y",
            permitir_futuras=True
        )

        if fecha_venc < fecha_ingreso:
            print("Error: La fecha de vencimiento no puede ser anterior a la fecha de ingreso.\n")
            continue

        break

    # ---------------- VALIDAR CANTIDAD ----------------
    while True:
        txt = input("Cantidad inicial: ").strip()

        if not txt.isdigit():
            print("Error: Debe ser un número entero.\n")
            continue

        cantidad = int(txt)

        if cantidad <= 0:
            print("Error: Debe ser mayor a 0.\n")
            continue

        break

    # ---------------- ARMAR OBJETO DE RETORNO ----------------
    datos_lote = {
        "id_producto": id_producto,
        "fecha_ingreso": fecha_ingreso,
        "fecha_venc": fecha_venc,
        "cantidad": cantidad,
        "estado": "activo",   # siempre nuevo lote = activo
        "usuario": usuario
    }

    print("\nLote preparado correctamente (SE CREARÁ SOLO SI CONFIRMÁS EL MOVIMIENTO).\n")

    return datos_lote

    # ---------------- LISTAR LOTES----------------


def ListarLotes(conn, cursor):
    print("\n--- LISTADO DE LOTES ---")

    try:
        cursor.execute("""
            SELECT id_lote, id_producto, cantidad, fecha_ingreso, fecha_vencimiento, estado
            FROM lotes
            ORDER BY id_lote DESC
        """)
        lotes = cursor.fetchall()

        if not lotes:
            print("No hay lotes cargados.\n")
            return

        # Encabezado
        print(f"{'ID Lote':<10} {'ID Prod':<10} {'Cantidad':<10} {'F. Ingreso':<15} {'F. Vencimiento':<17} {'Estado'}")
        print("-" * 80)

        for id_lote, id_prod, cantidad, fecha_ing, fecha_vto, estado in lotes:
            try:
                fecha_ing_dt = datetime.fromisoformat(fecha_ing)
                fecha_ing_str = fecha_ing_dt.strftime("%d/%m/%Y")
            except Exception:
                fecha_ing_str = fecha_ing  # por si viene ya formateada

            if fecha_vto:
                try:
                    fecha_vto_dt = datetime.fromisoformat(fecha_vto)
                    fecha_vto_str = fecha_vto_dt.strftime("%d/%m/%Y")
                except Exception:
                    fecha_vto_str = fecha_vto
            else:
                fecha_vto_str = "-"

            print(
                f"{id_lote:<10} {id_prod:<10} {cantidad:<10} {fecha_ing_str:<15} {fecha_vto_str:<17} {estado}")

        print()

    except Exception as e:
        print(f" Error al listar lotes: {e}\n")
        
        
        
def ListarLotesDeProducto(conn, cursor, id_producto):
    print(f"\n--- LOTES DEL PRODUCTO {id_producto} ---")

    try:
        cursor.execute("""
            SELECT id_lote, cantidad, fecha_ingreso, fecha_vencimiento, estado
            FROM lotes
            WHERE id_producto = ?
            ORDER BY id_lote DESC
        """, (id_producto,))
        lotes = cursor.fetchall()

        if not lotes:
            print("No hay lotes cargados para este producto.\n")
            return

        # Encabezado
        print(f"{'ID Lote':<10} {'Cantidad':<10} {'F. Ingreso':<15} {'F. Vencimiento':<17} {'Estado'}")
        print("-" * 80)

        for id_lote, cantidad, fecha_ing, fecha_vto, estado in lotes:

            # --- Formateo de fechas ---
            try:
                fecha_ing_dt = datetime.fromisoformat(fecha_ing)
                fecha_ing_str = fecha_ing_dt.strftime("%d/%m/%Y")
            except Exception:
                fecha_ing_str = fecha_ing

            if fecha_vto:
                try:
                    fecha_vto_dt = datetime.fromisoformat(fecha_vto)
                    fecha_vto_str = fecha_vto_dt.strftime("%d/%m/%Y")
                except Exception:
                    fecha_vto_str = fecha_vto
            else:
                fecha_vto_str = "-"

            print(
                f"{id_lote:<10} {cantidad:<10} {fecha_ing_str:<15} {fecha_vto_str:<17} {estado}"
            )

        print()

    except Exception as e:
        print(f"Error al listar los lotes del producto: {e}\n")
