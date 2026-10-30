<script>
  // Etiqueta pequeña de color (rol, estado, disponibilidad)
  export let texto = '';
  export let color = '#f59e0b';
</script>

<span class="insignia" style="background-color: {color}">{texto}</span>

<style>
  .insignia {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    color: #1f2937;
    font-size: 0.78rem;
    font-weight: bold;
  }
</style>
