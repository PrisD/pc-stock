-- Tabla Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(20) NOT NULL UNIQUE
);

-- Tabla Auditoria
CREATE TABLE IF NOT EXISTS Auditoria (
    id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    accion VARCHAR(50) NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    detalle VARCHAR(100),
    fecha_hora DATETIME,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

INSERT OR IGNORE INTO Usuario (nombre) VALUES ('admin');
INSERT OR IGNORE INTO Usuario (nombre) VALUES ('priscila');
INSERT OR IGNORE INTO Usuario (nombre) VALUES ('agustin');
INSERT OR IGNORE INTO Usuario (nombre) VALUES ('matias');
INSERT OR IGNORE INTO Usuario (nombre) VALUES ('lautaro');
INSERT OR IGNORE INTO Usuario (nombre) VALUES ('joaquin');