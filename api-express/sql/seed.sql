SET NAMES utf8mb4;
INSERT INTO punto_entrega (codigo, nombre, ubicacion, sede) VALUES
 ('PE-BIB','Biblioteca Central','Primer piso, junto a préstamo externo','Sede Principal'),
 ('PE-ING','Bloque de Ingeniería','Lobby bloque B','Sede Principal'),
 ('PE-CAF','Cafetería Norte','Mesa de bienestar','Sede Norte');
INSERT INTO horario_atencion (id_punto, dia_semana, hora_apertura, hora_cierre) VALUES
 (1,1,'07:00','19:00'),(1,2,'07:00','19:00'),(1,3,'07:00','19:00'),(2,1,'08:00','17:00'),(3,5,'10:00','14:00');
INSERT INTO tipo_incidencia (nombre, gravedad) VALUES
 ('Daño del objeto','alta'),('Pérdida','alta'),('Retraso en devolución','media'),('Objeto incompleto','media'),('Otro','baja');
INSERT INTO reporte_incidencia (codigo, id_tipo, id_punto, id_prestamo, id_usuario_reporta, descripcion) VALUES
 ('INC-DEMO-0001',3,1,1,2,'Ejemplo: el objeto se devolvió con 2 días de retraso');
