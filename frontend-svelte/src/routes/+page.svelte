<script>
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import Insignia from '$lib/components/Insignia.svelte';
  import { sesion } from '$lib/services/api_auth.js';
</script>

{#if $sesion}
  <Header titulo="Bienvenido(a), {$sesion.usuario}" subtitulo="Sistema web para gestionar préstamos de objetos entre estudiantes" />
  <Card>
    <p>Rol: <Insignia texto={$sesion.rol} />. Estos son los módulos que su rol tiene habilitados en la base de datos (tabla <b>moduloxrol</b>):</p>
    <div class="grilla">
      {#each $sesion.modulos as modulo (modulo.nombre)}
        <a class="modulo" href={modulo.ruta}>
          <strong>{modulo.descripcion}</strong>
          <small>
            {modulo.crear ? 'Crear · ' : ''}Consultar{modulo.actualizar ? ' · Editar' : ''}{modulo.eliminar ? ' · Eliminar' : ''}
          </small>
        </a>
      {/each}
    </div>
  </Card>
{/if}

<style>
  .grilla {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 14px;
  }
  .modulo {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #dbeafe;
    background: #eff6ff;
    color: #1e3a8a;
    text-decoration: none;
  }
  .modulo:hover {
    background: #dbeafe;
  }
  small {
    color: #555;
  }
</style>
