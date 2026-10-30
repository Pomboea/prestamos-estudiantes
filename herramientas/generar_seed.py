"""Genera sql/seed.sql (PostgreSQL) y sql/seed.sql (MySQL) con 20 registros en tablas principales
y 10 en tablas secundarias (catálogos), según el Taller 1 - Corte 2."""
import random, datetime as dt, pathlib
random.seed(7)
R = pathlib.Path(__file__).resolve().parents[1]
H_ADMIN = '$2b$12$aWUqdIj5Wpm5gVUwYBQUfuYFLzcVtYqbZVwBwJNcDIYGRI5PVoTn.'
H_EST = '$2b$12$UWPN5ujVE5wven/vqvFc2uXQJaWyyiuarPSufOmbr.3fzFL7DO1kS'
H_COO = '$2b$12$UqVnduRJmANur1uTrvAEZOW6syhG3MP1UqixG7PB/oeAvGLfkSKF6'
q = lambda v: 'NULL' if v is None else ("TRUE" if v is True else "FALSE" if v is False else (str(v) if isinstance(v,(int,float)) else "'" + str(v).replace("'", "''") + "'"))
def ins(t, cols, rows):
    return f"INSERT INTO {t} ({', '.join(cols)}) VALUES\n" + ",\n".join(" (" + ", ".join(q(v) for v in r) + ")" for r in rows) + ";\n\n"
o = ["-- Semilla Taller 1 Corte 2. Contraseñas: admin Admin123* | coordinadores Coordinador123* | estudiantes Estudiante123*\n"
     "-- Tablas principales: 20 registros. Tablas secundarias (catálogos): 10 registros. rol: 3 (los tres roles del sistema).\n\n"]
o.append(ins('rol', ['nombre','descripcion'], [('admin','Administrador del sistema'),('coordinador','Coordinador de Bienestar Universitario: supervisa préstamos, sanciones y catálogos'),('estudiante','Estudiante que presta y solicita objetos')]))
mods = [('roles','/roles','Gestión de roles'),('modulos','/modulos','Gestión de módulos'),('permisos','/moduloxrol','Permisos rol-módulo'),('usuarios','/usuarios','Gestión de usuarios'),('facultades','/facultades','Facultades'),('programas','/programas','Programas académicos'),('categorias','/categorias','Categorías de objetos'),('condiciones','/condiciones','Condiciones físicas del objeto'),('objetos','/objetos','Objetos publicados'),('imagenes','/imagenes','Imágenes de objetos'),('estados_solicitud','/estados-solicitud','Estados de solicitud'),('solicitudes','/solicitudes','Solicitudes de préstamo'),('prestamos','/prestamos','Préstamos'),('devoluciones','/devoluciones','Devoluciones'),('calificaciones','/calificaciones','Calificaciones entre estudiantes'),('notificaciones','/notificaciones','Notificaciones'),('sanciones','/sanciones','Sanciones'),
        ('puntos_entrega','/puntos-entrega','Puntos de entrega (API Express)'),('horarios','/horarios','Horarios de atención (API Express)'),('tipos_incidencia','/tipos-incidencia','Tipos de incidencia (API Express)'),('reportes_incidencia','/reportes-incidencia','Reportes de incidencia (API Express)')]
