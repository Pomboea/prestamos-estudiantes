// Servicio de Modulos - API FastAPI (PostgreSQL)
import { encabezados, procesarRespuesta, API_PRINCIPAL } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_PRINCIPAL + '/api/modulos/';

// GET /api/modulos/  -> lista de registros activos
export async function obtenerModulos() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/modulos/{id}  -> un registro
export async function obtenerModuloPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api/modulos/  -> crea un registro
export async function crearModulo(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api/modulos/{id}  -> actualiza un registro
export async function actualizarModulo(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api/modulos/{id}  -> eliminación lógica (estado = false)
export async function eliminarModulo(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
