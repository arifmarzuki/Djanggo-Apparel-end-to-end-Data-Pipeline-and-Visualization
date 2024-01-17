from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd

def read_csv_file():
    file_path = '/opt/airflow/dataset/order_details.csv'
    df = pd.read_csv(file_path)
    return df

def load_data_to_postgres():
    # Define connection
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

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
    pg_hook.run(create_table_query)

    data = read_csv_file()

    # Specify the columns to be used as the primary key
    index_columns = ['order_detail_id']

    # Use the to_sql method to insert data into PostgreSQL
    data.to_sql('order_details', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=1000)

    #close connection
    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

dag = DAG(
    '7-ingest_order_details',
    default_args=default_args,
    schedule_interval=None,
    description='A DAG to read CSV file name order_details and ingest into PostgreSQL',
)

read_csv = PythonOperator(
    task_id='read_csv',
    python_callable=read_csv_file,
    provide_context=True,
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_postgres,
    provide_context=True,
    dag=dag,
)
start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

start >> read_csv >> load_data >> end