o.append(ins('modulo',['nombre','ruta','descripcion'],mods))
o.append("""-- Permisos (moduloxrol). El menú del frontend se carga SOLO desde esta tabla.
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 1, id_modulo, TRUE, TRUE, TRUE, TRUE FROM modulo;
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 2, id_modulo, TRUE,
  nombre IN ('facultades','programas','categorias','condiciones','sanciones','notificaciones','puntos_entrega','horarios','tipos_incidencia','reportes_incidencia'),
  nombre IN ('facultades','programas','categorias','condiciones','sanciones','notificaciones','puntos_entrega','horarios','tipos_incidencia','reportes_incidencia','usuarios'),
  nombre IN ('facultades','programas','categorias','condiciones','sanciones','puntos_entrega','horarios','tipos_incidencia','reportes_incidencia')
FROM modulo WHERE nombre NOT IN ('modulos','permisos');
INSERT INTO moduloxrol (id_rol, id_modulo, puede_leer, puede_crear, puede_actualizar, puede_eliminar)
SELECT 3, id_modulo, TRUE,
  nombre IN ('objetos','imagenes','solicitudes','prestamos','devoluciones','calificaciones','reportes_incidencia'),
  nombre IN ('objetos','imagenes','solicitudes','notificaciones','calificaciones','reportes_incidencia'),
  nombre IN ('objetos','imagenes','solicitudes','calificaciones','reportes_incidencia')
FROM modulo WHERE nombre IN ('categorias','condiciones','estados_solicitud','objetos','imagenes','solicitudes','prestamos','devoluciones','calificaciones','notificaciones','sanciones','puntos_entrega','horarios','reportes_incidencia');

""")
fac = ['Ingeniería','Ciencias Económicas y Administrativas','Ciencias de la Salud','Ciencias Básicas','Derecho y Ciencias Políticas','Educación','Arquitectura y Diseño','Ciencias Sociales y Humanas','Comunicación','Artes']
o.append(ins('facultad',['nombre'],[(f,) for f in fac]))
progs = [('ING-SIS','Ingeniería de Sistemas',1),('ING-IND','Ingeniería Industrial',1),('ECO-ADM','Administración de Empresas',2),('SAL-ENF','Enfermería',3),('BAS-MAT','Matemáticas',4),('DER-DER','Derecho',5),('EDU-LIC','Licenciatura en Informática',6),('ARQ-ARQ','Arquitectura',7),('SOC-PSI','Psicología',8),('COM-SOC','Comunicación Social',9)]
o.append(ins('programa_academico',['codigo','nombre','id_facultad'],progs))
nombres = [('Ana','Gómez'),('Carlos','Pérez'),('Valentina','Rodríguez'),('Santiago','Martínez'),('Daniela','López'),('Andrés','Herrera'),('Camila','Torres'),('Juan Pablo','Ramírez'),('María José','Castro'),('Sebastián','Morales'),('Laura','Vargas'),('Mateo','Rojas'),('Isabella','Jiménez'),('Felipe','Ortiz'),('Sofía','Mendoza'),('Diego','Cárdenas'),('Paula','Navarro'),('Nicolás','Guerrero'),('Mariana','Salazar'),('Julián','Pineda')]
usuarios = [('Admin','Sistema','admin@uni.edu.co',None,'3000000000',H_ADMIN,1,None),
            ('Patricia','Restrepo','patricia.restrepo@uni.edu.co',None,'3015550101',H_COO,2,None),
            ('Hernán','Villa','hernan.villa@uni.edu.co',None,'3015550102',H_COO,2,None)]
def correo(n,a):
    import unicodedata
    s = (n.split()[0]+'.'+a).lower()
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c)!='Mn')+'@uni.edu.co'
for i,(n,a) in enumerate(nombres):
    c = 'ana@uni.edu.co' if i==0 else 'carlos@uni.edu.co' if i==1 else correo(n,a)
    usuarios.append((n,a,c,f'20210{i+1:02d}',f'30{random.randint(10,29)}{random.randint(1000000,9999999)}',H_EST,3,(i%10)+1))
