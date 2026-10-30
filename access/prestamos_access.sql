-- Script DDL para Microsoft Access - base prestamos
-- Ejecutar una sentencia por consulta (Vista SQL). Luego: Herramientas de base de datos > Relaciones.

CREATE TABLE [calificacion] (
  [id_calificacion] COUNTER,
  [id_prestamo] LONG NOT NULL,
  [id_evaluador] LONG NOT NULL,
  [id_evaluado] LONG NOT NULL,
  [puntaje] SHORT NOT NULL,
  [comentario] MEMO,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_calificacion] PRIMARY KEY (id_calificacion)
);

CREATE TABLE [categoria_objeto] (
  [id_categoria] COUNTER,
  [nombre] TEXT(60) NOT NULL,
  [descripcion] TEXT(200),
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_categoria_objeto] PRIMARY KEY (id_categoria)
);

CREATE TABLE [condicion_objeto] (
  [id_condicion] COUNTER,
  [nombre] TEXT(40) NOT NULL,
  [descripcion] TEXT(200),
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_condicion_objeto] PRIMARY KEY (id_condicion)
);

CREATE TABLE [devolucion] (
  [id_devolucion] COUNTER,
  [id_prestamo] LONG NOT NULL,
  [fecha_devolucion] DATETIME NOT NULL,
  [id_condicion_devolucion] LONG NOT NULL,
  [observaciones] MEMO,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_devolucion] PRIMARY KEY (id_devolucion)
);

CREATE TABLE [estado_solicitud] (
  [id_estado_solicitud] COUNTER,
  [nombre] TEXT(30) NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_estado_solicitud] PRIMARY KEY (id_estado_solicitud)
);

CREATE TABLE [facultad] (
  [id_facultad] COUNTER,
  [nombre] TEXT(100) NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_facultad] PRIMARY KEY (id_facultad)
);

CREATE TABLE [imagen_objeto] (
  [id_imagen] COUNTER,
  [id_objeto] LONG NOT NULL,
  [url] MEMO NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_imagen_objeto] PRIMARY KEY (id_imagen)
);

CREATE TABLE [modulo] (
  [id_modulo] COUNTER,
  [nombre] TEXT(60) NOT NULL,
  [ruta] TEXT(100) NOT NULL,
  [descripcion] TEXT(200),
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_modulo] PRIMARY KEY (id_modulo)
);

CREATE TABLE [moduloxrol] (
  [id_moduloxrol] COUNTER,
  [id_rol] LONG NOT NULL,
  [id_modulo] LONG NOT NULL,
  [puede_leer] YESNO NOT NULL,
  [puede_crear] YESNO NOT NULL,
  [puede_actualizar] YESNO NOT NULL,
  [puede_eliminar] YESNO NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_moduloxrol] PRIMARY KEY (id_moduloxrol)
);

CREATE TABLE [notificacion] (
  [id_notificacion] COUNTER,
  [codigo] TEXT(40) NOT NULL,
  [id_usuario] LONG NOT NULL,
  [titulo] TEXT(100) NOT NULL,
  [mensaje] MEMO NOT NULL,
  [leida] YESNO NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_notificacion] PRIMARY KEY (id_notificacion)
);

CREATE TABLE [objeto] (
  [id_objeto] COUNTER,
  [codigo] TEXT(30) NOT NULL,
  [nombre] TEXT(100) NOT NULL,
  [descripcion] MEMO,
  [id_categoria] LONG NOT NULL,
  [id_condicion] LONG NOT NULL,
  [id_propietario] LONG NOT NULL,
  [disponible] YESNO NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_objeto] PRIMARY KEY (id_objeto)
);

CREATE TABLE [prestamo] (
  [id_prestamo] COUNTER,
  [id_solicitud] LONG NOT NULL,
  [fecha_prestamo] DATETIME NOT NULL,
  [fecha_devolucion_esperada] DATETIME NOT NULL,
  [id_condicion_entrega] LONG NOT NULL,
  [observaciones] MEMO,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_prestamo] PRIMARY KEY (id_prestamo)
);

CREATE TABLE [programa_academico] (
  [id_programa] COUNTER,
  [codigo] TEXT(20) NOT NULL,
  [nombre] TEXT(120) NOT NULL,
  [id_facultad] LONG NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_programa_academico] PRIMARY KEY (id_programa)
);

CREATE TABLE [rol] (
  [id_rol] COUNTER,
  [nombre] TEXT(50) NOT NULL,
  [descripcion] TEXT(200),
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_rol] PRIMARY KEY (id_rol)
);

CREATE TABLE [sancion] (
  [id_sancion] COUNTER,
  [codigo] TEXT(40) NOT NULL,
  [id_usuario] LONG NOT NULL,
  [id_prestamo] LONG,
  [motivo] TEXT(200) NOT NULL,
  [fecha_inicio] DATETIME NOT NULL,
  [fecha_fin] DATETIME NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_sancion] PRIMARY KEY (id_sancion)
);

CREATE TABLE [solicitud_prestamo] (
  [id_solicitud] COUNTER,
  [codigo] TEXT(40) NOT NULL,
  [id_objeto] LONG NOT NULL,
  [id_solicitante] LONG NOT NULL,
  [id_estado_solicitud] LONG NOT NULL,
  [fecha_inicio_deseada] DATETIME NOT NULL,
  [fecha_fin_deseada] DATETIME NOT NULL,
  [mensaje] MEMO,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_solicitud_prestamo] PRIMARY KEY (id_solicitud)
);

