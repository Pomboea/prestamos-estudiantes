// Servicio de PuntosEntrega - API Express (MySQL)
import { encabezados, procesarRespuesta, API_AUXILIAR } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_AUXILIAR + '/puntos-entrega/';

// GET /api-aux/puntos-entrega/  -> lista de registros activos
export async function obtenerPuntosEntrega() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api-aux/puntos-entrega/{id}  -> un registro
export async function obtenerPuntoEntregaPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api-aux/puntos-entrega/  -> crea un registro
export async function crearPuntoEntrega(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api-aux/puntos-entrega/{id}  -> actualiza un registro
export async function actualizarPuntoEntrega(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api-aux/puntos-entrega/{id}  -> eliminación lógica (estado = false)
export async function eliminarPuntoEntrega(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
