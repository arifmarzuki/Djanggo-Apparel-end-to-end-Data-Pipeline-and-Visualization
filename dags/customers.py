from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def main():
    read_data()
    load_data_to_postgres()

def read_data():
    path = '/opt/airflow/dataset/customers.parquet'
    data = pd.read_parquet(path)
    return data

def load_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        gender TEXT
    )
    '''
    pg_hook.run(create_table_query)

    data = read_data()

    # Set PK
    index_columns = ['customer_id']

    # Load data
    data.to_sql('customers', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=500)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()
