// Servicio de Solicitudes - API FastAPI (PostgreSQL)
import { encabezados, procesarRespuesta, API_PRINCIPAL } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_PRINCIPAL + '/api/solicitudes/';

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
