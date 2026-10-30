<script>
  // Página /horarios: CRUD de horarios de atención usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerHorarios,
    obtenerHorarioPorId,
    crearHorario,
    actualizarHorario,
    eliminarHorario
  } from '$lib/services/api_horario.js';
  import { fuentePuntos, fuenteDias } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerHorarios,
    obtener: obtenerHorarioPorId,
    crear: crearHorario,
    actualizar: actualizarHorario,
    eliminar: eliminarHorario
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { puntos: fuentePuntos, dias: fuenteDias };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_punto', etiqueta: 'Punto de entrega', fuente: 'puntos', requerido: true },
    { nombre: 'dia_semana', etiqueta: 'Día', fuente: 'dias', requerido: true },
    { nombre: 'hora_apertura', etiqueta: 'Hora de apertura', tipo: 'hora', requerido: true },
    { nombre: 'hora_cierre', etiqueta: 'Hora de cierre', tipo: 'hora', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Punto', campo: 'id_punto', fuente: 'puntos' },
    { etiqueta: 'Día', campo: 'dia_semana', fuente: 'dias' },
    { etiqueta: 'Abre', campo: 'hora_apertura' },
    { etiqueta: 'Cierra', campo: 'hora_cierre' }
  ];
</script>

<CrudModulo
  titulo="Horarios de atención"
  subtitulo="API Express + MySQL: horario de cada punto de entrega"
  modulo="horarios"
  pk="id_horario"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
