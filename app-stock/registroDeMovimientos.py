from datetime import datetime
import sqlite3

# ------------------ "BASES DE DATOS" EN MEMORIA ------------------

productos = {}
lotes = {}
movimientos = []
alertas = []


# ---------------------------FECHA------------------------------------
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


# ---------------------------PRODUCTOS------------------------------------

def CrearProducto(conn, cursor):
    print("\n--- CREAR PRODUCTO ---")

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

        # FALTA CONTROLAR QUE CRITICO SEA MENOR QUE BAJO
        stock_critico = int(stock_critico_texto)

        if stock_critico < 0:
            print("Error: El stock critico debe ser mayor o igual a 0.\n")
            continue

        break  # Stock critico válido

    # ---------------- ASIGNAR NUEVO ID ----------------
    id_producto = len(productos) + 1

    # ---------------- GUARDAR EN "BASE DE DATOS" ----------------
    try:
        cursor.execute("""
            INSERT INTO productos (descripcion, stock_bajo, stock_critico)
            VALUES (?, ?, ?)
        """, (descripcion, stock_min, stock_critico))
        conn.commit()

        id_producto = cursor.lastrowid  # Recupera el ID asignado automáticamente

        print(
            f"\n Producto '{descripcion}' creado correctamente con ID {id_producto}.\n")
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
            "SELECT id_producto, descripcion, stock_bajo, stock_critico FROM productos")
        productos = cursor.fetchall()

        if not productos:
            print("No hay productos cargados.\n")
            return

        # Encabezado
        print(f"{'ID':<5} {'Descripción':<35} {'Stock Bajo':<12} {'Stock Crítico':<12}")
        print("-" * 70)

        # Filas
        for prod in productos:
            id_producto, descripcion, stock_bajo, stock_critico = prod
            descripcion_corta = cortar(descripcion, 35)
            print(
                f"{id_producto:<5} {descripcion_corta:<35} {stock_bajo:<12} {stock_critico:<12}")

        print()

    except Exception as e:
        print(f" Error al listar productos: {e}\n")


# ---------------------------LOTES------------------------------------

def CrearLote(conn, cursor, id_producto):
    print("\n--- CREAR LOTE ---")

    # ---------------- ID LOTES ----------------
    id_lote = len(lotes) + 1

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
            print(
                "❌ Error: La fecha de vencimiento no puede ser anterior a la de ingreso.")
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


# ---------------------------  CREAR MOVIMIENTOS------------------------------------

