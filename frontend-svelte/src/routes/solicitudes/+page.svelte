<script>
  // Página /solicitudes: CRUD de solicitudes de préstamo usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerSolicitudes,
    obtenerSolicitudPorId,
    crearSolicitud,
    actualizarSolicitud,
    eliminarSolicitud
  } from '$lib/services/api_solicitud.js';
  import { fuenteObjetos, fuenteUsuarios, fuenteEstadosSolicitud } from '$lib/services/fuentes.js';
  import { solicitarPrestamo, decidirSolicitud, entregarObjeto } from '$lib/services/api_flujo.js';
  import { obtenerObjetos } from '$lib/services/api_objeto.js';
  import { obtenerEstadosSolicitud } from '$lib/services/api_estado_solicitud.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerSolicitudes,
    obtener: obtenerSolicitudPorId,
    crear: crearSolicitud,
    actualizar: actualizarSolicitud,
    eliminar: eliminarSolicitud
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { objetos: fuenteObjetos, usuarios: fuenteUsuarios, estados_solicitud: fuenteEstadosSolicitud };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_objeto', etiqueta: 'Objeto', fuente: 'objetos', requerido: true, soloCrear: true },
    { nombre: 'fecha_inicio_deseada', etiqueta: 'Fecha de inicio', tipo: 'fecha', requerido: true },
    { nombre: 'fecha_fin_deseada', etiqueta: 'Fecha de fin', tipo: 'fecha', requerido: true },
    { nombre: 'mensaje', etiqueta: 'Mensaje al propietario', tipo: 'area' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Código', campo: 'codigo' },
    { etiqueta: 'Objeto', campo: 'id_objeto', fuente: 'objetos' },
    { etiqueta: 'Solicitante', campo: 'id_solicitante', fuente: 'usuarios' },
    { etiqueta: 'Estado', campo: 'id_estado_solicitud', fuente: 'estados_solicitud' },
    { etiqueta: 'Desde', campo: 'fecha_inicio_deseada' },
    { etiqueta: 'Hasta', campo: 'fecha_fin_deseada' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];

  // Acciones del flujo: solo el propietario del objeto (o el administrador) las ve
  let duenos = {};
  let estados = {};
  async function cargarAuxiliares() {
    (await obtenerObjetos()).forEach((o) => (duenos[o.id_objeto] = o.id_propietario));
    (await obtenerEstadosSolicitud()).forEach((e) => (estados[e.id_estado_solicitud] = e.nombre));
  }
  const listo = cargarAuxiliares();
  const esDueno = (fila, ses) => ses.rol === 'admin' || duenos[fila.id_objeto] === ses.id_usuario;
  const accionesExtra = [
    { texto: 'Aprobar', variante: 'exito', visible: (f, s) => esDueno(f, s) && estados[f.id_estado_solicitud] === 'Pendiente',
      ejecutar: async (f) => { await listo; await decidirSolicitud(f.id_solicitud, true); return 'Solicitud aprobada; el solicitante fue notificado'; } },
    { texto: 'Rechazar', variante: 'borrar', visible: (f, s) => esDueno(f, s) && estados[f.id_estado_solicitud] === 'Pendiente',
      ejecutar: async (f) => { await decidirSolicitud(f.id_solicitud, false); return 'Solicitud rechazada'; } },
    { texto: 'Entregar objeto', variante: 'primario', visible: (f, s) => esDueno(f, s) && estados[f.id_estado_solicitud] === 'Aprobada',
      ejecutar: async (f) => { await entregarObjeto(f.id_solicitud, 'Entregado desde la aplicación web'); return 'Préstamo registrado: el objeto quedó como prestado'; } }
  ];
</script>

<CrudModulo
  titulo="Solicitudes de préstamo"
  subtitulo="Función principal: un estudiante solicita, el propietario aprueba y entrega"
  modulo="solicitudes"
  pk="id_solicitud"
  {servicio}
  {fuentes}
  {campos}
  {columnas}
  alCrear={solicitarPrestamo}
  {accionesExtra}
/>
