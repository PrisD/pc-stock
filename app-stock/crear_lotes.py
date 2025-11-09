from datetime import datetime
from utils import pedir_fecha
import sqlite3


def CrearLote(conn, cursor, id_producto):
    print("\n--- CREAR LOTE ---")

    # ---------------- INGRESAR Y VALIDAR FECHAS ----------------
    fecha_ingreso = pedir_fecha(
        mensaje="Fecha de ingreso (dd/mm/aaaa) o presione Enter para usar la fecha actual: ",
        permitir_hoy=True,
        formato="%d/%m/%Y",
        permitir_futuras=False
    )

    while True:
        fecha_vencimiento = pedir_fecha(
            mensaje="Fecha de vencimiento (dd/mm/aaaa): ",
            permitir_hoy=False,
            formato="%d/%m/%Y",
            permitir_futuras=True  # El vencimiento sí puede ser futuro
        )

        if fecha_vencimiento < fecha_ingreso:
            print("Error: La fecha de vencimiento no puede ser anterior a la de ingreso.")
        else:
            break

    # ---------------- VALIDAR CANTIDAD ----------------
    while True:
        cantidad_texto = input("Cantidad inicial: ").strip()

        if not cantidad_texto.isdigit():
            print("Error: La cantidad debe ser un número entero.\n")
            continue

        cantidad = int(cantidad_texto)

        if cantidad <= 0:
            print("Error: La cantidad debe ser mayor a 0.\n")
            continue

        break  # Cantidad válida

    # ---------------- GUARDAR EN "BASE DE DATOS" ----------------
    try:
        cursor.execute("""
            INSERT INTO lotes (id_producto, fecha_ingreso, cantidad, estado, fecha_vencimiento)
            VALUES (?, DATE(?), ?, ?, DATE(?))
        """, (id_producto, fecha_ingreso.strftime("%Y-%m-%d"), cantidad, "activo", fecha_vencimiento.strftime("%Y-%m-%d")))
        conn.commit()

        id_lote = cursor.lastrowid
        print(
            f"\n Lote '{id_lote}' creado correctamente para el producto {id_producto}.\n")
        return id_lote

    except Exception as e:
        print(f" Error al crear el lote: {e}\n")
        conn.rollback()
        return None

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