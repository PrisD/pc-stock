from datetime import datetime
from .auditoria_db import AuditoriaDB

def _obtener_nombre_mes(numero_mes):
    return datetime.strptime(numero_mes, "%m").strftime("%B").capitalize()

def mostrar_consulta_auditoria(db: AuditoriaDB, id_usuario_actual: int):
    print("=== CONSULTA DE AUDITORÍAS ===")
    
    periodos = db.obtener_periodos_disponibles()

    if not periodos:
        print("No hay registros de auditoría disponibles.\n")
        return

    print("\nPeríodos disponibles:")
    for i, (anio, mes) in enumerate(periodos, start=1):
        nombre_mes = _obtener_nombre_mes(mes)
        print(f"{i}. {nombre_mes} {anio}")

    while True:
        try:
            seleccion = int(input("\nSeleccione el número del período a consultar: ").strip())
            if 1 <= seleccion <= len(periodos):
                anio, mes = periodos[seleccion - 1]
                break
            else:
                print("Número inválido. Intente nuevamente.")
        except ValueError:
            print("Entrada inválida. Ingrese un número.")

    filas = db.obtener_auditorias_por_periodo(anio, mes)
    
    nombre_mes_seleccionado = _obtener_nombre_mes(mes)
    print(f"\n=== REGISTROS DE AUDITORÍA - {nombre_mes_seleccionado} {anio} ===")
    
    if not filas:
        print("No se encontraron registros para este período.\n")
        return

    print("\nFecha/Hora | Usuario | Acción | Módulo | Detalle")
    print("-" * 100)

    for registro in filas:
        fecha, nombre, accion, modulo, detalle = registro
        print(f"{fecha} | {nombre:10} | {accion:10} | {modulo:10} | {detalle or ''}")

    try:
        detalle_log = f"Consultó registros de {mes}/{anio}"
        db.registrar_auditoria(id_usuario_actual, "CONSULTA", "AUDITORIA", detalle_log)
    except Exception:
        pass