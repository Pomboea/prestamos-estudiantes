-- Semilla Taller 1 Corte 2. Contraseñas: admin Admin123* | coordinadores Coordinador123* | estudiantes Estudiante123*
-- Tablas principales: 20 registros. Tablas secundarias (catálogos): 10 registros. rol: 3 (los tres roles del sistema).

INSERT INTO rol (nombre, descripcion) VALUES
 ('admin', 'Administrador del sistema'),
 ('coordinador', 'Coordinador de Bienestar Universitario: supervisa préstamos, sanciones y catálogos'),
 ('estudiante', 'Estudiante que presta y solicita objetos');

INSERT INTO modulo (nombre, ruta, descripcion) VALUES
 ('roles', '/roles', 'Gestión de roles'),
 ('modulos', '/modulos', 'Gestión de módulos'),
 ('permisos', '/moduloxrol', 'Permisos rol-módulo'),
 ('usuarios', '/usuarios', 'Gestión de usuarios'),
 ('facultades', '/facultades', 'Facultades'),
 ('programas', '/programas', 'Programas académicos'),
 ('categorias', '/categorias', 'Categorías de objetos'),
 ('condiciones', '/condiciones', 'Condiciones físicas del objeto'),
 ('objetos', '/objetos', 'Objetos publicados'),
 ('imagenes', '/imagenes', 'Imágenes de objetos'),
 ('estados_solicitud', '/estados-solicitud', 'Estados de solicitud'),
 ('solicitudes', '/solicitudes', 'Solicitudes de préstamo'),
 ('prestamos', '/prestamos', 'Préstamos'),
 ('devoluciones', '/devoluciones', 'Devoluciones'),
 ('calificaciones', '/calificaciones', 'Calificaciones entre estudiantes'),
 ('notificaciones', '/notificaciones', 'Notificaciones'),
 ('sanciones', '/sanciones', 'Sanciones'),
 ('puntos_entrega', '/puntos-entrega', 'Puntos de entrega (API Express)'),
 ('horarios', '/horarios', 'Horarios de atención (API Express)'),
 ('tipos_incidencia', '/tipos-incidencia', 'Tipos de incidencia (API Express)'),
 ('reportes_incidencia', '/reportes-incidencia', 'Reportes de incidencia (API Express)');

-- Permisos (moduloxrol). El menú del frontend se carga SOLO desde esta tabla.
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 1, id_modulo, TRUE, TRUE, TRUE, TRUE FROM modulo;
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 2, id_modulo, TRUE,
  nombre IN ('facultades','programas','categorias','condiciones','sanciones','notificaciones','puntos_entrega','horarios','tipos_incidencia','reportes_incidencia'),
  nombre IN ('facultades','programas','categorias','condiciones','sanciones','notificaciones','puntos_entrega','horarios','tipos_incidencia','reportes_incidencia','usuarios'),
  nombre IN ('facultades','programas','categorias','condiciones','sanciones','puntos_entrega','horarios','tipos_incidencia','reportes_incidencia')
FROM modulo WHERE nombre NOT IN ('modulos','permisos');
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 3, id_modulo, TRUE,
  nombre IN ('objetos','imagenes','solicitudes','prestamos','devoluciones','calificaciones','reportes_incidencia'),
  nombre IN ('objetos','imagenes','solicitudes','notificaciones','calificaciones','reportes_incidencia'),
  nombre IN ('objetos','imagenes','solicitudes','calificaciones','reportes_incidencia')
FROM modulo WHERE nombre IN ('categorias','condiciones','estados_solicitud','objetos','imagenes','solicitudes','prestamos','devoluciones','calificaciones','notificaciones','sanciones','puntos_entrega','horarios','reportes_incidencia');

INSERT INTO facultad (nombre) VALUES
 ('Ingeniería'),
 ('Ciencias Económicas y Administrativas'),
 ('Ciencias de la Salud'),
 ('Ciencias Básicas'),
 ('Derecho y Ciencias Políticas'),
 ('Educación'),
 ('Arquitectura y Diseño'),
 ('Ciencias Sociales y Humanas'),
 ('Comunicación'),
 ('Artes');

