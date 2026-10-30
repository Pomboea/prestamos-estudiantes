<script>
  // Página /sanciones: CRUD de sanciones usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerSanciones,
    obtenerSancionPorId,
    crearSancion,
    actualizarSancion,
    eliminarSancion
  } from '$lib/services/api_sancion.js';
  import { fuenteUsuarios, fuentePrestamos } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerSanciones,
    obtener: obtenerSancionPorId,
    crear: crearSancion,
    actualizar: actualizarSancion,
    eliminar: eliminarSancion
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { usuarios: fuenteUsuarios, prestamos: fuentePrestamos };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_usuario', etiqueta: 'Estudiante sancionado', fuente: 'usuarios', requerido: true },
    { nombre: 'id_prestamo', etiqueta: 'Préstamo relacionado', fuente: 'prestamos' },
    { nombre: 'motivo', etiqueta: 'Motivo', tipo: 'area', requerido: true },
    { nombre: 'fecha_fin', etiqueta: 'Vigente hasta', tipo: 'fecha', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Código', campo: 'codigo' },
    { etiqueta: 'Estudiante', campo: 'id_usuario', fuente: 'usuarios' },
    { etiqueta: 'Préstamo', campo: 'id_prestamo', fuente: 'prestamos' },
    { etiqueta: 'Motivo', campo: 'motivo' },
    { etiqueta: 'Desde', campo: 'fecha_inicio' },
    { etiqueta: 'Hasta', campo: 'fecha_fin' }
  ];
</script>

<CrudModulo
  titulo="Sanciones"
  subtitulo="Sanciones por retrasos o daños (las asigna el coordinador)"
  modulo="sanciones"
  pk="id_sancion"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
