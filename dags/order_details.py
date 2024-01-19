from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

#  Main function that orchestrates the Extract and Load process, so this scripts can be callabe
def main():
    read_data()
    load_data_to_postgres()

def read_data():
    file_path = '/opt/airflow/dataset/order_details.csv'
    df = pd.read_csv(file_path)
    return df

def load_data_to_postgres():
    # Get postgres connection from airflow
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')
    
    # Define SQL script to create table in postgres
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS order_details (
        order_detail_id INT PRIMARY KEY,
        order_id INT REFERENCES orders(order_id),
        product_id INT REFERENCES products(product_id),
        qty INT,
        item_price INT,
        unit_sales INT
    )
    '''
    # Execute SQL scripts
    pg_hook.run(create_table_query)

    data = read_data()

    # Specify the columns to be used as the primary key
    index_columns = ['order_detail_id']

    # Use the to_sql method to insert data into PostgreSQL
    data.to_sql('order_details', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=1000)

    #close connection
    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()
