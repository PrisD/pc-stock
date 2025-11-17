import sqlite3
from utils import stockdb_path


def actualizar_stock(conn, cursor, datos, auditoria):
    """
    Recibe un diccionario con toda la información del movimiento.
    - Inserta lote nuevo si corresponde.
    - Actualiza cantidad de lotes.
    - Inserta movimiento.
    - Actualiza stock general.
    - Hace un solo commit.
    """

    tipo = datos["tipo"]                     # "INGRESO" o "EGRESO"
    id_producto = datos["id_producto"]
    lote_es_nuevo = datos["lote_es_nuevo"]
    datos_lote_nuevo = datos["datos_lote_nuevo"]
    id_lote = datos["id_lote"]
    cantidad = datos["cantidad"]
    id_usuario = datos["id_usuario"]
    estado_lote = datos["estado_lote"]
    fecha = datos["fecha"]
    fecha_vencimiento = datos_lote_nuevo["fecha_venc"] if lote_es_nuevo else None
    fecha_ingreso= datos_lote_nuevo["fecha_ingreso"] if lote_es_nuevo else None


    if cantidad <= 0:
        raise ValueError("La cantidad debe ser positiva.")

    try:
        # ---------------------------------------------------------------------
        # 1) INSERTAR LOTE NUEVO (solo ahora si el usuario confirmó)
        # ---------------------------------------------------------------------
        if lote_es_nuevo:
            cursor.execute("""
                INSERT INTO lotes (id_producto, fecha_ingreso, cantidad, estado, fecha_vencimiento)
                VALUES (?, ?, ?, ?, ?)
            """, (
                id_producto,
                datos_lote_nuevo["fecha_ingreso"].strftime("%Y-%m-%d"),
                datos_lote_nuevo["cantidad"],
                datos_lote_nuevo["estado"],
                datos_lote_nuevo["fecha_venc"].strftime("%Y-%m-%d"),
            ))

            id_lote = cursor.lastrowid  # obtener ID real del lote recién creado

        else:
            # -----------------------------------------------------------------
            # 2) ACTUALIZAR LOTE EXISTENTE
            # -----------------------------------------------------------------
            if tipo == "INGRESO":
                cursor.execute("""
                    UPDATE lotes
                    SET cantidad = cantidad + ?
                    WHERE id_lote = ?
                """, (cantidad, id_lote))

            elif tipo == "EGRESO":
                # Verificar stock en el lote
                cursor.execute("SELECT cantidad FROM lotes WHERE id_lote = ?", (id_lote,))
                stock_actual = cursor.fetchone()[0]

                if cantidad > stock_actual:
                    raise ValueError(f"Egreso mayor al stock del lote (hay {stock_actual}).")

                cursor.execute("""
                    UPDATE lotes
                    SET cantidad = cantidad - ?
                    WHERE id_lote = ?
                """, (cantidad, id_lote))

        # ---------------------------------------------------------------------
        # 3) INSERTAR MOVIMIENTO
        # ---------------------------------------------------------------------
        cursor.execute("""
            INSERT INTO movimientos (id_lote, id_usuario, tipo, cantidad, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (
            id_lote,
            id_usuario[0],
            1 if tipo == "INGRESO" else 0,
            cantidad,
            fecha.strftime("%Y-%m-%d")
        ))

        # ---------------------------------------------------------------------
        # 4) ACTUALIZAR STOCK
        # ---------------------------------------------------------------------
        
        if lote_es_nuevo or estado_lote == "activo":  # solo actualizar stock si no esta vencido
            cursor.execute("""
                INSERT OR IGNORE INTO stock (id_producto, cantidad)
                VALUES (?, 0)
            """, (id_producto,))

            if tipo == "INGRESO":
                cursor.execute("""
                    UPDATE stock SET cantidad = cantidad + ?
                    WHERE id_producto = ?
                """, (cantidad, id_producto))

            else:  # EGRESO
                cursor.execute("SELECT cantidad FROM stock WHERE id_producto = ?", (id_producto,))
                stock_prod = cursor.fetchone()[0]

                if cantidad > stock_prod:
                    raise ValueError(f"No hay stock suficiente del producto (hay {stock_prod}).")

                cursor.execute("""
                    UPDATE stock SET cantidad = cantidad - ?
                    WHERE id_producto = ?
                """, (cantidad, id_producto))

        # ---------------------------------------------------------------------
        # 5) COMMIT FINAL
        # ---------------------------------------------------------------------
        conn.commit()

        # ---------------------------------------------------------------------
        # 6) AUDITORÍA
        # ---------------------------------------------------------------------
        
        if lote_es_nuevo:
            auditoria.registrar_auditoria(id_usuario[0], "CREAR_LOTE", "LOTES", f"Usuario {id_usuario[1]} creó el lote para el producto ID: {id_producto}, Cantidad: {cantidad}, Fecha Ingreso: {fecha_ingreso.strftime('%d/%m/%Y')}, Fecha Vencimiento: {fecha_vencimiento.strftime('%d/%m/%Y')}")
            
        if tipo == "INGRESO" and not lote_es_nuevo:
            auditoria.registrar_auditoria(id_usuario[0], "INGRESO_LOTE_EXISTENTE", "LOTES", f"Usuario {id_usuario[1]} ingresó {cantidad} unidades al lote ID: {id_lote} del producto ID: {id_producto}")
        
        if tipo == "EGRESO":
            auditoria.registrar_auditoria(id_usuario[0], "EGRESO_LOTE", "LOTES", f"Usuario {id_usuario[1]} retiró {cantidad} unidades del lote ID: {id_lote} del producto ID: {id_producto}")
        

        auditoria.registrar_auditoria(
            id_usuario[0],
            "REGISTRAR_MOVIMIENTO",
            "MOVIMIENTOS",
            f"Usuario {id_usuario[1]} registró un {tipo} de {cantidad} unidades "
            f"en lote ID {id_lote}, producto ID {id_producto} ({fecha.strftime('%d/%m/%Y')})"
        )

        print("Movimiento guardado correctamente. Stock actualizado.")

        return id_lote  # útil si el lote se creó recién

    except Exception as e:
        conn.rollback()
        raise e