o.append(ins('usuario',['nombres','apellidos','correo','codigo_estudiantil','telefono','contrasena_hash','id_rol','id_programa'],usuarios))
cats = [('Calculadoras','Calculadoras científicas y gráficas'),('Libros','Libros y textos académicos'),('Cargadores','Cargadores de portátil y celular'),('Computadores','Portátiles y tabletas'),('Audífonos','Audífonos y diademas'),('Materiales de laboratorio','Batas, gafas y kits de laboratorio'),('Instrumentos de dibujo','Escuadras, compases y reglas'),('Equipos deportivos','Balones, raquetas y conos'),('Instrumentos musicales','Guitarras, teclados y flautas'),('Accesorios tecnológicos','Mouse, USB, adaptadores HDMI')]
o.append(ins('categoria_objeto',['nombre','descripcion'],cats))
conds = [('Nuevo','Sin uso'),('Como nuevo','Usado una o dos veces'),('Excelente','Sin marcas de uso'),('Muy bueno','Marcas mínimas'),('Bueno','Uso normal sin daños'),('Aceptable','Funciona, con desgaste'),('Regular','Desgaste visible'),('Desgastado','Desgaste fuerte'),('Con fallas','Funciona parcialmente'),('Dañado','Presenta daños')]
o.append(ins('condicion_objeto',['nombre','descripcion'],conds))
ests = ['Pendiente','Aprobada','Rechazada','Cancelada','Finalizada','En revisión','Entregada','Vencida','Devuelta','Expirada']
o.append(ins('estado_solicitud',['nombre'],[(e,) for e in ests]))
objs = [('Calculadora Casio fx-991LA','Científica, con estuche',1),('Cálculo de Stewart 8va ed.','Cálculo diferencial e integral',2),('Cargador Lenovo 65W','USB-C punta delgada',3),('Audífonos JBL Tune 510BT','Bluetooth',5),('Portátil HP 14"','Intel i5, 8 GB RAM',4),('Bata de laboratorio talla M','Manga larga, blanca',6),('Juego de escuadras Faber-Castell','45° y 60°',7),('Balón de voleibol Mikasa','Tamaño oficial',8),('Guitarra acústica Yamaha C40','Con forro',9),('Mouse Logitech M170','Inalámbrico',10),
        ('Calculadora TI-84 Plus','Gráfica',1),('Física de Serway 10ma ed.','Tomo 1',2),('Cargador Samsung 25W','USB-C carga rápida',3),('Diadema Sony WH-CH520','Bluetooth',5),('Tablet Samsung Galaxy Tab A8','10.5 pulgadas',4),('Gafas de seguridad','Policarbonato',6),('Compás Staedtler Mars','Con adaptador',7),('Raqueta de tenis de mesa','Con 3 pelotas',8),('Teclado Casio CT-S1','61 teclas',9),('Adaptador HDMI a USB-C','4K',10)]
# los 5 primeros préstamos quedan activos -> esos objetos NO disponibles
rows=[]
for i,(n,d,c) in enumerate(objs):
    rows.append((f'OBJ-{i+1:04d}',n,d,c,random.choice([1,2,3,5]),4+(i%20),i>=5))
o.append(ins('objeto',['codigo','nombre','descripcion','id_categoria','id_condicion','id_propietario','disponible'],rows))
o.append(ins('imagen_objeto',['id_objeto','url'],[(i+1,f'https://picsum.photos/seed/obj{i+1}/400/300') for i in range(20)]))
# 20 solicitudes con préstamo (5 activas Aprobada, 15 Finalizada) -> 20 préstamos; 15 devoluciones + 5 más? (devolución requiere préstamo cerrado)
hoy = dt.date(2026,10,29)
sols=[]; pres=[]; devs=[]; cals=[]
for i in range(20):
    obj=i+1; dueno=4+(i%20); sol=4+((i+7)%20)
    ini = hoy-dt.timedelta(days=60-2*i) if i>=5 else hoy-dt.timedelta(days=3+i)
    fin = ini+dt.timedelta(days=7)
    sols.append((f'SOL-{i+1:04d}',obj,sol,2 if i<5 else 5,ini,fin,f'Hola, necesito el objeto para {random.choice(["un parcial","un laboratorio","una exposición","un proyecto","estudiar"])}'))
    pres.append((i+1,f'{ini} 10:00',fin,5,'Entregado en Biblioteca Central'))
for i in range(5,20):
    devs.append((i+1,f'{sols[i][5]} 16:00',5 if i%4 else 7,'Devuelto a tiempo' if i%4 else 'Devuelto con desgaste'))
o.append(ins('solicitud_prestamo',['codigo','id_objeto','id_solicitante','id_estado_solicitud','fecha_inicio_deseada','fecha_fin_deseada','mensaje'],sols))
o.append(ins('prestamo',['id_solicitud','fecha_prestamo','fecha_devolucion_esperada','id_condicion_entrega','observaciones'],pres))
o.append(ins('devolucion',['id_prestamo','fecha_devolucion','id_condicion_devolucion','observaciones'],devs))
coms=['Muy puntual y cuidadoso','Excelente trato','Devolvió en buen estado','Recomendado','Algo de retraso pero cumplió']
for k in range(20):
    i = 5+(k%15); s=sols[i]; dueno=4+(i%20); solic=s[2]
    ev,ed = (dueno,solic) if k<15 else (solic,dueno)
    cals.append((i+1,ev,ed,random.choice([4,5,5,3]),random.choice(coms)))