INSERT INTO programa_academico (codigo, nombre, id_facultad) VALUES
 ('ING-SIS', 'Ingeniería de Sistemas', 1),
 ('ING-IND', 'Ingeniería Industrial', 1),
 ('ECO-ADM', 'Administración de Empresas', 2),
 ('SAL-ENF', 'Enfermería', 3),
 ('BAS-MAT', 'Matemáticas', 4),
 ('DER-DER', 'Derecho', 5),
 ('EDU-LIC', 'Licenciatura en Informática', 6),
 ('ARQ-ARQ', 'Arquitectura', 7),
 ('SOC-PSI', 'Psicología', 8),
 ('COM-SOC', 'Comunicación Social', 9);

INSERT INTO usuario (nombres, apellidos, correo, codigo_estudiantil, telefono, contrasena_hash, id_rol, id_programa) VALUES
 ('Admin', 'Sistema', 'admin@uni.edu.co', NULL, '3000000000', '$2b$12$aWUqdIj5Wpm5gVUwYBQUfuYFLzcVtYqbZVwBwJNcDIYGRI5PVoTn.', 1, NULL),
 ('Patricia', 'Restrepo', 'patricia.restrepo@uni.edu.co', NULL, '3015550101', '$2b$12$UqVnduRJmANur1uTrvAEZOW6syhG3MP1UqixG7PB/oeAvGLfkSKF6', 2, NULL),
 ('Hernán', 'Villa', 'hernan.villa@uni.edu.co', NULL, '3015550102', '$2b$12$UqVnduRJmANur1uTrvAEZOW6syhG3MP1UqixG7PB/oeAvGLfkSKF6', 2, NULL),
 ('Ana', 'Gómez', 'ana@uni.edu.co', '2021001', '30203530829', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 1),
 ('Carlos', 'Pérez', 'carlos@uni.edu.co', '2021002', '30221810111', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 2),
 ('Valentina', 'Rodríguez', 'valentina.rodriguez@uni.edu.co', '2021003', '30129990608', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 3),
 ('Santiago', 'Martínez', 'santiago.martinez@uni.edu.co', '2021004', '30137135241', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 4),
 ('Daniela', 'López', 'daniela.lopez@uni.edu.co', '2021005', '30281973060', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 5),
 ('Andrés', 'Herrera', 'andres.herrera@uni.edu.co', '2021006', '30264602037', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 6),
 ('Camila', 'Torres', 'camila.torres@uni.edu.co', '2021007', '30112441955', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 7),
 ('Juan Pablo', 'Ramírez', 'juan.ramirez@uni.edu.co', '2021008', '30238015764', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 8),
 ('María José', 'Castro', 'maria.castro@uni.edu.co', '2021009', '30125037655', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 9),
 ('Sebastián', 'Morales', 'sebastian.morales@uni.edu.co', '2021010', '30128122250', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 10),
 ('Laura', 'Vargas', 'laura.vargas@uni.edu.co', '2021011', '30113077052', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 1),
 ('Mateo', 'Rojas', 'mateo.rojas@uni.edu.co', '2021012', '30172037872', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 2),
 ('Isabella', 'Jiménez', 'isabella.jimenez@uni.edu.co', '2021013', '30287655194', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 3),
 ('Felipe', 'Ortiz', 'felipe.ortiz@uni.edu.co', '2021014', '30114709137', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 4),
 ('Sofía', 'Mendoza', 'sofia.mendoza@uni.edu.co', '2021015', '30113234302', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 5),
 ('Diego', 'Cárdenas', 'diego.cardenas@uni.edu.co', '2021016', '30198031986', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 6),
 ('Paula', 'Navarro', 'paula.navarro@uni.edu.co', '2021017', '30142976225', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 7),
 ('Nicolás', 'Guerrero', 'nicolas.guerrero@uni.edu.co', '2021018', '30286175466', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 8),
 ('Mariana', 'Salazar', 'mariana.salazar@uni.edu.co', '2021019', '30274032085', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 9),
 ('Julián', 'Pineda', 'julian.pineda@uni.edu.co', '2021020', '30134151952', '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS', 3, 10);

