<script>
  // Página /roles: CRUD de roles usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerRoles,
    obtenerRolPorId,
    crearRol,
    actualizarRol,
    eliminarRol
  } from '$lib/services/api_rol.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerRoles,
    obtener: obtenerRolPorId,
    crear: crearRol,
    actualizar: actualizarRol,
    eliminar: eliminarRol
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
    { etiqueta: 'Creado', campo: 'creado' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Roles"
  subtitulo="Roles del sistema"
  modulo="roles"
  nombreSingular="rol"
  pk="id_rol"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
