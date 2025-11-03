from auditoria_db import AuditoriaDB
from login import LoginManager
from actualizacion_stock import iniciar_actualizacion_stock, actualizar_stock
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
    iniciar_actualizacion_stock(conn, cursor)

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
                    modulo_en_construccion("Registrar Movimientos")
                    input(
                        "\nPresione Enter para ver Stock Actual (módulo en construcción)...")
                    auditoria.registrar_auditoria(
                        usuario_actual[0], "USO", "REGISTRAR_MOVIMIENTOS", "Ingresó al módulo Registrar Movimientos (en construcción)")
                    input("\nPresione Enter para volver al menú...")

                case "2":
                    actualizar_stock(conn, cursor)
                    auditoria.registrar_auditoria(
                        usuario_actual[0], "CONSULTA", "STOCK", "Consultó stock actual (en construcción)")
                    input("\nPresione Enter para volver al menú...")

                case "3":
                    clear_screen()
                    auditoria.mostrar_auditorias(usuario_actual[0])
                    input("\nPresione Enter para volver al menú...")

                case "4":
                    modulo_en_construccion("Consultar Alertas de Stock Bajo")
                    auditoria.registrar_auditoria(
                        usuario_actual[0], "CONSULTA", "ALERTAS", "Consultó alertas de stock bajo (en construcción)")
                    input("\nPresione Enter para volver al menú...")

                case "5":
                    modulo_en_construccion("Visualizar Reporte")
                    auditoria.registrar_auditoria(
                        usuario_actual[0], "CONSULTA", "REPORTE", "Visualizó reporte (en construcción)")
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
