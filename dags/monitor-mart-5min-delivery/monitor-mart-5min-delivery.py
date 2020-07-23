from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor


app_name = "monitor-mart-5-min-delivery"
cluster_id = "j-1HHXQM194OUAM"

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

def issue_step(name, args):
  return [
    {
      "Name": name,
      "ActionOnFailure": "CONTINUE",
      "HadoopJarStep": {
        "Jar": "command-runner.jar",
        "Args": args
      }
    }
  ]

HDFS -> bash file
   gets the date `hdfs dfs -ls .... ` => 2020-07-23 09:30
  python script ^^ compares with 5 min ago
  return 0 if success
  return 1 if not => airflow step to fail

run_step = issue_step(
    app_name,
    ["bash","-c","hdfs dfs -ls /tw/stationMart/data | tr -s ' ' | cut -d' ' -f6-7 | grep '^[0-9]'"])

add_step_task = EmrAddStepsOperator(
    task_id='add_step',
    job_flow_id=cluster_id,
    aws_conn_id='aws_kmok',
    steps=run_step,
    dag=dag
)

watch_prev_step_task = EmrStepSensor(
    task_id='watch_prev_step',
    job_flow_id=cluster_id,
    step_id="{{ task_instance.xcom_pull('add_step', key='return_value')[0] }}",
    aws_conn_id='aws_kmok',
    dag=dag
)

add_step_task >> watch_prev_step_task

# check_output = BashOperator(
#   task_id='check_output',
#   bash_command='echo "{{ task_instance.xcom_pull("add_step_task")}}"',
#   dag=dag,
# )


# python operator => compare
#def is_5_min_ago_command(datetime_string):
#  datetime.strptime(datetime_string, '%d/%m/%y %H:%M:%S') - datetime.timedelta(minutes=5)


#PythonOperator(
#    task_id='is_5_mins_ago',
#    python_callable=is_5_min_ago_command("{{ task_instance.xcom_pull('last_timestamp')}}"),
#    dag=dag,
#)



# last_timestamp >> check_output
#last_timestamp >> watch_prev_step_task