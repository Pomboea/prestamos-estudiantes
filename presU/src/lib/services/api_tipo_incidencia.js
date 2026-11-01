// Servicio de TiposIncidencia - API Express (MySQL)
// Dirección de la API Express (MySQL). En local pasa por el proxy '/api-aux' de vite.config.js;
// en la nube se usa VITE_API_AUX_URL.
const API = import.meta.env.VITE_API_AUX_URL ? import.meta.env.VITE_API_AUX_URL + '/api' : '/api-aux';

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
const URL_BASE = API + '/tipos-incidencia/';

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
