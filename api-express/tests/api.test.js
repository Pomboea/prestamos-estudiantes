// Pruebas de la API auxiliar con node:test + supertest. Usa la BD prestamos_aux_test.
process.env.DB_NAME = process.env.DB_NAME_TEST || 'prestamos_aux_test';
process.env.SECRET_KEY = process.env.SECRET_KEY || 'cambie-esta-clave-secreta';

const { test, before, after } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const mysql = require('mysql2/promise');
const jwt = require('jsonwebtoken');
const request = require('supertest');

let app; let pool;
const firmar = (sub, rol) => jwt.sign({ sub: String(sub), correo: `${rol}@uni.edu.co`, rol }, process.env.SECRET_KEY, { expiresIn: '1h' });
const ADMIN = `Bearer ${firmar(1, 'admin')}`;
const ANA = `Bearer ${firmar(2, 'estudiante')}`;
const CARLOS = `Bearer ${firmar(3, 'estudiante')}`;
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

before(async () => {
  const c = await mysql.createConnection({
    host: process.env.DB_HOST || '127.0.0.1', user: process.env.DB_USER || 'prestamos',
    password: process.env.DB_PASSWORD || 'prestamos', database: process.env.DB_NAME, multipleStatements: true,
  });
  await c.query(fs.readFileSync(path.join(__dirname, '../sql/schema.sql'), 'utf8'));
  await c.query(fs.readFileSync(path.join(__dirname, '../sql/seed.sql'), 'utf8'));
  await c.end();
  app = require('../src/app');
  pool = require('../src/db');
});
after(async () => { await pool.end(); });

test('al menos 3 tablas y todas con PK, UNIQUE, estado, creado, actualizado', async () => {
  const [tablas] = await pool.query("SELECT table_name AS t FROM information_schema.tables WHERE table_schema = DATABASE() AND table_type='BASE TABLE'");
  assert.ok(tablas.length >= 3);
  for (const { t } of tablas) {
    const [cols] = await pool.query('SELECT column_name AS c, column_default AS d, extra AS e FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name = ?', [t]);
    const m = Object.fromEntries(cols.map((x) => [x.c, x]));
    assert.ok(m.estado && String(m.estado.d) === '1', `${t}.estado`);
    assert.ok(m.creado && /current_timestamp/i.test(m.creado.d), `${t}.creado`);
    assert.ok(m.actualizado && /on update current_timestamp/i.test(m.actualizado.e), `${t}.actualizado`);
    const [k] = await pool.query('SELECT constraint_type AS k FROM information_schema.table_constraints WHERE table_schema = DATABASE() AND table_name = ?', [t]);
    const tipos = new Set(k.map((x) => x.k));
    assert.ok(tipos.has('PRIMARY KEY') && tipos.has('UNIQUE'), `${t} PK/UNIQUE`);
  }
});

test('lectura pública de puntos y horarios', async () => {
  const r = await request(app).get('/api/puntos-entrega');
  assert.strictEqual(r.status, 200); assert.ok(r.body.length >= 3);
  assert.strictEqual((await request(app).get('/api/horarios')).status, 200);
  assert.strictEqual((await request(app).get('/api/tipos-incidencia')).status, 200);
});

test('escritura sin token -> 401, token inválido -> 401, estudiante en catálogo -> 403', async () => {
  assert.strictEqual((await request(app).post('/api/puntos-entrega').send({})).status, 401);
  assert.strictEqual((await request(app).post('/api/puntos-entrega').set('Authorization', 'Bearer x.y.z').send({})).status, 401);
  assert.strictEqual((await request(app).get('/api/reportes-incidencia')).status, 401);
  const r = await request(app).post('/api/puntos-entrega').set('Authorization', ANA)
    .send({ codigo: 'PE-X', nombre: 'X', ubicacion: 'X', sede: 'X' });
  assert.strictEqual(r.status, 403);
});

