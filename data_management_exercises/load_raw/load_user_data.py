from json import load
from faker import Faker
import pandas
from utils import get_pg_conn
from datetime import datetime, timedelta
import time


def get_initial_user_data():
    fake_user = Faker()
    user_list = []
    for _ in range(25):
        timestamp = fake_user.date_time_between('-10d', '-1d').strftime("%Y-%m-%d %H:%M:%S")
        user_list.append(
            {
                    "username": fake_user.user_name(),
                    "email_address": fake_user.email(),
                    "first_name": fake_user.first_name(),
                    "last_name": fake_user.last_name(),
                    "created_by": "api_v22",
                    "created_timestamp": timestamp,
                    "updated_by": "api_v22",
                    "updated_timestamp": timestamp
            }
        )
    return user_list


def add_updated_attributes(user_data_df):
    fake_user = Faker()
    last_name_list = []
    updated_timestamp_list = []
    for _ in range(5):
        last_name_list.append(fake_user.last_name())
        updated_timestamp_list.append(
            fake_user.date_time_between('-1d').strftime("%Y-%m-%d %H:%M:%S")
        )
    user_data_df['last_name'] = last_name_list
    user_data_df['updated_timestamp'] = updated_timestamp_list
    user_data_df['updated_by'] = 'api_v23'

    return user_data_df


def initial_load_raw_user_data():
    initial_user_data = get_initial_user_data()
    initial_user_data_df = pandas.DataFrame(initial_user_data)
    initial_user_data_df['load_datetime'] = datetime.now() - timedelta(1)
    pg_conn = get_pg_conn()
    initial_user_data_df.to_sql(
        'raw_user_data',
        con=pg_conn,
        if_exists='replace',
        index=False
    )
    pg_conn.close()


def load_updated_data():
    pg_conn = get_pg_conn()
    user_data_df = pandas.read_sql(
        'select username, email_address, first_name, created_by, created_timestamp \
        from public.raw_user_data limit 5;', pg_conn)
    user_data_df = add_updated_attributes(user_data_df)
    user_data_df['load_datetime'] = datetime.now()
    
    user_data_df.to_sql(
        'raw_user_data',
        con=pg_conn,
        if_exists='append',
        index=False
    )
    pg_conn.close()

