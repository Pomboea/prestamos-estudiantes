<script>
  // Página /prestamos: CRUD de préstamos usando el componente reutilizable CrudModulo
  import CrudModulo from '$lib/components/CrudModulo.svelte';
  import {
    obtenerPrestamos,
    obtenerPrestamoPorId,
    crearPrestamo,
    actualizarPrestamo,
    eliminarPrestamo
  } from '$lib/services/api_prestamo.js';
  import { fuenteSolicitudes, fuenteCondiciones } from '$lib/services/fuentes.js';
  import { sesion } from '$lib/services/api_auth.js';
  import { registrarDevolucion } from '$lib/services/api_flujo.js';

  // Las funciones del servicio que usa el módulo (listar, obtener, crear, actualizar, eliminar)
  const servicio = {
    listar: obtenerPrestamos,
    obtener: obtenerPrestamoPorId,
    crear: crearPrestamo,
    actualizar: actualizarPrestamo,
    eliminar: eliminarPrestamo
  };

  // Listas para mostrar NOMBRES en lugar de IDs
  const fuentes = { solicitudes: fuenteSolicitudes, condiciones: fuenteCondiciones };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_solicitud', etiqueta: 'Solicitud', fuente: 'solicitudes', requerido: true, soloCrear: true },
    { nombre: 'fecha_devolucion_esperada', etiqueta: 'Fecha de devolución esperada', tipo: 'fecha', requerido: true },
    { nombre: 'id_condicion_entrega', etiqueta: 'Condición de entrega', fuente: 'condiciones', requerido: true },
    { nombre: 'observaciones', etiqueta: 'Observaciones', tipo: 'area' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Solicitud', campo: 'id_solicitud', fuente: 'solicitudes' },
    { etiqueta: 'Fecha préstamo', campo: 'fecha_prestamo' },
    { etiqueta: 'Devolver antes de', campo: 'fecha_devolucion_esperada' },
    { etiqueta: 'Condición entrega', campo: 'id_condicion_entrega', fuente: 'condiciones' },
    { etiqueta: 'Observaciones', campo: 'observaciones' }
  ];

  // El propietario registra la devolución; el objeto vuelve a quedar disponible
  const accionesExtra = [
    { texto: 'Registrar devolución', variante: 'exito',
      ejecutar: async (f) => { await registrarDevolucion(f.id_prestamo, f.id_condicion_entrega, 'Devuelto desde la aplicación web'); return 'Devolución registrada'; } }
  ];
</script>

<CrudModulo
  titulo="Préstamos"
  subtitulo="Préstamos registrados (se crean al entregar una solicitud aprobada)"
  modulo="prestamos"
  nombreSingular="préstamo"
  pk="id_prestamo"
  {servicio}
  {fuentes}
  {campos}
  {columnas}
  permitirCrear={$sesion?.rol === 'admin'}
  {accionesExtra}
/>
