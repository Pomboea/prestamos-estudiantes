// Servicio de Roles - API FastAPI (PostgreSQL)
import { encabezados, procesarRespuesta, API_PRINCIPAL } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_PRINCIPAL + '/api/roles/';

// GET /api/roles/  -> lista de registros activos
export async function obtenerRoles() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/roles/{id}  -> un registro
export async function obtenerRolPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api/roles/  -> crea un registro
export async function crearRol(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api/roles/{id}  -> actualiza un registro
export async function actualizarRol(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api/roles/{id}  -> eliminación lógica (estado = false)
export async function eliminarRol(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
