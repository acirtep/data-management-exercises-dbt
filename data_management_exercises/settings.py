import os

POSTGRES_HOST = os.environ.get('DBT_POSTGRES_HOST')
POSTGRES_DB = os.environ.get('DBT_POSTGRES_DB')
POSTGRES_USER = os.environ.get('DBT_POSTGRES_USER')
POSTGRES_PWD = os.environ.get('DBT_POSTGRES_PWD')

SNOWFLAKE_USER =  os.environ.get('SNOWFLAKE_USER')
SNOWFLAKE_PWD = os.environ.get('SNOWFLAKE_PWD')
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')