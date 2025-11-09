from datetime import datetime
from actualizacion_stock import actualizar_stock
from crear_productos import CrearProducto, ListarProductos
from crear_lotes import CrearLote, ListarLotes  
from utils import pedir_fecha
import sqlite3


# ---------------------------  CREAR MOVIMIENTOS------------------------------------

def CrearMovimiento(conn, cursor, id_lote, id_usuario, tipo, cantidad):
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
        return actualizar_stock(id_lote, id_usuario, tipo, cantidad, fecha)

    except Exception as e:
        print(f"Error al registrar el movimiento: {e}")
        conn.rollback()
        return None

    # ---------------- LISTAR MOVIMIENTOS ---------------


def ListarMovimientos(conn, cursor):
    print("\n--- LISTADO DE MOVIMIENTOS ---")
    try:
        cursor.execute("""
            SELECT id_movimiento, id_lote, id_usuario, tipo, cantidad, fecha
            FROM movimientos
            ORDER BY id_movimiento DESC
        """)
        movimientos = cursor.fetchall()

        if not movimientos:
            print("No hay movimientos registrados.\n")
            return

        # Encabezado
        print(f"{'ID Mov':<10} {'ID Lote':<10} {'ID Usuario':<10} {'Tipo':<6} {'Cantidad':<10} {'Fecha':<12}")
        print("-" * 65)

        for id_mov, id_lote, id_usuario, tipo, cantidad, fecha in movimientos:
            fecha_str = datetime.strptime(
                fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
            tipo_str = "Ingreso" if tipo == 1 else "Egreso"
            print(
                f"{id_mov:<10} {id_lote:<10} {id_usuario:<10} {tipo_str:<6} {cantidad:<10} {fecha_str:<12}")

        print()

    except Exception as e:
        print(f"Error al listar movimientos: {e}\n")


# ---------------------------REGISTRAR MOVIMIENTOS------------------------------------
def RegistrarMovimiento(conn, cursor, tipo, id_usuario):
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
            "SELECT cantidad, estado FROM lotes WHERE id_lote = ? AND id_producto = ?", (id_lote, id_producto))
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
        
        if lote[1] == "vencido":
            print(f"Error: no se pueden hacer egresos de lotes vencidos\n")
            return

        # Actualizar stock del lote
        nueva_cantidad = lote[0] - cantidad
        cursor.execute(
            "UPDATE lotes SET cantidad = ? WHERE id_lote = ?", (nueva_cantidad, id_lote))
        conn.commit()
        print("Stock del lote actualizado.\n")

    # ---------------- 3) Registrar movimiento ----------------
    CrearMovimiento(conn, cursor, id_lote, id_usuario,
                    1 if tipo.upper() == "INGRESO" else 0, cantidad)


def menuRegistrarMovimiento(conn, cursor, id_usuario, auditoria): # falta agregar id_usuario
    auditoria.registrar_auditoria(id_usuario[0], "INGRESO","MOVIMIENTOS",f"Usuario {id_usuario[1]} ingresó al módulo")
    seguir = True
    while seguir:
        print("\n--- MENU DE REGISTRO DE ENTRADAS Y SALIDAS ---")
        print("1. Registrar Ingreso")
        print("2. Registrar Egreso")
        print("3. Crear Producto")
        print("4. Listar Productos")
        print("5. Listar Lotes")
        print("6. Listar Movimientos")
        print("7. Salir")
        opcion = input("> ")

        if opcion == "1":
            RegistrarMovimiento(conn, cursor, "INGRESO", id_usuario[0])
        elif opcion == "2":
            # falta agregar id_usuario
            RegistrarMovimiento(conn, cursor, "EGRESO", id_usuario[0])
        elif opcion == "3":
            CrearProducto(conn, cursor)
        elif opcion == "4":
            ListarProductos(conn, cursor)
        elif opcion == "5":
            ListarLotes(conn, cursor)
        elif opcion == "6":
            ListarMovimientos(conn, cursor)
        elif opcion == "7":
            print("Saliendo...")
            seguir = False
        else:
            print("Opción inválida.")


# -------------------- EJECUCIÓN PRINCIPAL --------------------

#QUE SE PUEDAN INGRESAR LOTES VENCIDOS
#QUE APAREZCAN ARRIBA LOS ULTIMOS LOTES, LOS ULTIMOS MOVIMIENTOS, LOS ULTIMOS PRODUCTOS CREADOS