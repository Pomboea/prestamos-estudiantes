// Validación del MISMO JWT emitido por la API FastAPI (SECRET_KEY compartida, HS256)
const jwt = require('jsonwebtoken');

function requiereToken(req, res, next) {
  const encabezado = req.headers.authorization || '';
  const [tipo, token] = encabezado.split(' ');
  if (tipo !== 'Bearer' || !token) {
    return res.status(401).json({ error: 'Token requerido (Authorization: Bearer <token>)' });
  }
  try {
    const datos = jwt.verify(token, process.env.SECRET_KEY || 'cambie-esta-clave-secreta', { algorithms: ['HS256'] });
    req.usuario = { id: Number(datos.sub), correo: datos.correo, rol: datos.rol };
    return next();
  } catch (e) {
    return res.status(401).json({ error: 'Token inválido o expirado' });
  }
}

const requiereRol = (...roles) => (req, res, next) => {
  if (!req.usuario || !roles.includes(req.usuario.rol)) {
    return res.status(403).json({ error: `Requiere rol: ${roles.join(', ')}` });
  }
  return next();
};

module.exports = { requiereToken, requiereRol };
