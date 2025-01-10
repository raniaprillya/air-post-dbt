# air-post-dbt

This is a random project which a data pipeline that orchestrates workflows using Airflow, stores data in a PostgreSQL database, and performs transformations using DBT (Data Build Tool). The pipeline will automate the extraction, loading, and transformation of random data, providing an end-to-end solution for data processing and analysis.

## Requirements

1. Airflow for workflow orchestration and task scheduling.
2. Postgre as the database to store and manage data.
3. DBT to transforms the data within the database.
** i'm using jaffle_shop which reserved by dbt example project for exploring the basic functionality and latest features of dbt. It's based on a fictional restaurant called the Jaffle Shop that serves jaffles.
[source](https://github.com/dbt-labs/jaffle-shop)

## Installation
1. Airflow Setup

```bash
pip install apache-airflow
```

Next, initialize the Airflow database:

```bash
airflow db init
```

Start the Airflow webserver:

```bash
airflow standalone
```

Make sure to set the Airflow home directory:

```bash
export AIRFLOW_HOME=~/apps/airflow-local
```

Create a dags folder inside the Airflow home directory, and configure the dags_folder in your airflow.cfg file:
dags_folder = /home/user/apps/airflow-local/dags
Place your DAG files in the dags folder.

2. PostgreSQL Setup
Install PostgreSQL and related dependencies:
```bash
sudo apt install postgresql postgresql-contrib libpq-dev
Start PostgreSQL service
sudo service postgresql start
```

3. DBT Setup
Install DBT and the necessary PostgreSQL adapter:

```bash
pip install dbt-core dbt-postgres
```

Now, initialize your DBT project:

```bash
mkdir dbt
cd dbt
dbt init projectname
```

run DBT transformations:

```bash
dbt run
```

Usage
After completing the installation, you can start the data pipeline by triggering Airflow to execute your tasks. Airflow will handle the orchestration of data extraction, loading into PostgreSQL, and then DBT will apply transformations to prepare the data for analysis.
