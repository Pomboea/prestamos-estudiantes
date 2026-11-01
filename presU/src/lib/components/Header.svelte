<script>
  export let titulo = 'Título';
  export let subtitulo = '';
</script>

<header class="encabezado">
  <h1>{titulo}</h1>
  {#if subtitulo}
    <p>{subtitulo}</p>
  {/if}
</header>

<style>
  .encabezado {
    text-align: center;
    margin-bottom: 24px;
  }
  .encabezado h1 {
    margin: 0;
    color: #1e3a8a;
  }
  .encabezado p {
    margin: 6px 0 0 0;
    color: #555;
  }
</style>
