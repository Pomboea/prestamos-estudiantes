<script>
  // Campo de formulario reutilizable. tipo: texto | numero | fecha | hora | correo | clave | area | bool | select
  // En los select el usuario ve NOMBRES; el ID viaja oculto como valor (nunca se escribe un ID a mano).
  export let etiqueta = '';
  export let nombre = '';
  export let tipo = 'texto';
  export let valor = '';
  export let opciones = [];
  export let requerido = false;
  export let ayuda = '';
</script>

<div class="campo">
  {#if tipo === 'bool'}
    <label class="check"><input id={nombre} type="checkbox" bind:checked={valor} /> {etiqueta}</label>
  {:else}
    <label for={nombre}>{etiqueta}{requerido ? ' *' : ''}</label>
    {#if tipo === 'select'}
      <select id={nombre} bind:value={valor} required={requerido}>
        <option value={null}>-- Seleccione --</option>
        {#each opciones as opcion (opcion.valor)}
          <option value={opcion.valor}>{opcion.etiqueta}</option>
        {/each}
      </select>
    {:else if tipo === 'area'}
      <textarea id={nombre} rows="3" bind:value={valor} required={requerido}></textarea>
    {:else if tipo === 'numero'}
      <input id={nombre} type="number" bind:value={valor} required={requerido} />
    {:else if tipo === 'fecha'}
      <input id={nombre} type="date" bind:value={valor} required={requerido} />
    {:else if tipo === 'hora'}
      <input id={nombre} type="time" bind:value={valor} required={requerido} />
    {:else if tipo === 'correo'}
      <input id={nombre} type="email" bind:value={valor} required={requerido} />
    {:else if tipo === 'clave'}
      <input id={nombre} type="password" bind:value={valor} required={requerido} autocomplete="new-password" />
    {:else}
      <input id={nombre} type="text" bind:value={valor} required={requerido} />
    {/if}
  {/if}
  {#if ayuda}<small>{ayuda}</small>{/if}
</div>

<style>
  .campo {
    display: flex;
    flex-direction: column;
    margin-bottom: 12px;
  }
  label {
    font-weight: bold;
    margin-bottom: 6px;
  }
  .check {
    font-weight: normal;
  }
  input,
  select,
  textarea {
    padding: 9px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
  }
  input:focus,
  select:focus,
  textarea:focus {
    outline: none;
    border-color: #1e3a8a;
  }
  small {
    color: #6b7280;
    margin-top: 4px;
  }
</style>
