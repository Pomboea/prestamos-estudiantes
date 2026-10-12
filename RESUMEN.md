# Resumen de la propuesta

## Sistema web para gestionar préstamos de objetos entre estudiantes universitarios

### Problemática
En la universidad los estudiantes se prestan con frecuencia calculadoras, libros, cargadores, computadores, audífonos y materiales de estudio. Estos préstamos se hacen de manera informal (de palabra o por chat), por lo que **no queda registro** de:

- quién tiene cada objeto,
- cuándo se prestó y cuándo debe devolverse,
- en qué condición se entregó y en qué condición regresó.

Esto genera pérdidas, retrasos, conflictos entre compañeros y desconfianza para volver a prestar.

### Población objetivo
- **Estudiantes universitarios** de pregrado y posgrado de los distintos programas y facultades, que desean prestar u obtener en préstamo objetos académicos.
- **Administradores** (bienestar universitario o personal designado) que gestionan catálogos, usuarios, permisos, puntos de entrega e incidencias.

### Flujo principal
1. El estudiante **publica** un objeto (categoría, condición, descripción, fotos).
2. Otro estudiante **solicita** el préstamo indicando fechas.
3. El propietario **aprueba o rechaza** la solicitud.
4. Se **registra el préstamo** (el objeto pasa a *no disponible* y se guarda la condición de entrega).
5. Se **registra la devolución** (el objeto vuelve a *disponible*, se guarda la condición de retorno y, si hay retraso, se genera una sanción automática).
6. Los participantes se **califican** y reciben **notificaciones** de cada paso.

### Requerimientos generales
**Funcionales**
- RF1. Registro e inicio de sesión de estudiantes con JWT.
- RF2. Gestión de roles, módulos y permisos por rol (rol, usuario, modulo, moduloxrol).
- RF3. Gestión de facultades, programas académicos, categorías y condiciones de objetos.
- RF4. Publicación, edición y eliminación lógica de objetos por su propietario, con imágenes.
- RF5. Solicitud, aprobación/rechazo, préstamo y devolución con trazabilidad de fechas y condición.
- RF6. Consulta de objetos disponibles, mis préstamos, mis solicitudes y solicitudes recibidas.
- RF7. Calificaciones entre estudiantes, notificaciones y sanciones por retraso.
- RF8. (API auxiliar) Puntos de entrega del campus, horarios de atención y reportes de incidencias (daño, pérdida, retraso).

**No funcionales**
- RNF1. Todas las tablas con llave primaria, campos únicos, `estado` (borrado lógico), `creado` y `actualizado` gestionados por el motor de BD.
- RNF2. Base principal en PostgreSQL normalizada (3FN, 17 tablas) y base auxiliar en MySQL (4 tablas).
- RNF3. Seguridad: contraseñas con bcrypt, tokens JWT con expiración, autorización por rol/módulo (401/403).
- RNF4. APIs documentadas (Swagger en `/docs`), desplegables con Docker y en la nube (Render / Railway).

### Tecnologías
PostgreSQL · FastAPI · SQLAlchemy 2 · Pydantic v2 · JWT · MySQL · Node.js · Express · Docker · Render/Railway.
