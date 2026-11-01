<script>
  // Barra de navegación. Los enlaces salen de la tabla moduloxrol (sesión del usuario).
  import { sesion } from '$lib/index.js';
  import { cerrarSesion } from '$lib/services/api_usuario.js';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import Insignia from './Insignia.svelte';

  let abierto = false;

  function salir() {
    cerrarSesion();
    goto('/login');
  }
</script>

<nav class="navbar">
  <div class="fila">
    <a class="navbar-logo" href="/">📦 PrestaU</a>
    {#if $sesion}
      <button class="hamburguesa" on:click={() => (abierto = !abierto)} aria-label="Abrir menú">☰</button>
    {/if}
  </div>
  {#if $sesion}
    <div class="navbar-links" class:abierto>
      <a href="/" class:activo={$page.url.pathname === '/'} on:click={() => (abierto = false)}>Inicio</a>
      {#each $sesion.modulos as modulo (modulo.nombre)}
        <a href={modulo.ruta} class:activo={$page.url.pathname === modulo.ruta} on:click={() => (abierto = false)}>
          {modulo.descripcion.replace(' (API Express)', '')}
        </a>
      {/each}
      <span class="usuario">{$sesion.usuario} <Insignia texto={$sesion.rol} /></span>
      <button class="salir" on:click={salir}>Salir</button>
    </div>
  {/if}
</nav>

<style>
  .navbar {
    background-color: #1e3a8a;
    color: white;
    padding: 12px 24px;
  }
  .fila {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .navbar-logo {
    font-weight: bold;
    font-size: 1.3rem;
    color: white;
    text-decoration: none;
  }
  .navbar-links {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 14px;
    margin-top: 10px;
    align-items: center;
  }
  .navbar-links a {
    color: #dbeafe;
    text-decoration: none;
    font-size: 0.92rem;
    padding: 4px 8px;
    border-radius: 6px;
  }
  .navbar-links a:hover,
  .navbar-links a.activo {
    background-color: #1d4ed8;
    color: white;
  }
  .usuario {
    margin-left: auto;
    font-size: 0.9rem;
  }
  .salir {
    background: #f59e0b;
    border: none;
    color: #1f2937;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
  }
  .hamburguesa {
    display: none;
    background: none;
    border: 1px solid white;
    color: white;
    font-size: 1.2rem;
    border-radius: 6px;
    cursor: pointer;
  }
  @media (max-width: 760px) {
    .hamburguesa {
      display: block;
    }
    .navbar-links {
      display: none;
      flex-direction: column;
      align-items: flex-start;
    }
    .navbar-links.abierto {
      display: flex;
    }
    .usuario {
      margin-left: 0;
    }
  }
</style>
