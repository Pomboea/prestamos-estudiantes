-- =====================================================================
-- Base de datos PRINCIPAL (PostgreSQL) - Sistema de préstamos de objetos
-- entre estudiantes universitarios. Normalizada en 3FN. 17 tablas.
-- TODAS las tablas tienen: PK, campo(s) UNIQUE, estado (BOOLEAN DEFAULT TRUE),
-- creado (TIMESTAMP DEFAULT, nunca cambia) y actualizado (TIMESTAMP, trigger).
-- =====================================================================
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- Función de auditoría: actualiza "actualizado" y protege "creado"
CREATE OR REPLACE FUNCTION fn_auditoria_actualizado() RETURNS TRIGGER AS $$
BEGIN
  NEW.actualizado := clock_timestamp();
  NEW.creado := OLD.creado;   -- "creado" jamás se modifica
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

-- 1. rol
CREATE TABLE rol (
  id_rol SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  descripcion VARCHAR(200),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 2. modulo
CREATE TABLE modulo (
  id_modulo SERIAL PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE,
  ruta VARCHAR(100) NOT NULL UNIQUE,
  descripcion VARCHAR(200),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 3. moduloxrol (permisos del rol sobre cada módulo)
CREATE TABLE moduloxrol (
  id_moduloxrol SERIAL PRIMARY KEY,
  id_rol INT NOT NULL REFERENCES rol(id_rol),
  id_modulo INT NOT NULL REFERENCES modulo(id_modulo),
  puede_leer BOOLEAN NOT NULL DEFAULT TRUE,
  puede_crear BOOLEAN NOT NULL DEFAULT FALSE,
  puede_actualizar BOOLEAN NOT NULL DEFAULT FALSE,
  puede_eliminar BOOLEAN NOT NULL DEFAULT FALSE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_moduloxrol UNIQUE (id_rol, id_modulo)
);
-- 4. facultad
CREATE TABLE facultad (
  id_facultad SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 5. programa_academico
CREATE TABLE programa_academico (
  id_programa SERIAL PRIMARY KEY,
  codigo VARCHAR(20) NOT NULL UNIQUE,
  nombre VARCHAR(120) NOT NULL,
  id_facultad INT NOT NULL REFERENCES facultad(id_facultad),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 6. usuario (incluye datos del estudiante)
CREATE TABLE usuario (
  id_usuario SERIAL PRIMARY KEY,
  nombres VARCHAR(80) NOT NULL,
  apellidos VARCHAR(80) NOT NULL,
  correo VARCHAR(120) NOT NULL UNIQUE,
  codigo_estudiantil VARCHAR(20) UNIQUE,
  telefono VARCHAR(20),
  contrasena_hash VARCHAR(255) NOT NULL,
  id_rol INT NOT NULL REFERENCES rol(id_rol),
  id_programa INT REFERENCES programa_academico(id_programa),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 7. categoria_objeto
CREATE TABLE categoria_objeto (
  id_categoria SERIAL PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE,
  descripcion VARCHAR(200),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 8. condicion_objeto (Nuevo, Bueno, Regular, Dañado)
CREATE TABLE condicion_objeto (
  id_condicion SERIAL PRIMARY KEY,
  nombre VARCHAR(40) NOT NULL UNIQUE,
  descripcion VARCHAR(200),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 9. objeto
CREATE TABLE objeto (
  id_objeto SERIAL PRIMARY KEY,
  codigo VARCHAR(30) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(300),
  id_categoria INT NOT NULL REFERENCES categoria_objeto(id_categoria),
  id_condicion INT NOT NULL REFERENCES condicion_objeto(id_condicion),
  id_propietario INT NOT NULL REFERENCES usuario(id_usuario),
  disponible BOOLEAN NOT NULL DEFAULT TRUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 10. imagen_objeto
CREATE TABLE imagen_objeto (
  id_imagen SERIAL PRIMARY KEY,
  id_objeto INT NOT NULL REFERENCES objeto(id_objeto),
  url VARCHAR(300) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 11. estado_solicitud (Pendiente, Aprobada, Rechazada, Cancelada)
CREATE TABLE estado_solicitud (
  id_estado_solicitud SERIAL PRIMARY KEY,
  nombre VARCHAR(30) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 12. solicitud_prestamo
CREATE TABLE solicitud_prestamo (
  id_solicitud SERIAL PRIMARY KEY,
  codigo VARCHAR(40) NOT NULL UNIQUE DEFAULT ('SOL-' || substr(md5(random()::text || clock_timestamp()::text), 1, 12)),
  id_objeto INT NOT NULL REFERENCES objeto(id_objeto),
  id_solicitante INT NOT NULL REFERENCES usuario(id_usuario),
  id_estado_solicitud INT NOT NULL REFERENCES estado_solicitud(id_estado_solicitud),
  fecha_inicio_deseada DATE NOT NULL,
  fecha_fin_deseada DATE NOT NULL,
  mensaje VARCHAR(300),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT ck_fechas_solicitud CHECK (fecha_fin_deseada >= fecha_inicio_deseada)
);
-- 13. prestamo (una solicitud aprobada genera a lo sumo un préstamo)
CREATE TABLE prestamo (
  id_prestamo SERIAL PRIMARY KEY,
  id_solicitud INT NOT NULL UNIQUE REFERENCES solicitud_prestamo(id_solicitud),
  fecha_prestamo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_devolucion_esperada DATE NOT NULL,
  id_condicion_entrega INT NOT NULL REFERENCES condicion_objeto(id_condicion),
  observaciones VARCHAR(300),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 14. devolucion
CREATE TABLE devolucion (
  id_devolucion SERIAL PRIMARY KEY,
  id_prestamo INT NOT NULL UNIQUE REFERENCES prestamo(id_prestamo),
  fecha_devolucion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_condicion_devolucion INT NOT NULL REFERENCES condicion_objeto(id_condicion),
  observaciones VARCHAR(300),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 15. calificacion (reseña de un participante del préstamo hacia el otro)
CREATE TABLE calificacion (
  id_calificacion SERIAL PRIMARY KEY,
  id_prestamo INT NOT NULL REFERENCES prestamo(id_prestamo),
  id_evaluador INT NOT NULL REFERENCES usuario(id_usuario),
  id_evaluado INT NOT NULL REFERENCES usuario(id_usuario),
  puntaje SMALLINT NOT NULL CHECK (puntaje BETWEEN 1 AND 5),
  comentario VARCHAR(300),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_calificacion UNIQUE (id_prestamo, id_evaluador)
);
-- 16. notificacion
CREATE TABLE notificacion (
  id_notificacion SERIAL PRIMARY KEY,
  codigo VARCHAR(40) NOT NULL UNIQUE DEFAULT ('NOT-' || substr(md5(random()::text || clock_timestamp()::text), 1, 12)),
  id_usuario INT NOT NULL REFERENCES usuario(id_usuario),
  titulo VARCHAR(100) NOT NULL,
  mensaje VARCHAR(300) NOT NULL,
  leida BOOLEAN NOT NULL DEFAULT FALSE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- 17. sancion (por devolución tardía o daño)
CREATE TABLE sancion (
  id_sancion SERIAL PRIMARY KEY,
  codigo VARCHAR(40) NOT NULL UNIQUE DEFAULT ('SAN-' || substr(md5(random()::text || clock_timestamp()::text), 1, 12)),
  id_usuario INT NOT NULL REFERENCES usuario(id_usuario),
  id_prestamo INT REFERENCES prestamo(id_prestamo),
  motivo VARCHAR(200) NOT NULL,
  fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
  fecha_fin DATE NOT NULL,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger de auditoría en TODAS las tablas
DO $$
DECLARE t TEXT;
BEGIN
  FOR t IN SELECT table_name FROM information_schema.tables
           WHERE table_schema='public' AND table_type='BASE TABLE' LOOP
    EXECUTE format('CREATE TRIGGER trg_%s_actualizado BEFORE UPDATE ON %I
                    FOR EACH ROW EXECUTE FUNCTION fn_auditoria_actualizado()', t, t);
  END LOOP;
END $$;
