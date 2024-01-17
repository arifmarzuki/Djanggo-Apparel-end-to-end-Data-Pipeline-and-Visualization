from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd

def read_data():
    path = '/opt/airflow/dataset/orders.csv'
    data = pd.read_csv(path)
    return data


def load_data_to_postgres():
    pg_hook = PostgresHook(postgres_conn_id='pg_conn')

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        order_date TIMESTAMP,
        customer_id INT REFERENCES customers(customer_id),
        province_id INT REFERENCES provinces(province_id),
        city_id INT REFERENCES cities(city_id)
    )
    '''

    pg_hook.run(create_table_query)

    data = read_data()
    # set PK
    index_columns = ['order_id']
    # load data
    data.to_sql('orders', con=pg_hook.get_sqlalchemy_engine(), index=False, if_exists='append', method='multi', chunksize=1000)

    pg_hook.get_conn().commit()
    pg_hook.get_conn().close()

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

dag = DAG(
    '6-ingest_orders',
    default_args=default_args,
    schedule_interval=None,
    description='A DAG to read JSON file name cities and ingest into PostgreSQL',
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
