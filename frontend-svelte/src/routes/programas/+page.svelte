<script>
  // Página /programas: CRUD de programas académicos usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerProgramas,
    obtenerProgramaPorId,
    crearPrograma,
    actualizarPrograma,
    eliminarPrograma
  } from '$lib/services/api_programa.js';
  import { fuenteFacultades } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerProgramas,
    obtener: obtenerProgramaPorId,
    crear: crearPrograma,
    actualizar: actualizarPrograma,
    eliminar: eliminarPrograma
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { facultades: fuenteFacultades };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'codigo', etiqueta: 'Código', tipo: 'texto', requerido: true },
    { nombre: 'nombre', etiqueta: 'Nombre', tipo: 'texto', requerido: true },
    { nombre: 'id_facultad', etiqueta: 'Facultad', fuente: 'facultades', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Código', campo: 'codigo' },
    { etiqueta: 'Nombre', campo: 'nombre' },
    { etiqueta: 'Facultad', campo: 'id_facultad', fuente: 'facultades' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Programas académicos"
  subtitulo="Programas por facultad"
  modulo="programas"
  nombreSingular="programa"
  pk="id_programa"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
