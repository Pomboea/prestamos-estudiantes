<script>
  // Mensaje para el usuario. tipo: info | exito | error
  export let mensaje = '';
  export let tipo = 'info';
</script>

{#if mensaje}
  <p class="alerta {tipo}">{mensaje}</p>
{/if}

<style>
  .alerta {
    margin: 12px 0;
    padding: 10px 14px;
    border-radius: 6px;
  }
  .info { background-color: #dbeafe; color: #1e3a8a; }
  .exito { background-color: #dcfce7; color: #166534; }
  .error { background-color: #fee2e2; color: #991b1b; }
</style>
