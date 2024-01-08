from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd


def load_data_to_postgres():
 
    path = '/opt/airflow/dags/provinces.xlsx'
    df = pd.read_excel(path)

    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS provinces (
        province_id SERIAL PRIMARY KEY,
        province_names VARCHAR(255)
    );
    '''

    pg_hook.run(create_table_query)

    for index, row in df.iterrows():
        insert_query = "INSERT INTO provinces (province_names) VALUES (%s)"
        values = (row['province_names'],)
        pg_hook.run(insert_query, autocommit=True, parameters=values)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1)
}

dag = DAG(
    'ingest_province',
    default_args=default_args,
    schedule_interval=None,
    description='A DAG to read xlsx file name province and ingest into PostgreSQL',
)

load_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_postgres,
    dag=dag,
)
start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id="end", dag=dag)


start >> load_data >> end


