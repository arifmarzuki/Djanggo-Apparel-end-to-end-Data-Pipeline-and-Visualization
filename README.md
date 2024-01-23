
# Django Apparel's Data Pipelines


## About The Project
This project aims to maximize Django Apparel's marketing and sales strategies by utilizing the data that has been collected. The hope is that along with a focused and efficient strategy design, the Django Apparel platform will be able to increase revenue significantly.


## 🖥️ Tools and Tech

<img alt="Python" src="https://img.shields.io/badge/Python-14354C.svg?logo=python&logoColor=white"></a>
<img alt="Dbeaver" src="https://custom-icon-badges.demolab.com/badge/-Dbeaver-372923?logo=dbeaver-mono&logoColor=white"></a>
<img alt="PostgreSQL" src ="https://img.shields.io/badge/PostgreSQL-316192.svg?logo=postgresql&logoColor=white"></a>
<img alt="DBT" src ="https://img.shields.io/badge/dbt-FF694B.svg?logo=dbt&logoColor=white"></a>
<img alt="Airflow" src ="https://img.shields.io/badge/Airflow-017CEE.svg?logo=Apache-Airflow&logoColor=white">
<img alt="Github" src ="https://img.shields.io/badge/GitHub-181717.svg?logo=GitHub&logoColor=white">
<img alt="Docker" src ="https://img.shields.io/badge/Docker-2496ED.svg?logo=Docker&logoColor=white">
<img alt="Metabase" src ="https://img.shields.io/badge/Metabase-509EE3.svg?logo=Metabase&logoColor=white">
<img alt ="Discord" src ="https://img.shields.io/badge/Discord-5865F2.svg?logo=Discord&logoColor=white">

## 🚀 ELT Process

![App Screenshot](/images/outline.png)
- Perform data retrieval, include orchestration, transformation. i.e., ELT
- Retrieving aggregation data from DB + Excel
- Create visualizations

# 📍 ERD

![App Screenshot](/images/erd.png)

## 🏃 Run Locally

Clone the project

```bash
  git clone https://github.com/CharisChakim/ELT-demo.git
```

run docker compose

```bash
  docker compose up -d
```
You can access airflow at `localhost:8080`

- User: `airflow`
- Password: `airflow`

After logging in, you can set the PostgreSQL connection in the admin tab and name it as 'pg_conn.' Configure it with settings similar to those in the existing configuration in [docker-compose.yaml](https://github.com/CharisChakim/ELT-demo/blob/main/docker-compose.yaml)

You can access metabase at `localhost:3000`
Configure the connection to postgres data warehouse. 

You can trigger DAG in airflow UI to do ELT task to get data into your database, And then you can visualizing data with metabase.

# 💻 Visualization Sample

![App Screenshot](/images/visual.png)


## 🧔 Author
- Charis Chakim [![Github Badge](https://img.shields.io/badge/Github-black?logo=github)](https://github.com/CharisChakim)

- Arif Marzuki  [![Github Badge](https://img.shields.io/badge/Github-black?logo=github)](https://github.com/arifmarzuki)

- Qorina Mumtaza  [![Github Badge](https://img.shields.io/badge/Github-black?logo=github)](https://github.com/qorinamumtaza)







