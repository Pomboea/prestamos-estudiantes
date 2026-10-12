-- Verificación de requisitos del parcial en MySQL (ejecutar: mysql prestamos_aux < sql/verificar.sql)
SELECT COUNT(*) AS total_tablas FROM information_schema.tables WHERE table_schema = DATABASE() AND table_type='BASE TABLE';
SELECT t.table_name AS tabla,
  EXISTS (SELECT 1 FROM information_schema.table_constraints c WHERE c.table_schema=t.table_schema AND c.table_name=t.table_name AND c.constraint_type='PRIMARY KEY') AS tiene_pk,
  EXISTS (SELECT 1 FROM information_schema.table_constraints c WHERE c.table_schema=t.table_schema AND c.table_name=t.table_name AND c.constraint_type='UNIQUE') AS tiene_unique,
  EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_schema=t.table_schema AND c.table_name=t.table_name AND c.column_name='estado' AND c.column_default='1') AS estado_ok,
  EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_schema=t.table_schema AND c.table_name=t.table_name AND c.column_name='creado' AND LOWER(c.column_default) LIKE 'current_timestamp%') AS creado_ok,
  EXISTS (SELECT 1 FROM information_schema.columns c WHERE c.table_schema=t.table_schema AND c.table_name=t.table_name AND c.column_name='actualizado' AND LOWER(c.extra) LIKE '%on update current_timestamp%') AS actualizado_ok
FROM information_schema.tables t
WHERE t.table_schema = DATABASE() AND t.table_type='BASE TABLE' ORDER BY t.table_name;
