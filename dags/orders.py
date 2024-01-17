from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def main():
    read_data()
    load_data_to_postgres()

def read_data():
    path = '/opt/airflow/dataset/orders.csv'
    data = pd.read_csv(path)
    return data


def load_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        order_date TIMESTAMP,
        customer_id INT REFERENCES customers(customer_id),
        province_id INT REFERENCES provinces(province_id),
        city_id INT REFERENCES cities(city_id)
    )
    '''

    pg_hook.run(create_table_query)

    data = read_data()
    # set PK
    index_columns = ['order_id']
    # load data
    data.to_sql('orders', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=1000)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()
