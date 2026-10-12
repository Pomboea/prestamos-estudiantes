"""Registra los routers CRUD de las 17 tablas de la base de datos principal."""
from fastapi import HTTPException, status

from app import models as m, schemas as s
from app.core.security import es_admin, hashear_contrasena
from app.routers.crud import crear_router_crud


def _hash_usuario(bd, datos, usuario, existente):
    if datos.get("contrasena"):
        datos["contrasena_hash"] = hashear_contrasena(datos.pop("contrasena"))
    else:
        datos.pop("contrasena", None)
    return datos


def _propietario_objeto(bd, datos, usuario, existente):
    # Un estudiante solo publica/edita objetos a su nombre
    if not es_admin(bd, usuario):
        datos.pop("id_propietario", None)
        datos.pop("disponible", None)
        if existente is None:
            datos["id_propietario"] = usuario.id_usuario
    elif existente is None and not datos.get("id_propietario"):
        datos["id_propietario"] = usuario.id_usuario
    return datos


def _solo_dueno_objeto(bd, obj, usuario):
    if not es_admin(bd, usuario) and obj.id_propietario != usuario.id_usuario:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el propietario del objeto puede modificarlo")


def _solo_dueno_imagen(bd, obj, usuario):
    _solo_dueno_objeto(bd, bd.get(m.Objeto, obj.id_objeto), usuario)


def _imagen_propia(bd, datos, usuario, existente):
    if "id_objeto" in datos and datos["id_objeto"] is not None:
        objeto = bd.get(m.Objeto, datos["id_objeto"])
        if not objeto:
            raise HTTPException(404, "Objeto no existe")
        _solo_dueno_objeto(bd, objeto, usuario)
    return datos


def _solicitud(bd, datos, usuario, existente):
    if not es_admin(bd, usuario):
        datos.pop("id_estado_solicitud", None)  # el estado lo cambia el flujo de aprobación
        datos.pop("id_solicitante", None)
        if existente is None:
            datos["id_solicitante"] = usuario.id_usuario
    if existente is None:
        datos.setdefault("id_solicitante", usuario.id_usuario)
        if not datos.get("id_solicitante"):
            datos["id_solicitante"] = usuario.id_usuario
        if not datos.get("id_estado_solicitud"):
            datos["id_estado_solicitud"] = 1  # Pendiente
    return datos


def _solo_solicitante(bd, obj, usuario):
    if not es_admin(bd, usuario) and obj.id_solicitante != usuario.id_usuario:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo el solicitante puede modificar su solicitud")


def _calificacion(bd, datos, usuario, existente):
    if not es_admin(bd, usuario) or not datos.get("id_evaluador"):
        if existente is None:
            datos["id_evaluador"] = usuario.id_usuario
        else:
            datos.pop("id_evaluador", None)
    return datos


def _solo_evaluador(bd, obj, usuario):
    if not es_admin(bd, usuario) and obj.id_evaluador != usuario.id_usuario:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo quien calificó puede modificar la calificación")


def _solo_destinatario(bd, obj, usuario):
    if not es_admin(bd, usuario) and obj.id_usuario != usuario.id_usuario:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "La notificación pertenece a otro usuario")


def _solo_admin_directo(bd, datos, usuario, existente):
    # Préstamos y devoluciones de estudiantes se registran por /flujo (aplica reglas de negocio)
    if not es_admin(bd, usuario):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "Los estudiantes registran préstamos/devoluciones mediante los endpoints /flujo")
    return datos


# (modelo, prefijo, módulo en tabla 'modulo', etiqueta, esquemas, hooks)
DEFINICIONES = [
    (m.Rol, "/roles", "roles", "Roles", s.RolCrear, s.RolActualizar, s.RolSalida, None, None),
    (m.Modulo, "/modulos", "modulos", "Módulos", s.ModuloCrear, s.ModuloActualizar, s.ModuloSalida, None, None),
    (m.ModuloXRol, "/moduloxrol", "permisos", "Permisos (moduloxrol)", s.ModuloXRolCrear, s.ModuloXRolActualizar, s.ModuloXRolSalida, None, None),
    (m.Usuario, "/usuarios", "usuarios", "Usuarios", s.UsuarioCrear, s.UsuarioActualizar, s.UsuarioSalida, _hash_usuario, None),
    (m.Facultad, "/facultades", "facultades", "Facultades", s.FacultadCrear, s.FacultadActualizar, s.FacultadSalida, None, None),
    (m.ProgramaAcademico, "/programas", "programas", "Programas académicos", s.ProgramaCrear, s.ProgramaActualizar, s.ProgramaSalida, None, None),
    (m.CategoriaObjeto, "/categorias", "categorias", "Categorías", s.CategoriaCrear, s.CategoriaActualizar, s.CategoriaSalida, None, None),
    (m.CondicionObjeto, "/condiciones", "condiciones", "Condiciones de objeto", s.CondicionCrear, s.CondicionActualizar, s.CondicionSalida, None, None),
    (m.Objeto, "/objetos", "objetos", "Objetos", s.ObjetoCrear, s.ObjetoActualizar, s.ObjetoSalida, _propietario_objeto, _solo_dueno_objeto),
    (m.ImagenObjeto, "/imagenes", "imagenes", "Imágenes de objeto", s.ImagenCrear, s.ImagenActualizar, s.ImagenSalida, _imagen_propia, _solo_dueno_imagen),
    (m.EstadoSolicitud, "/estados-solicitud", "estados_solicitud", "Estados de solicitud", s.EstadoSolicitudCrear, s.EstadoSolicitudActualizar, s.EstadoSolicitudSalida, None, None),
    (m.SolicitudPrestamo, "/solicitudes", "solicitudes", "Solicitudes de préstamo", s.SolicitudCrear, s.SolicitudActualizar, s.SolicitudSalida, _solicitud, _solo_solicitante),
    (m.Prestamo, "/prestamos", "prestamos", "Préstamos", s.PrestamoCrear, s.PrestamoActualizar, s.PrestamoSalida, _solo_admin_directo, None),
    (m.Devolucion, "/devoluciones", "devoluciones", "Devoluciones", s.DevolucionCrear, s.DevolucionActualizar, s.DevolucionSalida, _solo_admin_directo, None),
    (m.Calificacion, "/calificaciones", "calificaciones", "Calificaciones", s.CalificacionCrear, s.CalificacionActualizar, s.CalificacionSalida, _calificacion, _solo_evaluador),
    (m.Notificacion, "/notificaciones", "notificaciones", "Notificaciones", s.NotificacionCrear, s.NotificacionActualizar, s.NotificacionSalida, None, _solo_destinatario),
    (m.Sancion, "/sanciones", "sanciones", "Sanciones", s.SancionCrear, s.SancionActualizar, s.SancionSalida, None, None),
]

routers = [
    crear_router_crud(modelo=mo, prefijo=p, modulo=mod, etiqueta=e, esquema_crear=c,
                      esquema_actualizar=a, esquema_salida=sa, antes_guardar=h, verificar_acceso=v)
    for (mo, p, mod, e, c, a, sa, h, v) in DEFINICIONES
]
