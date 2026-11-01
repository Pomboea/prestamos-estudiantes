<script>
  // Página /modulos: CRUD de módulos usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerModulos,
    obtenerModuloPorId,
    crearModulo,
    actualizarModulo,
    eliminarModulo
  } from '$lib/services/api_modulo.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerModulos,
    obtener: obtenerModuloPorId,
    crear: crearModulo,
    actualizar: actualizarModulo,
    eliminar: eliminarModulo
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = {  };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'nombre', etiqueta: 'Nombre interno', tipo: 'texto', requerido: true },
    { nombre: 'ruta', etiqueta: 'Ruta de la página', tipo: 'texto', requerido: true },
    { nombre: 'descripcion', etiqueta: 'Descripción (texto del menú)', tipo: 'texto' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Nombre', campo: 'nombre' },
    { etiqueta: 'Ruta', campo: 'ruta' },
    { etiqueta: 'Descripción', campo: 'descripcion' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Módulos"
  subtitulo="Módulos (páginas) del sistema"
  modulo="modulos"
  nombreSingular="módulo"
  pk="id_modulo"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
