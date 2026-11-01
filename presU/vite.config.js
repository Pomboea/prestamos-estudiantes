import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      // API auxiliar Express: /api-aux/... se reenvía a http://localhost:3000/api/...
      '/api-aux': {
        target: 'http://localhost:3000',
        rewrite: (ruta) => ruta.replace(/^\/api-aux/, '/api')
      },
      // API principal FastAPI (igual que en el documento CRUD). Va después de /api-aux
      // porque vite compara por prefijo y '/api' también coincidiría con '/api-aux'.
      '/api': 'http://localhost:8000'
    }
  }
});