INSERT INTO categoria_objeto (nombre, descripcion) VALUES
 ('Calculadoras', 'Calculadoras científicas y gráficas'),
 ('Libros', 'Libros y textos académicos'),
 ('Cargadores', 'Cargadores de portátil y celular'),
 ('Computadores', 'Portátiles y tabletas'),
 ('Audífonos', 'Audífonos y diademas'),
 ('Materiales de laboratorio', 'Batas, gafas y kits de laboratorio'),
 ('Instrumentos de dibujo', 'Escuadras, compases y reglas'),
 ('Equipos deportivos', 'Balones, raquetas y conos'),
 ('Instrumentos musicales', 'Guitarras, teclados y flautas'),
 ('Accesorios tecnológicos', 'Mouse, USB, adaptadores HDMI');

INSERT INTO condicion_objeto (nombre, descripcion) VALUES
 ('Nuevo', 'Sin uso'),
 ('Como nuevo', 'Usado una o dos veces'),
 ('Excelente', 'Sin marcas de uso'),
 ('Muy bueno', 'Marcas mínimas'),
 ('Bueno', 'Uso normal sin daños'),
 ('Aceptable', 'Funciona, con desgaste'),
 ('Regular', 'Desgaste visible'),
 ('Desgastado', 'Desgaste fuerte'),
 ('Con fallas', 'Funciona parcialmente'),
 ('Dañado', 'Presenta daños');

INSERT INTO estado_solicitud (nombre) VALUES
 ('Pendiente'),
 ('Aprobada'),
 ('Rechazada'),
 ('Cancelada'),
 ('Finalizada'),
 ('En revisión'),
 ('Entregada'),
 ('Vencida'),
 ('Devuelta'),
 ('Expirada');

INSERT INTO objeto (codigo, nombre, descripcion, id_categoria, id_condicion, id_propietario, disponible) VALUES
 ('OBJ-0001', 'Calculadora Casio fx-991LA', 'Científica, con estuche', 1, 3, 4, FALSE),
 ('OBJ-0002', 'Cálculo de Stewart 8va ed.', 'Cálculo diferencial e integral', 2, 1, 5, FALSE),
 ('OBJ-0003', 'Cargador Lenovo 65W', 'USB-C punta delgada', 3, 1, 6, FALSE),
 ('OBJ-0004', 'Audífonos JBL Tune 510BT', 'Bluetooth', 5, 1, 7, FALSE),
 ('OBJ-0005', 'Portátil HP 14"', 'Intel i5, 8 GB RAM', 4, 2, 8, FALSE),
 ('OBJ-0006', 'Bata de laboratorio talla M', 'Manga larga, blanca', 6, 5, 9, TRUE),
 ('OBJ-0007', 'Juego de escuadras Faber-Castell', '45° y 60°', 7, 5, 10, TRUE),
 ('OBJ-0008', 'Balón de voleibol Mikasa', 'Tamaño oficial', 8, 3, 11, TRUE),
 ('OBJ-0009', 'Guitarra acústica Yamaha C40', 'Con forro', 9, 5, 12, TRUE),
 ('OBJ-0010', 'Mouse Logitech M170', 'Inalámbrico', 10, 5, 13, TRUE),
 ('OBJ-0011', 'Calculadora TI-84 Plus', 'Gráfica', 1, 3, 14, TRUE),
 ('OBJ-0012', 'Física de Serway 10ma ed.', 'Tomo 1', 2, 3, 15, TRUE),
 ('OBJ-0013', 'Cargador Samsung 25W', 'USB-C carga rápida', 3, 2, 16, TRUE),
 ('OBJ-0014', 'Diadema Sony WH-CH520', 'Bluetooth', 5, 2, 17, TRUE),
 ('OBJ-0015', 'Tablet Samsung Galaxy Tab A8', '10.5 pulgadas', 4, 2, 18, TRUE),
 ('OBJ-0016', 'Gafas de seguridad', 'Policarbonato', 6, 1, 19, TRUE),
 ('OBJ-0017', 'Compás Staedtler Mars', 'Con adaptador', 7, 3, 20, TRUE),
 ('OBJ-0018', 'Raqueta de tenis de mesa', 'Con 3 pelotas', 8, 5, 21, TRUE),
 ('OBJ-0019', 'Teclado Casio CT-S1', '61 teclas', 9, 3, 22, TRUE),
 ('OBJ-0020', 'Adaptador HDMI a USB-C', '4K', 10, 5, 23, TRUE);

