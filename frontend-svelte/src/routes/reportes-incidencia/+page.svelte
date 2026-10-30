<script>
  // Página /reportes-incidencia: CRUD de reportes de incidencia usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerReportesIncidencia,
    obtenerReporteIncidenciaPorId,
    crearReporteIncidencia,
    actualizarReporteIncidencia,
    eliminarReporteIncidencia
  } from '$lib/services/api_reporte_incidencia.js';
  import { fuenteTiposIncidencia, fuentePuntos, fuentePrestamos, fuenteUsuarios } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerReportesIncidencia,
    obtener: obtenerReporteIncidenciaPorId,
    crear: crearReporteIncidencia,
    actualizar: actualizarReporteIncidencia,
    eliminar: eliminarReporteIncidencia
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { tipos: fuenteTiposIncidencia, puntos: fuentePuntos, prestamos: fuentePrestamos, usuarios: fuenteUsuarios };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_tipo', etiqueta: 'Tipo de incidencia', fuente: 'tipos', requerido: true },
    { nombre: 'id_punto', etiqueta: 'Punto de entrega', fuente: 'puntos' },
    { nombre: 'id_prestamo', etiqueta: 'Préstamo', fuente: 'prestamos', requerido: true },
    { nombre: 'descripcion', etiqueta: 'Descripción', tipo: 'area', requerido: true },
    { nombre: 'resuelto', etiqueta: 'Resuelto', tipo: 'bool' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Código', campo: 'codigo' },
    { etiqueta: 'Tipo', campo: 'id_tipo', fuente: 'tipos' },
    { etiqueta: 'Punto', campo: 'id_punto', fuente: 'puntos' },
    { etiqueta: 'Préstamo', campo: 'id_prestamo', fuente: 'prestamos' },
    { etiqueta: 'Reportado por', campo: 'id_usuario_reporta', fuente: 'usuarios' },
    { etiqueta: 'Resuelto', campo: 'resuelto', bool: true },
    { etiqueta: 'Fecha', campo: 'creado' }
  ];
</script>

<CrudModulo
  titulo="Reportes de incidencia"
  subtitulo="API Express + MySQL: daños, pérdidas o retrasos en un préstamo"
  modulo="reportes_incidencia"
  pk="id_reporte"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
