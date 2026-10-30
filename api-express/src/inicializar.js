// Crea tablas y datos semilla si la BD está vacía o tiene la semilla anterior al Taller 1
// (sin el punto 'PE-POS'). Con FORZAR_SEMILLA=true siempre la recrea. Uso: node src/inicializar.js
const fs = require('fs');
const path = require('path');
const mysql = require('mysql2/promise');
require('dotenv').config({ quiet: true });

(async () => {
  const url = process.env.MYSQL_URL || process.env.DATABASE_URL;
  const ssl = process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : undefined;
  const c = url
    ? await mysql.createConnection({ uri: url, multipleStatements: true, ssl })
    : await mysql.createConnection({
      host: process.env.DB_HOST || '127.0.0.1', port: Number(process.env.DB_PORT || 3306),
      user: process.env.DB_USER || 'prestamos', password: process.env.DB_PASSWORD || 'prestamos',
      database: process.env.DB_NAME || 'prestamos_aux', multipleStatements: true, ssl,
    });
  const [t] = await c.query("SELECT COUNT(*) AS n FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'punto_entrega'");
  let vigente = false;
  if (t[0].n > 0) {
    const [p] = await c.query("SELECT COUNT(*) AS n FROM punto_entrega WHERE codigo = 'PE-POS'");
    vigente = p[0].n > 0;
  }
  if (vigente && process.env.FORZAR_SEMILLA !== 'true') {
    console.log('La base de datos ya tiene la semilla del Taller 1; no se modifica.');
  } else {
    await c.query(fs.readFileSync(path.join(__dirname, '../sql/schema.sql'), 'utf8'));
    await c.query(fs.readFileSync(path.join(__dirname, '../sql/seed.sql'), 'utf8'));
    console.log('Esquema y datos semilla creados.');
  }
  await c.end();
})().catch((e) => { console.error(e.message); process.exit(1); });
