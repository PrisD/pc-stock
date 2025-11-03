import sqlite3
from datetime import datetime
import os
from zoneinfo import ZoneInfo

class AuditoriaDB:
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
    
    def registrar_auditoria(self, id_usuario, accion, modulo, detalle=None):
        """Registra una acción en la tabla de auditoría"""
        # Obtener fecha y hora actual en Argentina
        fecha_hora = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO Auditoria (id_usuario, accion, modulo, detalle, fecha_hora)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_usuario, accion, modulo, detalle, fecha_hora))
        self.conn.commit()
        
    def obtener_auditorias(self):
        """Obtiene todas las auditorías con el nombre del usuario"""
        self.cursor.execute('''
            SELECT a.fecha_hora, u.nombre, a.accion, a.modulo, a.detalle
            FROM Auditoria a
            JOIN Usuario u ON a.id_usuario = u.id_usuario
            ORDER BY a.fecha_hora DESC
        ''')
        return self.cursor.fetchall()

    def mostrar_auditorias(self, id_usuario=None):
        """Muestra las auditorías de un mes y año seleccionados."""

        # === SELECCIÓN DE PERÍODO ===
        print("=== CONSULTA DE AUDITORÍAS ===")

        # Mostrar los meses y años disponibles en la base de datos
        self.cursor.execute("""
            SELECT DISTINCT strftime('%Y', fecha_hora) AS anio, strftime('%m', fecha_hora) AS mes
            FROM Auditoria
            ORDER BY anio DESC, mes DESC
        """)
        periodos = self.cursor.fetchall()

        if not periodos:
            print("No hay registros de auditoría disponibles.\n")
            return

        print("\nPeríodos disponibles:")
        for i, (anio, mes) in enumerate(periodos, start=1):
            nombre_mes = datetime.strptime(mes, "%m").strftime("%B").capitalize()
            print(f"{i}. {nombre_mes} {anio}")

        # Elegir un período
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

        # === CONSULTAR AUDITORÍAS DEL PERÍODO SELECCIONADO ===
        self.cursor.execute('''
            SELECT a.fecha_hora, u.nombre, a.accion, a.modulo, a.detalle
            FROM Auditoria a
            JOIN Usuario u ON a.id_usuario = u.id_usuario
            WHERE strftime('%Y', a.fecha_hora) = ? AND strftime('%m', a.fecha_hora) = ?
            ORDER BY a.fecha_hora DESC
        ''', (anio, mes))

        filas = self.cursor.fetchall()

        print(f"\n=== REGISTROS DE AUDITORÍA - {datetime.strptime(mes, '%m').strftime('%B').capitalize()} {anio} ===")
        if not filas:
            print("No se encontraron registros para este período.\n")
            return

        print("\nFecha/Hora | Usuario | Acción | Módulo | Detalle")
        print("-" * 100)

        for registro in filas:
            fecha, nombre, accion, modulo, detalle = registro
            print(f"{fecha} | {nombre:10} | {accion:10} | {modulo:10} | {detalle or ''}")

        # Registrar la consulta en la auditoría
        if id_usuario is not None:
            try:
                self.registrar_auditoria(id_usuario, "CONSULTA", "AUDITORIA", f"Consultó registros de {mes}/{anio}")
            except Exception:
                pass
