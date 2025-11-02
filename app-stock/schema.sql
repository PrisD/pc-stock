-- Tabla USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(20) NOT NULL UNIQUE
);

-- Tabla PRODUCTOS
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion VARCHAR(100) NOT NULL,
    stock_bajo INTEGER NOT NULL,
    stock_critico INTEGER NOT NULL
);

-- Tabla LOTES
CREATE TABLE IF NOT EXISTS lotes (
    id_lote INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    fecha_ingreso DATETIME NOT NULL DEFAULT (DATETIME('now')),
    cantidad INTEGER NOT NULL,
    estado VARCHAR(10),
    fecha_vencimiento DATETIME,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla STOCK
CREATE TABLE IF NOT EXISTS stock (
    id_stock INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL UNIQUE,
    cantidad INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla ALERTAS
CREATE TABLE IF NOT EXISTS alertas (
    id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_producto INTEGER NOT NULL,
    fecha DATETIME NOT NULL DEFAULT (DATETIME('now')),
    cantidad INTEGER NOT NULL,
    descripcion VARCHAR(100),
    tipo VARCHAR(20),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla MOVIMIENTOS
CREATE TABLE IF NOT EXISTS movimientos (
    id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_lote INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    tipo INTEGER NOT NULL CHECK (tipo IN (0,1)),
    cantidad INTEGER NOT NULL,
    fecha DATETIME NOT NULL DEFAULT (DATETIME('now')),
    FOREIGN KEY (id_lote) REFERENCES lotes(id_lote),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla AUDITORIAS
CREATE TABLE IF NOT EXISTS auditorias (
    id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    accion VARCHAR(50) NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    detalle VARCHAR(100),
    fecha_hora DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

INSERT OR IGNORE INTO usuarios (nombre) VALUES ('admin');
INSERT OR IGNORE INTO usuarios (nombre) VALUES ('priscila');
INSERT OR IGNORE INTO usuarios (nombre) VALUES ('agustin');
INSERT OR IGNORE INTO usuarios (nombre) VALUES ('matias');
INSERT OR IGNORE INTO usuarios (nombre) VALUES ('lautaro');
INSERT OR IGNORE INTO usuarios (nombre) VALUES ('joaquin');