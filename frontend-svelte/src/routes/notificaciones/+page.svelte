<script>
  // Página /notificaciones: CRUD de notificaciones usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerNotificaciones,
    obtenerNotificacionPorId,
    crearNotificacion,
    actualizarNotificacion,
    eliminarNotificacion
  } from '$lib/services/api_notificacion.js';
  import { fuenteUsuarios } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerNotificaciones,
    obtener: obtenerNotificacionPorId,
    crear: crearNotificacion,
    actualizar: actualizarNotificacion,
    eliminar: eliminarNotificacion
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { usuarios: fuenteUsuarios };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_usuario', etiqueta: 'Destinatario', fuente: 'usuarios', requerido: true },
    { nombre: 'titulo', etiqueta: 'Título', tipo: 'texto', requerido: true },
    { nombre: 'mensaje', etiqueta: 'Mensaje', tipo: 'area', requerido: true },
    { nombre: 'leida', etiqueta: 'Leída', tipo: 'bool' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Destinatario', campo: 'id_usuario', fuente: 'usuarios' },
    { etiqueta: 'Título', campo: 'titulo' },
    { etiqueta: 'Mensaje', campo: 'mensaje' },
    { etiqueta: 'Leída', campo: 'leida', bool: true },
    { etiqueta: 'Fecha', campo: 'creado' }
  ];
</script>

<CrudModulo
  titulo="Notificaciones"
  subtitulo="Avisos generados por el sistema y por los coordinadores"
  modulo="notificaciones"
  pk="id_notificacion"
  {servicio}
  {fuentes}
  {campos}
  {columnas}
  filtro={(f, s) => s.rol !== 'estudiante' || f.id_usuario === s.id_usuario}
/>
