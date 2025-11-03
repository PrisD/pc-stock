from datetime import datetime
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Alerta:
    id_producto: int
    nombre_producto: str
    cantidad_actual: int
    tipo_alerta: str
    mensaje: str
    fecha: str = None

    def __post_init__(self):
        if self.fecha is None:
            self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def traer_productos(conn,cursor):
    """Obtiene todos los productos de la base de datos"""
    try:
        cursor.execute("SELECT id_producto, descripcion FROM productos")
        return [{'id': row[0], 'nombre': row[1]} for row in cursor.fetchall()]
    finally:
        conn.commit()

def buscar_lotes(id_producto: int,conn,cursor) -> int:
    """Obtiene la suma de cantidades en lotes activos para un producto"""
    try:
        cursor.execute("""
            SELECT COALESCE(SUM(cantidad), 0)
            FROM lotes
            WHERE id_producto = ? AND estado = 'activo'
        """, (id_producto,))
        return cursor.fetchone()[0]
    finally:
        conn.commit()

def buscar_limites_stock(id_producto: int,conn,cursor) -> Tuple[int, int]:
    """Obtiene los límites de stock bajo y crítico para un producto"""
    try:
        cursor.execute("""
            SELECT stock_bajo, stock_critico
            FROM productos
            WHERE id_producto = ?
        """, (id_producto,))
        resultado = cursor.fetchone()
        return resultado if resultado else (0, 0)
    finally:
        conn.commit()

def obtener_nombre_producto(id_producto: int,conn,cursor) -> str:
    """Obtiene el nombre/descripción de un producto por su ID"""
    try:
        cursor.execute("SELECT descripcion FROM productos WHERE id_producto = ?", (id_producto,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else "Producto Desconocido"
    finally:
        conn.commit()

def crear_alerta(id_producto: int, cantidad_actual: int, tipo_alerta: str,conn,cursor) -> Alerta:
    """Crea un objeto Alerta con la información necesaria"""
    nombre_producto = obtener_nombre_producto(id_producto,conn,cursor)
    mensaje = f"Alerta de stock {tipo_alerta}: cantidad actual {cantidad_actual}"
    
    return Alerta(
        id_producto=id_producto,
        nombre_producto=nombre_producto,
        cantidad_actual=cantidad_actual,
        tipo_alerta=tipo_alerta,
        mensaje=mensaje
    )

def mostrar_alerta(alerta: Alerta):
    """Muestra la alerta en la consola"""
    print("\n=== ALERTA DE STOCK ===")
    print(f"Tipo: {alerta.tipo_alerta}")
    print(f"Producto: {alerta.nombre_producto}")
    print(f"Cantidad actual: {alerta.cantidad_actual}")
    print(f"Mensaje: {alerta.mensaje}")
    print("=" * 25)

def guardar_alerta(alerta: Alerta,conn,cursor):
    """Guarda la alerta en la base de datos"""
    try:
        cursor.execute("""
            INSERT INTO alertas (id_producto, fecha, cantidad, tipo_alerta, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, (
            alerta.id_producto,
            alerta.fecha,
            alerta.cantidad_actual,
            alerta.tipo_alerta,
            alerta.mensaje
        ))
    finally:
        conn.commit()

def lanzar_alerta(producto: dict, tipo_alerta: str, cantidad_actual: int,conn,cursor):
    """Proceso completo de crear, mostrar y guardar una alerta"""
    alerta = crear_alerta(producto['id'], cantidad_actual, tipo_alerta,conn,cursor)
    mostrar_alerta(alerta)
    guardar_alerta(alerta,conn,cursor)

def verificar_stock(conn,cursor):
    """Verifica el stock de todos los productos y genera alertas según corresponda"""
    productos = traer_productos(conn,cursor)
    
    for producto in productos:
        cantidad_actual = buscar_lotes(producto['id'],conn,cursor)
        stock_bajo, stock_critico = buscar_limites_stock(producto['id'],conn,cursor)

        if cantidad_actual == 0:
            lanzar_alerta(producto, "AGOTADO", cantidad_actual,conn,cursor)
        elif cantidad_actual < stock_critico:
            lanzar_alerta(producto, "CRITICO", cantidad_actual,conn,cursor)
        elif cantidad_actual < stock_bajo:
            lanzar_alerta(producto, "BAJO", cantidad_actual,conn,cursor)


       
          
        
            