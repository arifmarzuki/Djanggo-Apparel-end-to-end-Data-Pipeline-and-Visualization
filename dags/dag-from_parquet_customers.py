from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd
from sqlalchemy import MetaData, Table, Column, Text, Integer

def ingest_parquet_to_postgres():
    file_path = ('/opt/airflow/dags/customers.parquet')
    data = pd.read_parquet(file_path)
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    metadata = MetaData()
    tabel = Table(
        'customers',
        metadata,
        Column('customer_id', Integer, primary_key=True),
        Column('first_name', Text),
        Column('last_name', Text),
        Column('gender', Text)
    )
    # pg_hook.run(tabel)
    
    tabel.create(pg_hook.get_sqlalchemy_engine(), checkfirst=True)

    for _, row in data.iterrows():  # _ indikasi unused variable
        insert_query = f"INSERT INTO customers (customer_id, first_name, last_name, gender) VALUES (%s, %s, %s, %s)"
        values = (row['customer_id'], row['first_name'], row['last_name'], row['gender'])
        pg_hook.run(insert_query, autocommit=True, parameters=values)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 4)
}

dag = DAG('ingest_customers', schedule_interval=None, start_date=datetime(2024, 1, 4))

start = DummyOperator(task_id="start")

load_data = PythonOperator(
    task_id='ingest_customers',
    python_callable=ingest_parquet_to_postgres,
    provide_context=True,
    dag=dag,
)

end = DummyOperator(task_id="end")

start >> load_data >> end