o.append(ins('calificacion',['id_prestamo','id_evaluador','id_evaluado','puntaje','comentario'],cals))
o.append(ins('notificacion',['codigo','id_usuario','titulo','mensaje','leida'],[(f'NOT-{i+1:04d}',4+i,'Bienvenida','Bienvenido(a) al sistema de préstamos entre estudiantes',i%2==0) for i in range(20)]))
sanc=[]
for k in range(20):
    i=5+(k%15); u=sols[i][2]
    ini=hoy-dt.timedelta(days=120-k*3); sanc.append((f'SAN-{k+1:04d}',u,i+1,random.choice(['Devolución tardía','Objeto devuelto con desgaste','Incumplimiento de horario de entrega']),ini,ini+dt.timedelta(days=15)))
o.append(ins('sancion',['codigo','id_usuario','id_prestamo','motivo','fecha_inicio','fecha_fin'],sanc))
(R/'api-fastapi/sql/seed.sql').write_text(''.join(o),encoding='utf-8')

# ---- MySQL
m=["SET NAMES utf8mb4;\n-- Semilla API Express (MySQL). 10 en secundarias, 20 en principales.\n\n"]
qm=lambda v: 'NULL' if v is None else (str(v) if isinstance(v,int) else "'"+str(v).replace("'","''")+"'")
def insm(t,cols,rows): return f"INSERT INTO {t} ({', '.join(cols)}) VALUES\n"+",\n".join(" ("+", ".join(qm(v) for v in r)+")" for r in rows)+";\n\n"
pts=[('PE-BIB','Biblioteca Central','Primer piso, junto a préstamo externo','Sede Principal'),('PE-ING','Bloque de Ingeniería','Lobby bloque B','Sede Principal'),('PE-CAF','Cafetería Norte','Mesa de bienestar','Sede Norte'),('PE-BIE','Oficina de Bienestar','Segundo piso, bloque A','Sede Principal'),('PE-LAB','Laboratorios de Ciencias','Recepción laboratorios','Sede Principal'),('PE-DEP','Coliseo deportivo','Taquilla','Sede Deportiva'),('PE-ART','Bloque de Artes','Recepción','Sede Centro'),('PE-SAL','Bloque de Salud','Recepción primer piso','Sede Salud'),('PE-ADM','Edificio Administrativo','Ventanilla 3','Sede Principal'),('PE-POS','Bloque de Posgrados','Lobby','Sede Centro')]
m.append(insm('punto_entrega',['codigo','nombre','ubicacion','sede'],pts))
hor=[(p,d,'07:00','19:00' if d<6 else '12:00') for p in range(1,11) for d in (1,6)]
m.append(insm('horario_atencion',['id_punto','dia_semana','hora_apertura','hora_cierre'],hor))
tip=[('Daño del objeto','alta'),('Pérdida','alta'),('Retraso en devolución','media'),('Objeto incompleto','media'),('Objeto sucio','baja'),('Accesorio faltante','media'),('Falla eléctrica','alta'),('Uso indebido','alta'),('No se presentó a la entrega','baja'),('Otro','baja')]
m.append(insm('tipo_incidencia',['nombre','gravedad'],tip))
desc=['El objeto se devolvió con retraso','Falta el estuche','Presenta rayones nuevos','El cargador no enciende','Se devolvió sucio']
rep=[(f'INC-{k+1:04d}',random.randint(1,10),random.randint(1,10),5+(k%15)+1,4+((5+(k%15)+7)%20),random.choice(desc),k%3==0) for k in range(20)]
m.append(insm('reporte_incidencia',['codigo','id_tipo','id_punto','id_prestamo','id_usuario_reporta','descripcion','resuelto'],[(a,b,c,d,e,f,1 if g else 0) for a,b,c,d,e,f,g in rep]))
(R/'api-express/sql/seed.sql').write_text(''.join(m),encoding='utf-8')
print('ok')
