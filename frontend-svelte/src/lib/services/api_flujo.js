// Servicio del flujo principal: solicitar -> aprobar/rechazar -> prestar -> devolver
import { encabezados, procesarRespuesta, API_PRINCIPAL } from './api_base.js';

const URL_BASE = API_PRINCIPAL + '/api/flujo/';

async function enviar(ruta, datos) {
  const respuesta = await fetch(URL_BASE + ruta, {
    method: 'POST',
    headers: encabezados(true),
    body: JSON.stringify(datos)
  });
  return await procesarRespuesta(respuesta);
}

export async function solicitarPrestamo(solicitud) {
  return await enviar('solicitar', solicitud);
}

export async function decidirSolicitud(idSolicitud, aprobar, comentario = '') {
  return await enviar('solicitudes/' + idSolicitud + '/decision', { aprobar: aprobar, comentario: comentario });
}

export async function entregarObjeto(idSolicitud, observaciones = '') {
  return await enviar('solicitudes/' + idSolicitud + '/prestar', { observaciones: observaciones });
}

export async function registrarDevolucion(idPrestamo, idCondicion, observaciones = '') {
  return await enviar('prestamos/' + idPrestamo + '/devolver', {
    id_condicion_devolucion: idCondicion,
    observaciones: observaciones
  });
}
