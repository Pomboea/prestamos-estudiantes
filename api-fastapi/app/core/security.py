"""Seguridad: hash de contraseñas con bcrypt, JWT y autorización por rol/módulo (moduloxrol)."""
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import config
from app.db.session import obtener_bd
from app.models import Usuario, Rol, Modulo, ModuloXRol

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hashear_contrasena(clave: str) -> str:
    return bcrypt.hashpw(clave.encode(), bcrypt.gensalt()).decode()


def verificar_contrasena(clave: str, hash_: str) -> bool:
    try:
        return bcrypt.checkpw(clave.encode(), hash_.encode())
    except ValueError:
        return False


def crear_token(usuario: Usuario, rol: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    datos = {"sub": str(usuario.id_usuario), "correo": usuario.correo, "rol": rol, "exp": expira}
    return jwt.encode(datos, config.SECRET_KEY, algorithm=config.ALGORITHM)


def usuario_actual(token: str = Depends(esquema_oauth2), bd: Session = Depends(obtener_bd)) -> Usuario:
    """Valida el JWT y devuelve el usuario activo. 401 si el token falta, es inválido o expiró."""
    error = HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido o expirado",
                          headers={"WWW-Authenticate": "Bearer"})
    try:
        datos = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        id_usuario = int(datos["sub"])
    except (JWTError, KeyError, ValueError):
        raise error
    usuario = bd.get(Usuario, id_usuario)
    if not usuario or not usuario.estado:
        raise error
    return usuario


def es_admin(bd: Session, usuario: Usuario) -> bool:
    rol = bd.get(Rol, usuario.id_rol)
    return bool(rol and rol.nombre == "admin")


ACCIONES = {"leer": "puede_leer", "crear": "puede_crear",
            "actualizar": "puede_actualizar", "eliminar": "puede_eliminar"}


def requiere_permiso(modulo: str, accion: str):
    """Dependencia: verifica en moduloxrol que el rol del usuario tenga la acción sobre el módulo (403 si no)."""
    def _verificar(usuario: Usuario = Depends(usuario_actual), bd: Session = Depends(obtener_bd)) -> Usuario:
        permiso = bd.execute(
            select(ModuloXRol).join(Modulo, Modulo.id_modulo == ModuloXRol.id_modulo)
            .join(Rol, Rol.id_rol == ModuloXRol.id_rol)
            .where(ModuloXRol.id_rol == usuario.id_rol, Modulo.nombre == modulo,
                   ModuloXRol.estado.is_(True), Modulo.estado.is_(True), Rol.estado.is_(True))
        ).scalar_one_or_none()
        if not permiso or not getattr(permiso, ACCIONES[accion]):
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                f"Su rol no tiene permiso para '{accion}' en el módulo '{modulo}'")
        return usuario
    return _verificar
