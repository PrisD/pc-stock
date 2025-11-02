import sqlite3
import os

class LoginManager:
    def __init__(self, db_name='stock.db'):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establece la conexión con la base de datos"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def _verificar_usuario(self, nombre):
        """Verifica si existe un usuario y retorna su ID y nombre"""
        self.cursor.execute('SELECT id_usuario FROM Usuario WHERE nombre = ?', (nombre,))
        result = self.cursor.fetchone()
        if result:
            return result[0], nombre
        return None

    def mostrar_pantalla_login(self):
        """Maneja la pantalla de login y retorna el usuario si el login es exitoso"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== LOGIN ===")
        nombre = input("Ingrese su nombre de usuario (o 'salir' para terminar): ")

        if nombre.lower() == 'salir':
            return None, True  # (usuario, salir)

        usuario = self._verificar_usuario(nombre)
        if usuario:
            print(f"\nBienvenido, {nombre}!")
            input("Presione Enter para continuar...")
            return usuario, False  # (usuario, salir)
        else:
            print("\nUsuario no encontrado. Por favor, intente de nuevo.")
            input("Presione Enter para continuar...")
            return None, False  # (usuario, salir)