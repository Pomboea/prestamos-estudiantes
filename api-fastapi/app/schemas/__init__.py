"""Esquemas Pydantic v2 (validación de entrada y salida).
Por cada tabla: <X>Crear (POST), <X>Actualizar (PUT, todo opcional) y <X>Salida (respuesta).
El cliente NUNCA envía creado/actualizado; 'estado' solo puede reactivarse vía PUT."""
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, create_model


class Salida(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    estado: bool
    creado: datetime
    actualizado: datetime


def variantes(nombre: str, crear: type[BaseModel], pk: str, extra_salida: dict | None = None,
              ocultar: tuple = ()):
    """Genera los esquemas Actualizar (campos opcionales + estado) y Salida a partir de Crear."""
    opcionales = {k: (Optional[v.annotation], None) for k, v in crear.model_fields.items()}
    opcionales["estado"] = (Optional[bool], None)
    actualizar = create_model(f"{nombre}Actualizar", **opcionales)
    campos_salida = {k: (Optional[v.annotation], None) for k, v in crear.model_fields.items() if k not in ocultar}
    campos_salida[pk] = (int, ...)
    campos_salida.update(extra_salida or {})
    salida = create_model(f"{nombre}Salida", __base__=Salida, **campos_salida)
    return actualizar, salida


# ---------- Seguridad / control de acceso ----------
class RolCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)
RolActualizar, RolSalida = variantes("Rol", RolCrear, "id_rol")


class ModuloCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=60)
    ruta: str = Field(min_length=1, max_length=100)
    descripcion: Optional[str] = None
ModuloActualizar, ModuloSalida = variantes("Modulo", ModuloCrear, "id_modulo")


class ModuloXRolCrear(BaseModel):
    id_rol: int
    id_modulo: int
    puede_leer: bool = True
    puede_crear: bool = False
    puede_actualizar: bool = False
    puede_eliminar: bool = False
ModuloXRolActualizar, ModuloXRolSalida = variantes("ModuloXRol", ModuloXRolCrear, "id_moduloxrol")


class UsuarioCrear(BaseModel):
    nombres: str = Field(min_length=2, max_length=80)
    apellidos: str = Field(min_length=2, max_length=80)
    correo: EmailStr
    codigo_estudiantil: Optional[str] = Field(None, max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    contrasena: str = Field(min_length=6, max_length=72)
    id_rol: int
    id_programa: Optional[int] = None
UsuarioActualizar, UsuarioSalida = variantes("Usuario", UsuarioCrear, "id_usuario", ocultar=("contrasena",))


class RegistroEstudiante(BaseModel):
    """Registro público: siempre crea un usuario con rol 'estudiante'."""
    nombres: str = Field(min_length=2, max_length=80)
    apellidos: str = Field(min_length=2, max_length=80)
    correo: EmailStr
    codigo_estudiantil: str = Field(min_length=3, max_length=20)
    telefono: Optional[str] = None
    contrasena: str = Field(min_length=6, max_length=72)
    id_programa: Optional[int] = None


class LoginJSON(BaseModel):
    correo: EmailStr
    contrasena: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    id_usuario: int


# ---------- Catálogos ----------
class FacultadCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
FacultadActualizar, FacultadSalida = variantes("Facultad", FacultadCrear, "id_facultad")


class ProgramaCrear(BaseModel):
    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=120)
    id_facultad: int
ProgramaActualizar, ProgramaSalida = variantes("Programa", ProgramaCrear, "id_programa")


class CategoriaCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=60)
    descripcion: Optional[str] = None
CategoriaActualizar, CategoriaSalida = variantes("Categoria", CategoriaCrear, "id_categoria")


class CondicionCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=40)
    descripcion: Optional[str] = None
CondicionActualizar, CondicionSalida = variantes("Condicion", CondicionCrear, "id_condicion")


class EstadoSolicitudCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=30)
EstadoSolicitudActualizar, EstadoSolicitudSalida = variantes("EstadoSolicitud", EstadoSolicitudCrear, "id_estado_solicitud")


# ---------- Objetos ----------
class ObjetoCrear(BaseModel):
    codigo: str = Field(min_length=3, max_length=30)
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)
    id_categoria: int
    id_condicion: int
    id_propietario: Optional[int] = None  # si es estudiante se asigna automáticamente
ObjetoActualizar, ObjetoSalida = variantes("Objeto", ObjetoCrear, "id_objeto", {"disponible": (bool, True)})


class ImagenCrear(BaseModel):
    id_objeto: int
    url: str = Field(min_length=5, max_length=300)
ImagenActualizar, ImagenSalida = variantes("Imagen", ImagenCrear, "id_imagen")


# ---------- Flujo de préstamo ----------
class SolicitudCrear(BaseModel):
    id_objeto: int
    fecha_inicio_deseada: date
    fecha_fin_deseada: date
    mensaje: Optional[str] = Field(None, max_length=300)
    id_solicitante: Optional[int] = None        # se toma del token si no es admin
    id_estado_solicitud: Optional[int] = None   # por defecto 'Pendiente'
SolicitudActualizar, SolicitudSalida = variantes("Solicitud", SolicitudCrear, "id_solicitud", {"codigo": (str, ...)})


class PrestamoCrear(BaseModel):
    id_solicitud: int
    fecha_devolucion_esperada: date
    id_condicion_entrega: int
    observaciones: Optional[str] = None
PrestamoActualizar, PrestamoSalida = variantes("Prestamo", PrestamoCrear, "id_prestamo", {"fecha_prestamo": (datetime, ...)})


class DevolucionCrear(BaseModel):
    id_prestamo: int
    id_condicion_devolucion: int
    observaciones: Optional[str] = None
DevolucionActualizar, DevolucionSalida = variantes("Devolucion", DevolucionCrear, "id_devolucion", {"fecha_devolucion": (datetime, ...)})


class CalificacionCrear(BaseModel):
    id_prestamo: int
    id_evaluado: int
    puntaje: int = Field(ge=1, le=5)
    comentario: Optional[str] = None
    id_evaluador: Optional[int] = None
CalificacionActualizar, CalificacionSalida = variantes("Calificacion", CalificacionCrear, "id_calificacion")


class NotificacionCrear(BaseModel):
    id_usuario: int
    titulo: str = Field(min_length=2, max_length=100)
    mensaje: str = Field(min_length=2, max_length=300)
    leida: bool = False
NotificacionActualizar, NotificacionSalida = variantes("Notificacion", NotificacionCrear, "id_notificacion", {"codigo": (str, ...)})


class SancionCrear(BaseModel):
    id_usuario: int
    id_prestamo: Optional[int] = None
    motivo: str = Field(min_length=3, max_length=200)
    fecha_fin: date
SancionActualizar, SancionSalida = variantes("Sancion", SancionCrear, "id_sancion",
                                             {"codigo": (str, ...), "fecha_inicio": (date, ...)})


class DecisionSolicitud(BaseModel):
    aprobar: bool
    comentario: Optional[str] = None
