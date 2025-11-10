import sqlite3
import os
import utils
import pandas as pd
import matplotlib.pyplot as plt
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
      
    def reporte_egresos_producto(self, fecha_inicio, fecha_fin, producto, id_usuario, auditoria):
        if not self.cursor:
            raise ConnectionError("La conexion no esta iniciada.")
        
        query = """
            SELECT
                p.nombre_producto,
                t.fecha_completa,
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
            df_reporte['fecha_completa'] = pd.to_datetime(df_reporte['fecha_completa'])
            auditoria.registrar_auditoria(id_usuario[0], "GENERAR_REPORTE", "REPORTES", f"Usuario {id_usuario[1]} generó reporte de egresos para el producto ID: {producto} desde {fecha_inicio} hasta {fecha_fin}")
            return df_reporte
        except Exception as e:
            print(f"Error al generar reporte con pandas: {e}")
            return pd.DataFrame() # devuelvo un dataframe vacio en caso de error



    def graficar_reporte_egresos(self, df_reporte):
        if df_reporte.empty:
            print("No hay datos para graficar.")
            return
        
        try:
            nombre_producto = df_reporte['nombre_producto'].iloc[0]
            print("Generando dashboard de gráficos...")

            df_reporte = df_reporte.set_index('fecha_completa')

            df_diario = df_reporte['cantidad_egresos'].resample('D').sum()
            df_semanal = df_reporte['cantidad_egresos'].resample('W').sum()
            df_mensual = df_reporte['cantidad_egresos'].resample('M').sum()
            df_trimestral = df_reporte['cantidad_egresos'].resample('Q').sum()
            df_anual = df_reporte['cantidad_egresos'].resample('Y').sum()
            
            fig, axs = plt.subplots(3, 2, figsize=(18, 15)) 
            fig.suptitle(f'Dashboard de Egresos (Ventas) de: {nombre_producto}', fontsize=20)

            ax = axs[0, 0]
            if df_diario.shape[0] > 1:
                ax.plot(df_diario.index, df_diario.values, marker='.', linestyle='-', markersize=2)
                ax.set_title('Evolución Diaria')
                ax.set_ylabel('Cantidad Vendida')
                ax.grid(True)
            else:
                ax.axis('off')

            ax = axs[0, 1]
            if df_semanal.shape[0] > 1:
                ax.plot(df_semanal.index, df_semanal.values, marker='o', linestyle='-', markersize=4, color='teal')
                ax.set_title('Total Semanal')
                ax.grid(True)
            else:
                ax.axis('off')

            ax = axs[1, 0]
            if df_mensual.shape[0] > 1:
                ax.plot(df_mensual.index, df_mensual.values, marker='o', linestyle='-', markersize=5, color='cornflowerblue')
                ax.set_title('Total Mensual')
                ax.set_ylabel('Cantidad Vendida')
                ax.grid(True)
            else:
                ax.axis('off')

            ax = axs[1, 1]
            if df_trimestral.shape[0] > 1:
                ax.plot(df_trimestral.index, df_trimestral.values, marker='o', linestyle='-', markersize=5, color='mediumseagreen')
                ax.set_title('Total Trimestral')
                ax.grid(True)
            else:
                ax.axis('off')

            ax = axs[2, 0]
            if df_anual.shape[0] > 1:
                etiquetas_anuales = df_anual.index.strftime('%Y')
                ax.bar(
                    etiquetas_anuales, 
                    df_anual.values, 
                    color='salmon', 
                    width=0.8
                )
                ax.set_title('Total Anual')
                ax.set_ylabel('Cantidad Vendida')
                ax.grid(True)
            else:
                ax.axis('off')

            axs[2, 1].axis('off')

            plt.subplots_adjust(hspace=0.04, wspace=0.1)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=3.0, w_pad=2.0)
            plt.show()

        except Exception as e:
            print(f"Error al generar el gráfico: {e}")




    def reporte_vencimientos(self, fecha_inicio, fecha_fin, id_usuario, auditoria):
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
            auditoria.registrar_auditoria(id_usuario[0], "GENERAR_REPORTE", "REPORTES", f"Usuario {id_usuario[1]} generó reporte de vencimientos desde {fecha_inicio} hasta {fecha_fin}")
            return df_reporte
        except Exception as e:
            print(f"Error al generar reporte con pandas: {e}")
            return pd.DataFrame() # devuelvo un dataframe vacio en caso de error



    def reporte_evolucion_stock(self, tipo_periodo, fecha_fin, producto, id_usuario, auditoria):
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
            auditoria.registrar_auditoria(id_usuario[0], "GENERAR_REPORTE", "REPORTES", f"Usuario {id_usuario[1]} generó reporte de evolución de stock para el producto ID: {producto} desde {fecha_inicio_sql} hasta {fecha_fin_sql}")
            return df_reporte
        except Exception as e:
            print(f"Error al generar reporte con pandas: {e}")
            return pd.DataFrame()



    def generar_reporte(self, id_usuario, auditoria):
        auditoria.registrar_auditoria(id_usuario[0], "INGRESO","REPORTES",f"Usuario {id_usuario[1]} ingresó al módulo")
        print("Selecciones el tipo de reporte que desea:")
        print("1. Reporte de egresos por fecha dividido por producto.")

        eleccion = input("Ingrese el numero del tipo de reporte que desea: ")

        match eleccion:
            case "1":
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ") # INGRESO DE LA FECHA DE INICIO
                while not utils.validar_fecha_dw(fecha_inicio):
                    print("Formato de fecha incorrecto. Reintentar")
                    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")

                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ") # INGRESO DE LA FECHA DE FIN
                while not utils.validar_fecha_dw(fecha_fin):
                    print("Formato de fecha invalido. Reintentar")
                    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

                if not utils.validar_rango_fechas_dw(fecha_inicio, fecha_fin): # CHEQUEO RANGO DE FECHAS VALIDO
                    print("El rango de fechas es invalido. Recuerde que la fecha de inicio debe ser anterior o igual a la de fin.")
                    return # detengo la generacio del reporte
                

                producto = input("ingrese el producto: ") # INGRESO DEL ID DEL PRODUCTO
                if not self.validar_producto_dw(producto):
                    print(f"Error al validar {producto} en el data warehouse.")
                    return # detengo la generacion del reporte
            
            case _:
                print("Opcion no valida")
                return

        df_reporte = pd.DataFrame() # preparo un dataframe vacio

        match eleccion:
            case "1":
                fecha_inicio_sql = f"{fecha_inicio} 00:00:00"
                fecha_fin_sql = f"{fecha_fin} 23:59:59"
                df_reporte = self.reporte_egresos_producto(fecha_inicio_sql, fecha_fin_sql, producto, id_usuario, auditoria)
                #periodo = input("En que tipo de periodo desea el reporte 1=anio, 2=trimestre, 3=mes, 4=semana, 5=dia")
                self.graficar_reporte_egresos(df_reporte)
            
            
            case "3":
                df_reporte = self.reporte_evolucion_stock(periodo, fecha_fin, producto)
