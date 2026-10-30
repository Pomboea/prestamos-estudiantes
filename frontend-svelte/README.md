# frontend-svelte (Taller 1 Corte 2)

Proyecto creado con `npx sv create frontend-svelte` (plantilla **minimal**, **JavaScript**).
Sigue la estructura del documento "CRUD SvelteKit + FastAPI". Para ejecutarlo:

```bash
npm install
npm run dev
```

La app queda en http://localhost:5173. `vite.config.js` reenvía las rutas así:
- `/api` va a FastAPI (puerto 8000).
- `/api-aux` va a Express (puerto 3000).

Para la versión en la nube:

```bash
npm run build
```

Ese comando genera la carpeta `build/`. Antes de ejecutarlo, defina `VITE_API_URL` y `VITE_API_AUX_URL` (vea `.env.example`).
