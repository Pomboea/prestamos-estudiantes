<script>
  // Página /solicitudes: CRUD de solicitudes de préstamo (estructura del documento CRUD: formulario + lista en la misma página)
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { sesion } from '$lib/index.js';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Boton from '$lib/components/Boton.svelte';
  import Alerta from '$lib/components/Alerta.svelte';
  import Cargando from '$lib/components/Cargando.svelte';
  import CampoFormulario from '$lib/components/CampoFormulario.svelte';
  import DataTable from '$lib/components/DataTable.svelte';
  import {
    obtenerSolicitudes,
    obtenerSolicitudPorId,
    crearSolicitud,
    actualizarSolicitud,
    eliminarSolicitud
  } from '$lib/services/api_solicitud.js';
  import { obtenerDirectorio } from '$lib/services/api_usuario.js';
  import { solicitarPrestamo, decidirSolicitud, entregarObjeto } from '$lib/services/api_solicitud.js';
  import { obtenerObjetos } from '$lib/services/api_objeto.js';
  import { obtenerEstadosSolicitud } from '$lib/services/api_estado_solicitud.js';

  // Listas de opciones: muestran NOMBRES en lugar de IDs ([{ valor: id, etiqueta: texto }])
  const mapear = (lista, id, texto) => lista.map((x) => ({ valor: x[id], etiqueta: texto(x) }));
  const fuenteObjetos = async () => mapear(await obtenerObjetos(), 'id_objeto', (o) => o.nombre + ' (' + o.codigo + ')');
  const fuenteUsuarios = async () => mapear(await obtenerDirectorio(), 'id_usuario', (u) => u.nombre);
  const fuenteEstadosSolicitud = async () =>
    mapear(await obtenerEstadosSolicitud(), 'id_estado_solicitud', (e) => e.nombre);

  // Fuentes que usa este módulo (clave -> función)
  const fuentes = { objetos: fuenteObjetos, usuarios: fuenteUsuarios, estados_solicitud: fuenteEstadosSolicitud };

  // Campos del formulario (los ID nunca se escriben: se eligen por nombre en listas)
  const campos = [
    { nombre: 'id_objeto', etiqueta: 'Objeto', fuente: 'objetos', requerido: true, soloCrear: true },
    { nombre: 'fecha_inicio_deseada', etiqueta: 'Fecha de inicio', tipo: 'fecha', requerido: true },
    { nombre: 'fecha_fin_deseada', etiqueta: 'Fecha de fin', tipo: 'fecha', requerido: true },
    { nombre: 'mensaje', etiqueta: 'Mensaje al propietario', tipo: 'area' }
  ];

  // Columnas de la tabla (DataTables). No se muestra ningún ID.
  const columnas = [
    { etiqueta: 'Código', campo: 'codigo' },
    { etiqueta: 'Objeto', campo: 'id_objeto', fuente: 'objetos' },
    { etiqueta: 'Solicitante', campo: 'id_solicitante', fuente: 'usuarios' },
    { etiqueta: 'Estado', campo: 'id_estado_solicitud', fuente: 'estados_solicitud' },
    { etiqueta: 'Desde', campo: 'fecha_inicio_deseada' },
    { etiqueta: 'Hasta', campo: 'fecha_fin_deseada' },
    { etiqueta: 'Actualizado', campo: 'actualizado' }
  ];

  // Acciones del flujo: solo el propietario del objeto (o el administrador) las ve
  let duenos = {};
  let estados = {};
  async function cargarAuxiliares() {
    (await obtenerObjetos()).forEach((o) => (duenos[o.id_objeto] = o.id_propietario));
    (await obtenerEstadosSolicitud()).forEach((e) => (estados[e.id_estado_solicitud] = e.nombre));
  }
  const listo = browser ? cargarAuxiliares() : null;   // solo en el navegador
  const esDueno = (fila, ses) => ses.rol === 'admin' || duenos[fila.id_objeto] === ses.id_usuario;
  const accionesExtra = [
    { texto: 'Aprobar', variante: 'exito', visible: (f, s) => esDueno(f, s) && estados[f.id_estado_solicitud] === 'Pendiente',
      ejecutar: async (f) => { await listo; await decidirSolicitud(f.id_solicitud, true); return 'Solicitud aprobada; el solicitante fue notificado'; } },
    { texto: 'Rechazar', variante: 'borrar', visible: (f, s) => esDueno(f, s) && estados[f.id_estado_solicitud] === 'Pendiente',
      ejecutar: async (f) => { await decidirSolicitud(f.id_solicitud, false); return 'Solicitud rechazada'; } },
    { texto: 'Entregar objeto', variante: 'primario', visible: (f, s) => esDueno(f, s) && estados[f.id_estado_solicitud] === 'Aprobada',
      ejecutar: async (f) => { await entregarObjeto(f.id_solicitud, 'Entregado desde la aplicación web'); return 'Préstamo registrado: el objeto quedó como prestado'; } }
  ];

  // Datos del módulo
  const titulo = 'Solicitudes de préstamo';
  const subtitulo = 'Función principal: un estudiante solicita, el propietario aprueba y entrega';
  const modulo = 'solicitudes';          // nombre en la tabla "modulo" (permisos de moduloxrol)
  const nombreSingular = 'solicitud';
  const pk = 'id_solicitud';                  // llave primaria: se usa por dentro, NUNCA se muestra
  $: permitirCrear = true;
  const alCrear = solicitarPrestamo;
  const filtro = null;
  const campoNombre = null;          // null: el confirm() usa la primera columna

  let filas = [];
  let opciones = {};                  // { clave: [{valor, etiqueta}] }
  let cargando = false;
  let mensaje = '';
  let tipoMensaje = 'info';
  let idEditando = null;

  $: permiso = ($sesion?.modulos || []).find((m) => m.nombre === modulo) || {};

  // Traduce un ID a su nombre usando las fuentes (así el usuario nunca ve IDs)
  function ref(clave, valor) {
    if (valor === null || valor === undefined) return '—';
    const op = (opciones[clave] || []).find((o) => o.valor === valor);
    return op ? op.etiqueta : '—';
  }

  function textoColumna(columna, fila) {
    if (columna.valor) return columna.valor(fila, ref);
    const v = fila[columna.campo];
    if (columna.fuente) return ref(columna.fuente, v);
    if (v === true || (columna.bool && v === 1)) return columna.si || 'Sí';
    if (v === false || (columna.bool && v === 0)) return columna.no || 'No';
    if (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}/.test(v)) return v.replace('T', ' ').slice(0, 16);
    return v ?? '—';
  }

  $: columnasTabla = columnas.map((c) => ({ etiqueta: c.etiqueta, valor: (fila) => textoColumna(c, fila) }));

  async function cargarOpciones() {
    for (const clave of Object.keys(fuentes)) {
      try {
        opciones[clave] = await fuentes[clave]();
      } catch (e) {
        opciones[clave] = [];
      }
    }
    opciones = opciones;
  }

  async function cargarSolicitudes() {
    cargando = true;
    try {
      const datos = await obtenerSolicitudes();
      filas = filtro ? datos.filter((f) => filtro(f, $sesion)) : datos;
    } catch (error) {
      mostrar('No se pudo cargar la lista: ' + error.message, 'error');
    }
    cargando = false;
  }

  function mostrar(texto, tipo = 'info') {
    mensaje = texto;
    tipoMensaje = tipo;
  }

  onMount(async () => {
    await cargarOpciones();
    await cargarSolicitudes();
  });

  function valoresIniciales() {
    const vacio = {};
    campos.forEach((c) => (vacio[c.nombre] = c.tipo === 'bool' ? (c.porDefecto ?? false) : (c.porDefecto ?? null)));
    return vacio;
  }

  let formulario = valoresIniciales();

  function limpiarFormulario() {
    formulario = valoresIniciales();
    idEditando = null;
  }

  async function prepararEdicion(id) {
    try {
      const registro = await obtenerSolicitudPorId(id);
      idEditando = registro[pk];
      const datos = {};
      campos.forEach((c) => {
        let v = registro[c.nombre];
        if (c.tipo === 'bool') v = v === true || v === 1;
        if (c.tipo === 'hora' && typeof v === 'string') v = v.slice(0, 5);
        datos[c.nombre] = c.tipo === 'clave' ? null : (v ?? null);
      });
      formulario = datos;
      mensaje = '';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
      mostrar('No se pudo cargar el registro: ' + error.message, 'error');
    }
  }

  async function guardarSolicitud(evento) {
    evento.preventDefault();
    const datos = {};
    for (const c of campos) {
      if (idEditando === null && c.soloEditar) continue;
      if (idEditando !== null && c.soloCrear) continue;
      let v = formulario[c.nombre];
      if (v === '' || v === undefined) v = null;
      if (c.tipo === 'numero' && v !== null) v = Number(v);
      if (c.tipo === 'clave' && v === null) continue;
      datos[c.nombre] = v;
    }
    try {
      if (idEditando === null) {
        if (alCrear) await alCrear(datos);
        else await crearSolicitud(datos);
        mostrar('Registro creado correctamente (campo "creado" asignado por la base de datos)', 'exito');
      } else {
        await actualizarSolicitud(idEditando, datos);
        mostrar('Registro actualizado correctamente (campo "actualizado" modificado)', 'exito');
      }
      limpiarFormulario();
      await cargarOpciones();
      await cargarSolicitudes();
    } catch (error) {
      mostrar('No se pudo guardar: ' + error.message, 'error');
    }
  }

  async function borrarSolicitud(fila) {
    const nombre = campoNombre ? fila[campoNombre] : columnasTabla[0]?.valor(fila);
    const seguro = confirm('¿Eliminar a ' + nombre + '? (se cambiará su estado a inactivo)');
    if (!seguro) {
      return;
    }
    try {
      const respuesta = await eliminarSolicitud(fila[pk]);
      mostrar(respuesta.mensaje || 'Registro eliminado', 'exito');
      if (idEditando === fila[pk]) {
        limpiarFormulario();
      }
      await cargarSolicitudes();
    } catch (error) {
      mostrar('No se pudo eliminar: ' + error.message, 'error');
    }
  }

  async function ejecutarExtra(accion, fila) {
    try {
      const texto = await accion.ejecutar(fila);
      mostrar(texto || 'Operación realizada', 'exito');
      await cargarOpciones();
      await cargarSolicitudes();
    } catch (error) {
      mostrar('No se pudo completar: ' + error.message, 'error');
    }
  }
