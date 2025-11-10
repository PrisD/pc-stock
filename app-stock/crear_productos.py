from datetime import datetime
from actualizacion_stock import actualizar_stock
import sqlite3

def CrearProducto(conn, cursor, usuario, auditoria):
    print("\n--- CREAR PRODUCTO ---")

    # ---------------- VALIDAR NOMBRE ----------------
    while True:
        nombre = input("Nombre (máx 50 caracteres): ").strip()

        if len(nombre) > 50:
            print("Error: El nombre no debe exceder los 50 caracteres.\n")
            continue

        break  # nombre válida

    # ---------------- VALIDAR DESCRIPCIÓN ----------------
    while True:
        descripcion = input("Descripción (máx 100 caracteres): ").strip()

        if len(descripcion) > 100:
            print("Error: La descripción no debe exceder los 100 caracteres.\n")
            continue

        break  # Descripción válida

    # ---------------- VALIDAR STOCK BAJO ----------------
    while True:
        stock_min_texto = input("Stock bajo: ").strip()

        if not stock_min_texto.isdigit():
            print("Error: El stock bajo debe ser un número entero.\n")
            continue

        stock_min = int(stock_min_texto)

        if stock_min < 0:
            print("Error: El stock bajo debe ser mayor o igual a 0.\n")
            continue

        break  # Stock bajo válido

    # ---------------- VALIDAR STOCK CRITICO ----------------
    while True:
        stock_critico_texto = input("Stock critico: ").strip()

        if not stock_critico_texto.isdigit():
            print("Error: El stock critico debe ser un número entero.\n")
            continue

        stock_critico = int(stock_critico_texto)

        if stock_critico < 0:
            print("Error: El stock critico debe ser mayor o igual a 0.\n")
            continue

        if stock_critico > stock_min:
            print("Error: El stock critico debe ser mayor o igual al stock bajo.\n")
            continue

        break  # Stock critico válido

    # ---------------- GUARDAR EN "BASE DE DATOS" ----------------
    try:
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, stock_bajo, stock_critico)
            VALUES (?, ?, ?, ?)
        """, (nombre, descripcion, stock_min, stock_critico))
        conn.commit()

        id_producto = cursor.lastrowid  # Recupera el ID asignado automáticamente

        print(
            f"\n Producto '{nombre}' creado correctamente con ID {id_producto}.\n")
        auditoria.registrar_auditoria(usuario[0], "CREAR_PRODUCTO", "PRODUCTOS", f"Usuario {usuario[1]} creó el producto ID: {id_producto}, Nombre: {nombre} , Descripción: {descripcion}, Stock Bajo: {stock_min}, Stock Crítico: {stock_critico}")
        return id_producto

    except sqlite3.Error as e:
        print(f"\n Error al guardar el producto: {e}\n")
        conn.rollback()
        return None

    # ---------------- LISTAR PRODUCTOS----------------


def cortar(texto, max_len):
    return texto if len(texto) <= max_len else texto[:max_len-3] + "..."


def ListarProductos(conn, cursor):
    print("\n--- LISTADO DE PRODUCTOS ---")

    try:
        cursor.execute(
            "SELECT id_producto, nombre, descripcion, stock_bajo, stock_critico FROM productos ORDER BY id_producto DESC")
        productos = cursor.fetchall()

        if not productos:
            print("No hay productos cargados.\n")
            return

        # Encabezado
        print(
            f"{'ID':<5} {'nombre':<35} {'Descripción':<35} {'Stock Bajo':<12} {'Stock Crítico':<12}")
        print("-" * 105)

        # Filas
        for prod in productos:
            id_producto, nombre, descripcion, stock_bajo, stock_critico = prod
            descripcion_corta = cortar(descripcion, 35)
            nombre_corto = cortar(nombre, 35)
            print(
                f"{id_producto:<5} {nombre_corto:<35} {descripcion_corta:<35} {stock_bajo:<12} {stock_critico:<12}")

        print()

    except Exception as e:
        print(f" Error al listar productos: {e}\n")