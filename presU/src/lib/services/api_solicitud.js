// Servicio de Solicitudes - API FastAPI (PostgreSQL)
// Dirección de la API FastAPI (PostgreSQL). En local queda '' y el proxy '/api' de vite.config.js la reenvía;
// en la nube se usa VITE_API_URL.
const API = import.meta.env.VITE_API_URL || '';

// Cabeceras de la petición: JSON y, si hay sesión, el token JWT
function encabezados(conJson = false) {
  const cabeceras = {};
  if (conJson) cabeceras['Content-Type'] = 'application/json';
  const token = localStorage.getItem('token');
  if (token) cabeceras['Authorization'] = 'Bearer ' + token;
  return cabeceras;
}

// Función auxiliar: revisa la respuesta y la convierte a objeto JavaScript
async function procesarRespuesta(respuesta) {
  if (!respuesta.ok) {
    let detalle = respuesta.statusText;
    try {
      const cuerpo = await respuesta.json();
      detalle = cuerpo.detail || cuerpo.error || detalle;
      if (typeof detalle !== 'string') detalle = detalle.map((d) => d.msg).join(', ');
    } catch (e) {}
    if (respuesta.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('sesion');
    }
    throw new Error('Error ' + respuesta.status + ': ' + detalle);
  }
  return await respuesta.json();
}

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API + '/api/solicitudes/';

// GET /api/solicitudes/  -> lista de registros activos
export async function obtenerSolicitudes() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/solicitudes/{id}  -> un registro
export async function obtenerSolicitudPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api/solicitudes/  -> crea un registro
export async function crearSolicitud(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api/solicitudes/{id}  -> actualiza un registro
export async function actualizarSolicitud(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api/solicitudes/{id}  -> eliminación lógica (estado = false)
export async function eliminarSolicitud(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}

// ---------- Flujo principal: solicitar -> aprobar/rechazar -> entregar ----------
const URL_FLUJO = API + '/api/flujo/';

// POST /api/flujo/solicitar
export async function solicitarPrestamo(solicitud) {
  const respuesta = await fetch(URL_FLUJO + 'solicitar', {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(solicitud)
  });
  return await procesarRespuesta(respuesta);
}

// POST /api/flujo/solicitudes/{id}/decision
export async function decidirSolicitud(idSolicitud, aprobar, comentario = '') {
  const respuesta = await fetch(URL_FLUJO + 'solicitudes/' + idSolicitud + '/decision', {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify({ aprobar: aprobar, comentario: comentario })
  });
  return await procesarRespuesta(respuesta);
}

// POST /api/flujo/solicitudes/{id}/prestar
export async function entregarObjeto(idSolicitud, observaciones = '') {
  const respuesta = await fetch(URL_FLUJO + 'solicitudes/' + idSolicitud + '/prestar', {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify({ observaciones: observaciones })
  });
  return await procesarRespuesta(respuesta);
}
