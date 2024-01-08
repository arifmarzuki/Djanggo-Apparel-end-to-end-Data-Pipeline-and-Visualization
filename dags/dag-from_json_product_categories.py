from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd
from sqlalchemy import MetaData, Table, Column, Text, Integer

def ingest_json_to_postgres():
    file_path = ('/opt/airflow/dags/product_categories.json')
    data = pd.read_json(file_path)
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    metadata = MetaData()
    tabel = Table(
        'product_categories',
        metadata,
        Column('product_category_id', Integer,primary_key=True),
        Column('product_category_name', Text)
    )
    # pg_hook.run(tabel)
    
    tabel.create(pg_hook.get_sqlalchemy_engine(), checkfirst=True)

    for _, row in data.iterrows():  # _ indikasi unused variable
        insert_query = f"INSERT INTO product_categories (product_category_id, product_category_name) VALUES (%s, %s)"
        values = (row['product_category_id'], row['product_category_name'])
        pg_hook.run(insert_query, autocommit=True, parameters=values)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 4)
}

dag = DAG('ingest_product_categories', schedule_interval=None, start_date=datetime(2024, 1, 4))

start = DummyOperator(task_id="start")

load_data = PythonOperator(
    task_id='ingest_productcategories',
    python_callable=ingest_json_to_postgres,
    provide_context=True,
    dag=dag,
)

end = DummyOperator(task_id="end")

start >> load_data >> end

