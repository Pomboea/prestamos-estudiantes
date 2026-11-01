# Sistema web de préstamos de objetos entre estudiantes universitarios — Parcial I

Proyecto con **dos APIs y dos bases de datos**:

| Componente | Tecnología | Carpeta | Puerto local |
|---|---|---|---|
| BD principal (17 tablas) + API principal con JWT | PostgreSQL + FastAPI | `api-fastapi/` | 8000 |
| BD auxiliar (4 tablas) + API auxiliar | MySQL + Express (Node.js) | `api-express/` | 3000 |

La API Express **acepta el mismo token JWT** que emite FastAPI (comparten `SECRET_KEY`).

## Estructura
```
prestamos-estudiantes/
├── RESUMEN.md / Resumen_propuesta.docx   # Punto 0: resumen de la propuesta
├── GUIA_EXPOSICION.md                    # Qué mostrar en la exposición
├── render.yaml                           # Blueprint de despliegue en Render
├── docs/  (DESPLIEGUE.md, diagramas ER .mmd y .png)
├── api-fastapi/
│   ├── app/ core/(config, security) db/(session, inicializar) models/ schemas/ routers/(auth, crud, recursos, flujo) main.py
│   ├── sql/ schema.sql  seed.sql  verificar.sql
│   ├── tests/ (pytest)   requests.http   Dockerfile   docker-compose.yml   .env.example
└── api-express/
    ├── src/ app.js server.js db.js inicializar.js middleware/auth.js routes/(crud.js, index.js)
    ├── sql/ schema.sql  seed.sql  verificar.sql
    ├── tests/ (node:test + supertest)   requests.http   Dockerfile   docker-compose.yml   .env.example
```

## Requisitos del parcial en TODAS las tablas
| Requisito | PostgreSQL | MySQL |
|---|---|---|
| Llave primaria | `SERIAL PRIMARY KEY` | `INT AUTO_INCREMENT PRIMARY KEY` |
| Campos únicos | `UNIQUE` (nombre, correo, código, …) | `UNIQUE` |
| `estado` | `BOOLEAN DEFAULT TRUE` | `BOOLEAN DEFAULT 1` |
| `creado` | `DEFAULT CURRENT_TIMESTAMP` + trigger que impide cambiarlo | `DEFAULT CURRENT_TIMESTAMP` + trigger |
| `actualizado` | trigger `BEFORE UPDATE` (`fn_auditoria_actualizado`) | `ON UPDATE CURRENT_TIMESTAMP` |

- **DELETE** nunca borra físicamente: hace `estado = false`.
- **GET** lista solo `estado = true` (el admin puede usar `?incluir_inactivos=true`); un `PUT` con `{"estado": true}` reactiva.
- El cliente **nunca envía** `creado`/`actualizado`.
- Verificación: `api-fastapi/sql/verificar.sql` y `api-express/sql/verificar.sql`.

## Usuarios de prueba (API FastAPI)
| Rol | Correo | Contraseña |
|---|---|---|
| admin | admin@uni.edu.co | Admin123* |
| estudiante | ana@uni.edu.co | Estudiante123* |
| estudiante | carlos@uni.edu.co | Estudiante123* |

## Ejecución local SIN Docker (Windows)
### 1. API FastAPI + PostgreSQL
```powershell
cd api-fastapi
# Crear la base (use su usuario/clave de PostgreSQL)
psql -U postgres -c "CREATE DATABASE prestamos"
psql -U postgres -d prestamos -f sql/schema.sql
psql -U postgres -d prestamos -f sql/seed.sql
# Entorno Python 3.12
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
copy .env.example .env      # edite DATABASE_URL, p. ej. postgresql+psycopg2://postgres:SU_CLAVE@localhost:5432/prestamos
uvicorn app.main:app --reload
```
Swagger: http://localhost:8000/docs → botón **Authorize** (username = correo, password = contraseña).

### 2. API Express + MySQL
```powershell
cd api-express
mysql -u root -p -e "CREATE DATABASE prestamos_aux CHARACTER SET utf8mb4"
mysql -u root -p prestamos_aux < sql/schema.sql
mysql -u root -p prestamos_aux < sql/seed.sql
npm install
copy .env.example .env      # edite DB_USER, DB_PASSWORD y la MISMA SECRET_KEY de FastAPI
npm run dev
```
> Sin MySQL instalado puede usar XAMPP/MariaDB o Docker (abajo).