INSERT INTO imagen_objeto (id_objeto, url) VALUES
 (1, 'https://picsum.photos/seed/obj1/400/300'),
 (2, 'https://picsum.photos/seed/obj2/400/300'),
 (3, 'https://picsum.photos/seed/obj3/400/300'),
 (4, 'https://picsum.photos/seed/obj4/400/300'),
 (5, 'https://picsum.photos/seed/obj5/400/300'),
 (6, 'https://picsum.photos/seed/obj6/400/300'),
 (7, 'https://picsum.photos/seed/obj7/400/300'),
 (8, 'https://picsum.photos/seed/obj8/400/300'),
 (9, 'https://picsum.photos/seed/obj9/400/300'),
 (10, 'https://picsum.photos/seed/obj10/400/300'),
 (11, 'https://picsum.photos/seed/obj11/400/300'),
 (12, 'https://picsum.photos/seed/obj12/400/300'),
 (13, 'https://picsum.photos/seed/obj13/400/300'),
 (14, 'https://picsum.photos/seed/obj14/400/300'),
 (15, 'https://picsum.photos/seed/obj15/400/300'),
 (16, 'https://picsum.photos/seed/obj16/400/300'),
 (17, 'https://picsum.photos/seed/obj17/400/300'),
 (18, 'https://picsum.photos/seed/obj18/400/300'),
 (19, 'https://picsum.photos/seed/obj19/400/300'),
 (20, 'https://picsum.photos/seed/obj20/400/300');

INSERT INTO solicitud_prestamo (codigo, id_objeto, id_solicitante, id_estado_solicitud, fecha_inicio_deseada, fecha_fin_deseada, mensaje) VALUES
 ('SOL-0001', 1, 11, 2, '2026-10-26', '2026-11-02', 'Hola, necesito el objeto para una exposición'),
 ('SOL-0002', 2, 12, 2, '2026-10-25', '2026-11-01', 'Hola, necesito el objeto para estudiar'),
 ('SOL-0003', 3, 13, 2, '2026-10-24', '2026-10-31', 'Hola, necesito el objeto para un parcial'),
 ('SOL-0004', 4, 14, 2, '2026-10-23', '2026-10-30', 'Hola, necesito el objeto para un parcial'),
 ('SOL-0005', 5, 15, 2, '2026-10-22', '2026-10-29', 'Hola, necesito el objeto para estudiar'),
 ('SOL-0006', 6, 16, 5, '2026-09-09', '2026-09-16', 'Hola, necesito el objeto para un proyecto'),
 ('SOL-0007', 7, 17, 5, '2026-09-11', '2026-09-18', 'Hola, necesito el objeto para un laboratorio'),
 ('SOL-0008', 8, 18, 5, '2026-09-13', '2026-09-20', 'Hola, necesito el objeto para una exposición'),
 ('SOL-0009', 9, 19, 5, '2026-09-15', '2026-09-22', 'Hola, necesito el objeto para un laboratorio'),
 ('SOL-0010', 10, 20, 5, '2026-09-17', '2026-09-24', 'Hola, necesito el objeto para un proyecto'),
 ('SOL-0011', 11, 21, 5, '2026-09-19', '2026-09-26', 'Hola, necesito el objeto para un proyecto'),
 ('SOL-0012', 12, 22, 5, '2026-09-21', '2026-09-28', 'Hola, necesito el objeto para un parcial'),
 ('SOL-0013', 13, 23, 5, '2026-09-23', '2026-09-30', 'Hola, necesito el objeto para un parcial'),
 ('SOL-0014', 14, 4, 5, '2026-09-25', '2026-10-02', 'Hola, necesito el objeto para estudiar'),
 ('SOL-0015', 15, 5, 5, '2026-09-27', '2026-10-04', 'Hola, necesito el objeto para estudiar'),
 ('SOL-0016', 16, 6, 5, '2026-09-29', '2026-10-06', 'Hola, necesito el objeto para una exposición'),
 ('SOL-0017', 17, 7, 5, '2026-10-01', '2026-10-08', 'Hola, necesito el objeto para una exposición'),
 ('SOL-0018', 18, 8, 5, '2026-10-03', '2026-10-10', 'Hola, necesito el objeto para una exposición'),
 ('SOL-0019', 19, 9, 5, '2026-10-05', '2026-10-12', 'Hola, necesito el objeto para estudiar'),
 ('SOL-0020', 20, 10, 5, '2026-10-07', '2026-10-14', 'Hola, necesito el objeto para un proyecto');

