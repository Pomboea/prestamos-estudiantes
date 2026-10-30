"""Crea el esquema y los datos semilla si la BD está vacía o tiene la semilla anterior al Taller 1
(sin el rol 'coordinador'). Con FORZAR_SEMILLA=true siempre la recrea. Uso: python -m app.db.inicializar"""
import os
import pathlib

from sqlalchemy import inspect, text

from app.db.session import motor

SQL = pathlib.Path(__file__).resolve().parents[2] / "sql"


def inicializar():
    forzar = os.getenv("FORZAR_SEMILLA", "false").lower() == "true"
    if inspect(motor).has_table("rol") and not forzar:
        with motor.connect() as c:
            actual = c.execute(text("SELECT COUNT(*) FROM rol WHERE nombre = 'coordinador'")).scalar()
        if actual:
            print("La base de datos ya tiene la semilla del Taller 1; no se modifica.")
            return
        print("Semilla anterior detectada: se recrea el esquema con la semilla del Taller 1.")
    con = motor.raw_connection()
    try:
        cur = con.cursor()
        cur.execute((SQL / "schema.sql").read_text(encoding="utf-8"))
        cur.execute((SQL / "seed.sql").read_text(encoding="utf-8"))
        con.commit()
        print("Esquema y datos semilla creados.")
    finally:
        con.close()


if __name__ == "__main__":
    inicializar()
