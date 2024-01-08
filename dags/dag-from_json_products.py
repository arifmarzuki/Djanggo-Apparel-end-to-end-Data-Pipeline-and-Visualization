from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd
import json
from sqlalchemy import MetaData, Table, Column, Integer, Text, VARCHAR

def ingest_json_to_postgres():
    file_path = ('/opt/airflow/dags/products.json')
    data = pd.read_json(file_path)
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')
    
    metadata = MetaData()
    tabel = Table(
        'products',
        metadata,
        Column('product_id', Integer,primary_key=True),
        Column('product_name', Text),
        Column('size', Text),
        Column('price', Integer),
        Column('product_category_id', Integer)
    )
    # pg_hook.run(tabel)
    
    tabel.create(pg_hook.get_sqlalchemy_engine(), checkfirst=True)

    for _, row in data.iterrows():  # _ indikasi unused variable
        insert_query = f"INSERT INTO products (product_id, product_name, size, price, product_category_id) VALUES (%s, %s, %s, %s, %s)"
        values = (row['product_id'], row['product_name'], row['size'], row['price'], row['product_category_id'])
        pg_hook.run(insert_query, autocommit=True, parameters=values)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 4)
}

dag = DAG('ingest_products', schedule_interval=None, start_date=datetime(2024, 1, 4))

start = DummyOperator(task_id="start")

load_data = PythonOperator(
    task_id='ingest_products',
    python_callable=ingest_json_to_postgres,
    provide_context=True,
    dag=dag,
)

end = DummyOperator(task_id="end")

start >> load_data >> end

