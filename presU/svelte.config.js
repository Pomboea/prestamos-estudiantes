// adapter-static: genera un sitio estático (carpeta build/) que se puede publicar en la nube
// (Render Static Site, Netlify, Vercel). fallback permite que todas las rutas carguen la SPA.
import adapter from '@sveltejs/adapter-static';

const config = {
  kit: {
    adapter: adapter({ fallback: 'index.html' })
  }
};

export default config;
