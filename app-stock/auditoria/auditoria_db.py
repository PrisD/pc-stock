import sqlite3
from datetime import datetime
import os
from zoneinfo import ZoneInfo

class AuditoriaDB:
    def __init__(self, db_name='stock.db'):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.db_path = os.path.join(base_dir, db_name)
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        # Añadimos un try...except para que no falle silenciosamente
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"ERROR CRÍTICO: No se pudo conectar a la base de datos en {self.db_path}")
            print(f"Error: {e}")
            # Aseguramos que permanezcan como None si falla
            self.conn = None
            self.cursor = None
            
    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def _get_current_timestamp(self):
        return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%d %H:%M:%S")
    
    def registrar_auditoria(self, id_usuario, accion, modulo, detalle=None):
        fecha_hora = self._get_current_timestamp()
        try:
            self.cursor.execute('''
                INSERT INTO Auditoria (id_usuario, accion, modulo, detalle, fecha_hora)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_usuario, accion, modulo, detalle, fecha_hora))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar auditoría: {e}")
            self.conn.rollback()
            
    def obtener_auditorias_todas(self):
        self.cursor.execute('''
            SELECT a.fecha_hora, u.nombre, a.accion, a.modulo, a.detalle
            FROM Auditoria a
            JOIN Usuario u ON a.id_usuario = u.id_usuario
            ORDER BY a.fecha_hora DESC
        ''')
        return self.cursor.fetchall()

    def obtener_periodos_disponibles(self):
        self.cursor.execute("""
            SELECT DISTINCT strftime('%Y', fecha_hora) AS anio, strftime('%m', fecha_hora) AS mes
            FROM Auditoria
            ORDER BY anio DESC, mes DESC
        """)
        return self.cursor.fetchall()

    def obtener_auditorias_por_periodo(self, anio, mes):
        self.cursor.execute('''
            SELECT a.fecha_hora, u.nombre, a.accion, a.modulo, a.detalle
            FROM Auditoria a
            JOIN Usuario u ON a.id_usuario = u.id_usuario
            WHERE strftime('%Y', a.fecha_hora) = ? AND strftime('%m', a.fecha_hora) = ?
            ORDER BY a.fecha_hora DESC
        ''', (anio, mes))
        return self.cursor.fetchall()