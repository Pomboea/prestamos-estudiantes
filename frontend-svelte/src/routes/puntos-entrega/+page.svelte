<script>
  // Página /puntos-entrega: CRUD de puntos de entrega usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerPuntosEntrega,
    obtenerPuntoEntregaPorId,
    crearPuntoEntrega,
    actualizarPuntoEntrega,
    eliminarPuntoEntrega
  } from '$lib/services/api_punto_entrega.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerPuntosEntrega,
    obtener: obtenerPuntoEntregaPorId,
    crear: crearPuntoEntrega,
    actualizar: actualizarPuntoEntrega,
    eliminar: eliminarPuntoEntrega
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = {  };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'codigo', etiqueta: 'Código', tipo: 'texto', requerido: true },
    { nombre: 'nombre', etiqueta: 'Nombre', tipo: 'texto', requerido: true },
    { nombre: 'ubicacion', etiqueta: 'Ubicación', tipo: 'texto', requerido: true },
    { nombre: 'sede', etiqueta: 'Sede', tipo: 'texto', requerido: true }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Código', campo: 'codigo' },
    { etiqueta: 'Nombre', campo: 'nombre' },
    { etiqueta: 'Ubicación', campo: 'ubicacion' },
    { etiqueta: 'Sede', campo: 'sede' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Puntos de entrega"
  subtitulo="API Express + MySQL: lugares donde se entregan los objetos"
  modulo="puntos_entrega"
  pk="id_punto"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
