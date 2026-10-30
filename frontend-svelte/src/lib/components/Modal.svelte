<script>
  // Ventana emergente reutilizable (formularios de crear / editar)
  import { createEventDispatcher } from 'svelte';
  export let titulo = '';
  export let abierto = false;
  const despachar = createEventDispatcher();
</script>

{#if abierto}
  <div class="fondo" on:click|self={() => despachar('cerrar')} role="presentation">
    <div class="ventana" role="dialog" aria-modal="true">
      <div class="cabecera">
        <h2>{titulo}</h2>
        <button class="x" on:click={() => despachar('cerrar')} aria-label="Cerrar">✕</button>
      </div>
      <slot />
    </div>
  </div>
{/if}

<style>
  .fondo {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 50;
    padding: 12px;
  }
  .ventana {
    background: white;
    border-radius: 10px;
    padding: 20px;
    width: 100%;
    max-width: 560px;
    max-height: 90vh;
    overflow-y: auto;
  }
  .cabecera {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  h2 {
    margin: 0 0 12px 0;
    color: #1e3a8a;
  }
  .x {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
  }
</style>