### Pruebas automáticas
```powershell
# FastAPI (usa la BD prestamos_test; créela antes: psql -U postgres -c "CREATE DATABASE prestamos_test")
set DATABASE_URL=postgresql+psycopg2://postgres:SU_CLAVE@localhost:5432/prestamos_test
pytest -v
# Express (usa la BD prestamos_aux_test; créela antes)
npm test
```

## Ejecución local CON Docker
```bash
cd api-fastapi && docker compose up --build    # API en :8000, PostgreSQL en :5433
cd api-express && docker compose up --build    # API en :3000, MySQL en :3307
```
Las tablas y datos semilla se crean solos al arrancar si la BD está vacía.

## Despliegue
Ver [docs/DESPLIEGUE.md](docs/DESPLIEGUE.md) (Render Blueprint con `render.yaml`, alternativa Railway; MySQL en Railway/Aiven).

## Endpoints — API FastAPI (101 operaciones, ver /docs)
**Autenticación:** `POST /auth/registro`, `POST /auth/login` (formulario OAuth2), `POST /auth/login-json`, `GET /auth/yo`

**CRUD (17 tablas)** — cada recurso tiene `GET /recurso`, `GET /recurso/{id}`, `POST /recurso`, `PUT /recurso/{id}`, `DELETE /recurso/{id}` (lógico):
`/roles`, `/modulos`, `/moduloxrol`, `/usuarios`, `/facultades`, `/programas`, `/categorias`, `/condiciones`, `/objetos`, `/imagenes`, `/estados-solicitud`, `/solicitudes`, `/prestamos`, `/devoluciones`, `/calificaciones`, `/notificaciones`, `/sanciones`

**Flujo de negocio:**
| Método | Ruta | Descripción |
|---|---|---|
| GET | /flujo/objetos-disponibles | Objetos activos y disponibles (`?id_categoria=`) |
| POST | /flujo/publicar-objeto | Publicar objeto propio |
| POST | /flujo/solicitar | Solicitar préstamo (valida disponibilidad, que no sea propio, sanciones) |
| POST | /flujo/solicitudes/{id}/decision | Propietario aprueba/rechaza `{"aprobar": true}` |
| POST | /flujo/solicitudes/{id}/prestar | Registra el préstamo → objeto **no disponible** |
| POST | /flujo/prestamos/{id}/devolver | Registra devolución y condición → objeto **disponible**; sanción si hay retraso |
| GET | /flujo/mis-prestamos | Préstamos como prestador o prestatario |
| GET | /flujo/mis-solicitudes · /flujo/solicitudes-recibidas · /flujo/mis-notificaciones | Consultas personales |

**Seguridad:** sin token o token inválido/expirado → **401**; rol sin permiso en `moduloxrol` → **403** (p. ej. un estudiante en `/roles`); un estudiante solo edita/elimina sus propios objetos (403 si no); duplicado en campo único → **409**; validación → **422**.

## Endpoints — API Express (`/api`)
| Recurso | GET (lista / id) | POST / PUT / DELETE |
|---|---|---|
| /api/puntos-entrega | público | token rol **admin** |
| /api/horarios | público | token rol **admin** |
| /api/tipos-incidencia | público | token rol **admin** |
| /api/reportes-incidencia | token | token (el estudiante solo modifica sus reportes) |

Además: `GET /salud`. Errores: 401, 403, 404, 409 (duplicado/FK), 422 (validación con express-validator).

## Diagrama ER — PostgreSQL (principal)
![ER PostgreSQL](docs/er_postgres.png)

Todas las tablas además tienen `estado`, `creado` y `actualizado` (se omiten en algunas cajas por espacio). Tablas: rol, modulo, moduloxrol, usuario, facultad, programa_academico, categoria_objeto, condicion_objeto, objeto, imagen_objeto, estado_solicitud, solicitud_prestamo, prestamo, devolucion, calificacion, notificacion, sancion.

