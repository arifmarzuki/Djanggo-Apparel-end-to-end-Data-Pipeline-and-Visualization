from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def main():
    read_data()
    load_data_to_postgres()

def read_data():
    path = '/opt/airflow/dataset/products.json'
    data = pd.read_json(path)
    return data

def load_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY,
        product_name TEXT,
        size TEXT,
        price INT,
        product_category_id INT REFERENCES product_categories(product_category_id)
    );
    '''
    pg_hook.run(create_table_query)

    data = read_data()

    # Set PK
    index_columns = ['product_id']

    # load data
    data.to_sql('products', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=500)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()
