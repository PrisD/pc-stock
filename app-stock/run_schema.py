import sqlite3
import os


def run_schema():
    """Ejecuta un archivo schema.sql sobre una base de datos SQLite."""
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "stock.db"))
    cursor = conn.cursor()

    with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with open(os.path.join(os.path.dirname(__file__), "schemadw.sql"), "r", encoding="utf-8") as f:
        schemadw_sql = f.read()

    cursor.executescript(schema_sql)
    cursor.executescript(schemadw_sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    run_schema()
