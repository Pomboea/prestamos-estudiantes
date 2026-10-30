<script>
  import { goto } from '$app/navigation';
  import Header from '$lib/components/Header.svelte';
  import Card from '$lib/components/Card.svelte';
  import CampoFormulario from '$lib/components/CampoFormulario.svelte';
  import Boton from '$lib/components/Boton.svelte';
  import Alerta from '$lib/components/Alerta.svelte';
  import { iniciarSesion } from '$lib/services/api_auth.js';

  let correo = '';
  let contrasena = '';
  let mensaje = '';
  let enviando = false;

  async function entrar(evento) {
    evento.preventDefault();
    enviando = true;
    mensaje = '';
    try {
      await iniciarSesion(correo, contrasena);
      goto('/');
    } catch (error) {
      mensaje = 'No se pudo iniciar sesión: ' + error.message;
    }
    enviando = false;
  }
</script>

<div class="caja">
  <Header titulo="Iniciar sesión" subtitulo="Autenticación con JWT según su rol" />
  <Card>
    <form on:submit={entrar}>
      <CampoFormulario etiqueta="Correo institucional" nombre="correo" tipo="correo" requerido bind:valor={correo} />
      <CampoFormulario etiqueta="Contraseña" nombre="contrasena" tipo="clave" requerido bind:valor={contrasena} />
      <Boton tipo="submit" deshabilitado={enviando}>{enviando ? 'Ingresando...' : 'Ingresar'}</Boton>
    </form>
    <Alerta tipo="error" {mensaje} />
  </Card>
</div>

<style>
  .caja {
    max-width: 420px;
    margin: 40px auto;
  }
</style>
