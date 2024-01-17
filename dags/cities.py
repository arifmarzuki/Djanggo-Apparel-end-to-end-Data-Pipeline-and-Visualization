from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def main():
    read_data()
    load_data_to_postgres()

def read_data():
    path = '/opt/airflow/dataset/cities.xlsx'
    data = pd.read_excel(path)
    return data

def load_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS cities (
        city_id INT PRIMARY KEY,
        city_names TEXT,
        province_id INT REFERENCES provinces(province_id)
    )
    '''
    pg_hook.run(create_table_query)

    data = read_data()

    # Set PK
    index_columns = ['city_id']

    # Load Data
    data.to_sql('cities', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=500)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()