test('validación 422 y duplicado 409', async () => {
  const r = await request(app).post('/api/puntos-entrega').set('Authorization', ADMIN).send({ nombre: 'Sin código' });
  assert.strictEqual(r.status, 422);
  const d = await request(app).post('/api/puntos-entrega').set('Authorization', ADMIN)
    .send({ codigo: 'PE-BIB', nombre: 'Otra', ubicacion: 'x', sede: 'x' });
  assert.strictEqual(d.status, 409);
  const h = await request(app).post('/api/horarios').set('Authorization', ADMIN)
    .send({ id_punto: 1, dia_semana: 9, hora_apertura: '08:00', hora_cierre: '10:00' });
  assert.strictEqual(h.status, 422);
});

test('CRUD completo con borrado lógico y auditoría (creado fijo, actualizado cambia)', async () => {
  const c = await request(app).post('/api/puntos-entrega').set('Authorization', ADMIN)
    .send({ codigo: 'PE-LAB', nombre: 'Laboratorio de Física', ubicacion: 'Bloque C', sede: 'Sede Principal' });
  assert.strictEqual(c.status, 201); assert.strictEqual(c.body.estado, 1);
  const id = c.body.id_punto;
  await esperar(1100);
  const u = await request(app).put(`/api/puntos-entrega/${id}`).set('Authorization', ADMIN).send({ ubicacion: 'Bloque C, piso 2' });
  assert.strictEqual(u.status, 200);
  assert.strictEqual(u.body.creado, c.body.creado);
  assert.ok(u.body.actualizado > c.body.actualizado);
  const del = await request(app).delete(`/api/puntos-entrega/${id}`).set('Authorization', ADMIN);
  assert.strictEqual(del.status, 200);
  const lista = await request(app).get('/api/puntos-entrega');
  assert.ok(!lista.body.some((p) => p.id_punto === id));
  assert.strictEqual((await request(app).get(`/api/puntos-entrega/${id}`)).status, 404);
  const [f] = await pool.query('SELECT estado FROM punto_entrega WHERE id_punto = ?', [id]);
  assert.strictEqual(f[0].estado, 0); // sigue existiendo físicamente
  const todos = await request(app).get('/api/puntos-entrega?incluir_inactivos=true');
  assert.ok(todos.body.some((p) => p.id_punto === id));
});

test('reporte de incidencia: el estudiante crea, otro no puede editarlo, el dueño sí', async () => {
  const r = await request(app).post('/api/reportes-incidencia').set('Authorization', ANA)
    .send({ id_tipo: 1, id_punto: 1, id_prestamo: 1, descripcion: 'La calculadora llegó con la tapa rota' });
  assert.strictEqual(r.status, 201);
  assert.ok(r.body.codigo.startsWith('INC-'));
  assert.strictEqual(r.body.id_usuario_reporta, 2);
  const id = r.body.id_reporte;
  assert.strictEqual((await request(app).put(`/api/reportes-incidencia/${id}`).set('Authorization', CARLOS).send({ resuelto: true })).status, 403);
  const ok = await request(app).put(`/api/reportes-incidencia/${id}`).set('Authorization', ANA).send({ resuelto: true });
  assert.strictEqual(ok.status, 200); assert.strictEqual(ok.body.resuelto, 1);
  assert.strictEqual((await request(app).delete(`/api/reportes-incidencia/${id}`).set('Authorization', ADMIN)).status, 200);
});

test('CRUD horarios y tipos', async () => {
  const h = await request(app).post('/api/horarios').set('Authorization', ADMIN)
    .send({ id_punto: 2, dia_semana: 2, hora_apertura: '08:00', hora_cierre: '12:00' });
  assert.strictEqual(h.status, 201);
  const t = await request(app).post('/api/tipos-incidencia').set('Authorization', ADMIN).send({ nombre: 'Suciedad', gravedad: 'baja' });
  assert.strictEqual(t.status, 201);
  assert.strictEqual((await request(app).delete(`/api/tipos-incidencia/${t.body.id_tipo}`).set('Authorization', ADMIN)).status, 200);
});
