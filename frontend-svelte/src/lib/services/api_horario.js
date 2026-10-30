// Servicio de Horarios - API Express (MySQL)
import { encabezados, procesarRespuesta, API_AUXILIAR } from './api_base.js';

// Dirección base (el proxy de vite.config.js la reenvía a la API)
const URL_BASE = API_AUXILIAR + '/horarios/';

// GET /api-aux/horarios/  -> lista de registros activos
export async function obtenerHorarios() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api-aux/horarios/{id}  -> un registro
export async function obtenerHorarioPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api-aux/horarios/  -> crea un registro
export async function crearHorario(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api-aux/horarios/{id}  -> actualiza un registro
export async function actualizarHorario(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api-aux/horarios/{id}  -> eliminación lógica (estado = false)
export async function eliminarHorario(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}
