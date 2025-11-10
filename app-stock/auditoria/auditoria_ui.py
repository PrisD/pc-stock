from datetime import datetime
import textwrap
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

def mostrar_consulta_auditoria(db: AuditoriaDB, usuario_actual: tuple):
    print("=== CONSULTA DE AUDITORÍAS ===")
    
    anio, mes = _seleccionar_periodo(db)
    if anio is None:
        return 
    
    dia_filtro, nombre_dia_filtro = _seleccionar_dia(db, anio, mes)
    id_usuario_filtro, nombre_usuario_filtro = _seleccionar_usuario(db)
    accion_filtro, nombre_accion_filtro = _seleccionar_accion(db)
    
    try:
        detalle_log = f"Consultó registros de {mes}/{anio}. Filtros: Día='{nombre_dia_filtro}', Usuario='{nombre_usuario_filtro}', Acción='{nombre_accion_filtro}'"
        db.registrar_auditoria(usuario_actual[0], "CONSULTA", "AUDITORIA", detalle_log)
    except Exception as e:
        print(f"Advertencia: No se pudo registrar la auditoría de la consulta: {e}")
        pass

    filas = db.obtener_auditorias_filtradas(
        anio=anio, 
        mes=mes, 
        dia=dia_filtro,
        id_usuario=id_usuario_filtro, 
        accion=accion_filtro
    )
    
    nombre_mes_seleccionado = _obtener_nombre_mes(mes)
    print(f"\n=== REGISTROS DE AUDITORÍA ===")
    print(f"Período: {nombre_mes_seleccionado} {anio}")
    print(f"Día:     {nombre_dia_filtro}")  
    print(f"Usuario: {nombre_usuario_filtro}")
    print(f"Acción:  {nombre_accion_filtro}") 
    print("=" * 30)
    
    if not filas:
        print("\nNo se encontraron registros para los filtros seleccionados.\n")
        return


    ANCHO_FECHA = 19   
    ANCHO_USUARIO = 8 
    ANCHO_ACCION = 25  
    ANCHO_MODULO = 20  
    ANCHO_DETALLE = 100

    header = (
        f"{'Fecha/Hora'.ljust(ANCHO_FECHA)} | "
        f"{'Usuario'.ljust(ANCHO_USUARIO)} | "
        f"{'Acción'.ljust(ANCHO_ACCION)} | "
        f"{'Módulo'.ljust(ANCHO_MODULO)} | "
        f"{'Detalle'.ljust(ANCHO_DETALLE)}"
    )
    
    print(f"\n{header}")
    
    total_width = ANCHO_FECHA + ANCHO_USUARIO + ANCHO_ACCION + ANCHO_MODULO + ANCHO_DETALLE + (4 * 3)
    print("-" * total_width)
    padding_ancho = ANCHO_FECHA + 3 + ANCHO_USUARIO + 3 + ANCHO_ACCION + 3 + ANCHO_MODULO + 3
    detalle_padding = " " * padding_ancho

    for registro in filas:
        fecha, nombre, accion, modulo, detalle = registro
        
        detalle_str = detalle or ""
        
        fecha_str = (fecha or '')[:ANCHO_FECHA].ljust(ANCHO_FECHA)
        nombre_str = (nombre or '')[:ANCHO_USUARIO].ljust(ANCHO_USUARIO)
        accion_str = (accion or '')[:ANCHO_ACCION].ljust(ANCHO_ACCION)
        modulo_str = (modulo or '')[:ANCHO_MODULO].ljust(ANCHO_MODULO)
        lineas_detalle = textwrap.wrap(detalle_str, width=ANCHO_DETALLE)
        
        if not lineas_detalle:
            lineas_detalle = [""]
        
        print(f"{fecha_str} | {nombre_str} | {accion_str} | {modulo_str} | {lineas_detalle[0].ljust(ANCHO_DETALLE)}")
        
        for linea in lineas_detalle[1:]:
            print(f"{detalle_padding}{linea.ljust(ANCHO_DETALLE)}")
    
