"""Autenticación: registro de estudiantes, login (formulario OAuth2 y JSON) y perfil."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models as m, schemas as s
from app.core.security import hashear_contrasena, verificar_contrasena, crear_token, usuario_actual
from app.db.session import obtener_bd
from app.routers.crud import guardar

router = APIRouter(prefix="/auth", tags=["Autenticación (JWT)"])


def _autenticar(bd: Session, correo: str, clave: str) -> s.Token:
    usuario = bd.scalar(select(m.Usuario).where(m.Usuario.correo == correo.lower()))
    if not usuario or not usuario.estado or not verificar_contrasena(clave, usuario.contrasena_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos",
                            headers={"WWW-Authenticate": "Bearer"})
    rol = bd.get(m.Rol, usuario.id_rol)
    return s.Token(access_token=crear_token(usuario, rol.nombre), rol=rol.nombre, id_usuario=usuario.id_usuario)


@router.post("/login", response_model=s.Token, summary="Login con formulario OAuth2 (username=correo)")
def login(formulario: OAuth2PasswordRequestForm = Depends(), bd: Session = Depends(obtener_bd)):
    return _autenticar(bd, formulario.username, formulario.password)


@router.post("/login-json", response_model=s.Token, summary="Login con JSON {correo, contrasena}")
def login_json(datos: s.LoginJSON, bd: Session = Depends(obtener_bd)):
    return _autenticar(bd, datos.correo, datos.contrasena)


@router.post("/registro", response_model=s.UsuarioSalida, status_code=201, summary="Registro público de estudiante")
def registro(datos: s.RegistroEstudiante, bd: Session = Depends(obtener_bd)):
    rol = bd.scalar(select(m.Rol).where(m.Rol.nombre == "estudiante"))
    valores = datos.model_dump()
    valores["correo"] = valores["correo"].lower()
    valores["contrasena_hash"] = hashear_contrasena(valores.pop("contrasena"))
    usuario = m.Usuario(**valores, id_rol=rol.id_rol)
    bd.add(usuario)
    return guardar(bd, usuario)


@router.get("/yo", response_model=s.UsuarioSalida, summary="Perfil del usuario autenticado")
def yo(usuario: m.Usuario = Depends(usuario_actual)):
    return usuario


@router.get("/mis-modulos", summary="Módulos y permisos del rol del usuario (tabla moduloxrol) para armar el menú")
def mis_modulos(usuario: m.Usuario = Depends(usuario_actual), bd: Session = Depends(obtener_bd)):
    filas = bd.execute(
        select(m.Modulo, m.ModuloXRol).join(m.ModuloXRol, m.ModuloXRol.id_modulo == m.Modulo.id_modulo)
        .where(m.ModuloXRol.id_rol == usuario.id_rol, m.ModuloXRol.estado.is_(True), m.Modulo.estado.is_(True),
               m.ModuloXRol.puede_leer.is_(True))
        .order_by(m.Modulo.id_modulo)).all()
    rol = bd.get(m.Rol, usuario.id_rol)
    return {"usuario": f"{usuario.nombres} {usuario.apellidos}", "rol": rol.nombre,
            "modulos": [{"nombre": mo.nombre, "ruta": mo.ruta, "descripcion": mo.descripcion,
                         "leer": p.puede_leer, "crear": p.puede_crear,
                         "actualizar": p.puede_actualizar, "eliminar": p.puede_eliminar} for mo, p in filas]}


@router.get("/directorio", summary="Nombres de usuarios activos (para mostrar nombres en lugar de IDs)")
def directorio(usuario: m.Usuario = Depends(usuario_actual), bd: Session = Depends(obtener_bd)):
    us = bd.scalars(select(m.Usuario).where(m.Usuario.estado.is_(True))).all()
    return [{"id_usuario": u.id_usuario, "nombre": f"{u.nombres} {u.apellidos}"} for u in us]
