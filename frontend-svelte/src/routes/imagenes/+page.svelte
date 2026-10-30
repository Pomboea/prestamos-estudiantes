<script>
  // Página /imagenes: CRUD de imágenes de objetos usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerImagenes,
    obtenerImagenPorId,
    crearImagen,
    actualizarImagen,
    eliminarImagen
  } from '$lib/services/api_imagen.js';
  import { fuenteObjetos } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerImagenes,
    obtener: obtenerImagenPorId,
    crear: crearImagen,
    actualizar: actualizarImagen,
    eliminar: eliminarImagen
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { objetos: fuenteObjetos };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_objeto', etiqueta: 'Objeto', fuente: 'objetos', requerido: true },
    { nombre: 'url', etiqueta: 'URL de la imagen', tipo: 'texto', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Objeto', campo: 'id_objeto', fuente: 'objetos' },
    { etiqueta: 'URL', campo: 'url' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Imágenes de objetos"
  subtitulo="Fotos de los objetos publicados"
  modulo="imagenes"
  pk="id_imagen"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
