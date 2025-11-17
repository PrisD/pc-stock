from datetime import datetime
from actualizacion_stock import actualizar_stock
from crear_productos import CrearProducto, ListarProductos
from crear_lotes import CrearLote, ListarLotes, ListarLotesDeProducto  
from utils import pedir_fecha
import sqlite3

class SalidaAlMenu(Exception):
    pass

def pedir(mensaje):
    texto = input(mensaje).strip()
    if texto.lower() == "salir":
        raise SalidaAlMenu()
    return texto

# ---------------------------  CREAR MOVIMIENTOS------------------------------------

def CrearMovimiento(conn, cursor, datos, auditoria):
    print("\n--- REGISTRAR MOVIMIENTO ---")

    # Obtener fecha del movimiento
    fecha_input = pedir_fecha(
        mensaje="Ingrese fecha del movimiento (dd/mm/aaaa) o presione Enter para usar la fecha actual: ",
        permitir_hoy=True,
        formato="%d/%m/%Y",
        permitir_futuras=False
    )
    
    if isinstance(fecha_input, str):
        fecha = datetime.strptime(fecha_input, "%d/%m/%Y")
    else:
        fecha = fecha_input

    # Agregar la fecha al paquete de datos
    datos["fecha"] = fecha

    # Llamar al módulo que sí inserta y hace commit
    try:
        return actualizar_stock(conn, cursor, datos, auditoria)

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
def RegistrarMovimiento(conn, cursor, tipo, id_usuario, auditoria):
    try:
        print(f"\n--- REGISTRAR {tipo} DE MERCANCÍA ---")

        # ---------------- 1) Seleccionar producto ----------------
        try:
            id_producto = int(pedir("Ingrese el ID del producto: "))
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
                respuesta = pedir("> ").strip().upper()
                if respuesta == "S":
                    id_producto = CrearProducto(conn, cursor, id_usuario, auditoria)
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
        
        ListarLotesDeProducto(conn, cursor, id_producto)  # Mostrar los lotes del producto seleccionado
        
        lote_es_nuevo = False
        datos_lote_nuevo = None
        
        if tipo == "INGRESO":
            codigo = pedir(
                "Ingrese el ID del lote o presione ENTER para crear uno nuevo: ").strip()

            if codigo == "":  # Crear nuevo lote
                datos_lote_nuevo = CrearLote(conn, cursor, id_producto, id_usuario, auditoria)
                lote_es_nuevo = True

                cantidad = datos_lote_nuevo["cantidad"]
                id_lote = None  #se asignará al insertar en la DB
            
            else: # Usar lote existente
                try:
                    id_lote = int(codigo)
                except ValueError:
                    print("Error: El ID del lote debe ser un número.\n")
                    return

                # Verificar si el lote existe
                cursor.execute(
                    "SELECT cantidad, estado FROM lotes WHERE id_lote = ? AND id_producto = ?", (id_lote, id_producto))
                lote = cursor.fetchone()
                if lote is None:
                    print("El lote no existe.\n")
                    return

                stock_actual, estado_lote = lote
                
                try:
                    texto = pedir("Cantidad a INGRESAR: ").strip()

                    if not texto.isdigit():
                        raise ValueError("Debe ser un número entero positivo.")

                    cantidad = int(texto)

                    if cantidad <= 0:
                        raise ValueError("La cantidad debe ser mayor a 0.")

                except ValueError as e:
                    print(f"Error: {e}\n")
                    return

                except SalidaAlMenu:
                    print("Operación cancelada.\n")
                    return
                
        
        
        
        else:  # EGRESO
            try:
                id_lote = int(pedir("Ingrese el ID del lote: "))
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

            stock_actual, estado_lote = lote
            
            if estado_lote == "vencido":
                print("Egreso de un lote vencido, no apto para la venta.\n")
            
            try:
                texto = pedir("Cantidad a RETIRAR: ").strip()

                if not texto.isdigit():
                    raise ValueError("Debe ser un número entero positivo.")

                cantidad = int(texto)

                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0.")

            except ValueError as e:
                print(f"Error: {e}\n")
                return

            except SalidaAlMenu:
                print("Operación cancelada.\n")
                return

            if cantidad > stock_actual:
                print(f"Stock insuficiente (hay {stock_actual}).\n")
                return
            

        # ---------------- 3) Confirmación ----------------
        print("\n--- CONFIRMAR MOVIMIENTO ---")
        print(f"Producto ID: {id_producto}")
        print(f"Tipo: {tipo}")
        if lote_es_nuevo:
            print(f"Lote nuevo (sin ID aún)")
        else:
            print(f"Lote ID: {id_lote}")
        print(f"Cantidad: {cantidad}")

        confirm = pedir("ENTER para confirmar, otra cosa para cancelar: ").strip()
        if confirm != "":
            print("Movimiento cancelado.\n")
            return
        
        
            # ---------------- Crear movimiento ----------------
        datos = {
            "tipo": tipo,
            "id_producto": id_producto,
            "lote_es_nuevo": lote_es_nuevo,
            "id_lote": id_lote,
            "datos_lote_nuevo": datos_lote_nuevo,
            "cantidad": cantidad,
            "id_usuario": id_usuario,
            "estado_lote": estado_lote if not lote_es_nuevo else datos_lote_nuevo["estado"]
        }

        
        CrearMovimiento(conn, cursor, datos, auditoria)



    except SalidaAlMenu:
        print("\nOperación cancelada. Volviendo al menú...\n")
        return


# ---------------- MENU REGISTRO DE MOVIMIENTOS --------------------
def menuRegistrarMovimiento(conn, cursor, id_usuario, auditoria): # falta agregar id_usuario
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
        opcion = pedir("> ")

        if opcion == "1":
            RegistrarMovimiento(conn, cursor, "INGRESO", id_usuario, auditoria)
        elif opcion == "2":
            # falta agregar id_usuario
            RegistrarMovimiento(conn, cursor, "EGRESO", id_usuario, auditoria)
        elif opcion == "3":
            CrearProducto(conn, cursor, id_usuario, auditoria)
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




#QUE SE PUEDAN INGRESAR LOTES VENCIDOS
