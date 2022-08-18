from sqlalchemy import create_engine

from settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PWD,
    POSTGRES_USER,
)


def get_pg_conn():
    conn_string = f'postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
    db = create_engine(conn_string)
    return db.connect()