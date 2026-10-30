// Servicio de ReportesIncidencia - API Express (MySQL)
import { encabezados, procesarRespuesta, API_AUXILIAR } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_AUXILIAR + '/reportes-incidencia/';

// GET /api-aux/reportes-incidencia/  -> lista de registros activos
export async function obtenerReportesIncidencia() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api-aux/reportes-incidencia/{id}  -> un registro
export async function obtenerReporteIncidenciaPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api-aux/reportes-incidencia/  -> crea un registro
export async function crearReporteIncidencia(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api-aux/reportes-incidencia/{id}  -> actualiza un registro
export async function actualizarReporteIncidencia(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api-aux/reportes-incidencia/{id}  -> eliminación lógica (estado = false)
export async function eliminarReporteIncidencia(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
