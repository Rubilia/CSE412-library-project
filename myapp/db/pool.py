import psycopg2
import psycopg2.pool
from flask import current_app, g

def get_db():
    if 'db_pool' not in g:
        g.db_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,
            dsn=current_app.config['DB_DSN']
        )
    return g.db_pool

def get_conn():
    pool = get_db()
    return pool.getconn()

def put_conn(conn):
    pool = get_db()
    pool.putconn(conn)
