from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd
import pathlib
import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_datetime64(numpy_datetime64):
    return AsIs(numpy_datetime64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.datetime64, addapt_numpy_datetime64)
register_adapter(numpy.int64, addapt_numpy_int64)

# Instantiate the DAG
with DAG(
    dag_id='ingest_orders',
    description='A DAG to read csv file name order_details and ingest into PostgreSQL',
    schedule=None,
    start_date=datetime(2024, 1,1),
    catchup=False
) as dag:
    
    start = DummyOperator(task_id="start")
    
    def load_data_to_postgres(ti=None):
        #read dataset
        current_path = pathlib.Path(__file__).absolute()
        path = current_path.parent.joinpath("orders.csv")
        data = pd.read_csv(path)
        
        # Command untuk proses data ke PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id='pg_conn')
        
        create_table_in_db_task ="""
            CREATE TABLE IF NOT EXISTS orders (
            order_id INT,
            order_date TIMESTAMP,
            customer_id INT,
            province_id INT,
            city_id INT)
        """
        pg_hook.run(create_table_in_db_task)
        
        for index, row in data.iterrows():
            insert_query = """
                    INSERT INTO orders
                    (order_id, order_date, customer_id, province_id, city_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """
            values = (row['order_id'], row['order_date'], row['customer_id'], row['province_id'], row['city_id'])
            pg_hook.run(insert_query, autocommit=True, parameters=values)
              
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data_to_postgres
    )
    
    end = DummyOperator(task_id="end")
    
start >> load_data >> end
