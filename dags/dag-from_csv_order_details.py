from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd
import pathlib
import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.int64, addapt_numpy_int64)

# Instantiate the DAG
with DAG(
    dag_id='ingest_order_details',
    description='A DAG to read csv file name order_details and ingest into PostgreSQL',
    schedule=None,
    start_date=datetime(2024, 1,1),
    catchup=False
) as dag:
    
    start = DummyOperator(task_id="start")
    
    def load_data_to_postgres(ti=None):
        #read dataset
        current_path = pathlib.Path(__file__).absolute()
        path = current_path.parent.joinpath("order_details.csv")
        data = pd.read_csv(path)
        
        # Command untuk proses data ke PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id='pg_conn')
        
        create_table_in_db_task ="""
        CREATE TABLE IF NOT EXISTS order_details (
        order_detail_id INT,
        order_id INT,
        product_id INT,
        qty INT,
        item_price INT,
        unit_sales INT)
        """
        pg_hook.run(create_table_in_db_task)
        
        for index, row in data.iterrows():
            insert_query = """
                    INSERT INTO order_details
                    (order_detail_id, order_id, product_id, qty, item_price, unit_sales)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
            values = (row['order_detail_id'], row['order_id'], row['product_id'], row['qty'], row['item_price'], row['unit_sales'])
            pg_hook.run(insert_query, autocommit=True, parameters=values)
              
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data_to_postgres
    )
    
    end = DummyOperator(task_id="end")
    
start >> load_data >> end
