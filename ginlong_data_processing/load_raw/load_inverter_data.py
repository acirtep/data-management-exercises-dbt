import random
from datetime import date, datetime, timedelta
import pandas
from load_raw.utils import get_pg_conn


def generate_inverter_data(start_date, end_date):
    
    record_list = []

    while start_date <= end_date:
        start_datetime = datetime(
            start_date.year, start_date.month, start_date.day, 
            random.randrange(6, 8), random.randrange(0, 59), random.randrange(0, 59)
        )
        start_kwh = 0.0
        record_list.append([start_datetime, start_kwh])
        for i in range(1, random.randrange(2, 15)):
            record_list.append(
                [
                    start_datetime+timedelta(minutes=i*45), 
                    round(i*random.uniform(1.10, 1.15), 2)
                ]
            )
        start_date = start_date + timedelta(1)
     
    return record_list


def initial_inverter_daily_log(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    random_data = generate_inverter_data(start_date, end_date)
    random_data_df = pandas.DataFrame(
        random_data, 
        columns=['register_time', 'produced_since_morning_til_register_time']
    )
    random_data_df['inverter_serial_number'] = 'AB12345'
    random_data_df['inserted_datetime'] = datetime.now()
    pg_conn = get_pg_conn()
    random_data_df.to_sql(
        'inverter_daily_log',
        con=pg_conn,
        if_exists='replace',
        index=False
    )
    pg_conn.close()

    return len(random_data_df)
