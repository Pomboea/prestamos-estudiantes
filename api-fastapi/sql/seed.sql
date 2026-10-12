-- Datos iniciales (semilla). Contraseñas: admin -> Admin123* ; estudiantes -> Estudiante123*
INSERT INTO rol (nombre, descripcion) VALUES
 ('admin','Administrador del sistema'),
 ('estudiante','Estudiante que presta y solicita objetos');

INSERT INTO modulo (nombre, ruta, descripcion) VALUES
 ('roles','/roles','Gestión de roles'),
 ('modulos','/modulos','Gestión de módulos'),
 ('permisos','/moduloxrol','Permisos rol-módulo'),
 ('usuarios','/usuarios','Gestión de usuarios'),
 ('facultades','/facultades','Facultades'),
 ('programas','/programas','Programas académicos'),
 ('categorias','/categorias','Categorías de objetos'),
 ('condiciones','/condiciones','Condiciones físicas del objeto'),
 ('objetos','/objetos','Objetos publicados'),
 ('imagenes','/imagenes','Imágenes de objetos'),
 ('estados_solicitud','/estados-solicitud','Estados de solicitud'),
 ('solicitudes','/solicitudes','Solicitudes de préstamo'),
 ('prestamos','/prestamos','Préstamos'),
 ('devoluciones','/devoluciones','Devoluciones'),
 ('calificaciones','/calificaciones','Calificaciones entre estudiantes'),
 ('notificaciones','/notificaciones','Notificaciones'),
 ('sanciones','/sanciones','Sanciones');

-- Admin: todos los permisos sobre todos los módulos
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 1, id_modulo, TRUE, TRUE, TRUE, TRUE FROM modulo;

-- Estudiante: lectura de catálogos y operación del flujo de préstamo
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 2, id_modulo,
  TRUE,
  nombre IN ('objetos','imagenes','solicitudes','prestamos','devoluciones','calificaciones'),
  nombre IN ('objetos','imagenes','solicitudes','notificaciones','calificaciones'),
  nombre IN ('objetos','imagenes')
FROM modulo WHERE nombre NOT IN ('roles','modulos','permisos','usuarios');

INSERT INTO facultad (nombre) VALUES ('Ingeniería'),('Ciencias Económicas'),('Ciencias de la Salud');
INSERT INTO programa_academico (codigo, nombre, id_facultad) VALUES
 ('ING-SIS','Ingeniería de Sistemas',1),
 ('ING-IND','Ingeniería Industrial',1),
 ('ECO-ADM','Administración de Empresas',2),
 ('SAL-ENF','Enfermería',3);

INSERT INTO usuario (nombres, apellidos, correo, codigo_estudiantil, telefono, contrasena_hash, id_rol, id_programa) VALUES
 ('Admin','Sistema','admin@uni.edu.co',NULL,'3000000000','$2b$12$aWUqdIj5Wpm5gVUwYBQUfuYFLzcVtYqbZVwBwJNcDIYGRI5PVoTn.',1,NULL),
 ('Ana','Gómez','ana@uni.edu.co','2021001','3001112233','$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS',2,1),
 ('Carlos','Pérez','carlos@uni.edu.co','2021002','3004445566','$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS',2,2);

INSERT INTO categoria_objeto (nombre, descripcion) VALUES
 ('Calculadoras','Calculadoras científicas y gráficas'),
 ('Libros','Libros y textos académicos'),
 ('Cargadores','Cargadores de portátil y celular'),
 ('Computadores','Portátiles y tabletas'),
 ('Audífonos','Audífonos y diademas'),
 ('Materiales de estudio','Kits de laboratorio, batas, reglas, etc.');

INSERT INTO condicion_objeto (nombre, descripcion) VALUES
 ('Nuevo','Sin uso'),('Bueno','Uso normal sin daños'),('Regular','Desgaste visible'),('Dañado','Presenta daños');

INSERT INTO estado_solicitud (nombre) VALUES ('Pendiente'),('Aprobada'),('Rechazada'),('Cancelada'),('Finalizada');

INSERT INTO objeto (codigo, nombre, descripcion, id_categoria, id_condicion, id_propietario) VALUES
 ('OBJ-0001','Calculadora Casio fx-991LA','Científica, con estuche',1,2,2),
 ('OBJ-0002','Cálculo de Stewart 8va ed.','Libro de cálculo diferencial',2,2,2),
 ('OBJ-0003','Cargador Lenovo 65W','Punta delgada USB-C',3,1,3),
 ('OBJ-0004','Audífonos JBL Tune','Bluetooth',5,3,3);

INSERT INTO imagen_objeto (id_objeto, url) VALUES
 (1,'https://ejemplo.com/img/casio.jpg'),(3,'https://ejemplo.com/img/cargador.jpg');

INSERT INTO notificacion (id_usuario, titulo, mensaje) VALUES
 (2,'Bienvenida','Bienvenida al sistema de préstamos'),(3,'Bienvenida','Bienvenido al sistema de préstamos');
