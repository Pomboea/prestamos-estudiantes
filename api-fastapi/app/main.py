"""API principal (FastAPI) - Sistema de préstamos de objetos entre estudiantes.
Documentación interactiva en /docs (Swagger) y /redoc."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import config
from app.db.session import motor
from app.routers import auth, flujo, recursos

app = FastAPI(title="API Préstamos de Objetos entre Estudiantes",
              description="Parcial I - BD principal PostgreSQL + FastAPI + JWT. Borrado lógico con campo 'estado'.",
              version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS.split(","),
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(flujo.router)
for r in recursos.routers:
    app.include_router(r)


@app.get("/", tags=["Salud"])
def inicio():
    return {"mensaje": "API de préstamos de objetos entre estudiantes", "docs": "/docs"}


@app.get("/salud", tags=["Salud"])
def salud():
    with motor.connect() as c:
        c.execute(text("SELECT 1"))
    return {"estado": "ok", "base_de_datos": "conectada"}
