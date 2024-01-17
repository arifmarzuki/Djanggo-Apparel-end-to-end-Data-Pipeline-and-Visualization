from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def main():
    read_data()
    load_data_to_postgres()

def read_data():
    path = '/opt/airflow/dataset/product_categories.json'
    data = pd.read_json(path)
    return data

def load_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS product_categories (
        product_category_id INT PRIMARY KEY,
        product_category_name TEXT
    );
    '''
    pg_hook.run(create_table_query)

    data = read_data()
    # set PK
    index_columns = ['product_category_id']
    # load data
    data.to_sql('product_categories', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=500)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()
