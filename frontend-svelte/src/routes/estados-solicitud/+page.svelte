<script>
  // Página /estados-solicitud: CRUD de estados de solicitud usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerEstadosSolicitud,
    obtenerEstadoSolicitudPorId,
    crearEstadoSolicitud,
    actualizarEstadoSolicitud,
    eliminarEstadoSolicitud
  } from '$lib/services/api_estado_solicitud.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerEstadosSolicitud,
    obtener: obtenerEstadoSolicitudPorId,
    crear: crearEstadoSolicitud,
    actualizar: actualizarEstadoSolicitud,
    eliminar: eliminarEstadoSolicitud
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = {  };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'nombre', etiqueta: 'Nombre', tipo: 'texto', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Nombre', campo: 'nombre' },
    { etiqueta: 'Creado', campo: 'creado' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Estados de solicitud"
  subtitulo="Catálogo de estados del flujo"
  modulo="estados_solicitud"
  pk="id_estado_solicitud"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
