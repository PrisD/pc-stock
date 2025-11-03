import sqlite3
import os
import utils
import pandas as pd
from datetime import datetime, timedelta

class Reporte:
    def __init__(self, db_name='dw.db'):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = None
        self.cursor = None

    def iniciar_conexion_dw(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            raise

    def cerrar_conexion_dw(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print("--- Conexion con DW cerrada ---") # para depuracion por el momento

    def __enter__(self):
        self.iniciar_conexion_dw()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.cerrar_conexion_dw()
        if exc_type:
            print(f"Error durante ejecucion del reporte: {exc_value}")

    # Valida que un producto exista en DW. Asume que la conexion ya esta abierta. Devuelve TRUE/FALSE
    def validar_producto_dw(self, id_producto):
        if not self.cursor:
            raise ConnectionError("La conexion no esta iniciada.")
        
        try:
            query = "SELECT 1 FROM dim_productos WHERE id_producto = ? LIMIT 1" # La idea de la query es que si encuentra una coincidencia devuelva un 1 para simplificar respuesta
            self.cursor.execute(query, (id_producto))
            return self.cursor.fetchone() is not None # Si la respuesta no es vacia (None) entonces es que se encontro una coincidencia
        except sqlite3.Error as e:
            print(f"Error al validar el producto: {e}")
            return False


    # TODOS LOS REPORTES EJECUTARAN LA CONSULTA Y DEVUELVEN UN DATAFRAME DE PANDAS COMO RESPUESTA
      
    def reporte_ingresos_egresos_producto(self, fecha_inicio, fecha_fin, producto):
        if not self.cursor:
            raise ConnectionError("La conexion no esta iniciada.")
        
        query = """
            SELECT
                p.nombre_producto,
                t.fecha_completa,
                m.cantidad_ingresos,
                m.cantidad_egresos
            FROM fact_movimientos m
            JOIN dim_productos p ON m.id_producto = p.id_producto
            JOIN dim_tiempo t ON m.id_fecha = t.id_fecha
            WHERE
                p.id_producto = ?
                AND t.fecha_completa BETWEEN ? AND ?
            ORDER BY t.fecha_completa;
        """
        params = (producto, fecha_inicio, fecha_fin)

        try:
            df_reporte = pd.read_sql_query(query, self.conn, params=params)
            df_reporte['neto'] = df_reporte['cantidad_ingresos'] - df_reporte['cantidad_egresos']
            return df_reporte
        except Exception as e:
            print(f"Error al generar reporte con pandas: {e}")
            return pd.DataFrame() # devuelvo un dataframe vacio en caso de error



    def reporte_vencimientos(self, fecha_inicio, fecha_fin):
        if not self.cursor:
            raise ConnectionError("La conexion no esta iniciada.")
        
        query = """
            SELECT
                p.nombre_producto,
                SUM(m.cantidad_vencidos) AS total_vencidos
            FROM fact_movimientos m
            JOIN dim_productos p ON m.id_producto = p.id_producto
            JOIN dim_tiempo t ON m.id_fecha = t.id_fecha
            WHERE
                t.fecha_completa BETWEEN ? AND ?
                AND m.cantidad_vencidos > 0
            GROUP BY p.nombre_producto
            ORDER BY total_vencidos DESC;
        """
        params = (fecha_inicio, fecha_fin)

        try:
            df_reporte = pd.read_sql_query(query, self.conn, params=params)
            return df_reporte
        except Exception as e:
            print(f"Error al generar reporte con pandas: {e}")
            return pd.DataFrame() # devuelvo un dataframe vacio en caso de error



    def reporte_evolucion_stock(self, tipo_periodo, fecha_fin, producto):
        if not self.cursor:
            raise ConnectionError("La conexion no esta iniciada.")
        
        fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d')

        match tipo_periodo:
            case "1": 
                dias_restar = 7 # semana
            case "2": 
                dias_restar = 30 # mes
            case "3": 
                dias_restar = 90 # trimestre
            case "4": 
                dias_restar = 365 # anio
        
        fecha_inicio_obj = fecha_fin_obj - timedelta(days=dias_restar)

        fecha_inicio_sql = fecha_inicio_obj.strftime('%Y-%m-%d 00:00:00')
        fecha_fin_sql = fecha_fin_obj.strftime('%Y-%m-%d 23:59:59')

        query = """
            SELECT
                t.fecha_completa,
                p.nombre_producto,
                f.stock_final_del_dia
            FROM fact_stock_diario f
            JOIN dim_productos p ON f.id_producto = p.id_producto
            JOIN dim_tiempo t ON f.id_fecha = t.id_fecha
            WHERE
                p.id_producto = ?
                AND t.fecha_completa BETWEEN ? AND ?
            ORDER BY
                t.fecha_completa ASC;
        """
        params = (producto, fecha_inicio_sql, fecha_fin_sql)
        try:
            df_reporte = pd.read_sql_query(query, self.conn, params=params)
            return df_reporte
        except Exception as e:
            print(f"Error al generar reporte con pandas: {e}")
            return pd.DataFrame()

        

    def exportar_reporte(self, df, formato , nombre_archivo="reporte"):
        if df.empty:
            print("no hay datos para expotar")
            return
        
        try:
            match formato.lower():
                case "csv":
                    nombre = f"{nombre_archivo}.csv"
                    df.to_csv(nombre, index=False)
                    print(f"reporte {nombre} exportado exitosamente")
                
                case _:
                    print(f"Formato {formato} no soportado")
        except Exception as e:
            print(f"Error al exportar: {e}")


    def generar_reporte(self):
        print("Selecciones el tipo de reporte que desea:")
        print("1. Reporte de ingresos y egresos por fecha dividido por producto.")
        print("2. Reporte de vencimientos por fecha.")
        print("3. Reporte de evolucion de stock de un producto por periodo.")

        eleccion = input("Ingrese el numero del tipo de reporte que desea: ")

        match eleccion:
            case "1":
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ") # FALTA REPETIR MIENTRAS FALLE
                utils.validar_fecha(fecha_inicio)
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ") # FALTA REPETIR MIENTRAS FALLE
                utils.validar_fecha(fecha_fin)
                utils.validar_rango_fechas(fecha_inicio, fecha_fin)
                producto = input("ingrese el producto: ") # FALTA REPETIR MIENTRAS FALLE
                
                if not self.validar_producto_dw(producto):
                    print(f"Error al validar {producto} en el data warehouse.")
                    return # detengo la generacion del reporte
            
            case "2":
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                utils.validar_fecha(fecha_inicio)
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                utils.validar_fecha(fecha_fin)
                utils.validar_rango_fechas(fecha_inicio, fecha_fin)

            case "3":
                print("Determine el periodo que desea visualizar")
                print("1. Semana")
                print("2. Mes")
                print("3. Trimestre")
                print("4. Año")
                periodo = input("ingrese periodo: ") # FALTA REPETIR MIENTRAS FALLE
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                utils.validar_fecha(fecha_fin) # FALTA REPETIR MIENTRAS FALLE
                producto = input("ingrese el producto: ") # FALTA REPETIR MIENTRAS FALLE

                if not self.validar_producto_dw(producto):
                    print(f"Error al validar {producto} en el data warehouse.")
                    return 
            
            case _:
                print("Opcion no valida")
                return

        df_reporte = pd.DataFrame() # preparo un dataframe vacio

        match eleccion:
            case "1":
                fecha_inicio_sql = f"{fecha_inicio} 00:00:00"
                fecha_fin_sql = f"{fecha_fin} 23:59:59"
                df_reporte = self.reporte_ingresos_egresos_producto(fecha_inicio_sql, fecha_fin_sql, producto)
            
            case "2":
                fecha_inicio_sql = f"{fecha_inicio} 00:00:00"
                fecha_fin_sql = f"{fecha_fin} 23:59:59"
                df_reporte = self.reporte_vencimientos(fecha_inicio_sql, fecha_fin_sql)
            
            case "3":
                df_reporte = self.reporte_evolucion_stock(periodo, fecha_fin, producto)

        if not df_reporte.empty:
            print("\n --- Vista previa de las primeras 5 filas ---")
            print(df_reporte.head())
            print("-----------------------------------------------")

            formato = input("En que formato desea exportar? solo csv por ahora: ")
            nombre_archivo = input("ingrese el nombre para el archivo (sin extension): ")

            self.exportar_reporte(df_reporte, formato, nombre_archivo)
        else:
            print("no se generaron los datos para el reporte")



