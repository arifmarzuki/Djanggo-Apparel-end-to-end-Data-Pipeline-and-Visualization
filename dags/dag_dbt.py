from airflow import DAG
from datetime import datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount

default_args = {'owner' : 'airflow'}

with DAG(
    dag_id = 'dag_dbt',
    default_args=default_args,
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    start = DummyOperator(task_id="start")

    local_path = "/d/code-repository/capstone-project/transformation" #folder yang ada modelnya
    
    dbt_debug_cmd = DockerOperator(
        task_id='dbt_debug_cmd',
        image='dbt_in_docker_compose',
        container_name='dbt_cont',
        api_version='auto',
        auto_remove=True,
        command="bash -c 'dbt debug'",
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        mounts = [
            Mount(
                source=f"{local_path}", 
                target="/usr/app", 
                type="bind"
            ),
            Mount(
                source=f"{local_path}/profiles",
                target="/root/.dbt",
                type="bind"
            )
        ],
        mount_tmp_dir = False
    )

    dbt_run_cmd = DockerOperator(
        task_id='dbt_run_cmd',
        image='dbt_in_docker_compose',
        container_name='dbt_container',
        api_version='auto',
        auto_remove=True,
        command="bash -c 'dbt --no-partial-parse run'",
        docker_url="tcp://docker-proxy:2375",
        network_mode="bridge",
        mounts = [
            Mount(
                source=f"{local_path}", 
                target="/usr/app", 
                type="bind"
            ),
            Mount(
                source=f"{local_path}/profiles",
                target="/root/.dbt",
                type="bind"
            )
        ],
        mount_tmp_dir = False
    )

    end = DummyOperator(task_id="end")

    start >> dbt_debug_cmd >> dbt_run_cmd >> end 