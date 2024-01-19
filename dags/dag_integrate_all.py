from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import sys
sys.path.insert(0,"/root/airflow/dags/")
import product_categories as pc
import products as p
import customers as c
import cities as ci
import provinces as prov
import orders as o
import order_details as od

# Define default arguments for the DAG
default_args = { 
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}
# Define the DAG
dag = DAG(
    'ELT_dag',
    default_args=default_args,
    description='ELT DAG to run many task',
    schedule_interval=None,
)
# Define Task
start_operator = DummyOperator(
    task_id='start_excecution',
    dag=dag,
)

ingest_product_categories= PythonOperator(
    task_id='Extract_and_Load_product_categories',
    python_callable=pc.main,  
    dag=dag,
)

ingest_products= PythonOperator(
    task_id='Extract_and_Load_products',
    python_callable=p.main,  
    dag=dag,
)

ingest_customers= PythonOperator(
    task_id='Extract_and_Load_customers',
    python_callable=c.main,  
    dag=dag,
)

ingest_cities= PythonOperator(
    task_id='Extract_and_Load_cities',
    python_callable=ci.main,  
    dag=dag,
)

ingest_provinces= PythonOperator(
    task_id='Extract_and_Load_provinces',
    python_callable=prov.main,  
    dag=dag,
)

ingest_orders= PythonOperator(
    task_id='Extract_and_Load_orders',
    python_callable=o.main,  
    dag=dag,
)

ingest_order_details= PythonOperator(
    task_id='Extract_and_Load_order_details',
    python_callable=od.main,  
    dag=dag,
)

end_operator = DummyOperator(
    task_id='end_execution',
    dag=dag,
)
# Create Task Dependencies
start_operator >> ingest_product_categories>> ingest_products >> ingest_customers >> ingest_provinces >> ingest_cities >> ingest_orders >> ingest_order_details >> end_operator