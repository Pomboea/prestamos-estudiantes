// Fábrica genérica de CRUD con borrado lógico (estado = 0). creado/actualizado los maneja MySQL.
const express = require('express');
const { body, param, query, validationResult } = require('express-validator');
const pool = require('../db');
const { requiereToken } = require('../middleware/auth');

const validar = (req, res, next) => {
  const errores = validationResult(req);
  if (!errores.isEmpty()) return res.status(422).json({ error: 'Datos inválidos', detalles: errores.array() });
  return next();
};

/**
 * opciones:
 *  tabla, pk, campos: { nombre: { tipo:'texto'|'entero'|'hora'|'bool'|'enum', requerido, max, valores } }
 *  leerPublico: boolean, permisoEscritura: middleware[], antesCrear(req, datos), verificarDueno(req, fila)
 */
function crearCrud(op) {
  const router = express.Router();
  const nombres = Object.keys(op.campos);

  const reglas = (esCreacion) => nombres.map((n) => {
    const c = op.campos[n];
    let r = body(n);
    r = esCreacion && c.requerido ? r.exists({ values: 'null' }).withMessage(`${n} es obligatorio`) : r.optional({ values: 'null' });
    if (c.tipo === 'texto') r = r.isString().trim().isLength({ min: 1, max: c.max || 255 });
    if (c.tipo === 'entero') r = r.isInt({ min: c.min ?? 1, max: c.maxValor }).toInt();
    if (c.tipo === 'hora') r = r.matches(/^([01]\d|2[0-3]):[0-5]\d(:[0-5]\d)?$/).withMessage(`${n} debe ser HH:MM`);
    if (c.tipo === 'bool') r = r.isBoolean().toBoolean();
    if (c.tipo === 'enum') r = r.isIn(c.valores);
    return r;
  });
  const reglaEstado = body('estado').optional().isBoolean().toBoolean();
  const reglaId = param('id').isInt({ min: 1 }).toInt();

  const lectura = op.leerPublico ? [] : [requiereToken];
  const escritura = op.permisoEscritura || [requiereToken];

  async function buscar(id, incluirInactivos = false) {
    const [filas] = await pool.query(`SELECT * FROM ${op.tabla} WHERE ${op.pk} = ?`, [id]);
    const fila = filas[0];
    if (!fila || (!fila.estado && !incluirInactivos)) return null;
    return fila;
  }

  // LISTAR (solo estado = 1 salvo ?incluir_inactivos=true)
  router.get('/', ...lectura, query('incluir_inactivos').optional().isBoolean(), validar, async (req, res, next) => {
    try {
      const todos = req.query.incluir_inactivos === 'true';
      const [filas] = await pool.query(
        `SELECT * FROM ${op.tabla} ${todos ? '' : 'WHERE estado = 1'} ORDER BY ${op.pk}`);
      res.json(filas);
    } catch (e) { next(e); }
  });

  // OBTENER POR ID
  router.get('/:id', ...lectura, reglaId, validar, async (req, res, next) => {
    try {
      const fila = await buscar(req.params.id);
      if (!fila) return res.status(404).json({ error: `Registro ${req.params.id} no encontrado` });
      return res.json(fila);
    } catch (e) { return next(e); }
  });

  // CREAR
  router.post('/', ...escritura, ...reglas(true), validar, async (req, res, next) => {
    try {
      let datos = {};
      nombres.forEach((n) => { if (req.body[n] !== undefined) datos[n] = req.body[n]; });
      if (op.antesCrear) datos = await op.antesCrear(req, datos);
      const columnas = Object.keys(datos);
      const [r] = await pool.query(
        `INSERT INTO ${op.tabla} (${columnas.join(',')}) VALUES (${columnas.map(() => '?').join(',')})`,
        columnas.map((c) => datos[c]));
      res.status(201).json(await buscar(r.insertId));
    } catch (e) { next(e); }
  });

  // ACTUALIZAR (parcial). Permite reactivar con estado=true
  router.put('/:id', ...escritura, reglaId, ...reglas(false), reglaEstado, validar, async (req, res, next) => {
    try {
      const fila = await buscar(req.params.id, true);
      if (!fila) return res.status(404).json({ error: `Registro ${req.params.id} no encontrado` });
      if (op.verificarDueno && !op.verificarDueno(req, fila)) return res.status(403).json({ error: 'No puede modificar este registro' });
      const datos = {};
      [...nombres, 'estado'].forEach((n) => { if (req.body[n] !== undefined) datos[n] = req.body[n]; });
      (op.camposProtegidos || []).forEach((n) => delete datos[n]);
      const columnas = Object.keys(datos);
      if (columnas.length === 0) return res.status(422).json({ error: 'No envió campos para actualizar' });
      await pool.query(`UPDATE ${op.tabla} SET ${columnas.map((c) => `${c} = ?`).join(', ')} WHERE ${op.pk} = ?`,
        [...columnas.map((c) => datos[c]), req.params.id]);
      return res.json(await buscar(req.params.id, true));
    } catch (e) { return next(e); }
  });

  // ELIMINAR LÓGICO: estado = 0 (el registro permanece en la tabla)
  router.delete('/:id', ...escritura, reglaId, validar, async (req, res, next) => {
    try {
      const fila = await buscar(req.params.id);
      if (!fila) return res.status(404).json({ error: `Registro ${req.params.id} no encontrado` });
      if (op.verificarDueno && !op.verificarDueno(req, fila)) return res.status(403).json({ error: 'No puede eliminar este registro' });
      await pool.query(`UPDATE ${op.tabla} SET estado = 0 WHERE ${op.pk} = ?`, [req.params.id]);
      return res.json({ mensaje: `Registro ${req.params.id} eliminado lógicamente (estado = 0)`, id: req.params.id, estado: 0 });
    } catch (e) { return next(e); }
  });

  return router;
}

module.exports = { crearCrud };
