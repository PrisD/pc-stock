from datetime import datetime

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
                print("❌ Error: La fecha no puede ser futura.")
                continue

            return fecha

        except ValueError:
            print(f"❌ Error: Ingrese una fecha válida en el formato {formato}.")


# ---------------------------PRODUCTOS------------------------------------

def CrearProducto():
    print("\n--- CREAR PRODUCTO ---")

    # ---------------- VALIDAR NOMBRE ----------------
    while True:
        nombre = input("Nombre del producto: ").strip()

        if nombre == "":
            print("Error: El nombre no puede estar vacío.\n")
            continue

        if len(nombre) > 50:
            print("Error: El nombre no debe exceder los 50 caracteres.\n")
            continue
        
        # Validar si ya existe el producto (comparando por nombre)
        nombre_ya_existe = any(p["nombre"].lower() == nombre.lower() for p in productos.values())
        if nombre_ya_existe:
            print("Error: El producto ya existe.\n")
            continue

        break  # Nombre válido


    # ---------------- VALIDAR DESCRIPCIÓN ----------------
    while True:
        descripcion = input("Descripción (opcional, máx 100 caracteres): ").strip()

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

        stock_critico = int(stock_critico_texto)     #FALTA CONTROLAR QUE CRITICO SEA MENOR QUE BAJO

        if stock_critico < 0:
            print("Error: El stock critico debe ser mayor o igual a 0.\n")
            continue

        break  # Stock critico válido
    
    
    # ---------------- ASIGNAR NUEVO ID ----------------
    id_producto = len(productos) + 1

    # ---------------- GUARDAR EN "BASE DE DATOS" ----------------
    productos[id_producto] = {
        "nombre": nombre,
        "descripcion": descripcion,
        "stock_bajo": stock_min, 
        "stock_critico": stock_critico, 
    }

    print(f"\n Producto '{nombre}' creado correctamente con ID {id_producto}.\n")
    return id_producto



    # ---------------- LISTAR PRODUCTOS----------------
def cortar(texto, max_len):
    return texto if len(texto) <= max_len else texto[:max_len-3] + "..."


def ListarProductos():
    print("\n--- LISTADO DE PRODUCTOS ---")

    if not productos:
        print("No hay productos cargados.\n")
        return

    # Encabezado
    print(f"{'ID':<5} {'Nombre':<25} {'Descripción':<35} {'Stock Min':<12} {'Stock Crítico'}")
    print("-" * 90)

    for id_prod, prod in productos.items():
        nombre = cortar(prod['nombre'], 25)
        descripcion = cortar(prod['descripcion'], 35)

        print(f"{id_prod:<5} {nombre:<25} {descripcion:<35} {prod['stock_bajo']:<12} {prod['stock_critico']}")

    print()



# ---------------------------LOTES------------------------------------

def CrearLote(id_producto):
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
            print("❌ Error: La fecha de vencimiento no puede ser anterior a la de ingreso.")
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
    lotes[id_lote] = {
        "id_producto": id_producto,
        "cantidad": cantidad,
        "fecha_ingreso": fecha_ingreso,
        "fecha_vencimiento": fecha_vencimiento,
        "estado": "activo"
    }

    print(f"\nLote '{id_lote}' creado correctamente para el producto {id_producto}.\n")
    return id_lote


    # ---------------- LISTAR LOTES----------------
def ListarLotes():
    print("\n--- LISTADO DE LOTES ---")

    if not lotes:
        print("No hay lotes cargados.\n")
        return

    # Encabezado
    print(f"{'ID Lote':<10} {'ID Prod':<10} {'Cantidad':<10} {'F. Ingreso':<15} {'F. Vencimiento':<17} {'Estado'}")
    print("-" * 70)

    for id_lote, lote in lotes.items():
        fecha_ingreso_str = lote['fecha_ingreso'].strftime("%d/%m/%Y")
        fecha_vencimiento_str = lote['fecha_vencimiento'].strftime("%d/%m/%Y")
        print(f"{id_lote:<10} {lote['id_producto']:<10} {lote['cantidad']:<10} {fecha_ingreso_str:<12} {fecha_vencimiento_str:<12} {lote['estado']}")

    print()



# ---------------------------  CREAR MOVIMIENTOS------------------------------------

