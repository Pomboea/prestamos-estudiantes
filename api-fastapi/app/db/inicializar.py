"""Crea el esquema y los datos semilla SOLO si la BD está vacía (útil en Render/Railway).
Uso: python -m app.db.inicializar"""
import pathlib

from sqlalchemy import inspect

from app.db.session import motor

SQL = pathlib.Path(__file__).resolve().parents[2] / "sql"


def inicializar():
    if inspect(motor).has_table("rol"):
        print("La base de datos ya tiene tablas; no se modifica.")
        return
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