```mermaid
erDiagram
  rol ||--o{ usuario : tiene
  rol ||--o{ moduloxrol : permisos
  modulo ||--o{ moduloxrol : permisos
  facultad ||--o{ programa_academico : agrupa
  programa_academico ||--o{ usuario : cursa
  usuario ||--o{ objeto : publica
  categoria_objeto ||--o{ objeto : clasifica
  condicion_objeto ||--o{ objeto : condicion_actual
  objeto ||--o{ imagen_objeto : fotos
  objeto ||--o{ solicitud_prestamo : solicitado
  usuario ||--o{ solicitud_prestamo : solicita
  estado_solicitud ||--o{ solicitud_prestamo : estado
  solicitud_prestamo ||--o| prestamo : genera
  condicion_objeto ||--o{ prestamo : entrega
  prestamo ||--o| devolucion : cierra
  condicion_objeto ||--o{ devolucion : recibe
  prestamo ||--o{ calificacion : evalua
  usuario ||--o{ calificacion : evaluador_evaluado
  usuario ||--o{ notificacion : recibe
  usuario ||--o{ sancion : sancionado
  prestamo ||--o{ sancion : origina
  rol { int id_rol PK
        varchar nombre UK
        boolean estado
        timestamp creado
        timestamp actualizado }
  modulo { int id_modulo PK
        varchar nombre UK
        varchar ruta UK
        boolean estado }
  moduloxrol { int id_moduloxrol PK
        int id_rol FK
        int id_modulo FK
        boolean puede_leer
        boolean puede_crear
        boolean puede_actualizar
        boolean puede_eliminar
        boolean estado }
  usuario { int id_usuario PK
        varchar correo UK
        varchar codigo_estudiantil UK
        varchar contrasena_hash
        int id_rol FK
        int id_programa FK
        boolean estado }
  objeto { int id_objeto PK
        varchar codigo UK
        varchar nombre
        int id_categoria FK
        int id_condicion FK
        int id_propietario FK
        boolean disponible
        boolean estado }
  solicitud_prestamo { int id_solicitud PK
        varchar codigo UK
        int id_objeto FK
        int id_solicitante FK
        int id_estado_solicitud FK
        date fecha_inicio_deseada
        date fecha_fin_deseada }
  prestamo { int id_prestamo PK
        int id_solicitud FK,UK
        date fecha_devolucion_esperada
        int id_condicion_entrega FK }
  devolucion { int id_devolucion PK
        int id_prestamo FK,UK
        int id_condicion_devolucion FK }
```

## Diagrama ER — MySQL (auxiliar)
![ER MySQL](docs/er_mysql.png)

```mermaid
erDiagram
  punto_entrega ||--o{ horario_atencion : atiende
  punto_entrega ||--o{ reporte_incidencia : lugar
  tipo_incidencia ||--o{ reporte_incidencia : clasifica
  punto_entrega { int id_punto PK
        varchar codigo UK
        varchar nombre UK
        varchar ubicacion
        varchar sede
        boolean estado
        timestamp creado
        timestamp actualizado }
  horario_atencion { int id_horario PK
        int id_punto FK
        tinyint dia_semana "UK(id_punto,dia_semana)"
        time hora_apertura
        time hora_cierre
        boolean estado
        timestamp creado
        timestamp actualizado }
  tipo_incidencia { int id_tipo PK
        varchar nombre UK
        enum gravedad
        boolean estado
        timestamp creado
        timestamp actualizado }
  reporte_incidencia { int id_reporte PK
        varchar codigo UK
        int id_tipo FK
        int id_punto FK
        int id_prestamo "ref BD principal"
        int id_usuario_reporta "ref BD principal"
        boolean resuelto
        boolean estado
        timestamp creado
        timestamp actualizado }
```

---

# Taller 1 – Corte 2: Frontend SvelteKit + APIs

Esta versión adapta el proyecto a la estructura del documento **"CRUD SvelteKit + FastAPI"** y a los requisitos del Taller 1.
El documento completo está en `Taller1_Corte2_Documentacion.docx`.

## Cambios principales
- **APIs**: todas las rutas de FastAPI quedan en `/api/<recurso>/` (con barra final, como en el documento CRUD). Hay dos endpoints nuevos:
  - `GET /api/auth/mis-modulos`: devuelve el menú del rol desde `moduloxrol`.
  - `GET /api/auth/directorio`: devuelve nombres para mostrar en lugar de IDs.
- **Roles**: hay 3 roles, `admin`, `coordinador` y `estudiante`. Los permisos por módulo se leen de la base de datos.
- **Datos**: 20 registros en las tablas principales y 10 en las secundarias (generados con `herramientas/generar_seed.py`).
- **`frontend-svelte/`**: proyecto SvelteKit (`npx sv create`, plantilla minimal, JavaScript), con esta estructura:
  - `src/lib/components/`: 11 componentes reutilizables (Navbar, Footer, Header, Card, Boton, Alerta, Cargando, Insignia, CampoFormulario, DataTable, CrudModulo).
  - `src/lib/services/api_<recurso>.js`: funciones `obtenerX`, `obtenerXPorId`, `crearX`, `actualizarX`, `eliminarX` y `procesarRespuesta`.
  - `src/routes/+layout.svelte`: Navbar, `<slot />` y Footer, más la protección de rutas por rol.
  - `src/routes/<modulo>/+page.svelte`: una página por módulo, con DataTables, y un solo formulario para crear y editar (`idEditando`).
