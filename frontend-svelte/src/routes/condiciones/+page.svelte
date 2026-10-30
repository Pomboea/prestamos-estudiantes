<script>
  // Página /condiciones: CRUD de condiciones de objeto usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerCondiciones,
    obtenerCondicionPorId,
    crearCondicion,
    actualizarCondicion,
    eliminarCondicion
  } from '$lib/services/api_condicion.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerCondiciones,
    obtener: obtenerCondicionPorId,
    crear: crearCondicion,
    actualizar: actualizarCondicion,
    eliminar: eliminarCondicion
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = {  };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'nombre', etiqueta: 'Nombre', tipo: 'texto', requerido: true },
    { nombre: 'descripcion', etiqueta: 'Descripción', tipo: 'area' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Nombre', campo: 'nombre' },
    { etiqueta: 'Descripción', campo: 'descripcion' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Condiciones de objeto"
  subtitulo="Estado físico de los objetos"
  modulo="condiciones"
  pk="id_condicion"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
