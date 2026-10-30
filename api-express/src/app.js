// API auxiliar (Express + MySQL): puntos de entrega, horarios e incidencias
const express = require('express');
const cors = require('cors');
require('dotenv').config({ quiet: true });
const pool = require('./db');
const { puntos, horarios, tipos, reportes } = require('./routes');

const app = express();
// CORS_ORIGINS='*' (o sin definir) permite cualquier origen; si no, lista separada por comas.
// Ojo: cors() no trata ['*'] como comodín, por eso se pasa '*' como texto.
const origenes = (process.env.CORS_ORIGINS || '*').trim();
app.use(cors({ origin: origenes === '*' ? '*' : origenes.split(',').map((o) => o.trim()) }));
app.use(express.json());

app.get('/', (req, res) => res.json({
  mensaje: 'API auxiliar de préstamos (Express + MySQL)',
  recursos: ['/api/puntos-entrega', '/api/horarios', '/api/tipos-incidencia', '/api/reportes-incidencia'],
}));
app.get('/salud', async (req, res, next) => {
  try { await pool.query('SELECT 1'); res.json({ estado: 'ok', base_de_datos: 'conectada' }); } catch (e) { next(e); }
});

app.use('/api/puntos-entrega', puntos);
app.use('/api/horarios', horarios);
app.use('/api/tipos-incidencia', tipos);
app.use('/api/reportes-incidencia', reportes);

app.use((req, res) => res.status(404).json({ error: 'Ruta no encontrada' }));

// Manejo centralizado de errores (traduce errores de MySQL a códigos HTTP)
// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  if (err.code === 'ER_DUP_ENTRY') return res.status(409).json({ error: 'Valor duplicado en un campo único', detalle: err.sqlMessage });
  if (err.code === 'ER_NO_REFERENCED_ROW_2') return res.status(409).json({ error: 'Referencia inválida (llave foránea)', detalle: err.sqlMessage });
  if (err.code === 'ER_CHECK_CONSTRAINT_VIOLATED' || err.errno === 4025) return res.status(422).json({ error: 'Restricción CHECK violada', detalle: err.sqlMessage });
  if (err.type === 'entity.parse.failed') return res.status(400).json({ error: 'JSON mal formado' });
  console.error(err);
  return res.status(500).json({ error: 'Error interno del servidor' });
});

module.exports = app;
