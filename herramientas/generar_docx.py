from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
C = os.path.join(os.path.dirname(__file__), '..', 'capturas')
d = Document()
st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
def h(t, n=1): d.add_heading(t, n)
def p(t): d.add_paragraph(t)
def b(t): d.add_paragraph(t, style='List Bullet')
def tabla(filas, enc):
    t = d.add_table(rows=1, cols=len(enc)); t.style = 'Light Grid Accent 1'
    for i, e in enumerate(enc): t.rows[0].cells[i].text = e
    for f in filas:
        r = t.add_row().cells
        for i, v in enumerate(f): r[i].text = str(v)
    d.add_paragraph()
def img(nombre, pie, ancho=6.3):
    ruta = os.path.join(C, nombre)
    if os.path.exists(ruta):
        d.add_picture(ruta, width=Inches(ancho)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c = d.add_paragraph(f'Captura {nombre[:3].strip("_")}: {pie}'); c.alignment = WD_ALIGN_PARAGRAPH.CENTER; c.runs[0].italic = True

t = d.add_heading('Taller 1 – Corte 2', 0)
p('Sistema web de préstamos de objetos entre estudiantes universitarios (PrestaU)')
p('Frontend SvelteKit + API FastAPI (PostgreSQL) + API Express (MySQL) con JWT y roles')

h('1. Requisitos del taller y cómo se cumplen')
tabla([
 ('Campos creado, actualizado y estado en todas las tablas', 'Cumplido: las 21 tablas los tienen; DELETE hace borrado lógico (estado=false)'),
 ('Estructura vista en clase (documento CRUD)', 'Cumplido: rutas /api/<recurso>/, servicios api_<recurso>.js, components/, routes/<modulo>/+page.svelte, proxy en vite.config.js'),
 ('Login con JWT por roles', 'Cumplido: /api/auth/login-json; el mismo token sirve en FastAPI y Express'),
 ('Tres roles funcionales con mínimo 3 páginas', 'Cumplido: admin (21 módulos), coordinador (19), estudiante (14)'),
 ('Módulos del rol cargados solo desde la BD', 'Cumplido: menú e inicio salen de la tabla moduloxrol (GET /api/auth/mis-modulos); botones Crear/Editar/Eliminar según sus permisos'),
 ('Lo que hace un rol se refleja en los otros', 'Cumplido: solicitud → aprobación → préstamo → devolución, con notificaciones y visibles para el coordinador'),
 ('No mostrar ni escribir IDs', 'Cumplido: tablas muestran nombres; formularios usan listas desplegables con nombres'),
 ('DataTables en todas las tablas', 'Cumplido: componente DataTable.svelte con datatables.net (buscar, ordenar, paginar, en español)'),
 ('Mínimo 10 componentes reutilizables', 'Cumplido: 12 componentes'),
 ('Responsive y menú funcional', 'Cumplido: menú hamburguesa en móvil (captura 42)'),
 ('20 registros en tablas principales y 10 en secundarias', 'Cumplido excepto: devolucion 15 (solo hay devolución para préstamos terminados) y rol 3 (solo existen 3 roles)'),
 ('Base de datos en Microsoft Access con relaciones', 'Entregado: access/prestamos.accdb y prestamos_aux.accdb + guía para imprimir relaciones'),
 ('Versión local y en la nube', 'Cumplido: local y en Render (frontend estático + 2 APIs)'),
], ['Requisito', 'Estado'])

h('2. Roles y usuarios de prueba')
tabla([('admin','admin@uni.edu.co','Admin123*','Todo, incluidos roles, módulos y permisos'),
       ('coordinador','patricia.restrepo@uni.edu.co','Coordinador123*','Catálogos, usuarios, sanciones, notificaciones, supervisa préstamos; roles solo consulta'),
       ('estudiante','ana@uni.edu.co / carlos@uni.edu.co','Estudiante123*','Publica objetos, solicita, aprueba/entrega sus objetos, califica, reporta incidencias')],
      ['Rol','Correo','Contraseña','Qué puede hacer'])

h('3. Base de datos')
p('BD principal PostgreSQL "prestamos" (17 tablas) y BD auxiliar MySQL "prestamos_aux" (4 tablas). Scripts en api-fastapi/sql y api-express/sql (schema.sql, seed.sql, verificar.sql).')
img('05_conteo_registros.png', 'registros por tabla')
p('Microsoft Access: access/prestamos.accdb (17 tablas, 22 relaciones con integridad referencial) y access/prestamos_aux.accdb (4 tablas, 3 relaciones). Para imprimir: Herramientas de base de datos > Relaciones > Informe de relación (ver access/GUIA_ACCESS.md).')
img('46_access_accdb_verificado.png', 'archivos Access verificados')

h('4. Estructura del frontend (documento CRUD)')
for x in ['npx sv create frontend-svelte – plantilla minimal – JavaScript',
          'src/lib/components/: Navbar, Footer, Header, Card, Boton, Alerta, Cargando, Insignia, CampoFormulario, DataTable, CrudModulo',
          'src/lib/services/api_<recurso>.js con procesarRespuesta, obtenerX, obtenerXPorId, crearX, actualizarX, eliminarX',
          'src/routes/+layout.svelte con Navbar, <slot /> y Footer; +page.svelte es el inicio; login/ y una carpeta por módulo',
          'vite.config.js: proxy /api → http://localhost:8000 y /api-aux → http://localhost:3000',
          'Mismo formulario para crear y editar (idEditando) y confirm() antes de eliminar']: b(x)
img('47b_arbol_despues_frontend.png', 'árbol del frontend', 5)

h('5. Ejecución local paso a paso')
for x in ['Crear las bases prestamos (PostgreSQL) y prestamos_aux (MySQL) y ejecutar schema.sql y seed.sql de cada API (o python herramientas/cargar_bd.py).',
          'api-fastapi: python -m venv .venv, pip install -r requirements.txt, copiar .env.example a .env, uvicorn app.main:app --reload --port 8000',
          'api-express: npm install, copiar .env.example a .env (misma SECRET_KEY), npm run dev',
          'frontend-svelte: npm install, npm run dev y abrir http://localhost:5173']: d.add_paragraph(x, style='List Number')
for f, pie in [('04a_instalacion_fastapi.png','instalación FastAPI'),('04c_instalacion_frontend.png','instalación frontend'),('06_arranque_fastapi.png','arranque FastAPI'),('07_arranque_express.png','arranque Express'),('08_arranque_frontend.png','arranque SvelteKit'),('10_swagger_fastapi.png','Swagger de FastAPI'),('09_pruebas_endpoints_curl.png','pruebas de endpoints (crear, editar, borrado lógico, JWT compartido, 401/403)')]: img(f, pie)

h('6. Pantallas por rol')
for f, pie in [('11_login_jwt.png','login'),('12_inicio_admin_21_modulos.png','inicio admin'),('13_inicio_coordinador_19_modulos.png','inicio coordinador'),('14_inicio_estudiante_14_modulos.png','inicio estudiante'),('15_admin_moduloxrol.png','permisos por rol'),('16_admin_usuarios.png','usuarios (sin IDs)'),('19_admin_puntos-entrega.png','módulo de la API Express'),('21_coordinador_sanciones.png','sanciones (coordinador)')]: img(f, pie)

h('7. Prueba de la función principal entre roles')
p('Prueba automática con Chrome: Ana publica y edita un objeto; Carlos lo solicita; Ana recibe la notificación, aprueba y entrega; la coordinadora ve el préstamo y el objeto como "Prestado"; Ana registra la devolución. El admin crea, edita y elimina (borrado lógico) una categoría. Todo verificado en la BD.')
for f, pie in [('30_estudiante_crea_objeto_formulario.png','formulario sin IDs'),('33_estudiante2_solicita_prestamo.png','otro estudiante solicita'),('35_estudiante_recibe_notificacion.png','notificación'),('36_estudiante_aprueba_y_entrega.png','aprobar y entregar'),('37_coordinador_ve_prestamo_nuevo.png','reflejado en coordinador'),('41_admin_categoria_eliminada.png','borrado lógico'),('42_responsive_movil.png','vista móvil'),('43_estudiante_sin_permiso_roles.png','ruta no permitida'),('44_resultado_flujo_ui.png','resultado de la prueba'),('45_verificacion_en_bd.png','verificación en la BD'),('26_pruebas_automaticas_apis.png','pruebas automáticas de las APIs')]:
    img(f, pie)

h('8. Versión en la nube')
for x in ['Frontend: https://prestamos-frontend-svelte.onrender.com',
          'API FastAPI: https://api-prestamos-fastapi.onrender.com/docs',
          'API Express: https://api-prestamos-express.onrender.com/api/puntos-entrega/',
          'Repositorio: https://github.com/Pomboea/prestamos-estudiantes','APIs: render.yaml y docs/DESPLIEGUE.md (servicios FastAPI y Express, misma SECRET_KEY).',
          'Frontend: sitio estático. Build: npm install && npm run build. Publicar carpeta build/. Variables VITE_API_URL y VITE_API_AUX_URL. Regla de reescritura /* → /index.html.',
          'Las APIs recrean el esquema con la semilla nueva al arrancar si detectan la anterior (o con FORZAR_SEMILLA=true); también herramientas/recargar_remoto.py.']: b(x)
for f, pie in [('48_nube_inicio_admin.png','nube: inicio admin'),('49_nube_coordinador_puntos_entrega.png','nube: módulo Express'),('50_nube_estudiante_solicitudes.png','nube: solicitudes del estudiante')]: img(f, pie)

h('9. Pendientes y observaciones')
for x in ['En el plan gratuito de Render las APIs se duermen: la primera petición puede tardar ~1 minuto.',
          'El taller indica que no se acepta una base de datos hecha con IA: revise y rehaga/ajuste en Access usted mismo antes de entregar.',
          'devolucion tiene 15 registros y rol 3 (no 20/10) por la lógica del negocio.',
          '"Estructura de la clase 1" para las APIs se interpretó como el documento CRUD (rutas /api/<recurso>/).']: b(x)
d.save(os.path.join(os.path.dirname(__file__), '..', 'Taller1_Corte2_Documentacion.docx'))
print('docx ok')
