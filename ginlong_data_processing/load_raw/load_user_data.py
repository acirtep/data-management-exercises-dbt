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


def get_updated_data(initial_user_data):
    fake_user = Faker()
    user_list = []
    for user in initial_user_data:
        user_list.append(
                        {
                    "username": user['username'],
                    "email_address": user['email_address'],
                    "first_name": user['first_name'],
                    "last_name": fake_user.last_name(),
                    "created_by": "api_v22",
                    "created_timestamp": user['created_timestamp'],
                    "updated_by": "api_v23",
                    "updated_timestamp": fake_user.date_time_between('-5d').strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    return user_list


def initial_load_raw_user_data():
    initial_user_data = get_initial_user_data()
    initial_user_data_df = pandas.DataFrame(initial_user_data)
    initial_user_data_df['inserted_datetime'] = datetime.now() - timedelta(1)
    pg_conn = get_pg_conn()
    initial_user_data_df.to_sql(
        'raw_user_data',
        con=pg_conn,
        if_exists='replace',
        index=False
    )
    pg_conn.close()

    return initial_user_data[12:17]


def load_updated_data(initial_user_data):
    user_data = get_updated_data(initial_user_data)
    user_data_df = pandas.DataFrame(user_data)
    user_data_df['inserted_datetime'] = datetime.now()
    pg_conn = get_pg_conn()
    user_data_df.to_sql(
        'raw_user_data',
        con=pg_conn,
        if_exists='append',
        index=False
    )
    pg_conn.close()


if __name__ == "__main__":
    print("loading initial data")
    initial_user_data = initial_load_raw_user_data()
    print("loading updated data")
    load_updated_data(initial_user_data)
