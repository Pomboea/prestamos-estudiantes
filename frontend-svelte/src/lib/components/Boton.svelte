<script>
  // Botón reutilizable. variante: primario | gris | editar | borrar | exito
  export let variante = 'primario';
  export let tipo = 'button';
  export let deshabilitado = false;
</script>

<button type={tipo} class="btn btn-{variante}" disabled={deshabilitado} on:click>
  <slot />
</button>

<style>
  .btn {
    padding: 8px 14px;
    border: none;
    border-radius: 6px;
    color: white;
    font-size: 0.9rem;
    cursor: pointer;
    margin: 2px;
  }
  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  .btn-primario { background-color: #1e3a8a; }
  .btn-primario:hover { background-color: #1d4ed8; }
  .btn-gris { background-color: #6b7280; }
  .btn-gris:hover { background-color: #4b5563; }
  .btn-editar { background-color: #f59e0b; }
  .btn-editar:hover { background-color: #d97706; }
  .btn-borrar { background-color: #dc2626; }
  .btn-borrar:hover { background-color: #b91c1c; }
  .btn-exito { background-color: #16a34a; }
  .btn-exito:hover { background-color: #15803d; }
</style>
