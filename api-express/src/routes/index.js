// Rutas de las 4 tablas de la BD auxiliar
const crypto = require('crypto');
const { crearCrud } = require('./crud');
const { requiereToken, requiereRol } = require('../middleware/auth');

const soloAdmin = [requiereToken, requiereRol('admin')];

const puntos = crearCrud({
  tabla: 'punto_entrega', pk: 'id_punto', leerPublico: true, permisoEscritura: soloAdmin,
  campos: {
    codigo: { tipo: 'texto', requerido: true, max: 20 },
    nombre: { tipo: 'texto', requerido: true, max: 100 },
    ubicacion: { tipo: 'texto', requerido: true, max: 200 },
    sede: { tipo: 'texto', requerido: true, max: 80 },
  },
});

const horarios = crearCrud({
  tabla: 'horario_atencion', pk: 'id_horario', leerPublico: true, permisoEscritura: soloAdmin,
  campos: {
    id_punto: { tipo: 'entero', requerido: true },
    dia_semana: { tipo: 'entero', requerido: true, maxValor: 7 },
    hora_apertura: { tipo: 'hora', requerido: true },
    hora_cierre: { tipo: 'hora', requerido: true },
  },
});

const tipos = crearCrud({
  tabla: 'tipo_incidencia', pk: 'id_tipo', leerPublico: true, permisoEscritura: soloAdmin,
  campos: {
    nombre: { tipo: 'texto', requerido: true, max: 60 },
    gravedad: { tipo: 'enum', valores: ['baja', 'media', 'alta'] },
  },
});

const reportes = crearCrud({
  tabla: 'reporte_incidencia', pk: 'id_reporte', leerPublico: false, permisoEscritura: [requiereToken],
  campos: {
    id_tipo: { tipo: 'entero', requerido: true },
    id_punto: { tipo: 'entero' },
    id_prestamo: { tipo: 'entero', requerido: true },
    descripcion: { tipo: 'texto', requerido: true, max: 500 },
    resuelto: { tipo: 'bool' },
  },
  camposProtegidos: ['id_usuario_reporta'],
  // El código único y el usuario que reporta se generan en el servidor
  antesCrear: async (req, datos) => ({
    ...datos,
    codigo: `INC-${crypto.randomBytes(5).toString('hex').toUpperCase()}`,
    id_usuario_reporta: req.usuario.id,
  }),
  verificarDueno: (req, fila) => req.usuario.rol === 'admin' || fila.id_usuario_reporta === req.usuario.id,
});

module.exports = { puntos, horarios, tipos, reportes };
