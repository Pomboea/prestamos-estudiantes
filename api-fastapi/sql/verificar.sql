-- Verificación de requisitos del parcial en PostgreSQL (ejecutar: psql -d prestamos -f sql/verificar.sql)
SELECT count(*) AS total_tablas FROM information_schema.tables
WHERE table_schema='public' AND table_type='BASE TABLE';

SELECT t.table_name AS tabla,
  EXISTS (SELECT 1 FROM information_schema.table_constraints c WHERE c.table_name=t.table_name AND c.constraint_type='PRIMARY KEY') AS tiene_pk,
  EXISTS (SELECT 1 FROM information_schema.table_constraints c WHERE c.table_name=t.table_name AND c.constraint_type='UNIQUE') AS tiene_unique,
  EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_name=t.table_name AND c.column_name='estado' AND c.data_type='boolean' AND c.column_default='true') AS estado_ok,
  EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_name=t.table_name AND c.column_name='creado' AND c.column_default IS NOT NULL) AS creado_ok,
  EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_name=t.table_name AND c.column_name='actualizado' AND c.column_default IS NOT NULL) AS actualizado_ok,
  EXISTS (SELECT 1 FROM information_schema.triggers g WHERE g.event_object_table=t.table_name AND g.event_manipulation='UPDATE') AS trigger_ok
FROM information_schema.tables t
WHERE t.table_schema='public' AND t.table_type='BASE TABLE'
ORDER BY t.table_name;
