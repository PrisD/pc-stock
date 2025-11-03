import sqlite3
import random
from datetime import datetime, timedelta
import os

# --- Configuración ---
DB_NAME = 'dw.db'
NUM_MOVIMIENTOS = 500 # Cantidad de movimientos aleatorios a generar
# ---------------------

def poblar_base_de_datos():
    """
    Puebla la base de datos dw.db con datos de prueba.
    Usa 'INSERT OR IGNORE' para evitar fallos si los datos ya existen.
    """
    
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    
    if not os.path.exists(db_path):
        print(f"Error: La base de datos '{db_path}' no existe.")
        print("Por favor, ejecuta primero tu script 'crear_db.py'.")
        return

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # --- 1. Poblar dim_productos ---
        print("Poblando dim_productos...")
        productos = [
            (1, 'Arroz 1kg', 'Arroz blanco tipo 000', 20),
            (2, 'Fideos 500g', 'Fideos tirabuzón', 30),
            (3, 'Aceite Girasol 1.5L', 'Aceite de girasol', 10),
            (4, 'Lentejas 400g', 'Lentejas en lata', 15)
        ]
        # 'INSERT OR IGNORE' evita errores de Clave Primaria duplicada
        cursor.executemany(
            "INSERT OR IGNORE INTO dim_productos VALUES (?, ?, ?, ?)", 
            productos
        )

        # --- 2. Poblar dim_tiempo ---
        print("Poblando dim_tiempo...")
        
        fecha_inicio = datetime(2024, 1, 1)
        fecha_fin = datetime(2025, 12, 31)
        dias_totales = (fecha_fin - fecha_inicio).days + 1
        
        registros_tiempo = []
        ids_fechas_generados = []
        
        nombres_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        nombres_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        for i in range(dias_totales):
            fecha_actual = fecha_inicio + timedelta(days=i)
            id_fecha_int = int(fecha_actual.strftime('%Y%m%d'))
            trimestre = (fecha_actual.month - 1) // 3 + 1
            
            fila = (
                id_fecha_int,
                fecha_actual,
                fecha_actual.day,
                fecha_actual.month,
                fecha_actual.year,
                trimestre,
                nombres_dias[fecha_actual.weekday()],
                nombres_meses[fecha_actual.month - 1]
            )
            registros_tiempo.append(fila)
            ids_fechas_generados.append(id_fecha_int)

        cursor.executemany(
            "INSERT OR IGNORE INTO dim_tiempo VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            registros_tiempo
        )
        print(f"Se insertaron/ignoraron {len(registros_tiempo)} registros en dim_tiempo.")

        # --- 3. Poblar fact_movimientos ---
        print("Poblando fact_movimientos...")
        ids_productos = [p[0] for p in productos]
        ids_fechas = ids_fechas_generados
        
        movimientos = set()
        while len(movimientos) < NUM_MOVIMIENTOS:
            id_prod = random.choice(ids_productos)
            id_fec = random.choice(ids_fechas)
            ingresos = random.randint(0, 100)
            egresos = random.randint(0, 50) if ingresos < 20 else 0
            vencidos = random.randint(0, 5)
            # Asegúrate de que los nombres de columnas coincidan con tu schemadw.sql
            # (id_producto, id_fecha, cantidad_ingresos, cantidad_egresos, cantidad_vencidos)
            movimientos.add((id_prod, id_fec, ingresos, egresos, vencidos))

        cursor.executemany(
            "INSERT OR IGNORE INTO fact_movimientos VALUES (?, ?, ?, ?, ?)",
            list(movimientos)
        )
        print(f"Se insertaron/ignoraron {len(movimientos)} movimientos.")

        conn.commit()
        print(f"\nBase de datos '{DB_NAME}' poblada exitosamente.")
        
    except sqlite3.Error as e:
        print(f"Error al poblar la base de datos: {e}")
        print("Posible causa: Los nombres de las tablas o columnas en este script")
        print("no coinciden con tu archivo 'schemadw.sql'.")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

if __name__ == '__main__':
    poblar_base_de_datos()