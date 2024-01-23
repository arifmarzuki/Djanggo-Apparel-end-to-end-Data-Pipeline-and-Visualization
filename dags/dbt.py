from airflow import DAG
from datetime import datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount

default_args = {'owner' : 'airflow'} # Define default arguments for the DAG

# Define the DAG
with DAG(
    dag_id = 'dag_dbt',
    default_args=default_args,
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    start = DummyOperator(task_id="start")
    # Set DBT/data model path
    local_path = "/c/Users/USER/GIT/SoloLearn/ELT-demo/transformation" #Ganti sesuai dengan folder yang ada folder model
    
    # Define a DockerOperator for running the dbt debug command
    dbt_debug = DockerOperator(
        task_id='dbt_debug',                    # Unique identifier for the task
        image='dbt_in_docker_compose',          # Docker image to use
        container_name='dbt_container',         # Name of the Docker container
        api_version='auto',                     # Docker API version
        auto_remove=True,                       # Automatically remove the container after execution
        command="bash -c 'dbt debug'",          # Command to run inside the Docker container
        docker_url="tcp://docker-proxy:2375",   # Docker daemon URL
        network_mode="bridge",                  # Network mode for the container
        mounts = [                              # Define mounts to share volumes between host and container
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
        mount_tmp_dir = False                    # Disable mounting temporary directories
    )

    # DockerOperator for running the dbt run command
    dbt_run = DockerOperator(
        task_id='dbt_run',
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
    
    # DockerOperator for running the dbt test command
    dbt_test = DockerOperator(
        task_id='dbt_test',
        image='dbt_in_docker_compose',
        container_name='dbt_container',
        api_version='auto',
        auto_remove=True,
        command="bash -c 'dbt test'",
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
    
# Set Task Dependencies
start >> dbt_debug >> dbt_run >> dbt_test >> end 