CREATE TABLE [usuario] (
  [id_usuario] COUNTER,
  [nombres] TEXT(80) NOT NULL,
  [apellidos] TEXT(80) NOT NULL,
  [correo] TEXT(120) NOT NULL,
  [codigo_estudiantil] TEXT(20),
  [telefono] TEXT(20),
  [contrasena_hash] TEXT(255) NOT NULL,
  [id_rol] LONG NOT NULL,
  [id_programa] LONG,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_usuario] PRIMARY KEY (id_usuario)
);

-- ===== Relaciones (integridad referencial) =====

ALTER TABLE [calificacion] ADD CONSTRAINT [fk_calificacion_id_evaluado] FOREIGN KEY ([id_evaluado]) REFERENCES [usuario] ([id_usuario]);

ALTER TABLE [calificacion] ADD CONSTRAINT [fk_calificacion_id_evaluador] FOREIGN KEY ([id_evaluador]) REFERENCES [usuario] ([id_usuario]);

ALTER TABLE [calificacion] ADD CONSTRAINT [fk_calificacion_id_prestamo] FOREIGN KEY ([id_prestamo]) REFERENCES [prestamo] ([id_prestamo]);

ALTER TABLE [devolucion] ADD CONSTRAINT [fk_devolucion_id_condicion_devolucion] FOREIGN KEY ([id_condicion_devolucion]) REFERENCES [condicion_objeto] ([id_condicion]);

ALTER TABLE [devolucion] ADD CONSTRAINT [fk_devolucion_id_prestamo] FOREIGN KEY ([id_prestamo]) REFERENCES [prestamo] ([id_prestamo]);

ALTER TABLE [imagen_objeto] ADD CONSTRAINT [fk_imagen_objeto_id_objeto] FOREIGN KEY ([id_objeto]) REFERENCES [objeto] ([id_objeto]);

ALTER TABLE [moduloxrol] ADD CONSTRAINT [fk_moduloxrol_id_modulo] FOREIGN KEY ([id_modulo]) REFERENCES [modulo] ([id_modulo]);

ALTER TABLE [moduloxrol] ADD CONSTRAINT [fk_moduloxrol_id_rol] FOREIGN KEY ([id_rol]) REFERENCES [rol] ([id_rol]);

ALTER TABLE [notificacion] ADD CONSTRAINT [fk_notificacion_id_usuario] FOREIGN KEY ([id_usuario]) REFERENCES [usuario] ([id_usuario]);

ALTER TABLE [objeto] ADD CONSTRAINT [fk_objeto_id_categoria] FOREIGN KEY ([id_categoria]) REFERENCES [categoria_objeto] ([id_categoria]);

ALTER TABLE [objeto] ADD CONSTRAINT [fk_objeto_id_condicion] FOREIGN KEY ([id_condicion]) REFERENCES [condicion_objeto] ([id_condicion]);

ALTER TABLE [objeto] ADD CONSTRAINT [fk_objeto_id_propietario] FOREIGN KEY ([id_propietario]) REFERENCES [usuario] ([id_usuario]);

ALTER TABLE [prestamo] ADD CONSTRAINT [fk_prestamo_id_condicion_entrega] FOREIGN KEY ([id_condicion_entrega]) REFERENCES [condicion_objeto] ([id_condicion]);

ALTER TABLE [prestamo] ADD CONSTRAINT [fk_prestamo_id_solicitud] FOREIGN KEY ([id_solicitud]) REFERENCES [solicitud_prestamo] ([id_solicitud]);

ALTER TABLE [programa_academico] ADD CONSTRAINT [fk_programa_academico_id_facultad] FOREIGN KEY ([id_facultad]) REFERENCES [facultad] ([id_facultad]);

ALTER TABLE [sancion] ADD CONSTRAINT [fk_sancion_id_prestamo] FOREIGN KEY ([id_prestamo]) REFERENCES [prestamo] ([id_prestamo]);

ALTER TABLE [sancion] ADD CONSTRAINT [fk_sancion_id_usuario] FOREIGN KEY ([id_usuario]) REFERENCES [usuario] ([id_usuario]);

ALTER TABLE [solicitud_prestamo] ADD CONSTRAINT [fk_solicitud_prestamo_id_estado_solicitud] FOREIGN KEY ([id_estado_solicitud]) REFERENCES [estado_solicitud] ([id_estado_solicitud]);

ALTER TABLE [solicitud_prestamo] ADD CONSTRAINT [fk_solicitud_prestamo_id_objeto] FOREIGN KEY ([id_objeto]) REFERENCES [objeto] ([id_objeto]);

ALTER TABLE [solicitud_prestamo] ADD CONSTRAINT [fk_solicitud_prestamo_id_solicitante] FOREIGN KEY ([id_solicitante]) REFERENCES [usuario] ([id_usuario]);

ALTER TABLE [usuario] ADD CONSTRAINT [fk_usuario_id_programa] FOREIGN KEY ([id_programa]) REFERENCES [programa_academico] ([id_programa]);

ALTER TABLE [usuario] ADD CONSTRAINT [fk_usuario_id_rol] FOREIGN KEY ([id_rol]) REFERENCES [rol] ([id_rol]);