def CrearMovimiento(id_lote, tipo, cantidad, id_usuario):
    print("\n--- REGISTRAR MOVIMIENTO ---")

    # 1) Obtener fecha actual directamente
    fecha = pedir_fecha(
        mensaje="Ingrese fecha del movimiento (dd/mm/aaaa) o presione Enter para usar la fecha actual: ",
        permitir_hoy=True,
        formato="%d/%m/%Y",
        permitir_futuras=False
    )

    # 2) Generar ID de movimiento (siguiente número)
    id_movimiento = len(movimientos) + 1

    # 3) Guardar en la "base de datos"
    movimientos.append({
        "id_movimiento": id_movimiento,
        "id_lote": id_lote,
        "tipo": tipo,
        "cantidad": cantidad,
        "fecha": fecha,
        "id_usuario": id_usuario
    })

    print(f"Movimiento {id_movimiento} registrado correctamente.\n")
    return id_movimiento


    # ---------------- LISTAR MOVIMIENTOS ---------------
def ListarMovimientos():
    print("\n--- LISTADO DE MOVIMIENTOS ---")

    if not movimientos:
        print("No hay movimientos registrados.\n")
        return

    # Encabezado
    print(f"{'ID Mov':<10} {'ID Lote':<10} {'Tipo':<10} {'Cantidad':<10} {'Fecha':<12} {'ID Usuario':<12}")
    print("-" * 65)

    for movimiento in movimientos:
        fecha_str = movimiento['fecha'].strftime("%d/%m/%Y")
        print(f"{movimiento['id_movimiento']:<10} "
              f"{movimiento['id_lote']:<10} "
              f"{movimiento['tipo']:<10} "
              f"{movimiento['cantidad']:<10} "
              f"{fecha_str:<12} "
              f"{movimiento['id_usuario']:<12}")

    print()



# ---------------------------REGISTRAR MOVIMIENTOS------------------------------------
def RegistrarMovimiento(tipo):
    print(f"\n--- REGISTRAR {tipo} DE MERCANCÍA ---")
    id_usuario = 1  # Usuario fijo por ahora

    # ---------------- 1) Seleccionar producto ----------------
    try:
        id_producto = int(input("Ingrese el ID del producto: "))
    except ValueError:
        print("Error: El ID del producto debe ser un número.\n")    #Hay que hacer un bucle para que no se cierre de una
        return

    producto = productos.get(id_producto)

    if producto is None:
        if tipo == "INGRESO":
            print("Producto no encontrado. ¿Desea crearlo ahora? (S/N)")
            respuesta = input("> ").strip().upper()
            if respuesta == "S":
                id_producto = CrearProducto()
                producto = productos.get(id_producto)
                if producto is None:
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
        codigo = input("Ingrese el ID del lote o presione ENTER para crear uno nuevo: ").strip()

        if codigo == "":  # Crear nuevo lote
            id_lote = CrearLote(id_producto)
            if id_lote is None:
                print("Error al crear el lote. Operación cancelada.\n")
                return

            lote = lotes.get(id_lote)
            cantidad = 0
            cantidad = lote['cantidad']  # La cantidad del movimiento es la del lote recién creado

        else:
            try:
                id_lote = int(codigo)
            except ValueError:
                print("Error: El ID del lote debe ser un número.\n")
                return

            lote = lotes.get(id_lote)
            if lote is not None:
                try:
                    cantidad = int(input("Ingrese la cantidad a ingresar al lote (unidades): "))
                except ValueError:
                    print("Error: La cantidad debe ser un número entero.\n")
                    return

                lote['cantidad'] += cantidad
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

        lote = lotes.get(id_lote)
        if lote is None:
            print("Error: El lote no existe. No se puede registrar el egreso.\n")
            return

        try:
            cantidad = int(input("Ingrese la cantidad a retirar del lote (unidades): "))
        except ValueError:
            print("Error: La cantidad debe ser un número entero.\n")
            return

        if cantidad > lote['cantidad']:
            print(f"Error: Stock insuficiente. Disponible: {lote['cantidad']}\n")
            return

        lote['cantidad'] -= cantidad
        print("Stock del lote actualizado.\n")

    # ---------------- 3) Registrar movimiento ----------------
    CrearMovimiento(id_lote, tipo, cantidad, id_usuario)




def Menu():
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
            RegistrarMovimiento("INGRESO")
        elif opcion == "2":
            RegistrarMovimiento("EGRESO")
        elif opcion == "3":
            CrearProducto()
        elif opcion == "4":
            CrearLote(1)  # Por ahora, se pasa un id_producto fijo
        elif opcion == "5":
            CrearMovimiento(1, 1, 100, 1)  # Parámetros de ejemplo
        elif opcion == "6":
            print("\n--- LISTA DE PRODUCTOS ---")
            ListarProductos()
        elif opcion == "7":
            print("\n--- LISTA DE LOTES ---")
            ListarLotes()
        elif opcion == "8":
            print("\n--- LISTA DE MOVIMIENTOS ---")
            ListarMovimientos()
        elif opcion == "9":
            print("Saliendo...")
            seguir = False
        else:
            print("Opción inválida.")


# -------------------- EJECUCIÓN PRINCIPAL --------------------
Menu()
