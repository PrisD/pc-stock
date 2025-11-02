import sqlite3
import os
import utils

class Reportes:
    def __init__(self, db_name='dw.db'):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conn = None
        self.cursor = None

    def iniciar_conexion_dw(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def cerrar_conexion_dw(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def validar_producto_dw(self, prodcuto):
        pass

    def reporte_ingresos_egresos_producto(self, fecha_inicio, fecha_fin, producto):
        pass

    def reporte_vencimientos(self, fecha_inicio, fecha_fin):
        pass

    def reporte_evolucion_stock(self, tipo_periodo, fecha_inicio, producto):
        pass

    def exportar_reporte(self, formato): # DETERMINAR SI SE ELIJE ANTES O DESPUES DE GENERAR
        pass


    def generar_reporte(self):
        print("Selecciones el tipo de reporte que desea:")
        print("1. Reporte de ingresos y egresos por fecha dividido por producto.")
        print("2. Reporte de vencimientos por fecha.")
        print("3. Reporte de evolucion de stock de un producto por periodo.")

        eleccion = input("Ingrese el numero del tipo de reporte que desea: ")

        match eleccion:
            case "1":
                fecha_inicio = input("Ingrese la fecha de inicio: ") # FALTA REPETIR MIENTRAS FALLE
                utils.validar_fecha(fecha_inicio)
                fecha_fin = input("Ingrese la fecha de fin: ") # FALTA REPETIR MIENTRAS FALLE
                utils.validar_fecha(fecha_fin)
                utils.validar_rango_fechas(fecha_inicio, fecha_fin)
                producto = input("ingrese el prodcuto: ") # FALTA REPETIR MIENTRAS FALLE
                self.validar_producto_dw(producto)
            
            case "2":
                fecha_inicio = input("Ingrese la fecha de inicio: ")
                utils.validar_fecha(fecha_inicio)
                fecha_fin = input("Ingrese la fecha de fin: ")
                utils.validar_fecha(fecha_fin)
                utils.validar_rango_fechas(fecha_inicio, fecha_fin)

            case "3":
                periodo = input("ingrese periodo: ") # FALTA MOSTRAR OPCIONES Y REPETIR MIENTRAS FALLE
                fecha_fin = input("Ingrese la fecha de fin: ")
                utils.validar_fecha(fecha_fin) # FALTA REPETIR MIENTRAS FALLE
                producto = input("ingrese el prodcuto: ") # FALTA REPETIR MIENTRAS FALLE
                self.validar_producto_dw(producto)

        self.iniciar_conexion_dw()

        match eleccion:
            case "1":
                self.reporte_ingresos_egresos_producto(fecha_inicio, fecha_fin, producto)
            
            case "2":
                self.reporte_vencimientos(fecha_inicio, fecha_fin)
            
            case "3":
                self.reporte_evolucion_stock(periodo, fecha_fin, producto)

        self.cerrar_conexion_dw()



