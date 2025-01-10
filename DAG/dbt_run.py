# Define the default arguments for the DAG
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
}

# Create the DAG with the specified schedule interval
# this will will run 1 day after the last run. 
# it depends on my start_date default args 
# and then every 24 hours after that 
# (i.e., the next run will be on January 11th, 2025 at 9:00 AM, and so on).
# can be changed using cron tab
# ex : schedule_interval='0 6 * * 1-5',  this cron expression will run on Mon-Fri at 6 AM
dag = DAG('dbt_run', default_args=default_args, schedule_interval=timedelta(days=1))

# Define the dbt run command as a BashOperator
run_dbt_model = BashOperator(
    task_id='run_dbt_model',
    bash_command='cd /home/user/apps/dbt-demo && source dbt-env/bin/activate && cd jaffle_shop_main && dbt run',
    dag=dag
)
