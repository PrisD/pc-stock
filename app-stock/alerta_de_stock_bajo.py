from datetime import datetime
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Alerta:
    id_producto: int
    cantidad: int
    tipo_alerta: str
    descripcion: str
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
            SELECT cantidad
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


def crear_alerta(producto: dict, cantidad_actual: int,cantidad_faltante:int, tipo_alerta: str) -> Alerta:
    """Crea un objeto Alerta con la información necesaria"""
    mensaje = f"Alerta de stock {tipo_alerta}: cantidad actual {cantidad_actual}, necesitas {cantidad_faltante} para reponer tu nivel normal de stock del producto {producto['nombre']}"
    
    return Alerta(
        id_producto=producto['id'],
        cantidad=cantidad_faltante,
        tipo_alerta=tipo_alerta,
        descripcion=mensaje
    )

def mostrar_alerta(alerta: Alerta,cantidad_actual,producto):
    """Muestra la alerta en la consola"""
    print("\n=== ALERTA DE STOCK ===")
    print(f"Tipo: {alerta.tipo_alerta}")
    print(f"Producto: {producto['nombre']}")
    print(f"Cantidad actual: {cantidad_actual}")
    print(f"Cantidad que necesitas comprar: {alerta.cantidad}")
    print(f"Mensaje: {alerta.descripcion}")
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
            alerta.cantidad,
            alerta.tipo_alerta,
            alerta.descripcion
        ))
    finally:
        conn.commit()

def lanzar_alerta(producto: dict, tipo_alerta: str, cantidad_actual: int,stock_bajo,conn,cursor):
    """Proceso completo de crear, mostrar y guardar una alerta"""
    cant_faltante = stock_bajo - cantidad_actual
    alerta = crear_alerta(producto, cantidad_actual,cant_faltante, tipo_alerta)
    mostrar_alerta(alerta,cantidad_actual,producto)
    guardar_alerta(alerta,conn,cursor)

def verificar_stock(conn,cursor):
    """Verifica el stock de todos los productos y genera alertas según corresponda"""
    productos = traer_productos(conn,cursor)
    
    for producto in productos:
        cantidad_actual = buscar_lotes(producto['id'],conn,cursor)
        stock_bajo, stock_critico = buscar_limites_stock(producto['id'],conn,cursor)

        if cantidad_actual == 0:
            lanzar_alerta(producto, "AGOTADO", cantidad_actual,stock_bajo,conn,cursor)
        elif cantidad_actual < stock_critico:
            lanzar_alerta(producto, "CRITICO", cantidad_actual,stock_bajo,conn,cursor)
        elif cantidad_actual < stock_bajo:
            lanzar_alerta(producto, "BAJO", cantidad_actual,stock_bajo,conn,cursor)


       
          
        
            