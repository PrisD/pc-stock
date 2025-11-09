from datetime import datetime
from .auditoria_db import AuditoriaDB

def _obtener_nombre_mes(numero_mes):
    return datetime.strptime(numero_mes, "%m").strftime("%B").capitalize()

def _seleccionar_periodo(db: AuditoriaDB):
    periodos = db.obtener_periodos_disponibles()
    if not periodos:
        print("No hay registros de auditoría disponibles.\n")
        return None, None

    print("\nPeríodos disponibles:")
    for i, (anio, mes) in enumerate(periodos, start=1):
        nombre_mes = _obtener_nombre_mes(mes)
        print(f"{i}. {nombre_mes} {anio}")

    while True:
        try:
            seleccion = int(input("\nSeleccione el número del período a consultar: ").strip())
            if 1 <= seleccion <= len(periodos):
                return periodos[seleccion - 1] # Devuelve (anio, mes)
            else:
                print("Número inválido. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

def _seleccionar_dia(db: AuditoriaDB, anio: str, mes: str):
    opcion = input("\n¿Desea filtrar por un día específico? (s/n): ").strip().lower()
    if opcion != 's':
        return None, "Todos"

    dias = db.obtener_dias_disponibles(anio, mes)
    if not dias:
        print("No se encontraron días con registros para este mes.")
        return None, "Todos"

    print("\nDías disponibles:")
    for i, dia in enumerate(dias, start=1):
        print(f"{i}. {dia}")

    while True:
        try:
            seleccion = int(input("Seleccione el número del día: ").strip())
            if 1 <= seleccion <= len(dias):
                dia_sel = dias[seleccion - 1]
                return dia_sel, dia_sel
            else:
                print("Número inválido. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

def _seleccionar_usuario(db: AuditoriaDB):
    opcion = input("¿Desea filtrar por un usuario específico? (s/n): ").strip().lower()
    if opcion != 's':
        return None, "Todos"

    usuarios = db.obtener_usuarios_con_registros()
    if not usuarios:
        print("No se encontraron usuarios en los registros de auditoría.")
        return None, "Todos"

    print("\nUsuarios disponibles:")
    for i, (id_usuario, nombre) in enumerate(usuarios, start=1):
        print(f"{i}. {nombre}")

    while True:
        try:
            seleccion = int(input("Seleccione el número del usuario: ").strip())
            if 1 <= seleccion <= len(usuarios):
                id_sel, nombre_sel = usuarios[seleccion - 1]
                return id_sel, nombre_sel
            else:
                print("Número inválido. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

def _seleccionar_accion(db: AuditoriaDB):
    opcion = input("¿Desea filtrar por una acción específica? (s/n): ").strip().lower()
    if opcion != 's':
        return None, "Todas"

    acciones = db.obtener_acciones_disponibles()
    print("\nAcciones disponibles:")
    for i, accion in enumerate(acciones, start=1):
        print(f"{i}. {accion}")

    while True:
        try:
            seleccion = int(input("Seleccione el número de la acción: ").strip())
            if 1 <= seleccion <= len(acciones):
                accion_sel = acciones[seleccion - 1]
                return accion_sel, accion_sel
            else:
                print("Número inválido. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

def mostrar_consulta_auditoria(db: AuditoriaDB, id_usuario_actual: int):
    print("=== CONSULTA DE AUDITORÍAS ===")
    
    # --- 1. SELECCIONAR PERÍODO (Obligatorio) ---
    anio, mes = _seleccionar_periodo(db)
    if anio is None:
        return # No hay registros para mostrar
    # --- 2. SELECCIONAR FILTROS OPCIONALES ---
    dia_filtro, nombre_dia_filtro = _seleccionar_dia(db, anio, mes)
    id_usuario_filtro, nombre_usuario_filtro = _seleccionar_usuario(db)
    accion_filtro, nombre_accion_filtro = _seleccionar_accion(db)
    
    try:
        detalle_log = f"Consultó registros de {mes}/{anio}. Filtros: Día='{nombre_dia_filtro}', Usuario='{nombre_usuario_filtro}', Acción='{nombre_accion_filtro}'"
        db.registrar_auditoria(id_usuario_actual[0], "CONSULTA", "AUDITORIA", detalle_log)
    except Exception:
        pass

    # --- 3. OBTENER DATOS FILTRADOS  ---
    filas = db.obtener_auditorias_filtradas(
        anio=anio, 
        mes=mes, 
        dia=dia_filtro,
        id_usuario=id_usuario_filtro, 
        accion=accion_filtro
    )
    
    # --- 4. MOSTRAR RESULTADOS ---
    nombre_mes_seleccionado = _obtener_nombre_mes(mes)
    print(f"\n=== REGISTROS DE AUDITORÍA ===")
    print(f"Período: {nombre_mes_seleccionado} {anio}")
    print(f"Día:     {nombre_dia_filtro}") # <-- Línea nueva
    print(f"Usuario: {nombre_usuario_filtro}")
    print(f"Acción:  {nombre_accion_filtro}")
    print("=" * 30)
    
    if not filas:
        print("\nNo se encontraron registros para los filtros seleccionados.\n")
        return

    print("\nFecha/Hora | Usuario | Acción | Módulo | Detalle")
    print("-" * 100)

    for registro in filas:
        fecha, nombre, accion, modulo, detalle = registro
        print(f"{fecha} | {nombre:10} | {accion:10} | {modulo:10} | {detalle or ''}")
    
