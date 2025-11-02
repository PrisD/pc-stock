import sqlite3
from datetime import datetime
import os
from zoneinfo import ZoneInfo

class AuditoriaDB:
    def __init__(self, db_name='stock.db'):
        # Asegurarse que la base de datos se crea en el directorio correcto
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establece la conexión con la base de datos"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.conn:
            self.conn.close()
            
    def setup_database(self):
        """Configura la base de datos con el esquema inicial"""
        with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
            self.cursor.executescript(f.read())
        self.conn.commit()
            
    def login(self, nombre):
        """Verifica si existe un usuario y retorna su ID"""
        self.cursor.execute('SELECT id_usuario FROM Usuario WHERE nombre = ?', (nombre,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
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
        """Obtiene e imprime los registros de auditoría formateados.

        Si se pasa id_usuario, registra la acción de consulta automáticamente.
        """
        filas = self.obtener_auditorias()
        # Imprimir encabezado
        print("=== REGISTROS DE AUDITORÍA ===")
        print("\nFecha/Hora | Usuario | Acción | Módulo | Detalle")
        print("-" * 80)

        for registro in filas:
            fecha, nombre, accion, modulo, detalle = registro
            print(f"{fecha} | {nombre:8} | {accion:6} | {modulo:7} | {detalle}")

        # Registrar la consulta si nos pasan un usuario
        if id_usuario is not None:
            try:
                self.registrar_auditoria(id_usuario, "CONSULTA", "AUDITORIA", "Consultó registros de auditoría")
            except Exception:
                # No queremos que la impresión falle si la auditoría no se puede registrar
                pass