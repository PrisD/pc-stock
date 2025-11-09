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
                INSERT INTO auditorias (id_usuario, accion, modulo, detalle, fecha_hora)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_usuario, accion, modulo, detalle, fecha_hora))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar auditoría: {e}")
            self.conn.rollback()

    def obtener_periodos_disponibles(self):
        self.cursor.execute("""
            SELECT DISTINCT strftime('%Y', fecha_hora) AS anio, strftime('%m', fecha_hora) AS mes
            FROM auditorias
            ORDER BY anio DESC, mes DESC
        """)
        return self.cursor.fetchall()

    def obtener_auditorias_filtradas(self, anio, mes, dia=None, id_usuario=None, accion=None):
        """
        Obtiene auditorías filtrando por período (obligatorio)
        y opcionalmente por día, usuario y/o acción.
        """
        
        query_base = '''
            SELECT a.fecha_hora, u.nombre, a.accion, a.modulo, a.detalle
            FROM auditorias a
            JOIN usuarios u ON a.id_usuario = u.id_usuario
        '''
        
        # Filtros base obligatorios
        filtros = [
            "strftime('%Y', a.fecha_hora) = ?",
            "strftime('%m', a.fecha_hora) = ?"
        ]
        parametros = [anio, mes]

        # --- INICIO DE MODIFICACIÓN ---
        # Añadir filtro de día opcional
        if dia is not None:
            filtros.append("strftime('%d', a.fecha_hora) = ?")
            parametros.append(dia)
        # --- FIN DE MODIFICACIÓN ---

        if id_usuario is not None:
            filtros.append("a.id_usuario = ?")
            parametros.append(id_usuario)
            
        if accion is not None:
            filtros.append("a.accion = ?")
            parametros.append(accion)
            
        query_completa = query_base + " WHERE " + " AND ".join(filtros) + " ORDER BY a.fecha_hora ASC"

        self.cursor.execute(query_completa, parametros)
        return self.cursor.fetchall()
    
    def obtener_usuarios_con_registros(self):
        """Devuelve usuarios que existen en la tabla de auditoría."""
        self.cursor.execute("""
            SELECT DISTINCT u.id_usuario, u.nombre
            FROM auditorias a
            JOIN usuarios u ON a.id_usuario = u.id_usuario
            ORDER BY u.nombre
        """)
        return self.cursor.fetchall()

    def obtener_acciones_disponibles(self):
        """Devuelve todas las acciones únicas registradas."""
        self.cursor.execute("""
            SELECT DISTINCT accion
            FROM auditorias
            ORDER BY accion
        """)
        # .fetchall() devuelve tuplas, ej: [('LOGIN',), ('CONSULTA',)]
        # Lo convertimos a una lista simple: ['LOGIN', 'CONSULTA']
        return [row[0] for row in self.cursor.fetchall()]

    def obtener_dias_disponibles(self, anio, mes):
        """Devuelve los días con registros para un mes y año específicos."""
        self.cursor.execute("""
            SELECT DISTINCT strftime('%d', fecha_hora)
            FROM auditorias
            WHERE strftime('%Y', fecha_hora) = ? AND strftime('%m', fecha_hora) = ?
            ORDER BY 1
        """, (anio, mes))
        # Convertimos [('01',), ('05',)] en ['01', '05']
        return [row[0] for row in self.cursor.fetchall()]
    