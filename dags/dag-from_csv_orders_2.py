from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
import pandas as pd
import pathlib

# Instantiate the DAG
with DAG(
    dag_id='ingest_orders_2',
    description='A DAG to read csv file name order_details and ingest into PostgreSQL',
    schedule=None,
    start_date=datetime(2024, 1,1),
    catchup=False
) as dag:
    
    start = DummyOperator(task_id="start")
    
    create_table_in_db_task = PostgresOperator(
        task_id='create_table_in_db',
        sql=('CREATE TABLE IF NOT EXISTS orders ' +
            '(' +
            'order_id INT,' +
            'order_date TIMESTAMP,' +
            'customer_id INT, ' +
            'province_id INT, ' +
            'city_id INT ' +
            ')'),
        postgres_conn_id='pg_conn',
        autocommit=True,
    )
    
    def load_data_to_postgres(ti=None):
        #read dataset
        current_path = pathlib.Path(__file__).absolute()
        path = current_path.parent.joinpath("orders.csv")
        data = pd.read_csv(path)
        
        insert = """
                INSERT INTO orders
                (order_id, order_date, customer_id, province_id, city_id)
                VALUES (%s, %s, %s, %s, %s)
            """
        # Command untuk proses data ke PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id='pg_conn')
        
        for _, row in data.iterrows():
            values = (row['order_id'], row['order_date'], row['customer_id'], row['province_id'], row['city_id'])
            pg_hook.run(insert, parameters=values)

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data_to_postgres
    )
    
    end = DummyOperator(task_id="end")
    
start >> create_table_in_db_task >> load_data >> end
