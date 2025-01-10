from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 1)
}

# Define the DAG
dag = DAG('postgres_conn', default_args=default_args, schedule_interval=None)

# Function to create the table
def create_table_raw_payments():
    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_conn')
    sql = """
    CREATE TABLE IF NOT EXISTS public.raw_payments (
        id INTEGER,
        order_id INTEGER,
        payment_method VARCHAR(100),
        amount INTEGER
    );
    """
    postgres_hook.run(sql)  # for executing the query

def create_table_raw_customers():
    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_conn')
    sql = """
    CREATE TABLE IF NOT EXISTS public.raw_customers (
        id INTEGER,
        first_name VARCHAR(100),
        last_name VARCHAR(100)
    );
    """
    postgres_hook.run(sql) 

def create_table_raw_orders():
    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_conn')
    sql = """
    CREATE TABLE IF NOT EXISTS public.raw_orders (
        id INTEGER,
        user_id INTEGER,
        order_date DATE,
        status VARCHAR(100)
    );
    """
    postgres_hook.run(sql) 

# Function to load data from CSV using \COPY

def load_data_raw_payments():
    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_conn')
    sql = """
    COPY public.raw_payments(id, order_id, payment_method, amount) 
    FROM '/tmp/raw_payments.csv' DELIMITER ',' QUOTE '"' CSV HEADER;
    """
    postgres_hook.run(sql) 

def load_data_raw_customers():
    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_conn')
    sql = """
    COPY public.raw_customers(id,first_name,last_name) 
    FROM '/tmp/raw_customers.csv' DELIMITER ',' QUOTE '"' CSV HEADER;
    """
    postgres_hook.run(sql)  

def load_data_raw_orders():
    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_conn')
    sql = """
    COPY public.raw_orders(id,user_id,order_date,status) 
    FROM '/tmp/raw_orders.csv' DELIMITER ',' QUOTE '"' CSV HEADER;
    """
    postgres_hook.run(sql) 

# PythonOperator to create table and load data
query_task_1 = PythonOperator(
    task_id='create_table_raw_payments',
    python_callable=create_table_raw_payments,
    dag=dag
)

task_branch_1 = PythonOperator(
    task_id='load_data_raw_payments',
    python_callable=load_data_raw_payments,
    dag=dag
)

query_task_2 = PythonOperator(
    task_id='create_table_raw_customers',
    python_callable=create_table_raw_customers,
    dag=dag
)

task_branch_2 = PythonOperator(
    task_id='load_data_raw_customers',
    python_callable=load_data_raw_customers,
    dag=dag
)

query_task_3 = PythonOperator(
    task_id='create_table_raw_orders',
    python_callable=create_table_raw_orders,
    dag=dag
)

task_branch_3 = PythonOperator(
    task_id='load_data_raw_orders',
    python_callable=load_data_raw_orders,
    dag=dag
)

# EmptrOperator is an empty task to define a start and end task in a DAG.
start = EmptyOperator(task_id="start")

end = EmptyOperator(task_id="end")

# [query_task_1, query_task_2, query_task_3]: 
# will executed in parallel immediately after the start task.
# it has dependency where the start task must run successfully 
# before query_task_1, query_task_2, and query_task_3

start >> [query_task_1, query_task_2, query_task_3]

query_task_1 >> task_branch_1
query_task_2 >> task_branch_2
query_task_3 >> task_branch_3

[task_branch_1, task_branch_2, task_branch_3] >> end
