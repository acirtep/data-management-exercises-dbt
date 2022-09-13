from faker import Faker
import pandas
from utils import get_pg_conn, get_snowflake_conn
from datetime import datetime


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


if __name__ == "__main__":
    pg_conn = get_pg_conn()
    user_data_df = pandas.read_sql(
        'select username, email_address, first_name, created_by, created_timestamp \
        from raw_layer.raw_user_registration_events limit 5;', pg_conn)
    user_data_df = add_updated_attributes(user_data_df)
    user_data_df['load_timestamp'] = datetime.now()
    
    user_data_df.to_sql(
        name='raw_user_registration_events',
        schema='raw_layer',
        con=pg_conn,
        if_exists='append',
        index=False
    )
    pg_conn.close()


def load_updated_to_snowflake():
    snowflake_conn = get_snowflake_conn()
    user_data_df = pandas.read_sql(
        'select username, email_address, first_name, created_by, created_timestamp \
        from raw_layer.raw_user_registration_events limit 5;', snowflake_conn)
    user_data_df = add_updated_attributes(user_data_df)
    user_data_df['load_timestamp'] = datetime.now()
    
    user_data_df.to_sql(
        name='raw_user_registration_events',
        schema='raw_layer',
        con=snowflake_conn,
        if_exists='append',
        index=False
    )
    snowflake_conn.close()
