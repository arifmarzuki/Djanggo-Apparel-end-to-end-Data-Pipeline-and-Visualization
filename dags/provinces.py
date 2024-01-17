from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def main():
    read_data()
    load_data_to_postgres()

def read_data():
    path = '/opt/airflow/dataset/provinces.xlsx'
    data = pd.read_excel(path)
    return data

def load_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS provinces (
        province_id INT PRIMARY KEY,
        province_names TEXT
    )
    '''
    pg_hook.run(create_table_query)

    data = read_data()

    # Set PK
    index_columns = ['province_id']

    # Load data
    data.to_sql('provinces', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=500)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()
