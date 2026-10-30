<script>
  // Tabla con la librería DataTables (búsqueda, orden, paginación) - requisito del taller.
  // columnas: [{ etiqueta, valor: (fila) => texto }]. Las acciones llegan por el slot "acciones".
  import { onMount, tick, beforeUpdate, afterUpdate } from 'svelte';
  import 'datatables.net-dt/css/dataTables.dataTables.css';

  export let filas = [];
  export let columnas = [];
  export let clave = 'id';
  export let conAcciones = true;

  let tablaHtml;
  let instancia = null;
  let DataTable = null;
  let version = 0;
  let filasPrevias = null;

  async function iniciar() {
    if (!DataTable || !tablaHtml) return;
    if (instancia) {
      instancia.destroy();
      instancia = null;
    }
    instancia = new DataTable(tablaHtml, {
      pageLength: 10,
      order: [],
      language: {
        search: 'Buscar:',
        lengthMenu: 'Mostrar _MENU_ registros',
        info: 'Mostrando _START_ a _END_ de _TOTAL_ registros',
        infoEmpty: 'Sin registros',
        infoFiltered: '(filtrado de _MAX_)',
        zeroRecords: 'No se encontraron coincidencias',
        emptyTable: 'No hay registros',
        paginate: { first: 'Primero', last: 'Último', next: 'Siguiente', previous: 'Anterior' }
      }
    });
  }

  onMount(async () => {
    DataTable = (await import('datatables.net-dt')).default;
    await iniciar();
  });

  // Antes de redibujar con filas nuevas se destruye DataTables; después se vuelve a aplicar
  let pendiente = false;
  beforeUpdate(() => {
    if (filas !== filasPrevias) {
      filasPrevias = filas;
      if (instancia) {
        instancia.destroy();
        instancia = null;
        version += 1;
      }
      pendiente = true;
    }
  });
  afterUpdate(async () => {
    if (pendiente && DataTable) {
      pendiente = false;
      await tick();
      await iniciar();
    }
  });
</script>

{#key version}
  <table bind:this={tablaHtml} class="display compact" style="width:100%">
    <thead>
      <tr>
        {#each columnas as columna}
          <th>{columna.etiqueta}</th>
        {/each}
        {#if conAcciones}<th>Acciones</th>{/if}
      </tr>
    </thead>
    <tbody>
      {#each filas as fila (fila[clave])}
        <tr>
          {#each columnas as columna}
            <td>{columna.valor(fila)}</td>
          {/each}
          {#if conAcciones}
            <td class="acciones"><slot name="acciones" {fila} /></td>
          {/if}
        </tr>
      {/each}
    </tbody>
  </table>
{/key}

<style>
  .acciones {
    white-space: nowrap;
  }
  :global(table.dataTable thead th) {
    background-color: #f3f4f6;
  }
</style>
