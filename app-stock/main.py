from auditoria.auditoria_db import AuditoriaDB
from auditoria.auditoria_ui import mostrar_consulta_auditoria
from login import LoginManager
from reportes import Reporte
from chequeo_vencimiento import programar_chequear_vencimiento
from alerta_de_stock_bajo import verificar_stock
from registroDeMovimientos import *
from utils import listarStock
import sqlite3
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Registrar Movimientos")
    print("2. Consultar Stock Actual")
    print("3. Consultar Movimientos (Auditoría)")
    print("4. Consultar Alertas de Stock Bajo")
    print("5. Visualizar Reporte")
    print("6. Cerrar Sesión")
    print("Seleccione una opción: ", end="")


def modulo_en_construccion(nombre_modulo: str):
    clear_screen()
    print(f"=== {nombre_modulo} ===")
    print("Módulo en construcción. Próximamente estará disponible.")


def main():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "stock.db"))
    cursor = conn.cursor()

    auditoria = AuditoriaDB()
    login_manager = LoginManager()
    usuario_actual = None
    programar_chequear_vencimiento(periodo=60)

    while True:
        if usuario_actual is None:
            usuario, debe_salir = login_manager.mostrar_pantalla_login()
            if debe_salir:
                break

            if usuario:
                usuario_actual = usuario
                auditoria.registrar_auditoria(
                    usuario[0], "LOGIN", "MAIN", f"Usuario {usuario[1]} inició sesión")

        else:
            clear_screen()
            print(f"Usuario: {usuario_actual[1]}")
            mostrar_menu()
            opcion = input().strip()

            match opcion:
                case "1":
                    # abre el menu de registro de movimientos (hay que cambiar esto)
                    clear_screen()
                    menuRegistrarMovimiento(conn, cursor, usuario_actual,auditoria)
                    verificar_stock(conn, cursor,usuario_actual,auditoria)
                    input("\nPresione Enter para volver al menú...")
                    
                case "2":
                    clear_screen()
                    listarStock(conn, cursor)
                    input("\nPresione Enter para volver al menú...")
                # --- Fin de la modificación ---

                # 2. CASE 3 ACTUALIZADO
                case "3":
                    clear_screen()
                    mostrar_consulta_auditoria(auditoria, usuario_actual)
                    input("\nPresione Enter para volver al menú...")

                case "4":
                    clear_screen()
                    verificar_stock(conn, cursor,usuario_actual,auditoria)
                    input("\nPresione Enter para volver al menú...")

                case "5":
                    handler_de_reportes = Reporte('dw.db')
                    try:
                        with handler_de_reportes as r:
                            r.generar_reporte(usuario_actual, auditoria)
                    except ConnectionError as e:
                        print(f"No se pudo iniciar el modulo de reportes: {e}")
                    input("\nPresione Enter para volver al menú...")

                case "6":
                    auditoria.registrar_auditoria(
                        usuario_actual[0], "LOGOUT", "MAIN", f"Usuario {usuario_actual[1]} cerró sesión")
                    usuario_actual = None
                    print("\nSesión cerrada.")
                    input("Presione Enter para continuar...")

                case _:
                    print("\nOpción no válida. Por favor, intente de nuevo.")
                    input("Presione Enter para continuar...")

    try:
        auditoria.disconnect()
        login_manager.disconnect()
    finally:
        print("\n¡Gracias por usar el sistema!")


if __name__ == "__main__":
    main()
