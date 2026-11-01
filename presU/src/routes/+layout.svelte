<script>
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import favicon from '$lib/assets/favicon.png';
  import { page } from '$app/stores';
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import Card from '$lib/components/Card.svelte';
  import Alerta from '$lib/components/Alerta.svelte';
  import { sesion } from '$lib/index.js';

  // Protección de rutas: sin sesión -> /login. Con sesión, solo los módulos de moduloxrol.
  $: ruta = $page.url.pathname;
  $: if (browser && !$sesion && ruta !== '/login') goto('/login');
  $: permitido = ruta === '/' || ruta === '/login' || ($sesion?.modulos || []).some((m) => m.ruta === ruta);
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<div class="contenedor-app">
  <Navbar />
  <main class="contenido">
    {#if ruta === '/login' || ($sesion && permitido)}
      <slot />
    {:else if $sesion}
      <Card><Alerta tipo="error" mensaje="Su rol no tiene acceso a este módulo (según la tabla moduloxrol)." /></Card>
    {/if}
  </main>
  <Footer />
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background-color: #f9fafb;
    color: #1f2937;
  }
  .contenedor-app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  .contenido {
    flex: 1;
    width: 90%;
    max-width: 1200px;
    margin: 24px auto;
  }
</style>
