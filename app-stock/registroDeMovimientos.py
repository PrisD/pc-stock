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

def CrearMovimiento(conn, cursor, datos, fecha_ingreso, auditoria):
    print("\n--- REGISTRAR MOVIMIENTO ---")

    # -------------------------------------------------------------
    # BUCLE PARA PEDIR FECHA HASTA QUE SEA VÁLIDA
    # -------------------------------------------------------------
    while True:
        try:
            fecha_input = pedir_fecha(
                mensaje="Ingrese fecha del movimiento (dd/mm/aaaa) o presione Enter para usar la fecha actual: ",
                permitir_hoy=True,
                formato="%d/%m/%Y",
                permitir_futuras=False
            )

            # convertir si viene como string
            if isinstance(fecha_input, str):
                fecha = datetime.strptime(fecha_input, "%d/%m/%Y")
            else:
                fecha = fecha_input

            # ----- Validar que la fecha del movimiento sea >= fecha ingreso del lote -----
            if datos["lote_es_nuevo"]:
                fecha_ingreso_lote = datos["datos_lote_nuevo"]["fecha_ingreso"]
            else:
                fecha_ingreso_lote = fecha_ingreso

            # convertir si viene string
            if isinstance(fecha_ingreso_lote, str):
                fecha_ingreso_lote = datetime.strptime(fecha_ingreso_lote, "%Y-%m-%d")

            # Validación final
            if fecha < fecha_ingreso_lote:
                print(
                    f"\nError: La fecha del movimiento ({fecha.strftime('%d/%m/%Y')}) "
                    f"no puede ser anterior a la fecha de ingreso del lote "
                    f"({fecha_ingreso_lote.strftime('%d/%m/%Y')}).\n"
                )
                continue  # <-- volver a pedir fecha

            break  # <-- fecha válida, salimos del while

        except ValueError:
            print("Error: La fecha ingresada no tiene el formato correcto.\n")
            continue

        except SalidaAlMenu:
            print("Operación cancelada.\n")
            return None

    # -------------------------------------------------------------
    # FECHA VÁLIDA → PROCESAR MOVIMIENTO
    # -------------------------------------------------------------
    datos["fecha"] = fecha

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
        while True:
            try:
                id_producto = int(pedir("Ingrese el ID del producto: "))
                
                if id_producto < 0:
                    print("Error: El ID del producto no puede ser negativo.\n")
                    continue
                
                break  # válido → salimos del while
    
            except ValueError:
                print("Error: El ID del producto debe ser un número.\n")
                continue
            except SalidaAlMenu:
                print("\nOperación cancelada. Volviendo al menú...\n")
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
            
            # --- seleccionar lote ---
            while True:
                try:
                    codigo = pedir("Ingrese el ID del lote o ENTER para crear uno nuevo: ").strip()
                    break
                except SalidaAlMenu:
                    print("Operación cancelada.\n")
                    return


            if codigo == "":  # Crear nuevo lote
                datos_lote_nuevo = CrearLote(conn, cursor, id_producto, id_usuario, auditoria)
                lote_es_nuevo = True
                cantidad = datos_lote_nuevo["cantidad"]
                id_lote = None  #se asignará al insertar en la DB
            
            else: # Usar lote existente
                # validar ID lote
                while True:
                    try:
                        id_lote = int(codigo)
                        break
                    except ValueError:
                        print("Error: El ID del lote debe ser un número.\n")
                        try:
                            codigo = pedir("Ingrese el ID del lote: ").strip()
                        except SalidaAlMenu:
                            print("Operación cancelada.\n")
                            return

                # Verificar si el lote existe
                cursor.execute(
                    "SELECT cantidad, estado,fecha_ingreso FROM lotes WHERE id_lote = ? AND id_producto = ?", (id_lote, id_producto))
                lote = cursor.fetchone()
                if lote is None:
                    print("El lote no existe.\n")
                    return

                stock_actual, estado_lote, fecha_ingreso = lote
                
                # validar cantidad a ingresar
                while True:
                    try:
                        texto = pedir("Cantidad a INGRESAR: ").strip()

                        if not texto.isdigit():
                            raise ValueError("Debe ser un número entero positivo.")

                        cantidad = int(texto)

                        if cantidad <= 0:
                            raise ValueError("La cantidad debe ser mayor a 0.")

                        break

                    except ValueError as e:
                        print(f"Error: {e}\n")
                        continue
                    except SalidaAlMenu:
                        print("Operación cancelada.\n")
                        return
                
        
        
        
        else:  # EGRESO
            # validar ID lote
            while True:
                try:
                    texto = pedir("Ingrese el ID del lote: ").strip()
                    id_lote = int(texto)
                    break
                except ValueError:
                    print("Error: El ID del lote debe ser un número.\n")
                    continue
                except SalidaAlMenu:
                    print("Operación cancelada.\n")
                    return


            # Obtener stock actual del lote
            cursor.execute(
                "SELECT cantidad, estado, fecha_ingreso FROM lotes WHERE id_lote = ? AND id_producto = ?", (id_lote, id_producto))
            lote = cursor.fetchone()
            
            if lote is None:
                print("Error: El lote no existe. No se puede registrar el egreso.\n")
                return

            stock_actual, estado_lote, fecha_ingreso = lote
            
            if estado_lote == "vencido":
                print("Egreso de un lote vencido, no apto para la venta.\n")
                
            if stock_actual == 0:
                print("No se puede retirar de un lote vacio.\n")
                return
                
            
            # validar cantidad a retirar
            while True:
                try:
                    texto = pedir("Cantidad a RETIRAR: ").strip()

                    if not texto.isdigit():
                        raise ValueError("Debe ser un número entero positivo.")

                    cantidad = int(texto)

                    if cantidad <= 0:
                        raise ValueError("La cantidad debe ser mayor a 0.")

                    if cantidad > stock_actual:
                        raise ValueError(f"Stock insuficiente (hay {stock_actual}).")

                    break

                except ValueError as e:
                    print(f"Error: {e}\n")
                    continue
                except SalidaAlMenu:
                    print("Operación cancelada.\n")
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
        fecha_ingreso = fecha_ingreso if not lote_es_nuevo else datos_lote_nuevo["fecha_ingreso"]
        
        CrearMovimiento(conn, cursor, datos,fecha_ingreso, auditoria)



    except SalidaAlMenu:
        print("\nOperación cancelada. Volviendo al menú...\n")
        return


# ---------------- MENU REGISTRO DE MOVIMIENTOS --------------------
def menuRegistrarMovimiento(conn, cursor, id_usuario, auditoria): # falta agregar id_usuario
    seguir = True
    try:
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
    
    except SalidaAlMenu:
        print("\nOperación cancelada. Volviendo al menú...\n")
        return




#QUE SE PUEDAN INGRESAR LOTES VENCIDOS
