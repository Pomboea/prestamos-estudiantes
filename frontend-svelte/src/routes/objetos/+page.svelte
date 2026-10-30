<script>
  // Página /objetos: CRUD de objetos usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerObjetos,
    obtenerObjetoPorId,
    crearObjeto,
    actualizarObjeto,
    eliminarObjeto
  } from '$lib/services/api_objeto.js';
  import { fuenteCategorias, fuenteCondiciones, fuenteUsuarios } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerObjetos,
    obtener: obtenerObjetoPorId,
    crear: crearObjeto,
    actualizar: actualizarObjeto,
    eliminar: eliminarObjeto
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { categorias: fuenteCategorias, condiciones: fuenteCondiciones, usuarios: fuenteUsuarios };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'codigo', etiqueta: 'Código', tipo: 'texto', requerido: true, ayuda: 'Ej: OBJ-0021' },
    { nombre: 'nombre', etiqueta: 'Nombre', tipo: 'texto', requerido: true },
    { nombre: 'descripcion', etiqueta: 'Descripción', tipo: 'area' },
    { nombre: 'id_categoria', etiqueta: 'Categoría', fuente: 'categorias', requerido: true },
    { nombre: 'id_condicion', etiqueta: 'Condición', fuente: 'condiciones', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Código', campo: 'codigo' },
    { etiqueta: 'Nombre', campo: 'nombre' },
    { etiqueta: 'Categoría', campo: 'id_categoria', fuente: 'categorias' },
    { etiqueta: 'Condición', campo: 'id_condicion', fuente: 'condiciones' },
    { etiqueta: 'Propietario', campo: 'id_propietario', fuente: 'usuarios' },
    { etiqueta: 'Disponible', campo: 'disponible', bool: true, no: 'Prestado' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Objetos"
  subtitulo="Objetos publicados para préstamo"
  modulo="objetos"
  pk="id_objeto"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
