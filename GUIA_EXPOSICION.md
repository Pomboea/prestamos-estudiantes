# Guía para la exposición (un integrante expone)

Tenga abiertos: Swagger (`/docs`), pgAdmin/psql, MySQL Workbench/consola, VS Code con `requests.http`.

## 0. Resumen de la propuesta (10%) — 2 min
- Mostrar `RESUMEN.md` / `Resumen_propuesta.docx`: problema (préstamos informales sin registro), población (estudiantes y administradores), flujo publicar → solicitar → aprobar → prestar → devolver, requerimientos.

## 1.1 BD PostgreSQL normalizada (parte del 60%) — 4 min
- Mostrar el diagrama `docs/er_postgres.png`: 17 tablas (mínimo 12), incluidas **rol, usuario, modulo, moduloxrol**.
- Explicar 3FN: catálogos separados (categoría, condición, estado_solicitud, facultad→programa), sin datos repetidos.
- Ejecutar `psql -d prestamos -f sql/verificar.sql` → todas las filas en `t` (PK, UNIQUE, estado, creado, actualizado, trigger).
- Abrir `schema.sql`: función `fn_auditoria_actualizado` y triggers.

## 1.2 API FastAPI — 4 min
- `/docs`: grupos de endpoints, CRUD de cada tabla y flujo de préstamo.
- Demostrar en vivo (o con `requests.http`): Carlos solicita el objeto 1 → Ana aprueba → Ana presta (objeto `disponible=false`) → `mis-prestamos` → devolución (vuelve a `disponible=true` y cambia su condición).
- Borrado lógico: `DELETE /categorias/{id}` → desaparece del GET, pero en la BD sigue con `estado=false`.
- Auditoría: `PUT` de una categoría → `creado` igual, `actualizado` cambia.

## 1.3 JWT y validación — 3 min
- `POST /auth/login` → copiar token → **Authorize** en Swagger.
- Sin token `GET /objetos` → **401**. Con token de estudiante `GET /roles` → **403** (permiso leído de `moduloxrol`).
- Carlos intenta editar el objeto de Ana → **403**. Registro duplicado → **409**. Datos inválidos → **422**.
- Mostrar `core/security.py`: bcrypt, expiración del token, dependencia `requiere_permiso(modulo, accion)`.

## 1.4 Despliegue de la API — 2 min
- Mostrar la URL pública en Render (`/docs` y `/salud`), `render.yaml`, `Dockerfile` y `docs/DESPLIEGUE.md`.

## 2.1 BD MySQL auxiliar (30%) — 2 min
- `docs/er_mysql.png`: punto_entrega, horario_atencion, tipo_incidencia, reporte_incidencia (mínimo 3).
- `mysql prestamos_aux < sql/verificar.sql` → todo en 1. Mostrar `ON UPDATE CURRENT_TIMESTAMP`.

## 2.2 API Express — 2 min
- `GET /api/puntos-entrega`; crear/actualizar/eliminar (lógico) con token de admin.
- Crear un reporte de incidencia **con el token emitido por FastAPI** (misma SECRET_KEY) → muestra integración entre APIs.
- Sin token → 401; estudiante creando punto → 403.

## 2.3 Despliegue Express — 1 min
- URL pública en Render + MySQL en Railway/Aiven.

## Cierre — 1 min
- Pruebas automáticas: `pytest -v` (16 pruebas) y `npm test` (7 pruebas) en verde.

**Preguntas probables:** ¿por qué borrado lógico? (trazabilidad/auditoría) · ¿quién llena `creado`/`actualizado`? (el motor, con DEFAULT y triggers) · ¿cómo se valida el rol? (JWT → usuario → `moduloxrol`) · ¿por qué dos BD? (la auxiliar maneja logística del campus e incidencias, desacoplada del núcleo).
