// Servicio de Imagenes - API FastAPI (PostgreSQL)
import { encabezados, procesarRespuesta, API_PRINCIPAL } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_PRINCIPAL + '/api/imagenes/';

// GET /api/imagenes/  -> lista de registros activos
export async function obtenerImagenes() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/imagenes/{id}  -> un registro
export async function obtenerImagenPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api/imagenes/  -> crea un registro
export async function crearImagen(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api/imagenes/{id}  -> actualiza un registro
export async function actualizarImagen(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api/imagenes/{id}  -> eliminación lógica (estado = false)
export async function eliminarImagen(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
