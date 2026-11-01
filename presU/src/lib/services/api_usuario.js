import { sesion } from '$lib/index.js';
// Servicio de Usuarios - API FastAPI (PostgreSQL)
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
const URL_BASE = API + '/api/usuarios/';

// GET /api/usuarios/  -> lista de registros activos
export async function obtenerUsuarios() {
  const respuesta = await fetch(URL_BASE, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/usuarios/{id}  -> un registro
export async function obtenerUsuarioPorId(id) {
  const respuesta = await fetch(URL_BASE + id, { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// POST /api/usuarios/  -> crea un registro
export async function crearUsuario(datos) {
  const respuesta = await fetch(URL_BASE, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// PUT /api/usuarios/{id}  -> actualiza un registro
export async function actualizarUsuario(id, datos) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'PUT',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

// DELETE /api/usuarios/{id}  -> eliminación lógica (estado = false)
export async function eliminarUsuario(id) {
  const respuesta = await fetch(URL_BASE + id, {
    method: 'DELETE',
    headers: encabezados()
  });
  return await procesarRespuesta(respuesta);
}

// ---------- Autenticación (JWT emitido por FastAPI y aceptado también por Express) ----------

const URL_AUTH = API + '/api/auth/';

// POST /api/auth/login-json -> token; luego GET /api/auth/mis-modulos -> menú del rol (moduloxrol)
export async function iniciarSesion(correo, contrasena) {
  const respuesta = await fetch(URL_AUTH + 'login-json', {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify({ correo: correo, contrasena: contrasena })
  });
  const datos = await procesarRespuesta(respuesta);
  localStorage.setItem('token', datos.access_token);
  const perfil = await obtenerMisModulos();
  const nuevaSesion = { ...perfil, id_usuario: datos.id_usuario };
  localStorage.setItem('sesion', JSON.stringify(nuevaSesion));
  sesion.set(nuevaSesion);
  return nuevaSesion;
}

export function cerrarSesion() {
  localStorage.removeItem('token');
  localStorage.removeItem('sesion');
  sesion.set(null);
}

// GET /api/auth/mis-modulos -> módulos y permisos del rol
export async function obtenerMisModulos() {
  const respuesta = await fetch(URL_AUTH + 'mis-modulos', { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/auth/directorio -> nombres de usuarios (para mostrar nombres y no IDs)
export async function obtenerDirectorio() {
  const respuesta = await fetch(URL_AUTH + 'directorio', { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}
