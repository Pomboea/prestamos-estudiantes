"""Conexión a PostgreSQL con SQLAlchemy 2."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import config

motor = create_engine(config.url_bd, pool_pre_ping=True)
SesionLocal = sessionmaker(bind=motor, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def obtener_bd():
    """Dependencia de FastAPI: abre y cierra una sesión por petición."""
    bd = SesionLocal()
    try:
        yield bd
    finally:
        bd.close()