- **`access/`**: base de datos en Microsoft Access (`.accdb`) con relaciones. Ver `access/GUIA_ACCESS.md`.
- **`capturas/`**: capturas numeradas de cada paso.

## Ejecutar en local
```bash
# 1. Bases de datos: crear 'prestamos' (PostgreSQL) y 'prestamos_aux' (MySQL), luego:
python herramientas/cargar_bd.py          # ejecuta schema.sql + seed.sql en las dos (o use psql / mysql)
# 2. API FastAPI
cd api-fastapi && python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env && .venv/bin/uvicorn app.main:app --reload --port 8000
# 3. API Express
cd api-express && npm install && cp .env.example .env && npm run dev     # puerto 3000
# 4. Frontend
cd frontend-svelte && npm install && npm run dev                        # http://localhost:5173
```
Las dos APIs deben usar la **misma `SECRET_KEY`** en su `.env`.

## Usuarios de prueba
| Rol | Correo | Contraseña |
|---|---|---|
| admin | admin@uni.edu.co | Admin123* |
| coordinador | patricia.restrepo@uni.edu.co / hernan.villa@uni.edu.co | Coordinador123* |
| estudiante | ana@uni.edu.co, carlos@uni.edu.co (y 18 más) | Estudiante123* |

## Pruebas
- `api-fastapi`: `pytest`. Resultado: 16 pruebas aprobadas. Usa la base `prestamos_test`; defina `DATABASE_URL` si su usuario no es `prestamos`.
- `api-express`: `npm test`. Resultado: 7 pruebas aprobadas. Usa la base `prestamos_aux_test`; defina `DB_USER` y `DB_PASSWORD`.

## Nube
Para publicar el proyecto, siga estos pasos:
1. Despliegue las dos APIs como antes (ver `render.yaml` y `docs/DESPLIEGUE.md`).
2. Publique el frontend como sitio estático. El build usa `adapter-static`.
   - Comando de build: `npm install && npm run build`.
   - Carpeta a publicar: `build`.
   - Variables de entorno: `VITE_API_URL` (la URL de FastAPI) y `VITE_API_AUX_URL` (la URL de Express). Hay un ejemplo en `frontend-svelte/.env.example`.
   - Regla de reescritura: `/*` → `/index.html`.

## Taller 1 · Conformidad con el documento CRUD (SvelteKit + FastAPI)

| Punto del documento | Estado | Nota |
|---|---|---|
| `npx sv create`, plantilla minimal, JavaScript | Cumple | `jsconfig.json`, sin TypeScript |
| `vite.config.js` con proxy `'/api': 'http://localhost:8000'` | Cumple + extra | se añade `'/api-aux'` → Express (3000) antes de `/api` |
| `src/lib/components/` Navbar, Footer, Header, Card | Cumple | Header y Card idénticos al documento; Navbar dinámico (moduloxrol) |
| `src/lib/services/api_<recurso>.js` con `procesarRespuesta`, `obtenerX`, `obtenerXPorId`, `crearX`, `actualizarX`, `eliminarX` | Cumple con diferencia | `procesarRespuesta` y cabeceras JWT están en `api_base.js` (compartido) |
| `URL_BASE = '/api/<recurso>/'` con barra final | Cumple con diferencia | se antepone `API_PRINCIPAL` (vacío en local, URL de Render en la nube) |
| `+layout.svelte` con Navbar, `<slot />`, Footer | Cumple + extra | protección de rutas por sesión/rol |
| `+page.svelte` de inicio con Header y Card | Cumple | |
| `routes/<modulo>/+page.svelte` | Cumple | 21 módulos |
| Página: Header + Card con formulario (`idEditando`, "Registrar"/"Guardar cambios", "Cancelar"), mensaje, lista con Cargando / vacío / tabla, `confirm()` al eliminar, `onMount` | Cumple con diferencia | la lógica está en el componente reutilizable `CrudModulo` (requisito del taller: 10 componentes reutilizados) |
| Tabla HTML con `{#each}` | Cumple + DataTables | requisito del taller |
| Columna ID en la tabla | No se aplica a propósito | el taller prohíbe mostrar IDs |
| API: `/api/<recurso>/` GET/POST, `/api/<recurso>/{id}` GET/PUT/DELETE, DELETE devuelve `{mensaje}` | Cumple | DELETE es lógico (estado=false) |
