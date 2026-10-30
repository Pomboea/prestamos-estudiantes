# Base de datos en Microsoft Access (requisito del Taller 1)

El taller pide la base de datos en **Microsoft Access** para imprimir las tablas con sus relaciones.

## Archivos
| Archivo | Contenido |
|---|---|
| `prestamos.accdb` | 17 tablas de la BD principal (PostgreSQL / FastAPI): llaves primarias, 22 relaciones con integridad referencial y todos los registros de prueba |
| `prestamos_aux.accdb` | 4 tablas de la BD auxiliar (MySQL / Express): llaves primarias, 3 relaciones y los registros |
| `prestamos_access.sql`, `prestamos_aux_access.sql` | Script DDL en dialecto Access (CREATE TABLE + ALTER TABLE ... FOREIGN KEY), por si quiere crear la base a mano |
| `generador/` | Programa (Python + Java/Jackcess) que lee las bases locales y genera los `.accdb` |

> La relación `reporte_incidencia.id_prestamo` apunta a la tabla `prestamo`, que está en la otra base
> (PostgreSQL). Como son motores distintos, esa relación no se puede declarar.

## Ver e imprimir las relaciones (Access 2016 / 365)
1. Abra `prestamos.accdb`. Si aparece el aviso amarillo, haga clic en **Habilitar contenido**.
2. Vaya a **Herramientas de base de datos > Relaciones**.
3. Si no aparecen todas las tablas, haga clic en **Todas las relaciones** (o **Agregar tablas**, seleccione todas y luego **Agregar**).
4. Ordene los cuadros arrastrándolos, de modo que las líneas 1 → ∞ se vean bien (como en la imagen del taller).
5. Haga doble clic en una línea para ver **Exigir integridad referencial** activado.
6. **Diseño de relación > Informe de relación** y luego **Imprimir** (o Exportar a PDF).
7. Para imprimir una tabla: ábrala en Vista Hoja de datos y use **Archivo > Imprimir**.

## Crear la base a mano con el script SQL (alternativa)
1. Access: **Archivo > Nuevo > Base de datos en blanco**.
2. **Crear > Diseño de consulta**, cierre el cuadro de tablas y cambie a **Vista SQL**.
3. Pegue **una sola** sentencia `CREATE TABLE` del script y presione **Ejecutar**. Repita con cada tabla.
4. Ejecute luego cada `ALTER TABLE ... FOREIGN KEY` (relaciones).
5. Para cargar los datos: **Datos externos > Nuevo origen de datos > Desde archivo > Texto**, o copie y pegue desde las bases locales.
6. Abra **Relaciones** (paso 2 de la sección anterior) para verlas e imprimirlas.

## Regenerar los .accdb
Con las bases locales en marcha: `cd access/generador && ./generar.sh` (requiere Java 17+ y Python con psycopg2 y pymysql).
