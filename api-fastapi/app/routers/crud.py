"""Fábrica genérica de routers CRUD con borrado lógico (estado=false) y permisos por módulo."""
from typing import Callable, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import requiere_permiso, es_admin
from app.db.session import obtener_bd
from app.models import Usuario


def guardar(bd: Session, obj=None):
    """Confirma la transacción traduciendo violaciones de UNIQUE/FK a 409."""
    try:
        bd.commit()
    except IntegrityError as e:
        bd.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT,
                            f"Conflicto de integridad (campo único duplicado o referencia inválida): {e.orig.diag.message_primary if hasattr(e.orig, 'diag') else e.orig}")
    if obj is not None:
        bd.refresh(obj)  # recarga valores generados por la BD (creado, actualizado, códigos)
    return obj


def crear_router_crud(*, modelo, prefijo: str, modulo: str, etiqueta: str,
                      esquema_crear, esquema_actualizar, esquema_salida,
                      antes_guardar: Optional[Callable] = None,
                      verificar_acceso: Optional[Callable] = None) -> APIRouter:
    """
    antes_guardar(bd, datos: dict, usuario, existente|None) -> dict : ajusta datos (p.ej. hash de clave, dueño).
    verificar_acceso(bd, obj, usuario) : lanza 403 si el usuario no puede modificar ese registro.
    """
    router = APIRouter(prefix=prefijo, tags=[etiqueta])
    pk = modelo.__mapper__.primary_key[0]

    def buscar(bd: Session, id_: int, incluir_inactivos=False):
        obj = bd.get(modelo, id_)
        if not obj or (not obj.estado and not incluir_inactivos):
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"{etiqueta}: registro {id_} no encontrado")
        return obj

    @router.get("", response_model=list[esquema_salida], summary=f"Listar {etiqueta} (solo activos por defecto)")
    def listar(incluir_inactivos: bool = Query(False, description="Solo admin: incluir registros con estado=false"),
               saltar: int = Query(0, ge=0), limite: int = Query(100, ge=1, le=500),
               bd: Session = Depends(obtener_bd), usuario: Usuario = Depends(requiere_permiso(modulo, "leer"))):
        consulta = select(modelo)
        if not (incluir_inactivos and es_admin(bd, usuario)):
            consulta = consulta.where(modelo.estado.is_(True))
        return bd.scalars(consulta.order_by(pk).offset(saltar).limit(limite)).all()

    @router.get("/{id_}", response_model=esquema_salida, summary=f"Obtener {etiqueta} por id")
    def obtener(id_: int, bd: Session = Depends(obtener_bd),
                usuario: Usuario = Depends(requiere_permiso(modulo, "leer"))):
        return buscar(bd, id_, es_admin(bd, usuario))

    @router.post("", response_model=esquema_salida, status_code=201, summary=f"Crear {etiqueta}")
    def crear(datos: esquema_crear, bd: Session = Depends(obtener_bd),
              usuario: Usuario = Depends(requiere_permiso(modulo, "crear"))):
        valores = datos.model_dump()
        if antes_guardar:
            valores = antes_guardar(bd, valores, usuario, None)
        obj = modelo(**{k: v for k, v in valores.items() if hasattr(modelo, k) and v is not None})
        bd.add(obj)
        return guardar(bd, obj)

    @router.put("/{id_}", response_model=esquema_salida, summary=f"Actualizar {etiqueta}")
    def actualizar(id_: int, datos: esquema_actualizar, bd: Session = Depends(obtener_bd),
                   usuario: Usuario = Depends(requiere_permiso(modulo, "actualizar"))):
        obj = buscar(bd, id_, incluir_inactivos=es_admin(bd, usuario))
        if verificar_acceso:
            verificar_acceso(bd, obj, usuario)
        valores = datos.model_dump(exclude_unset=True)
        if antes_guardar:
            valores = antes_guardar(bd, valores, usuario, obj)
        for campo, valor in valores.items():
            if hasattr(modelo, campo) and campo not in ("creado", "actualizado"):
                setattr(obj, campo, valor)
        return guardar(bd, obj)

    @router.delete("/{id_}", summary=f"Eliminar (lógico) {etiqueta}: estado=false")
    def eliminar(id_: int, bd: Session = Depends(obtener_bd),
                 usuario: Usuario = Depends(requiere_permiso(modulo, "eliminar"))):
        obj = buscar(bd, id_)
        if verificar_acceso:
            verificar_acceso(bd, obj, usuario)
        obj.estado = False          # borrado lógico: el registro NO se elimina físicamente
        guardar(bd, obj)
        return {"mensaje": f"{etiqueta} {id_} eliminado lógicamente (estado=false)", "id": id_, "estado": False}

    return router
