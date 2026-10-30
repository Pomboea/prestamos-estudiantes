"""Recrea las dos bases locales ejecutando schema.sql + seed.sql (sin necesidad de psql/mysql CLI)."""
import os, pathlib, psycopg2, pymysql
R = pathlib.Path(__file__).resolve().parent.parent
pg = psycopg2.connect(host='localhost', port=5432, user=os.getenv('PG_USER', 'prestamos'), password=os.getenv('PG_PASSWORD', 'prestamos'), dbname='prestamos'); pg.autocommit = True
c = pg.cursor(); c.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')
for f in ('schema.sql', 'seed.sql'): c.execute((R / 'api-fastapi/sql' / f).read_text())
my = pymysql.connect(host='127.0.0.1', user=os.getenv('MYSQL_USER', 'prestamos'), password=os.getenv('MYSQL_PASSWORD', 'prestamos'), client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)
mc = my.cursor(); mc.execute('DROP DATABASE IF EXISTS prestamos_aux'); mc.execute('CREATE DATABASE prestamos_aux CHARACTER SET utf8mb4'); mc.execute('USE prestamos_aux')
for f in ('schema.sql', 'seed.sql'):
    mc.execute((R / 'api-express/sql' / f).read_text())
    while mc.nextset(): pass
my.commit(); print('bases recreadas')
