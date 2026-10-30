"""Lee la estructura (tablas, columnas, PK, FK) y los datos de PostgreSQL y MySQL
y los deja en un archivo de texto que lee GenerarAccess.java (Jackcess)."""
import os, psycopg2, pymysql, datetime, decimal

def esc(v):
    if v is None: return '\\N'
    if isinstance(v, bool): return '1' if v else '0'
    if isinstance(v, datetime.datetime): return v.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(v, datetime.date): return v.strftime('%Y-%m-%d 00:00:00')
    if isinstance(v, datetime.timedelta):
        s = int(v.total_seconds()); return f'1899-12-30 {s//3600:02d}:{s%3600//60:02d}:{s%60:02d}'
    if isinstance(v, datetime.time): return '1899-12-30 ' + v.strftime('%H:%M:%S')
    return str(v).replace('\\', '\\\\').replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')

def exportar(salida, cur, tablas_sql, cols_sql, pk_sql, fk_sql, citar):
    with open(salida, 'w', encoding='utf-8') as f:
        cur.execute(tablas_sql); tablas = [r[0] for r in cur.fetchall()]
        for t in tablas:
            cur.execute(pk_sql, (t,)); pks = {r[0] for r in cur.fetchall()}
            cur.execute(cols_sql, (t,)); cols = cur.fetchall()
            f.write(f'T|{t}\n')
            for nombre, tipo, largo, nulo, extra in cols:
                f.write(f'C|{nombre}|{tipo}|{largo or 0}|{1 if nulo in ("YES", True) else 0}|{1 if nombre in pks else 0}|{extra or ""}\n')
            cur.execute(f'SELECT * FROM {citar(t)} ORDER BY 1')
            for fila in cur.fetchall(): f.write('R|' + '\t'.join(esc(v) for v in fila) + '\n')
        cur.execute(fk_sql)
        for padre, cpadre, hija, chija in cur.fetchall(): f.write(f'F|{padre}|{cpadre}|{hija}|{chija}\n')

pg = psycopg2.connect(host='localhost', user=os.getenv('PG_USER', 'prestamos'), password=os.getenv('PG_PASSWORD', 'prestamos'), dbname='prestamos').cursor()
exportar('prestamos.def', pg,
  "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name",
  "SELECT column_name, data_type, character_maximum_length, is_nullable, column_default FROM information_schema.columns WHERE table_schema='public' AND table_name=%s ORDER BY ordinal_position",
  "SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=ANY(i.indkey) WHERE i.indrelid=%s::regclass AND i.indisprimary",
  """SELECT ccu.table_name, ccu.column_name, kcu.table_name, kcu.column_name FROM information_schema.table_constraints tc
     JOIN information_schema.key_column_usage kcu ON tc.constraint_name=kcu.constraint_name
     JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name=ccu.constraint_name
     WHERE tc.constraint_type='FOREIGN KEY' AND tc.table_schema='public' ORDER BY 3,4""", lambda t: '"' + t + '"')
my = pymysql.connect(host='127.0.0.1', user=os.getenv('MYSQL_USER', 'prestamos'), password=os.getenv('MYSQL_PASSWORD', 'prestamos'), database='prestamos_aux').cursor()
exportar('prestamos_aux.def', my,
  "SELECT table_name FROM information_schema.tables WHERE table_schema='prestamos_aux' AND table_type='BASE TABLE' ORDER BY table_name",
  "SELECT column_name, data_type, character_maximum_length, is_nullable, extra FROM information_schema.columns WHERE table_schema='prestamos_aux' AND table_name=%s ORDER BY ordinal_position",
  "SELECT column_name FROM information_schema.key_column_usage WHERE table_schema='prestamos_aux' AND table_name=%s AND constraint_name='PRIMARY'",
  "SELECT referenced_table_name, referenced_column_name, table_name, column_name FROM information_schema.key_column_usage WHERE table_schema='prestamos_aux' AND referenced_table_name IS NOT NULL ORDER BY 3,4",
  lambda t: '`' + t + '`')
print('ok')
