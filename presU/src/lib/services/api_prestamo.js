// Servicio de Prestamos - API FastAPI (PostgreSQL)
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
const URL_BASE = API + '/api/prestamos/';

// GET /api/prestamos/  -> lista de registros activos
export async function obtenerPrestamos() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/prestamos/{id}  -> un registro
export async function obtenerPrestamoPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api/prestamos/  -> crea un registro
export async function crearPrestamo(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api/prestamos/{id}  -> actualiza un registro
export async function actualizarPrestamo(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api/prestamos/{id}  -> eliminación lógica (estado = false)
export async function eliminarPrestamo(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}

// ---------- Flujo principal: devolución ----------
// POST /api/flujo/prestamos/{id}/devolver
export async function registrarDevolucion(idPrestamo, idCondicion, observaciones = '') {
  const respuesta = await fetch(API + '/api/flujo/prestamos/' + idPrestamo + '/devolver', {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify({ id_condicion_devolucion: idCondicion, observaciones: observaciones })
  });
  return await procesarRespuesta(respuesta);
}
