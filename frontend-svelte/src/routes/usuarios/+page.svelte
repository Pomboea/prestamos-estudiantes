<script>
  // Página /usuarios: CRUD de usuarios usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerUsuarios,
    obtenerUsuarioPorId,
    crearUsuario,
    actualizarUsuario,
    eliminarUsuario
  } from '$lib/services/api_usuario.js';
  import { fuenteRoles, fuenteProgramas } from '$lib/services/fuentes.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerUsuarios,
    obtener: obtenerUsuarioPorId,
    crear: crearUsuario,
    actualizar: actualizarUsuario,
    eliminar: eliminarUsuario
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { roles: fuenteRoles, programas: fuenteProgramas };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'nombres', etiqueta: 'Nombres', tipo: 'texto', requerido: true },
    { nombre: 'apellidos', etiqueta: 'Apellidos', tipo: 'texto', requerido: true },
    { nombre: 'correo', etiqueta: 'Correo', tipo: 'correo', requerido: true },
    { nombre: 'codigo_estudiantil', etiqueta: 'Código estudiantil', tipo: 'texto' },
    { nombre: 'telefono', etiqueta: 'Teléfono', tipo: 'texto' },
    { nombre: 'contrasena', etiqueta: 'Contraseña', tipo: 'clave', requerido: true, ayuda: 'Al editar, déjela vacía para no cambiarla' },
    { nombre: 'id_rol', etiqueta: 'Rol', fuente: 'roles', requerido: true },
    { nombre: 'id_programa', etiqueta: 'Programa académico', fuente: 'programas' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Nombres', campo: 'nombres' },
    { etiqueta: 'Apellidos', campo: 'apellidos' },
    { etiqueta: 'Correo', campo: 'correo' },
    { etiqueta: 'Código', campo: 'codigo_estudiantil' },
    { etiqueta: 'Rol', campo: 'id_rol', fuente: 'roles' },
    { etiqueta: 'Programa', campo: 'id_programa', fuente: 'programas' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];
</script>

<CrudModulo
  titulo="Usuarios"
  subtitulo="Administradores, coordinadores y estudiantes"
  modulo="usuarios"
  pk="id_usuario"
  {servicio}
  {fuentes}
  {campos}
  {columnas}

/>
