"""Modelos ORM (SQLAlchemy 2). Reflejan sql/schema.sql.
Los campos estado/creado/actualizado los gestiona la BD (DEFAULT + trigger)."""
from datetime import datetime, date
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, Date, SmallInteger, text, FetchedValue
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Auditoria:
    """Mixin con los 3 campos obligatorios en todas las tablas."""
    estado: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    creado: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    actualizado: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"),
                                                  server_onupdate=FetchedValue(), nullable=False)


def fk(destino: str, nulo: bool = False):
    return mapped_column(Integer, ForeignKey(destino), nullable=nulo)


class Rol(Auditoria, Base):
    __tablename__ = "rol"
    id_rol: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(200))


class Modulo(Auditoria, Base):
    __tablename__ = "modulo"
    id_modulo: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), unique=True)
    ruta: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(200))


class ModuloXRol(Auditoria, Base):
    __tablename__ = "moduloxrol"
    id_moduloxrol: Mapped[int] = mapped_column(primary_key=True)
    id_rol: Mapped[int] = fk("rol.id_rol")
    id_modulo: Mapped[int] = fk("modulo.id_modulo")
    puede_leer: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    puede_crear: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    puede_actualizar: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    puede_eliminar: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))


class Facultad(Auditoria, Base):
    __tablename__ = "facultad"
    id_facultad: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)


class ProgramaAcademico(Auditoria, Base):
    __tablename__ = "programa_academico"
    id_programa: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True)
    nombre: Mapped[str] = mapped_column(String(120))
    id_facultad: Mapped[int] = fk("facultad.id_facultad")


class Usuario(Auditoria, Base):
    __tablename__ = "usuario"
    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    nombres: Mapped[str] = mapped_column(String(80))
    apellidos: Mapped[str] = mapped_column(String(80))
    correo: Mapped[str] = mapped_column(String(120), unique=True)
    codigo_estudiantil: Mapped[str | None] = mapped_column(String(20), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(20))
    contrasena_hash: Mapped[str] = mapped_column(String(255))
    id_rol: Mapped[int] = fk("rol.id_rol")
    id_programa: Mapped[int | None] = fk("programa_academico.id_programa", True)


class CategoriaObjeto(Auditoria, Base):
    __tablename__ = "categoria_objeto"
    id_categoria: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(200))


class CondicionObjeto(Auditoria, Base):
    __tablename__ = "condicion_objeto"
    id_condicion: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(40), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(200))


class Objeto(Auditoria, Base):
    __tablename__ = "objeto"
    id_objeto: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(30), unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(300))
    id_categoria: Mapped[int] = fk("categoria_objeto.id_categoria")
    id_condicion: Mapped[int] = fk("condicion_objeto.id_condicion")
    id_propietario: Mapped[int] = fk("usuario.id_usuario")
    disponible: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))


class ImagenObjeto(Auditoria, Base):
    __tablename__ = "imagen_objeto"
    id_imagen: Mapped[int] = mapped_column(primary_key=True)
    id_objeto: Mapped[int] = fk("objeto.id_objeto")
    url: Mapped[str] = mapped_column(String(300), unique=True)


class EstadoSolicitud(Auditoria, Base):
    __tablename__ = "estado_solicitud"
    id_estado_solicitud: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), unique=True)


class SolicitudPrestamo(Auditoria, Base):
    __tablename__ = "solicitud_prestamo"
    id_solicitud: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(40), unique=True, server_default=FetchedValue())
    id_objeto: Mapped[int] = fk("objeto.id_objeto")
    id_solicitante: Mapped[int] = fk("usuario.id_usuario")
    id_estado_solicitud: Mapped[int] = fk("estado_solicitud.id_estado_solicitud")
    fecha_inicio_deseada: Mapped[date] = mapped_column(Date)
    fecha_fin_deseada: Mapped[date] = mapped_column(Date)
    mensaje: Mapped[str | None] = mapped_column(String(300))


class Prestamo(Auditoria, Base):
    __tablename__ = "prestamo"
    id_prestamo: Mapped[int] = mapped_column(primary_key=True)
    id_solicitud: Mapped[int] = mapped_column(ForeignKey("solicitud_prestamo.id_solicitud"), unique=True)
    fecha_prestamo: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    fecha_devolucion_esperada: Mapped[date] = mapped_column(Date)
    id_condicion_entrega: Mapped[int] = fk("condicion_objeto.id_condicion")
    observaciones: Mapped[str | None] = mapped_column(String(300))


class Devolucion(Auditoria, Base):
    __tablename__ = "devolucion"
    id_devolucion: Mapped[int] = mapped_column(primary_key=True)
    id_prestamo: Mapped[int] = mapped_column(ForeignKey("prestamo.id_prestamo"), unique=True)
    fecha_devolucion: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    id_condicion_devolucion: Mapped[int] = fk("condicion_objeto.id_condicion")
    observaciones: Mapped[str | None] = mapped_column(String(300))


class Calificacion(Auditoria, Base):
    __tablename__ = "calificacion"
    id_calificacion: Mapped[int] = mapped_column(primary_key=True)
    id_prestamo: Mapped[int] = fk("prestamo.id_prestamo")
    id_evaluador: Mapped[int] = fk("usuario.id_usuario")
    id_evaluado: Mapped[int] = fk("usuario.id_usuario")
    puntaje: Mapped[int] = mapped_column(SmallInteger)
    comentario: Mapped[str | None] = mapped_column(String(300))


class Notificacion(Auditoria, Base):
    __tablename__ = "notificacion"
    id_notificacion: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(40), unique=True, server_default=FetchedValue())
    id_usuario: Mapped[int] = fk("usuario.id_usuario")
    titulo: Mapped[str] = mapped_column(String(100))
    mensaje: Mapped[str] = mapped_column(String(300))
    leida: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))


class Sancion(Auditoria, Base):
    __tablename__ = "sancion"
    id_sancion: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(40), unique=True, server_default=FetchedValue())
    id_usuario: Mapped[int] = fk("usuario.id_usuario")
    id_prestamo: Mapped[int | None] = fk("prestamo.id_prestamo", True)
    motivo: Mapped[str] = mapped_column(String(200))
    fecha_inicio: Mapped[date] = mapped_column(Date, server_default=text("CURRENT_DATE"))
    fecha_fin: Mapped[date] = mapped_column(Date)
