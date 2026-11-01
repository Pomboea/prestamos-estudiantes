<script>
  // Página /tipos-incidencia: CRUD de tipos de incidencia usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerTiposIncidencia,
    obtenerTipoIncidenciaPorId,
    crearTipoIncidencia,
    actualizarTipoIncidencia,
    eliminarTipoIncidencia
  } from '$lib/services/api_tipo_incidencia.js';
  import { fuenteGravedad } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerTiposIncidencia,
    obtener: obtenerTipoIncidenciaPorId,
    crear: crearTipoIncidencia,
    actualizar: actualizarTipoIncidencia,
    eliminar: eliminarTipoIncidencia
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { gravedad: fuenteGravedad };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'nombre', etiqueta: 'Nombre', tipo: 'texto', requerido: true },
    { nombre: 'gravedad', etiqueta: 'Gravedad', fuente: 'gravedad', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Nombre', campo: 'nombre' },
    { etiqueta: 'Gravedad', campo: 'gravedad', fuente: 'gravedad' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Tipos de incidencia"
  subtitulo="API Express + MySQL: catálogo de incidencias"
  modulo="tipos_incidencia"
  nombreSingular="tipo de incidencia"
  pk="id_tipo"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
