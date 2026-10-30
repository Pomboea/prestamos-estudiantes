// Servicio de TiposIncidencia - API Express (MySQL)
import { encabezados, procesarRespuesta, API_AUXILIAR } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_AUXILIAR + '/tipos-incidencia/';

// GET /api-aux/tipos-incidencia/  -> lista de registros activos
export async function obtenerTiposIncidencia() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api-aux/tipos-incidencia/{id}  -> un registro
export async function obtenerTipoIncidenciaPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api-aux/tipos-incidencia/  -> crea un registro
export async function crearTipoIncidencia(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api-aux/tipos-incidencia/{id}  -> actualiza un registro
export async function actualizarTipoIncidencia(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api-aux/tipos-incidencia/{id}  -> eliminación lógica (estado = false)
export async function eliminarTipoIncidencia(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
