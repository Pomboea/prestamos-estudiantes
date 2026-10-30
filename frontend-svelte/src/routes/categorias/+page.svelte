<script>
  // Página /categorias: CRUD de categorías de objetos usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerCategorias,
    obtenerCategoriaPorId,
    crearCategoria,
    actualizarCategoria,
    eliminarCategoria
  } from '$lib/services/api_categoria.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerCategorias,
    obtener: obtenerCategoriaPorId,
    crear: crearCategoria,
    actualizar: actualizarCategoria,
    eliminar: eliminarCategoria
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
  titulo="Categorías de objetos"
  subtitulo="Tipos de objetos que se prestan"
  modulo="categorias"
  pk="id_categoria"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
