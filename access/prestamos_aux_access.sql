-- Script DDL para Microsoft Access - base prestamos_aux
-- Ejecutar una sentencia por consulta (Vista SQL). Luego: Herramientas de base de datos > Relaciones.

CREATE TABLE [horario_atencion] (
  [id_horario] COUNTER,
  [id_punto] LONG NOT NULL,
  [dia_semana] YESNO NOT NULL,
  [hora_apertura] DATETIME NOT NULL,
  [hora_cierre] DATETIME NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_horario_atencion] PRIMARY KEY (id_horario)
);

CREATE TABLE [punto_entrega] (
  [id_punto] COUNTER,
  [codigo] TEXT(20) NOT NULL,
  [nombre] TEXT(100) NOT NULL,
  [ubicacion] TEXT(200) NOT NULL,
  [sede] TEXT(80) NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_punto_entrega] PRIMARY KEY (id_punto)
);

CREATE TABLE [reporte_incidencia] (
  [id_reporte] COUNTER,
  [codigo] TEXT(40) NOT NULL,
  [id_tipo] LONG NOT NULL,
  [id_punto] LONG,
  [id_prestamo] LONG NOT NULL,
  [id_usuario_reporta] LONG NOT NULL,
  [descripcion] MEMO NOT NULL,
  [resuelto] YESNO NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_reporte_incidencia] PRIMARY KEY (id_reporte)
);

CREATE TABLE [tipo_incidencia] (
  [id_tipo] COUNTER,
  [nombre] TEXT(60) NOT NULL,
  [gravedad] TEXT(5) NOT NULL,
  [estado] YESNO NOT NULL,
  [creado] DATETIME NOT NULL,
  [actualizado] DATETIME NOT NULL,
  CONSTRAINT [pk_tipo_incidencia] PRIMARY KEY (id_tipo)
);

-- ===== Relaciones (integridad referencial) =====

ALTER TABLE [horario_atencion] ADD CONSTRAINT [fk_horario_atencion_id_punto] FOREIGN KEY ([id_punto]) REFERENCES [punto_entrega] ([id_punto]);

ALTER TABLE [reporte_incidencia] ADD CONSTRAINT [fk_reporte_incidencia_id_punto] FOREIGN KEY ([id_punto]) REFERENCES [punto_entrega] ([id_punto]);

ALTER TABLE [reporte_incidencia] ADD CONSTRAINT [fk_reporte_incidencia_id_tipo] FOREIGN KEY ([id_tipo]) REFERENCES [tipo_incidencia] ([id_tipo]);
