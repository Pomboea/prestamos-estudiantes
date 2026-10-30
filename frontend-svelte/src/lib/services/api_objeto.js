// Servicio de Objetos - API FastAPI (PostgreSQL)
import { encabezados, procesarRespuesta, API_PRINCIPAL } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_PRINCIPAL + '/api/objetos/';

// GET /api/objetos/  -> lista de registros activos
export async function obtenerObjetos() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/objetos/{id}  -> un registro
export async function obtenerObjetoPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api/objetos/  -> crea un registro
export async function crearObjeto(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api/objetos/{id}  -> actualiza un registro
export async function actualizarObjeto(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api/objetos/{id}  -> eliminación lógica (estado = false)
export async function eliminarObjeto(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
