// Funciones compartidas por todos los servicios: cabeceras (JWT) y revisión de la respuesta.

// En local las URL quedan relativas ('/api/...') y las reenvía el proxy de vite.config.js.
// En la nube se definen VITE_API_URL (FastAPI) y VITE_API_AUX_URL (Express) en el hosting.
export const API_PRINCIPAL = import.meta.env.VITE_API_URL || '';
// Express publica sus rutas en /api/...; en local se pasa por el proxy '/api-aux'.
export const API_AUXILIAR = import.meta.env.VITE_API_AUX_URL ? import.meta.env.VITE_API_AUX_URL + '/api' : '/api-aux';

// Cabeceras de la petición. Si hay sesión, se envía el token JWT.
export function encabezados(conJson = false) {
  const cabeceras = {};
  if (conJson) cabeceras['Content-Type'] = 'application/json';
  const token = localStorage.getItem('token');
  if (token) cabeceras['Authorization'] = 'Bearer ' + token;
  return cabeceras;
}

// Revisa la respuesta y la convierte a objeto JavaScript (igual que en el documento CRUD)
export async function procesarRespuesta(respuesta) {
  if (!respuesta.ok) {
    let detalle = '';
    try {
      const cuerpo = await respuesta.json();
      detalle = cuerpo.detail || cuerpo.error || '';
      if (typeof detalle !== 'string') detalle = detalle.map((d) => d.msg).join(', ');
    } catch (e) {
      detalle = respuesta.statusText;
    }
    if (respuesta.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('sesion');
    }
    throw new Error('Error ' + respuesta.status + ': ' + detalle);
  }
  return await respuesta.json();
}
