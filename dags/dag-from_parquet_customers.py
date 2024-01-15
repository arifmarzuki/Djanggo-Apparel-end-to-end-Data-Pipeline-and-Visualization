from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd

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
    gender TEXT)
    '''
    pg_hook.run(create_table_query)

    for _, row in read_data().iterrows():
        insert_query = "INSERT INTO customers (customer_id, first_name, last_name, gender) VALUES (%s, %s, %s, %s)"
        values = int(row['customer_id']),row['first_name'], row['last_name'], row['gender']
        pg_hook.run(insert_query, autocommit=True, parameters=values)
    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1)
}

dag = DAG(
    '3-ingest_customers',
    default_args=default_args,
    schedule_interval=None,
    description='A DAG to read PARQUET file name cities and ingest into PostgreSQL',
)

read_dataset = PythonOperator(
    task_id='read_data',
    python_callable=read_data,
    dag=dag,
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_postgres,
    dag=dag,
)
start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id='end', dag=dag)

start >> read_dataset >> load_data >> end