INSERT INTO prestamo (id_solicitud, fecha_prestamo, fecha_devolucion_esperada, id_condicion_entrega, observaciones) VALUES
 (1, '2026-10-26 10:00', '2026-11-02', 5, 'Entregado en Biblioteca Central'),
 (2, '2026-10-25 10:00', '2026-11-01', 5, 'Entregado en Biblioteca Central'),
 (3, '2026-10-24 10:00', '2026-10-31', 5, 'Entregado en Biblioteca Central'),
 (4, '2026-10-23 10:00', '2026-10-30', 5, 'Entregado en Biblioteca Central'),
 (5, '2026-10-22 10:00', '2026-10-29', 5, 'Entregado en Biblioteca Central'),
 (6, '2026-09-09 10:00', '2026-09-16', 5, 'Entregado en Biblioteca Central'),
 (7, '2026-09-11 10:00', '2026-09-18', 5, 'Entregado en Biblioteca Central'),
 (8, '2026-09-13 10:00', '2026-09-20', 5, 'Entregado en Biblioteca Central'),
 (9, '2026-09-15 10:00', '2026-09-22', 5, 'Entregado en Biblioteca Central'),
 (10, '2026-09-17 10:00', '2026-09-24', 5, 'Entregado en Biblioteca Central'),
 (11, '2026-09-19 10:00', '2026-09-26', 5, 'Entregado en Biblioteca Central'),
 (12, '2026-09-21 10:00', '2026-09-28', 5, 'Entregado en Biblioteca Central'),
 (13, '2026-09-23 10:00', '2026-09-30', 5, 'Entregado en Biblioteca Central'),
 (14, '2026-09-25 10:00', '2026-10-02', 5, 'Entregado en Biblioteca Central'),
 (15, '2026-09-27 10:00', '2026-10-04', 5, 'Entregado en Biblioteca Central'),
 (16, '2026-09-29 10:00', '2026-10-06', 5, 'Entregado en Biblioteca Central'),
 (17, '2026-10-01 10:00', '2026-10-08', 5, 'Entregado en Biblioteca Central'),
 (18, '2026-10-03 10:00', '2026-10-10', 5, 'Entregado en Biblioteca Central'),
 (19, '2026-10-05 10:00', '2026-10-12', 5, 'Entregado en Biblioteca Central'),
 (20, '2026-10-07 10:00', '2026-10-14', 5, 'Entregado en Biblioteca Central');

INSERT INTO devolucion (id_prestamo, fecha_devolucion, id_condicion_devolucion, observaciones) VALUES
 (6, '2026-09-16 16:00', 5, 'Devuelto a tiempo'),
 (7, '2026-09-18 16:00', 5, 'Devuelto a tiempo'),
 (8, '2026-09-20 16:00', 5, 'Devuelto a tiempo'),
 (9, '2026-09-22 16:00', 7, 'Devuelto con desgaste'),
 (10, '2026-09-24 16:00', 5, 'Devuelto a tiempo'),
 (11, '2026-09-26 16:00', 5, 'Devuelto a tiempo'),
 (12, '2026-09-28 16:00', 5, 'Devuelto a tiempo'),
 (13, '2026-09-30 16:00', 7, 'Devuelto con desgaste'),
 (14, '2026-10-02 16:00', 5, 'Devuelto a tiempo'),
 (15, '2026-10-04 16:00', 5, 'Devuelto a tiempo'),
 (16, '2026-10-06 16:00', 5, 'Devuelto a tiempo'),
 (17, '2026-10-08 16:00', 7, 'Devuelto con desgaste'),
 (18, '2026-10-10 16:00', 5, 'Devuelto a tiempo'),
 (19, '2026-10-12 16:00', 5, 'Devuelto a tiempo'),
 (20, '2026-10-14 16:00', 5, 'Devuelto a tiempo');

