// Fuentes de opciones para listas desplegables y para mostrar NOMBRES en lugar de IDs.
// Cada función devuelve [{ valor: id, etiqueta: texto }].
import { obtenerDirectorio } from './api_auth.js';
import { obtenerRoles } from './api_rol.js';
import { obtenerModulos } from './api_modulo.js';
import { obtenerFacultades } from './api_facultad.js';
import { obtenerProgramas } from './api_programa.js';
import { obtenerCategorias } from './api_categoria.js';
import { obtenerCondiciones } from './api_condicion.js';
import { obtenerObjetos } from './api_objeto.js';
import { obtenerEstadosSolicitud } from './api_estado_solicitud.js';
import { obtenerSolicitudes } from './api_solicitud.js';
import { obtenerPrestamos } from './api_prestamo.js';
import { obtenerPuntosEntrega } from './api_punto_entrega.js';
import { obtenerTiposIncidencia } from './api_tipo_incidencia.js';

const mapear = (lista, id, texto) => lista.map((x) => ({ valor: x[id], etiqueta: texto(x) }));

export const fuenteUsuarios = async () => mapear(await obtenerDirectorio(), 'id_usuario', (u) => u.nombre);
export const fuenteRoles = async () => mapear(await obtenerRoles(), 'id_rol', (r) => r.nombre);
export const fuenteModulos = async () => mapear(await obtenerModulos(), 'id_modulo', (m) => m.descripcion || m.nombre);
export const fuenteFacultades = async () => mapear(await obtenerFacultades(), 'id_facultad', (f) => f.nombre);
export const fuenteProgramas = async () => mapear(await obtenerProgramas(), 'id_programa', (p) => p.nombre);
export const fuenteCategorias = async () => mapear(await obtenerCategorias(), 'id_categoria', (c) => c.nombre);
export const fuenteCondiciones = async () => mapear(await obtenerCondiciones(), 'id_condicion', (c) => c.nombre);
export const fuenteObjetos = async () => mapear(await obtenerObjetos(), 'id_objeto', (o) => o.nombre + ' (' + o.codigo + ')');
export const fuenteEstadosSolicitud = async () =>
  mapear(await obtenerEstadosSolicitud(), 'id_estado_solicitud', (e) => e.nombre);
export const fuenteSolicitudes = async () => {
  const objetos = await fuenteObjetos();
  return mapear(await obtenerSolicitudes(), 'id_solicitud', (s) =>
    s.codigo + ' · ' + ((objetos.find((o) => o.valor === s.id_objeto) || {}).etiqueta || ''));
};
export const fuentePrestamos = async () => {
  const solicitudes = await fuenteSolicitudes();
  return mapear(await obtenerPrestamos(), 'id_prestamo', (p) =>
    'Préstamo ' + ((solicitudes.find((s) => s.valor === p.id_solicitud) || {}).etiqueta || ''));
};
export const fuentePuntos = async () => mapear(await obtenerPuntosEntrega(), 'id_punto', (p) => p.nombre);
export const fuenteTiposIncidencia = async () => mapear(await obtenerTiposIncidencia(), 'id_tipo', (t) => t.nombre);
export const fuenteDias = async () =>
  ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'].map((d, i) => ({ valor: i + 1, etiqueta: d }));
export const fuenteGravedad = async () =>
  ['baja', 'media', 'alta'].map((g) => ({ valor: g, etiqueta: g.charAt(0).toUpperCase() + g.slice(1) }));
