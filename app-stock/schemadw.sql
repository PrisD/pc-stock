
-- Tabla DIMPRODUCTOS
CREATE TABLE dim_productos (
    id_producto INTEGER PRIMARY KEY,
    nombre_producto VARCHAR(50,)
    descripcion_producto VARCHAR(100),
    stock_minimo INTEGER,
);

-- Tabla DIMTIEMPO
CREATE TABLE dim_tiempo (
    id_fecha INTEGER PRIMARY KEY,
    fecha_completa DATETIME NOT NULL,
    dia INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    nombre_dia VARCHAR(10),
    nombre_mes VARCHAR(10)
);

-- Tabla FACTMOVIMIENTOS
CREATE TABLE fact_movimientos (
    id_producto INTEGER NOT NULL,
    id_fecha INTEGER NOT NULL,
    cantidad_ingresos INTEGER,
    cantidad_egresos INTEGER,
    cantidad_vencidos INTEGER,

    PRIMARY KEY (id_producto, id_fecha),

    FOREIGN KEY (id_producto) REFERENCES dim_productos(id_producto),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo(id_fecha)
);


-- Tabla FACTSTOCKDIARIOS
CREATE TABLE fact_stock_diario (
    id_producto INTEGER NOT NULL,
    id_fecha INTEGER NOT NULL,
    stock_final_del_dia INTEGER NOT NULL,

    PRIMARY KEY (id_producto, id_fecha),

    FOREIGN KEY (id_producto) REFERENCES dim_productos(id_producto),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo(id_fecha)
)