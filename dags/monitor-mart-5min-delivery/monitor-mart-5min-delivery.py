from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator


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

def some_function() :
  return "foo"


modified_in_last_5mins = PythonOperator(
   task_id='is_5_mins_ago',
   python_callable=some_function(),
   dag=dag,
)

modified_in_last_5mins