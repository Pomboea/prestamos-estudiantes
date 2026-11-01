<script>
  // Página /calificaciones: CRUD de calificaciones usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerCalificaciones,
    obtenerCalificacionPorId,
    crearCalificacion,
    actualizarCalificacion,
    eliminarCalificacion
  } from '$lib/services/api_calificacion.js';
  import { fuentePrestamos, fuenteUsuarios } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerCalificaciones,
    obtener: obtenerCalificacionPorId,
    crear: crearCalificacion,
    actualizar: actualizarCalificacion,
    eliminar: eliminarCalificacion
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { prestamos: fuentePrestamos, usuarios: fuenteUsuarios };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_prestamo', etiqueta: 'Préstamo', fuente: 'prestamos', requerido: true, soloCrear: true },
    { nombre: 'id_evaluado', etiqueta: 'Estudiante calificado', fuente: 'usuarios', requerido: true, soloCrear: true },
    { nombre: 'puntaje', etiqueta: 'Puntaje (1 a 5)', tipo: 'numero', requerido: true },
    { nombre: 'comentario', etiqueta: 'Comentario', tipo: 'area' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Préstamo', campo: 'id_prestamo', fuente: 'prestamos' },
    { etiqueta: 'Evaluador', campo: 'id_evaluador', fuente: 'usuarios' },
    { etiqueta: 'Evaluado', campo: 'id_evaluado', fuente: 'usuarios' },
    { etiqueta: 'Puntaje', valor: (f) => '★'.repeat(f.puntaje) },
    { etiqueta: 'Comentario', campo: 'comentario' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Calificaciones"
  subtitulo="Reseñas entre quien presta y quien recibe"
  modulo="calificaciones"
  nombreSingular="calificación"
  pk="id_calificacion"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
