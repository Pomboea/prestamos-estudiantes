// Servicio de autenticación (JWT emitido por FastAPI y aceptado también por Express)
import { writable } from 'svelte/store';
import { encabezados, procesarRespuesta, API_PRINCIPAL } from './api_base.js';

const URL_BASE = API_PRINCIPAL + '/api/auth/';

function sesionGuardada() {
  try {
    return JSON.parse(localStorage.getItem('sesion'));
  } catch (e) {
    return null;
  }
}

// Sesión actual: { usuario, rol, modulos[] }. Los módulos vienen de la tabla moduloxrol.
export const sesion = writable(sesionGuardada());

// POST /api/auth/login-json -> token; luego GET /api/auth/mis-modulos -> menú del rol
export async function iniciarSesion(correo, contrasena) {
  const respuesta = await fetch(URL_BASE + 'login-json', {
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

// GET /api/auth/mis-modulos -> módulos y permisos del rol (moduloxrol)
export async function obtenerMisModulos() {
  const respuesta = await fetch(URL_BASE + 'mis-modulos', { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}

// GET /api/auth/directorio -> nombres de usuarios (para mostrar nombres y no IDs)
export async function obtenerDirectorio() {
  const respuesta = await fetch(URL_BASE + 'directorio', { headers: encabezados() });
  return await procesarRespuesta(respuesta);
}
