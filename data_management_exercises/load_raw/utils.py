from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

from settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PWD,
    POSTGRES_USER,
    SNOWFLAKE_PWD,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_USER
)


def get_pg_conn():
    conn_string = f'postgresql://{POSTGRES_USER}:{POSTGRES_PWD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
    db = create_engine(conn_string)
    return db.connect()


def get_snowflake_conn(): 
    conn_string = URL(
        account = SNOWFLAKE_ACCOUNT,
        user = SNOWFLAKE_USER,
        password = SNOWFLAKE_PWD,
        database = 'POC_DBT',
        schema = 'RAW_LAYER',
        warehouse = 'COMPUTE_WH'
    )
    engine = create_engine(conn_string)
    return engine.connect()
