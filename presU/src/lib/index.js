// $lib/index.js: estado compartido de la aplicación (se importa con '$lib' o '$lib/index.js').
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function sesionGuardada() {
  if (!browser) return null;
  try {
    return JSON.parse(localStorage.getItem('sesion'));
  } catch (e) {
    return null;
  }
}

// Sesión actual: { usuario, rol, id_usuario, modulos[] }. Los módulos vienen de la tabla moduloxrol.
export const sesion = writable(sesionGuardada());
