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
