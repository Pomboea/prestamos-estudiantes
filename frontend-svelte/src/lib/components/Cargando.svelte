<script>
  export let texto = 'Cargando...';
</script>

<div class="cargando"><span class="rueda"></span> {texto}</div>

<style>
  .cargando {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #1e3a8a;
    padding: 12px;
  }
  .rueda {
    width: 18px;
    height: 18px;
    border: 3px solid #dbeafe;
    border-top-color: #1e3a8a;
    border-radius: 50%;
    animation: girar 0.8s linear infinite;
  }
  @keyframes girar {
    to { transform: rotate(360deg); }
  }
</style>
