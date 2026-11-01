<script>
  // Módulo CRUD reutilizable con la estructura del documento CRUD (Partes 5 a 9):
  // Card con formulario (crear/editar con idEditando) + mensaje + Card con la lista (DataTable).
  // Permisos desde moduloxrol.
  // Cada página (routes/<modulo>/+page.svelte) lo configura con su servicio, campos y columnas.
  import { onMount } from 'svelte';
  import { sesion } from '$lib/services/api_auth.js';
  import Card from './Card.svelte';
  import Header from './Header.svelte';
  import Boton from './Boton.svelte';
  import Alerta from './Alerta.svelte';
  import Cargando from './Cargando.svelte';
  import CampoFormulario from './CampoFormulario.svelte';
  import DataTable from './DataTable.svelte';

  export let titulo = '';
  export let subtitulo = '';
  export let modulo = '';             // nombre del módulo en la tabla "modulo"
  export let pk = 'id';               // llave primaria (se usa por dentro, NUNCA se muestra)
  export let servicio;                // { listar, obtener, crear, actualizar, eliminar }
  export let campos = [];             // [{ nombre, etiqueta, tipo, fuente?, requerido?, soloCrear?, soloEditar? }]
  export let columnas = [];           // [{ etiqueta, campo?, fuente?, valor?(fila, ref) }]
  export let fuentes = {};            // { clave: async () => [{ valor, etiqueta }] }  (para FK -> nombres)
  export let permitirCrear = true;
  export let accionesExtra = [];      // [{ texto, variante, visible(fila, sesion), ejecutar(fila) }]
  export let filtro = null;           // (fila, sesion) => boolean
  export let alCrear = null;          // función propia para crear (por ejemplo, flujo de solicitud)
  export let nombreSingular = 'registro'; // para los títulos: 'Registrar categoría' / 'Editar categoría'
  export let campoNombre = null;      // campo que se muestra en el confirm() de eliminar

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

  async function cargarRegistros() {
    cargando = true;
    try {
      const datos = await servicio.listar();
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
    await cargarRegistros();
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
      const registro = await servicio.obtener(id);
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

  async function guardarRegistro(evento) {
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
        else await servicio.crear(datos);
        mostrar('Registro creado correctamente (campo "creado" asignado por la base de datos)', 'exito');
      } else {
        await servicio.actualizar(idEditando, datos);
        mostrar('Registro actualizado correctamente (campo "actualizado" modificado)', 'exito');
      }
      limpiarFormulario();
      await cargarOpciones();
      await cargarRegistros();
    } catch (error) {
      mostrar('No se pudo guardar: ' + error.message, 'error');
    }
  }

  async function borrarRegistro(fila) {
    const nombre = campoNombre ? fila[campoNombre] : columnasTabla[0]?.valor(fila);
    const seguro = confirm('¿Eliminar a ' + nombre + '? (se cambiará su estado a inactivo)');
    if (!seguro) {
      return;
    }
    try {
      const respuesta = await servicio.eliminar(fila[pk]);
      mostrar(respuesta.mensaje || 'Registro eliminado', 'exito');
      if (idEditando === fila[pk]) {
        limpiarFormulario();
      }
      await cargarRegistros();
    } catch (error) {
      mostrar('No se pudo eliminar: ' + error.message, 'error');
    }
  }

  async function ejecutarExtra(accion, fila) {
    try {
      const texto = await accion.ejecutar(fila);
      mostrar(texto || 'Operación realizada', 'exito');
      await cargarOpciones();
      await cargarRegistros();
    } catch (error) {
      mostrar('No se pudo completar: ' + error.message, 'error');
    }
  }
</script>

<Header {titulo} {subtitulo} />

{#if (permiso.crear && permitirCrear) || idEditando !== null}
  <Card>
    <h2>{idEditando === null ? 'Registrar ' + nombreSingular : 'Editar ' + nombreSingular}</h2>
    <form on:submit={guardarRegistro}>
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
          <Boton variante="borrar" on:click={() => borrarRegistro(fila)}>Eliminar</Boton>
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
