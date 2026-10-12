-- =====================================================================
-- Base de datos AUXILIAR (MySQL/MariaDB): puntos de entrega, horarios
-- e incidencias de los préstamos. Normalizada en 3FN. 4 tablas.
-- Todas: PK, UNIQUE, estado (BOOLEAN DEFAULT 1), creado y actualizado
-- (DEFAULT CURRENT_TIMESTAMP / ON UPDATE CURRENT_TIMESTAMP).
-- id_prestamo e id_usuario referencian registros de la BD principal (PostgreSQL).
-- =====================================================================
SET NAMES utf8mb4;
DROP TABLE IF EXISTS reporte_incidencia;
DROP TABLE IF EXISTS tipo_incidencia;
DROP TABLE IF EXISTS horario_atencion;
DROP TABLE IF EXISTS punto_entrega;

-- 1. Lugares del campus donde se entregan/devuelven objetos
CREATE TABLE punto_entrega (
  id_punto INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(20) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  ubicacion VARCHAR(200) NOT NULL,
  sede VARCHAR(80) NOT NULL,
  estado BOOLEAN NOT NULL DEFAULT 1,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Horarios de atención por punto y día (1=lunes ... 7=domingo)
CREATE TABLE horario_atencion (
  id_horario INT AUTO_INCREMENT PRIMARY KEY,
  id_punto INT NOT NULL,
  dia_semana TINYINT NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),
  hora_apertura TIME NOT NULL,
  hora_cierre TIME NOT NULL,
  estado BOOLEAN NOT NULL DEFAULT 1,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT uq_horario UNIQUE (id_punto, dia_semana),
  CONSTRAINT fk_horario_punto FOREIGN KEY (id_punto) REFERENCES punto_entrega(id_punto),
  CONSTRAINT ck_horas CHECK (hora_cierre > hora_apertura)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Catálogo de tipos de incidencia
CREATE TABLE tipo_incidencia (
  id_tipo INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE,
  gravedad ENUM('baja','media','alta') NOT NULL DEFAULT 'baja',
  estado BOOLEAN NOT NULL DEFAULT 1,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Reportes de incidencias (daño, pérdida, retraso) sobre un préstamo
CREATE TABLE reporte_incidencia (
  id_reporte INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(40) NOT NULL UNIQUE,
  id_tipo INT NOT NULL,
  id_punto INT NULL,
  id_prestamo INT NOT NULL,          -- id del préstamo en la BD principal
  id_usuario_reporta INT NOT NULL,   -- id del usuario en la BD principal (tomado del JWT)
  descripcion VARCHAR(500) NOT NULL,
  resuelto BOOLEAN NOT NULL DEFAULT 0,
  estado BOOLEAN NOT NULL DEFAULT 1,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_reporte_tipo FOREIGN KEY (id_tipo) REFERENCES tipo_incidencia(id_tipo),
  CONSTRAINT fk_reporte_punto FOREIGN KEY (id_punto) REFERENCES punto_entrega(id_punto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Triggers: "creado" nunca se modifica
CREATE TRIGGER trg_punto_creado BEFORE UPDATE ON punto_entrega FOR EACH ROW SET NEW.creado = OLD.creado;
CREATE TRIGGER trg_horario_creado BEFORE UPDATE ON horario_atencion FOR EACH ROW SET NEW.creado = OLD.creado;
CREATE TRIGGER trg_tipo_creado BEFORE UPDATE ON tipo_incidencia FOR EACH ROW SET NEW.creado = OLD.creado;
CREATE TRIGGER trg_reporte_creado BEFORE UPDATE ON reporte_incidencia FOR EACH ROW SET NEW.creado = OLD.creado;
