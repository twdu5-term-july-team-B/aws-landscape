from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator


app_name = "monitor-mart-5-min-delivery"

args = {
  'owner': 'airflow',
  'start_date': datetime(2020, 7, 18),
  'schedule_interval': '*/2 * * * *'
}

dag = DAG(
    app_name,
    default_args = args,
    max_active_runs = 1
)

# bash operator => hadoop => datetime
last_timestamp_command = """
hadoop fs -fs hdfs://emr-master.twdu5-term-july-team-b.training -ls /tw/stationMart/data | tr -s ' ' | cut -d' ' -f6-7 | grep '^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}'
"""



last_timestamp = BashOperator(
    task_id='last_timestamp',
    bash_command=last_timestamp_command,
    dag=dag,
)


# python operator => compare
def is_5_min_ago_command(datetime_string):
  datetime.strptime(datetime_string, '%d/%m/%y %H:%M:%S') - datetime.timedelta(minutes=5)


PythonOperator(
    task_id='is_5_mins_ago',
    python_callable=is_5_min_ago_command("{{ task_instance.xcom_pull('add_step', key='return_value')[0] }}"),
    dag=dag,
)



# last_timestamp >> watch_prev_step_task