</script>

<Header {titulo} {subtitulo} />

{#if (permiso.crear && permitirCrear) || idEditando !== null}
  <Card>
    <h2>{idEditando === null ? 'Registrar ' + nombreSingular : 'Editar ' + nombreSingular}</h2>
    <form on:submit={guardarSolicitud}>
      {#each campos as campo (campo.nombre)}
        {#if !(idEditando === null && campo.soloEditar) && !(idEditando !== null && campo.soloCrear)}
          <CampoFormulario
            etiqueta={campo.etiqueta}
            nombre={campo.nombre}
            tipo={campo.fuente ? 'select' : campo.tipo}
            opciones={campo.fuente ? opciones[campo.fuente] || [] : campo.opciones || []}
            requerido={campo.requerido && !(campo.tipo === 'clave' && idEditando !== null)}
            ayuda={campo.ayuda || ''}
            bind:valor={formulario[campo.nombre]}
          />
        {/if}
      {/each}
      <div class="botones">
        <Boton tipo="submit">{idEditando === null ? 'Registrar' : 'Guardar cambios'}</Boton>
        {#if idEditando !== null}
          <Boton variante="gris" on:click={limpiarFormulario}>Cancelar</Boton>
        {/if}
      </div>
    </form>
  </Card>
{/if}

<Alerta mensaje={mensaje} tipo={tipoMensaje} />

<Card>
  <h2>Lista de {titulo.toLowerCase()}</h2>
  {#if cargando && filas.length === 0}
    <Cargando />
  {:else if filas.length === 0}
    <p>No hay registros.</p>
  {:else}
    <DataTable {filas} columnas={columnasTabla} clave={pk}>
      <svelte:fragment slot="acciones" let:fila>
        {#each accionesExtra as accion}
          {#if !accion.visible || accion.visible(fila, $sesion)}
            <Boton variante={accion.variante || 'exito'} on:click={() => ejecutarExtra(accion, fila)}>{accion.texto}</Boton>
          {/if}
        {/each}
        {#if permiso.actualizar}
          <Boton variante="editar" on:click={() => prepararEdicion(fila[pk])}>Editar</Boton>
        {/if}
        {#if permiso.eliminar}
          <Boton variante="borrar" on:click={() => borrarSolicitud(fila)}>Eliminar</Boton>
        {/if}
      </svelte:fragment>
    </DataTable>
  {/if}
</Card>

<style>
  h2 {
    margin-top: 0;
    color: #1e3a8a;
  }
  .botones {
    display: flex;
    gap: 10px;
  }
</style>
