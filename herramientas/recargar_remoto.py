"""Recarga esquema + semilla del Taller 1 en las BD de la nube (Render PostgreSQL y Railway MySQL).
Las URL se leen de variables de entorno (NUNCA se escriben en el código):
  PG_URL_REMOTA     -> "External Database URL" de Render (postgresql://...)
  MYSQL_URL_REMOTA  -> "MYSQL_PUBLIC_URL" de Railway (mysql://...)
Uso: PG_URL_REMOTA=... MYSQL_URL_REMOTA=... python herramientas/recargar_remoto.py
(requiere: pip install psycopg2-binary pymysql)"""
import os, pathlib, urllib.parse
R = pathlib.Path(__file__).resolve().parent.parent
pg_url = os.getenv('PG_URL_REMOTA'); my_url = os.getenv('MYSQL_URL_REMOTA')
if pg_url:
    import psycopg2
    con = psycopg2.connect(pg_url, sslmode='require'); cur = con.cursor()
    for f in ('schema.sql', 'seed.sql'): cur.execute((R / 'api-fastapi/sql' / f).read_text(encoding='utf-8'))
    con.commit(); cur.execute('SELECT COUNT(*) FROM usuario'); print('PostgreSQL recargada; usuarios:', cur.fetchone()[0])
if my_url:
    import pymysql
    u = urllib.parse.urlparse(my_url)
    con = pymysql.connect(host=u.hostname, port=u.port or 3306, user=urllib.parse.unquote(u.username),
                          password=urllib.parse.unquote(u.password or ''), database=u.path.lstrip('/'),
                          client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)
    cur = con.cursor()
    for f in ('schema.sql', 'seed.sql'):
        cur.execute((R / 'api-express/sql' / f).read_text(encoding='utf-8'))
        while cur.nextset(): pass
    con.commit(); cur.execute('SELECT COUNT(*) FROM punto_entrega'); print('MySQL recargada; puntos:', cur.fetchone()[0])
if not (pg_url or my_url): print('Defina PG_URL_REMOTA y/o MYSQL_URL_REMOTA')
