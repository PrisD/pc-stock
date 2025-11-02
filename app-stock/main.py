from auditoria_db import AuditoriaDB
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
    db = AuditoriaDB()
    db.connect()
    db.setup_database()

    usuario_actual = None

    while True:
        if usuario_actual is None:
            clear_screen()
            print("=== LOGIN ===")
            nombre = input("Ingrese su nombre de usuario (o 'salir' para terminar): ")

            if nombre.lower() == 'salir':
                break
            usuario_id = db.login(nombre)
            if usuario_id:
                usuario_actual = (usuario_id, nombre)
                db.registrar_auditoria(usuario_id, "LOGIN", "MAIN", f"Usuario {nombre} inició sesión")
                print(f"\nBienvenido, {nombre}!")
                input("Presione Enter para continuar...")
            else:
                print("\nUsuario no encontrado. Por favor, intente de nuevo.")
                input("Presione Enter para continuar...")
                continue

        else:
            clear_screen()
            print(f"Usuario: {usuario_actual[1]}")
            mostrar_menu()
            opcion = input().strip()

            match opcion:
                case "1":
                    modulo_en_construccion("Registrar Movimientos")
                    input("\nPresione Enter para ver Stock Actual (módulo en construcción)...")
                    db.registrar_auditoria(usuario_actual[0], "USO", "REGISTRAR_MOVIMIENTOS", "Ingresó al módulo Registrar Movimientos (en construcción)")
                    input("\nPresione Enter para volver al menú...")

                case "2":
                    modulo_en_construccion("Consultar Stock Actual")
                    db.registrar_auditoria(usuario_actual[0], "CONSULTA", "STOCK", "Consultó stock actual (en construcción)")
                    input("\nPresione Enter para volver al menú...")

                case "3":
                    clear_screen()
                    db.mostrar_auditorias(usuario_actual[0])
                    input("\nPresione Enter para volver al menú...")

                case "4":
                    modulo_en_construccion("Consultar Alertas de Stock Bajo")
                    db.registrar_auditoria(usuario_actual[0], "CONSULTA", "ALERTAS", "Consultó alertas de stock bajo (en construcción)")
                    input("\nPresione Enter para volver al menú...")

                case "5":
                    modulo_en_construccion("Visualizar Reporte")
                    db.registrar_auditoria(usuario_actual[0], "CONSULTA", "REPORTE", "Visualizó reporte (en construcción)")
                    input("\nPresione Enter para volver al menú...")

                case "6":
                    db.registrar_auditoria(usuario_actual[0], "LOGOUT", "MAIN", f"Usuario {usuario_actual[1]} cerró sesión")
                    usuario_actual = None
                    print("\nSesión cerrada.")
                    input("Presione Enter para continuar...")

                case _:
                    print("\nOpción no válida. Por favor, intente de nuevo.")
                    input("Presione Enter para continuar...")

    db.disconnect()
    print("\n¡Gracias por usar el sistema!")


if __name__ == "__main__":
    main()