# Guía de despliegue (paso a paso)

> Requisitos: cuenta de **GitHub**, cuenta en **Render** (https://render.com) y, para MySQL, cuenta en **Railway** (https://railway.app) o **Aiven** (https://aiven.io). Todas tienen plan gratuito.

## 0. Subir el proyecto a GitHub
```bash
cd prestamos-estudiantes
git init && git add . && git commit -m "Parcial I - préstamos entre estudiantes"
# Cree un repositorio vacío en github.com y luego:
git remote add origin https://github.com/SU_USUARIO/prestamos-estudiantes.git
git branch -M main && git push -u origin main
```

## 1. API FastAPI + PostgreSQL en Render (Blueprint, casi un clic)
1. En Render: **New > Blueprint** y seleccione el repositorio. Render lee `render.yaml` de la raíz.
2. Render crea: la BD **prestamos-db** (PostgreSQL free) y el servicio **api-prestamos-fastapi**. `DATABASE_URL` y `SECRET_KEY` se configuran solas.
3. Al arrancar, `python -m app.db.inicializar` crea las 17 tablas, triggers y datos semilla **solo si la BD está vacía**.
4. Abra `https://api-prestamos-fastapi.onrender.com/docs` (la URL exacta aparece en el panel).
5. Copie el valor de `SECRET_KEY` (pestaña *Environment* del servicio FastAPI); lo necesitará para Express.

> Plan free: el servicio "se duerme" tras 15 min sin uso (la primera petición tarda ~1 min) y la BD free de Render expira a los 30 días.

**Alternativa manual en Render:** New > PostgreSQL (free) → copie la *Internal Database URL*. New > Web Service → repo, *Root Directory* `api-fastapi`, Build `pip install -r requirements.txt`, Start `python -m app.db.inicializar && uvicorn app.main:app --host 0.0.0.0 --port $PORT`, variables `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION=3.12.7`.

## 2. Base MySQL gratuita
**Railway:** New Project > Database > **MySQL**. En la pestaña *Variables* copie `MYSQL_PUBLIC_URL` (formato `mysql://root:clave@host:puerto/railway`).

**Aiven (alternativa):** Create service > MySQL > plan Free. Copie la *Service URI* y use `DB_SSL=true`.

## 3. API Express en Render
El Blueprint ya creó **api-prestamos-express**. En *Environment* complete:
- `MYSQL_URL` = la URL del paso 2
- `SECRET_KEY` = el mismo valor de la API FastAPI (así Express acepta los tokens emitidos por FastAPI)
- `DB_SSL` = `true` si usa Aiven

Haga *Manual Deploy*. `npm start` ejecuta `src/inicializar.js` (crea tablas y semilla si la BD está vacía) y levanta el servidor. Pruebe `https://api-prestamos-express.onrender.com/salud`.

## Alternativa: todo en Railway
1. New Project > **Deploy from GitHub repo** (dos veces, una por API) y en *Settings > Root Directory* ponga `api-fastapi` o `api-express`. Railway detecta el `Dockerfile`.
2. Agregue al proyecto **PostgreSQL** y **MySQL** (New > Database).
3. Variables: FastAPI → `DATABASE_URL=${{Postgres.DATABASE_URL}}`, `SECRET_KEY=...`. Express → `MYSQL_URL=${{MySQL.MYSQL_URL}}`, `SECRET_KEY` (la misma).
4. *Settings > Networking > Generate Domain* para obtener la URL pública.

## Cargar la BD manualmente (opcional)
```bash
psql "URL_POSTGRES" -f api-fastapi/sql/schema.sql -f api-fastapi/sql/seed.sql
mysql -h HOST -P PUERTO -u USUARIO -p BASE < api-express/sql/schema.sql
mysql -h HOST -P PUERTO -u USUARIO -p BASE < api-express/sql/seed.sql
```
> `schema.sql` de PostgreSQL **borra y recrea** el esquema `public`; úselo solo en una BD dedicada al proyecto.

## Taller 1 Corte 2: frontend y nueva semilla
1. Render: abra el Blueprint del repositorio y haga clic en **Sync**. Se crea el sitio estático `prestamos-frontend-svelte`, y las APIs se vuelven a desplegar con el último commit.
2. Al arrancar, las APIs detectan la semilla anterior y recrean el esquema con la semilla del Taller 1:
   - FastAPI revisa si existe el rol `coordinador`.
   - Express revisa si existe el punto `PE-POS`.
   - Si quiere forzar la recarga, ponga `FORZAR_SEMILLA=true`, despliegue y luego vuelva a `false`.
3. También puede recargar a mano:
   ```bash
   PG_URL_REMOTA=... MYSQL_URL_REMOTA=... python herramientas/recargar_remoto.py
   ```
4. Variables del sitio estático:
   - `VITE_API_URL=https://api-prestamos-fastapi.onrender.com`
   - `VITE_API_AUX_URL=https://api-prestamos-express.onrender.com`
   - Regla de reescritura `/*` → `/index.html`.
