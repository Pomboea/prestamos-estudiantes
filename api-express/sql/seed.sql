SET NAMES utf8mb4;
-- Semilla API Express (MySQL). 10 en secundarias, 20 en principales.

INSERT INTO punto_entrega (codigo, nombre, ubicacion, sede) VALUES
 ('PE-BIB', 'Biblioteca Central', 'Primer piso, junto a préstamo externo', 'Sede Principal'),
 ('PE-ING', 'Bloque de Ingeniería', 'Lobby bloque B', 'Sede Principal'),
 ('PE-CAF', 'Cafetería Norte', 'Mesa de bienestar', 'Sede Norte'),
 ('PE-BIE', 'Oficina de Bienestar', 'Segundo piso, bloque A', 'Sede Principal'),
 ('PE-LAB', 'Laboratorios de Ciencias', 'Recepción laboratorios', 'Sede Principal'),
 ('PE-DEP', 'Coliseo deportivo', 'Taquilla', 'Sede Deportiva'),
 ('PE-ART', 'Bloque de Artes', 'Recepción', 'Sede Centro'),
 ('PE-SAL', 'Bloque de Salud', 'Recepción primer piso', 'Sede Salud'),
 ('PE-ADM', 'Edificio Administrativo', 'Ventanilla 3', 'Sede Principal'),
 ('PE-POS', 'Bloque de Posgrados', 'Lobby', 'Sede Centro');

INSERT INTO horario_atencion (id_punto, dia_semana, hora_apertura, hora_cierre) VALUES
 (1, 1, '07:00', '19:00'),
 (1, 6, '07:00', '12:00'),
 (2, 1, '07:00', '19:00'),
 (2, 6, '07:00', '12:00'),
 (3, 1, '07:00', '19:00'),
 (3, 6, '07:00', '12:00'),
 (4, 1, '07:00', '19:00'),
 (4, 6, '07:00', '12:00'),
 (5, 1, '07:00', '19:00'),
 (5, 6, '07:00', '12:00'),
 (6, 1, '07:00', '19:00'),
 (6, 6, '07:00', '12:00'),
 (7, 1, '07:00', '19:00'),
 (7, 6, '07:00', '12:00'),
 (8, 1, '07:00', '19:00'),
 (8, 6, '07:00', '12:00'),
 (9, 1, '07:00', '19:00'),
 (9, 6, '07:00', '12:00'),
 (10, 1, '07:00', '19:00'),
 (10, 6, '07:00', '12:00');

INSERT INTO tipo_incidencia (nombre, gravedad) VALUES
 ('Daño del objeto', 'alta'),
 ('Pérdida', 'alta'),
 ('Retraso en devolución', 'media'),
 ('Objeto incompleto', 'media'),
 ('Objeto sucio', 'baja'),
 ('Accesorio faltante', 'media'),
 ('Falla eléctrica', 'alta'),
 ('Uso indebido', 'alta'),
 ('No se presentó a la entrega', 'baja'),
 ('Otro', 'baja');

INSERT INTO reporte_incidencia (codigo, id_tipo, id_punto, id_prestamo, id_usuario_reporta, descripcion, resuelto) VALUES
 ('INC-0001', 3, 9, 6, 16, 'Se devolvió sucio', 1),
 ('INC-0002', 1, 8, 7, 17, 'Se devolvió sucio', 0),
 ('INC-0003', 7, 7, 8, 18, 'El cargador no enciende', 0),
 ('INC-0004', 7, 2, 9, 19, 'El cargador no enciende', 1),
 ('INC-0005', 7, 1, 10, 20, 'Falta el estuche', 0),
 ('INC-0006', 2, 4, 11, 21, 'El cargador no enciende', 0),
 ('INC-0007', 3, 2, 12, 22, 'Presenta rayones nuevos', 1),
 ('INC-0008', 10, 1, 13, 23, 'El objeto se devolvió con retraso', 0),
 ('INC-0009', 1, 10, 14, 4, 'Falta el estuche', 0),
 ('INC-0010', 9, 2, 15, 5, 'Presenta rayones nuevos', 1),
 ('INC-0011', 10, 1, 16, 6, 'El objeto se devolvió con retraso', 0),
 ('INC-0012', 4, 10, 17, 7, 'El cargador no enciende', 0),
 ('INC-0013', 3, 5, 18, 8, 'Presenta rayones nuevos', 1),
 ('INC-0014', 10, 6, 19, 9, 'El cargador no enciende', 0),
 ('INC-0015', 2, 2, 20, 10, 'El cargador no enciende', 0),
 ('INC-0016', 8, 8, 6, 16, 'El cargador no enciende', 1),
 ('INC-0017', 5, 2, 7, 17, 'Falta el estuche', 0),
 ('INC-0018', 2, 6, 8, 18, 'Presenta rayones nuevos', 0),
 ('INC-0019', 8, 3, 9, 19, 'Se devolvió sucio', 1),
 ('INC-0020', 1, 4, 10, 20, 'Se devolvió sucio', 0);

