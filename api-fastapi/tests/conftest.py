"""Configuración de pruebas: usa la BD 'prestamos_test' y la recrea (schema + seed) al iniciar."""
import os
import pathlib

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg2://prestamos:prestamos@localhost:5432/prestamos_test")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.db.session import motor
from app.main import app

SQL = pathlib.Path(__file__).resolve().parents[1] / "sql"


@pytest.fixture(scope="session", autouse=True)
def base_limpia():
    con = motor.raw_connection()
    try:
        cur = con.cursor()
        cur.execute((SQL / "schema.sql").read_text())
        cur.execute((SQL / "seed.sql").read_text())
        con.commit()
    finally:
        con.close()
    yield


@pytest.fixture(scope="session")
def cliente():
    return TestClient(app)


def token(cliente, correo, clave):
    r = cliente.post("/api/auth/login", data={"username": correo, "password": clave})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture(scope="session")
def admin(cliente):
    return token(cliente, "admin@uni.edu.co", "Admin123*")


@pytest.fixture(scope="session")
def ana(cliente):
    return token(cliente, "ana@uni.edu.co", "Estudiante123*")


@pytest.fixture(scope="session")
def carlos(cliente):
    return token(cliente, "carlos@uni.edu.co", "Estudiante123*")


@pytest.fixture
def sql():
    def _ejecutar(consulta, **p):
        with motor.connect() as c:
            return c.execute(text(consulta), p).mappings().all()
    return _ejecutar