def CrearMovimiento(conn, cursor, id_lote, id_producto, tipo, cantidad):
    print("\n--- REGISTRAR MOVIMIENTO ---")

    # 1) Obtener fecha actual directamente
    fecha = pedir_fecha(
        mensaje="Ingrese fecha del movimiento (dd/mm/aaaa) o presione Enter para usar la fecha actual: ",
        permitir_hoy=True,
        formato="%d/%m/%Y",
        permitir_futuras=False
    )

    # 2) Guardar en la base de datos
    try:
        cursor.execute("""
            INSERT INTO movimientos (id_lote, id_producto, tipo, cantidad, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (id_lote, id_producto, tipo, cantidad, fecha.strftime("%Y-%m-%d")))
        conn.commit()

        id_movimiento = cursor.lastrowid
        print(f"Movimiento {id_movimiento} registrado correctamente.\n")
        return id_movimiento

    except Exception as e:
        print(f"Error al registrar el movimiento: {e}")
        conn.rollback()
        return None

    # ---------------- LISTAR MOVIMIENTOS ---------------


def ListarMovimientos(conn, cursor):
    print("\n--- LISTADO DE MOVIMIENTOS ---")
    try:
        cursor.execute("""
            SELECT id_movimiento, id_lote, id_producto, tipo, cantidad, fecha
            FROM movimientos
            ORDER BY id_movimiento
        """)
        movimientos = cursor.fetchall()

        if not movimientos:
            print("No hay movimientos registrados.\n")
            return

        # Encabezado
        print(
            f"{'ID Mov':<10} {'ID Lote':<10} {'ID Prod':<10} {'Tipo':<6} {'Cantidad':<10} {'Fecha':<12}")
        print("-" * 65)

        for id_mov, id_lote, id_prod, tipo, cantidad, fecha in movimientos:
            fecha_str = datetime.strptime(
                fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
            tipo_str = "Ingreso" if tipo == 1 else "Egreso"
            print(
                f"{id_mov:<10} {id_lote:<10} {id_prod:<10} {tipo_str:<6} {cantidad:<10} {fecha_str:<12}")

        print()

    except Exception as e:
        print(f"Error al listar movimientos: {e}\n")


# ---------------------------REGISTRAR MOVIMIENTOS------------------------------------
def RegistrarMovimiento(conn, cursor, tipo):
    print(f"\n--- REGISTRAR {tipo} DE MERCANCÍA ---")

    # ---------------- 1) Seleccionar producto ----------------
    try:
        id_producto = int(input("Ingrese el ID del producto: "))
    except ValueError:
        # Hay que hacer un bucle para que no se cierre de una
        print("Error: El ID del producto debe ser un número.\n")
        return

    # Verificar si el producto existe en la DB
    cursor.execute(
        "SELECT id_producto FROM productos WHERE id_producto = ?", (id_producto,))
    producto = cursor.fetchone()

    if producto is None:
        if tipo == "INGRESO":
            print("Producto no encontrado. ¿Desea crearlo ahora? (S/N)")
            respuesta = input("> ").strip().upper()
            if respuesta == "S":
                id_producto = CrearProducto(conn, cursor)
                if id_producto is None:
                    print("Error al crear producto. Operación cancelada.\n")
                    return
            else:
                print("Operación cancelada.\n")
                return
        else:
            print("Error: No se puede registrar egreso de un producto inexistente.\n")
            return

    # ---------------- 2) Seleccionar lote ----------------
    if tipo == "INGRESO":
        codigo = input(
            "Ingrese el ID del lote o presione ENTER para crear uno nuevo: ").strip()

        if codigo == "":  # Crear nuevo lote
            id_lote = CrearLote(conn, cursor, id_producto)
            if id_lote is None:
                print("Error al crear el lote. Operación cancelada.\n")
                return

            # Obtener la cantidad inicial del lote recién creado
            cursor.execute(
                "SELECT cantidad FROM lotes WHERE id_lote = ?", (id_lote,))
            cantidad = cursor.fetchone()[0]

        else:
            try:
                id_lote = int(codigo)
            except ValueError:
                print("Error: El ID del lote debe ser un número.\n")
                return

            # Verificar si el lote existe
            cursor.execute(
                "SELECT cantidad FROM lotes WHERE id_lote = ? AND id_producto = ?", (id_lote, id_producto))
            lote = cursor.fetchone()
            if lote is not None:
                try:
                    cantidad_ingreso = int(
                        input("Ingrese la cantidad a ingresar al lote (unidades): "))
                except ValueError:
                    print("Error: La cantidad debe ser un número entero.\n")
                    return

                # Actualizar stock del lote
                nueva_cantidad = lote[0] + cantidad_ingreso
                cursor.execute(
                    "UPDATE lotes SET cantidad = ? WHERE id_lote = ?", (nueva_cantidad, id_lote))
                conn.commit()
                cantidad = cantidad_ingreso
                print("Stock del lote existente actualizado.\n")
            else:
                print("Error: El lote no existe. Operación cancelada.\n")
                return

    else:  # EGRESO
        try:
            id_lote = int(input("Ingrese el ID del lote: "))
        except ValueError:
            print("Error: El ID del lote debe ser un número.\n")
            return

        # Obtener stock actual del lote
        cursor.execute(
            "SELECT cantidad FROM lotes WHERE id_lote = ? AND id_producto = ?", (id_lote, id_producto))
        lote = cursor.fetchone()
        if lote is None:
            print("Error: El lote no existe. No se puede registrar el egreso.\n")
            return

        try:
            cantidad = int(
                input("Ingrese la cantidad a retirar del lote (unidades): "))
        except ValueError:
            print("Error: La cantidad debe ser un número entero.\n")
            return

        if cantidad > lote[0]:
            print(f"Error: Stock insuficiente. Disponible: {lote[0]}\n")
            return

        # Actualizar stock del lote
        nueva_cantidad = lote[0] - cantidad
        cursor.execute(
            "UPDATE lotes SET cantidad = ? WHERE id_lote = ?", (nueva_cantidad, id_lote))
        conn.commit()
        print("Stock del lote actualizado.\n")

    # ---------------- 3) Registrar movimiento ----------------
    CrearMovimiento(conn, cursor, id_lote, id_producto,
                    1 if tipo.upper() == "INGRESO" else 0, cantidad)


def Menu(conn, cursor):
    seguir = True
    while seguir:
        print("\n--- MENU DE REGISTRO DE ENTRADAS Y SALIDAS ---")
        print("1. Registrar Ingreso")
        print("2. Registrar Egreso")
        print("3. Crear Producto")
        print("4. Crear Lote")
        print("5. Crear movimiento")
        print("6. Listar Productos")
        print("7. Listar Lotes")
        print("8. Listar Movimientos")
        print("9. Salir")
        opcion = input("> ")

        if opcion == "1":
            RegistrarMovimiento(conn, cursor, "INGRESO")
        elif opcion == "2":
            RegistrarMovimiento(conn, cursor, "EGRESO")
        elif opcion == "3":
            CrearProducto(conn, cursor)
        elif opcion == "4":
            # Por ahora, se pasa un id_producto fijo
            CrearLote(conn, cursor, 1)
        elif opcion == "5":
            # Parámetros de ejemplo
            CrearMovimiento(conn, cursor, 1, 1, 1, 100)
        elif opcion == "6":
            ListarProductos(conn, cursor)
        elif opcion == "7":
            ListarLotes(conn, cursor)
        elif opcion == "8":
            ListarMovimientos(conn, cursor)
        elif opcion == "9":
            print("Saliendo...")
            seguir = False
        else:
            print("Opción inválida.")


# -------------------- EJECUCIÓN PRINCIPAL --------------------
