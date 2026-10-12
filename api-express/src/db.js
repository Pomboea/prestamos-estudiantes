// Pool de conexiones a MySQL con mysql2/promise
const mysql = require('mysql2/promise');
require('dotenv').config({ quiet: true });

function configuracion() {
  // Railway/Aiven/Clever Cloud pueden entregar una URL completa
  const url = process.env.MYSQL_URL || process.env.DATABASE_URL;
  const ssl = process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : undefined;
  const base = { waitForConnections: true, connectionLimit: 10, dateStrings: true, ssl };
  if (url) return { uri: url, ...base };
  return {
    host: process.env.DB_HOST || '127.0.0.1',
    port: Number(process.env.DB_PORT || 3306),
    user: process.env.DB_USER || 'prestamos',
    password: process.env.DB_PASSWORD || 'prestamos',
    database: process.env.DB_NAME || 'prestamos_aux',
    ...base,
  };
}

const pool = mysql.createPool(configuracion());
module.exports = pool;
