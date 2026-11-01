<script>
  // Página /facultades: CRUD de facultades usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerFacultades,
    obtenerFacultadPorId,
    crearFacultad,
    actualizarFacultad,
    eliminarFacultad
  } from '$lib/services/api_facultad.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerFacultades,
    obtener: obtenerFacultadPorId,
    crear: crearFacultad,
    actualizar: actualizarFacultad,
    eliminar: eliminarFacultad
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
  titulo="Facultades"
  subtitulo="Facultades de la universidad"
  modulo="facultades"
  nombreSingular="facultad"
  pk="id_facultad"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
