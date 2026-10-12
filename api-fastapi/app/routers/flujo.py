"""Endpoints de negocio: publicar -> solicitar -> aprobar/rechazar -> prestar -> devolver."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app import models as m, schemas as s
from app.core.security import requiere_permiso, es_admin, usuario_actual
from app.db.session import obtener_bd
from app.routers.crud import guardar

router = APIRouter(prefix="/flujo", tags=["Flujo de préstamo"])

PENDIENTE, APROBADA, RECHAZADA, CANCELADA, FINALIZADA = "Pendiente", "Aprobada", "Rechazada", "Cancelada", "Finalizada"


def id_estado(bd: Session, nombre: str) -> int:
    return bd.scalar(select(m.EstadoSolicitud.id_estado_solicitud).where(m.EstadoSolicitud.nombre == nombre))


def notificar(bd: Session, id_usuario: int, titulo: str, mensaje: str):
    bd.add(m.Notificacion(id_usuario=id_usuario, titulo=titulo, mensaje=mensaje))


def objeto_activo(bd: Session, id_objeto: int) -> m.Objeto:
    obj = bd.get(m.Objeto, id_objeto)
    if not obj or not obj.estado:
        raise HTTPException(404, "Objeto no encontrado")
    return obj


class PrestarEntrada(BaseModel):
    fecha_devolucion_esperada: date | None = None   # por defecto la fecha fin de la solicitud
    observaciones: str | None = None


class DevolverEntrada(BaseModel):
    id_condicion_devolucion: int
    observaciones: str | None = None


@router.get("/objetos-disponibles", response_model=list[s.ObjetoSalida], summary="Objetos activos y disponibles para préstamo")
def objetos_disponibles(id_categoria: int | None = None, bd: Session = Depends(obtener_bd),
                        usuario: m.Usuario = Depends(requiere_permiso("objetos", "leer"))):
    q = select(m.Objeto).where(m.Objeto.estado.is_(True), m.Objeto.disponible.is_(True))
    if id_categoria:
        q = q.where(m.Objeto.id_categoria == id_categoria)
    return bd.scalars(q.order_by(m.Objeto.id_objeto)).all()


@router.post("/publicar-objeto", response_model=s.ObjetoSalida, status_code=201, summary="El estudiante publica un objeto propio")
def publicar(datos: s.ObjetoCrear, bd: Session = Depends(obtener_bd),
             usuario: m.Usuario = Depends(requiere_permiso("objetos", "crear"))):
    valores = datos.model_dump(exclude={"id_propietario"})
    obj = m.Objeto(**valores, id_propietario=usuario.id_usuario)
    bd.add(obj)
    return guardar(bd, obj)


@router.post("/solicitar", response_model=s.SolicitudSalida, status_code=201, summary="Solicitar en préstamo un objeto de otro estudiante")
def solicitar(datos: s.SolicitudCrear, bd: Session = Depends(obtener_bd),
              usuario: m.Usuario = Depends(requiere_permiso("solicitudes", "crear"))):
    obj = objeto_activo(bd, datos.id_objeto)
    if obj.id_propietario == usuario.id_usuario:
        raise HTTPException(400, "No puede solicitar su propio objeto")
    if not obj.disponible:
        raise HTTPException(409, "El objeto no está disponible (ya está prestado)")
    if datos.fecha_fin_deseada < datos.fecha_inicio_deseada:
        raise HTTPException(422, "La fecha fin debe ser mayor o igual a la fecha inicio")
    sancion = bd.scalar(select(m.Sancion).where(m.Sancion.id_usuario == usuario.id_usuario, m.Sancion.estado.is_(True),
                                                m.Sancion.fecha_fin >= date.today()))
    if sancion:
        raise HTTPException(403, f"Tiene una sanción vigente hasta {sancion.fecha_fin}")
    sol = m.SolicitudPrestamo(id_objeto=obj.id_objeto, id_solicitante=usuario.id_usuario,
                              id_estado_solicitud=id_estado(bd, PENDIENTE),
                              fecha_inicio_deseada=datos.fecha_inicio_deseada,
                              fecha_fin_deseada=datos.fecha_fin_deseada, mensaje=datos.mensaje)
    bd.add(sol)
    notificar(bd, obj.id_propietario, "Nueva solicitud", f"Solicitaron su objeto '{obj.nombre}'")
    return guardar(bd, sol)


def _solicitud_de_mi_objeto(bd, id_solicitud, usuario):
    sol = bd.get(m.SolicitudPrestamo, id_solicitud)
    if not sol or not sol.estado:
        raise HTTPException(404, "Solicitud no encontrada")
    obj = bd.get(m.Objeto, sol.id_objeto)
    if not es_admin(bd, usuario) and obj.id_propietario != usuario.id_usuario:
        raise HTTPException(403, "Solo el propietario del objeto puede gestionar esta solicitud")
    return sol, obj


@router.post("/solicitudes/{id_solicitud}/decision", response_model=s.SolicitudSalida, summary="Aprobar o rechazar una solicitud (propietario)")
def decidir(id_solicitud: int, datos: s.DecisionSolicitud, bd: Session = Depends(obtener_bd),
            usuario: m.Usuario = Depends(requiere_permiso("solicitudes", "actualizar"))):
    sol, obj = _solicitud_de_mi_objeto(bd, id_solicitud, usuario)
    if sol.id_estado_solicitud != id_estado(bd, PENDIENTE):
        raise HTTPException(409, "Solo se pueden decidir solicitudes en estado Pendiente")
    if datos.aprobar and not obj.disponible:
        raise HTTPException(409, "El objeto ya está prestado")
    sol.id_estado_solicitud = id_estado(bd, APROBADA if datos.aprobar else RECHAZADA)
    notificar(bd, sol.id_solicitante, "Solicitud " + ("aprobada" if datos.aprobar else "rechazada"),
              f"Su solicitud por '{obj.nombre}' fue {'aprobada' if datos.aprobar else 'rechazada'}. {datos.comentario or ''}")
    return guardar(bd, sol)


@router.post("/solicitudes/{id_solicitud}/prestar", response_model=s.PrestamoSalida, status_code=201,
             summary="Registrar la entrega del objeto (marca el objeto como NO disponible)")
def prestar(id_solicitud: int, datos: PrestarEntrada, bd: Session = Depends(obtener_bd),
            usuario: m.Usuario = Depends(requiere_permiso("prestamos", "crear"))):
    sol, obj = _solicitud_de_mi_objeto(bd, id_solicitud, usuario)
    if sol.id_estado_solicitud != id_estado(bd, APROBADA):
        raise HTTPException(409, "La solicitud debe estar Aprobada para registrar el préstamo")
    if not obj.disponible:
        raise HTTPException(409, "El objeto ya está prestado")
    prestamo = m.Prestamo(id_solicitud=sol.id_solicitud,
                          fecha_devolucion_esperada=datos.fecha_devolucion_esperada or sol.fecha_fin_deseada,
                          id_condicion_entrega=obj.id_condicion, observaciones=datos.observaciones)
    obj.disponible = False
    bd.add(prestamo)
    notificar(bd, sol.id_solicitante, "Préstamo registrado", f"Recibió '{obj.nombre}'. Devuélvalo a tiempo.")
    return guardar(bd, prestamo)


@router.post("/prestamos/{id_prestamo}/devolver", response_model=s.DevolucionSalida, status_code=201,
             summary="Registrar la devolución (objeto vuelve a disponible y se registra su condición)")
def devolver(id_prestamo: int, datos: DevolverEntrada, bd: Session = Depends(obtener_bd),
             usuario: m.Usuario = Depends(requiere_permiso("devoluciones", "crear"))):
    prestamo = bd.get(m.Prestamo, id_prestamo)
    if not prestamo or not prestamo.estado:
        raise HTTPException(404, "Préstamo no encontrado")
    sol, obj = _solicitud_de_mi_objeto(bd, prestamo.id_solicitud, usuario)
    if bd.scalar(select(m.Devolucion).where(m.Devolucion.id_prestamo == id_prestamo)):
        raise HTTPException(409, "Este préstamo ya fue devuelto")
    if not bd.get(m.CondicionObjeto, datos.id_condicion_devolucion):
        raise HTTPException(422, "Condición de devolución inválida")
    dev = m.Devolucion(id_prestamo=id_prestamo, id_condicion_devolucion=datos.id_condicion_devolucion,
                       observaciones=datos.observaciones)
    obj.disponible = True
    obj.id_condicion = datos.id_condicion_devolucion
    sol.id_estado_solicitud = id_estado(bd, FINALIZADA)
    bd.add(dev)
    # Sanción automática por devolución tardía (7 días)
    if date.today() > prestamo.fecha_devolucion_esperada:
        from datetime import timedelta
        bd.add(m.Sancion(id_usuario=sol.id_solicitante, id_prestamo=id_prestamo,
                         motivo="Devolución tardía", fecha_fin=date.today() + timedelta(days=7)))
    notificar(bd, sol.id_solicitante, "Devolución registrada", f"Se registró la devolución de '{obj.nombre}'")
    return guardar(bd, dev)


@router.get("/mis-prestamos", summary="Préstamos donde soy prestador o prestatario")
def mis_prestamos(bd: Session = Depends(obtener_bd), usuario: m.Usuario = Depends(usuario_actual)):
    filas = bd.execute(
        select(m.Prestamo, m.SolicitudPrestamo, m.Objeto)
        .join(m.SolicitudPrestamo, m.SolicitudPrestamo.id_solicitud == m.Prestamo.id_solicitud)
        .join(m.Objeto, m.Objeto.id_objeto == m.SolicitudPrestamo.id_objeto)
        .where(m.Prestamo.estado.is_(True),
               or_(m.SolicitudPrestamo.id_solicitante == usuario.id_usuario,
                   m.Objeto.id_propietario == usuario.id_usuario))
        .order_by(m.Prestamo.id_prestamo)).all()
    resultado = []
    for p, sol, obj in filas:
        devuelto = bd.scalar(select(m.Devolucion.id_devolucion).where(m.Devolucion.id_prestamo == p.id_prestamo)) is not None
        resultado.append({
            "id_prestamo": p.id_prestamo, "objeto": obj.nombre, "id_objeto": obj.id_objeto,
            "rol_en_prestamo": "prestatario" if sol.id_solicitante == usuario.id_usuario else "prestador",
            "fecha_prestamo": p.fecha_prestamo, "fecha_devolucion_esperada": p.fecha_devolucion_esperada,
            "devuelto": devuelto,
        })
    return resultado


@router.get("/mis-solicitudes", response_model=list[s.SolicitudSalida], summary="Solicitudes que he realizado")
def mis_solicitudes(bd: Session = Depends(obtener_bd), usuario: m.Usuario = Depends(usuario_actual)):
    return bd.scalars(select(m.SolicitudPrestamo).where(m.SolicitudPrestamo.id_solicitante == usuario.id_usuario,
                                                        m.SolicitudPrestamo.estado.is_(True))).all()


@router.get("/solicitudes-recibidas", response_model=list[s.SolicitudSalida], summary="Solicitudes sobre mis objetos")
def solicitudes_recibidas(bd: Session = Depends(obtener_bd), usuario: m.Usuario = Depends(usuario_actual)):
    return bd.scalars(select(m.SolicitudPrestamo).join(m.Objeto, m.Objeto.id_objeto == m.SolicitudPrestamo.id_objeto)
                      .where(m.Objeto.id_propietario == usuario.id_usuario, m.SolicitudPrestamo.estado.is_(True))).all()


@router.get("/mis-notificaciones", response_model=list[s.NotificacionSalida], summary="Mis notificaciones")
def mis_notificaciones(bd: Session = Depends(obtener_bd), usuario: m.Usuario = Depends(usuario_actual)):
    return bd.scalars(select(m.Notificacion).where(m.Notificacion.id_usuario == usuario.id_usuario,
                                                   m.Notificacion.estado.is_(True))
                      .order_by(m.Notificacion.id_notificacion.desc())).all()
