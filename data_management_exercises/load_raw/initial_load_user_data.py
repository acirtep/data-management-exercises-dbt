from faker import Faker
import pandas
from utils import get_pg_conn, get_snowflake_conn
from datetime import datetime, timedelta


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

def get_initial_user_df():
    initial_user_data = get_initial_user_data()
    initial_user_data_df = pandas.DataFrame(initial_user_data)
    initial_user_data_df['load_timestamp'] = datetime.now() - timedelta(1)
    return initial_user_data_df


if __name__ == "__main__":
    initial_user_data_df = get_initial_user_df()
    pg_conn = get_pg_conn()
    initial_user_data_df.to_sql(
        name='raw_user_registration_events',
        schema='raw_layer',
        con=pg_conn,
        if_exists='replace',
        index=False
    )
    pg_conn.close()


def load_to_snowflake():
    initial_user_data_df = get_initial_user_df()
    snowflake_conn = get_snowflake_conn()
    initial_user_data_df.to_sql(
        name='raw_user_registration_events',
        schema='raw_layer',
        con=snowflake_conn,
        if_exists='replace',
        index=False
    )
    snowflake_conn.close()