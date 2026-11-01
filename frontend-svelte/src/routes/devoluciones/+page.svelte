<script>
  // Página /devoluciones: CRUD de devoluciones usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerDevoluciones,
    obtenerDevolucionPorId,
    crearDevolucion,
    actualizarDevolucion,
    eliminarDevolucion
  } from '$lib/services/api_devolucion.js';
  import { fuentePrestamos, fuenteCondiciones } from '$lib/services/fuentes.js';
  import { sesion } from '$lib/services/api_auth.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerDevoluciones,
    obtener: obtenerDevolucionPorId,
    crear: crearDevolucion,
    actualizar: actualizarDevolucion,
    eliminar: eliminarDevolucion
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { prestamos: fuentePrestamos, condiciones: fuenteCondiciones };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_prestamo', etiqueta: 'Préstamo', fuente: 'prestamos', requerido: true, soloCrear: true },
    { nombre: 'id_condicion_devolucion', etiqueta: 'Condición de devolución', fuente: 'condiciones', requerido: true },
    { nombre: 'observaciones', etiqueta: 'Observaciones', tipo: 'area' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Préstamo', campo: 'id_prestamo', fuente: 'prestamos' },
    { etiqueta: 'Fecha devolución', campo: 'fecha_devolucion' },
    { etiqueta: 'Condición', campo: 'id_condicion_devolucion', fuente: 'condiciones' },
    { etiqueta: 'Observaciones', campo: 'observaciones' }
  ];
</script>

<CrudModulo
  titulo="Devoluciones"
  subtitulo="Objetos devueltos y su condición"
  modulo="devoluciones"
  nombreSingular="devolución"
  pk="id_devolucion"
  {servicio}
  {fuentes}
  {campos}
  {columnas}
  permitirCrear={$sesion?.rol === 'admin'}
/>