INSERT INTO calificacion (id_prestamo, id_evaluador, id_evaluado, puntaje, comentario) VALUES
 (6, 9, 16, 3, 'Muy puntual y cuidadoso'),
 (7, 10, 17, 4, 'Devolvió en buen estado'),
 (8, 11, 18, 3, 'Muy puntual y cuidadoso'),
 (9, 12, 19, 4, 'Devolvió en buen estado'),
 (10, 13, 20, 3, 'Devolvió en buen estado'),
 (11, 14, 21, 3, 'Devolvió en buen estado'),
 (12, 15, 22, 4, 'Recomendado'),
 (13, 16, 23, 5, 'Excelente trato'),
 (14, 17, 4, 4, 'Recomendado'),
 (15, 18, 5, 4, 'Excelente trato'),
 (16, 19, 6, 5, 'Excelente trato'),
 (17, 20, 7, 5, 'Recomendado'),
 (18, 21, 8, 3, 'Recomendado'),
 (19, 22, 9, 4, 'Excelente trato'),
 (20, 23, 10, 3, 'Recomendado'),
 (6, 16, 9, 5, 'Excelente trato'),
 (7, 17, 10, 3, 'Algo de retraso pero cumplió'),
 (8, 18, 11, 5, 'Recomendado'),
 (9, 19, 12, 5, 'Recomendado'),
 (10, 20, 13, 5, 'Excelente trato');

INSERT INTO notificacion (codigo, id_usuario, titulo, mensaje, leida) VALUES
 ('NOT-0001', 4, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0002', 5, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0003', 6, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0004', 7, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0005', 8, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0006', 9, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0007', 10, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0008', 11, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0009', 12, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0010', 13, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0011', 14, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0012', 15, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0013', 16, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0014', 17, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0015', 18, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0016', 19, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0017', 20, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0018', 21, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE),
 ('NOT-0019', 22, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', TRUE),
 ('NOT-0020', 23, 'Bienvenida', 'Bienvenido(a) al sistema de préstamos entre estudiantes', FALSE);

INSERT INTO sancion (codigo, id_usuario, id_prestamo, motivo, fecha_inicio, fecha_fin) VALUES
 ('SAN-0001', 16, 6, 'Devolución tardía', '2026-07-01', '2026-07-16'),
 ('SAN-0002', 17, 7, 'Devolución tardía', '2026-07-04', '2026-07-19'),
 ('SAN-0003', 18, 8, 'Devolución tardía', '2026-07-07', '2026-07-22'),
 ('SAN-0004', 19, 9, 'Devolución tardía', '2026-07-10', '2026-07-25'),
 ('SAN-0005', 20, 10, 'Incumplimiento de horario de entrega', '2026-07-13', '2026-07-28'),
 ('SAN-0006', 21, 11, 'Devolución tardía', '2026-07-16', '2026-07-31'),
 ('SAN-0007', 22, 12, 'Devolución tardía', '2026-07-19', '2026-08-03'),
 ('SAN-0008', 23, 13, 'Objeto devuelto con desgaste', '2026-07-22', '2026-08-06'),
 ('SAN-0009', 4, 14, 'Incumplimiento de horario de entrega', '2026-07-25', '2026-08-09'),
 ('SAN-0010', 5, 15, 'Devolución tardía', '2026-07-28', '2026-08-12'),
 ('SAN-0011', 6, 16, 'Objeto devuelto con desgaste', '2026-07-31', '2026-08-15'),
 ('SAN-0012', 7, 17, 'Objeto devuelto con desgaste', '2026-08-03', '2026-08-18'),
 ('SAN-0013', 8, 18, 'Devolución tardía', '2026-08-06', '2026-08-21'),
 ('SAN-0014', 9, 19, 'Devolución tardía', '2026-08-09', '2026-08-24'),
 ('SAN-0015', 10, 20, 'Objeto devuelto con desgaste', '2026-08-12', '2026-08-27'),
 ('SAN-0016', 16, 6, 'Incumplimiento de horario de entrega', '2026-08-15', '2026-08-30'),
 ('SAN-0017', 17, 7, 'Objeto devuelto con desgaste', '2026-08-18', '2026-09-02'),
 ('SAN-0018', 18, 8, 'Incumplimiento de horario de entrega', '2026-08-21', '2026-09-05'),
 ('SAN-0019', 19, 9, 'Incumplimiento de horario de entrega', '2026-08-24', '2026-09-08'),
 ('SAN-0020', 20, 10, 'Objeto devuelto con desgaste', '2026-08-27', '2026-09-11');

