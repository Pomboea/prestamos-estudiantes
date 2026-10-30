<script>
  // Página /moduloxrol: CRUD de permisos por rol usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerPermisos,
    obtenerPermisoPorId,
    crearPermiso,
    actualizarPermiso,
    eliminarPermiso
  } from '$lib/services/api_moduloxrol.js';
  import { fuenteRoles, fuenteModulos } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerPermisos,
    obtener: obtenerPermisoPorId,
    crear: crearPermiso,
    actualizar: actualizarPermiso,
    eliminar: eliminarPermiso
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { roles: fuenteRoles, modulos: fuenteModulos };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_rol', etiqueta: 'Rol', fuente: 'roles', requerido: true },
    { nombre: 'id_modulo', etiqueta: 'Módulo', fuente: 'modulos', requerido: true },
    { nombre: 'puede_leer', etiqueta: 'Puede consultar', tipo: 'bool', porDefecto: true },
    { nombre: 'puede_crear', etiqueta: 'Puede crear', tipo: 'bool' },
    { nombre: 'puede_actualizar', etiqueta: 'Puede actualizar', tipo: 'bool' },
    { nombre: 'puede_eliminar', etiqueta: 'Puede eliminar', tipo: 'bool' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Rol', campo: 'id_rol', fuente: 'roles' },
    { etiqueta: 'Módulo', campo: 'id_modulo', fuente: 'modulos' },
    { etiqueta: 'Consultar', campo: 'puede_leer', bool: true },
    { etiqueta: 'Crear', campo: 'puede_crear', bool: true },
    { etiqueta: 'Actualizar', campo: 'puede_actualizar', bool: true },
    { etiqueta: 'Eliminar', campo: 'puede_eliminar', bool: true }
  ];
</script>

<CrudModulo
  titulo="Permisos por rol"
  subtitulo="Tabla moduloxrol: qué módulos ve y qué puede hacer cada rol"
  modulo="permisos"
  pk="id_moduloxrol"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
