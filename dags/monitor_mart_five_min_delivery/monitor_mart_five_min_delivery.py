from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import requests

app_name = "monitor-mart-5-min-delivery"
cluster_id = "j-1HHXQM194OUAM"

args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 7, 18),
    'schedule_interval': '*/2 * * * *'
}

dag = DAG(
    app_name,
    default_args=args,
    max_active_runs=1
)


def fetch_modification_times_from_response(response_data):
    return []


def get_modification_times():
    url = "http://emr-master.twdu5-term-july-team-b.training:50070/webhdfs/v1/tw/stationMart/data?op=LISTSTATUS"
    res = requests.get(url)

    return res.text


modified_in_last_5mins = PythonOperator(
    task_id='is_5_mins_ago',
    python_callable=get_modification_times(),
    dag=dag,
)

modified_in_last_5mins
