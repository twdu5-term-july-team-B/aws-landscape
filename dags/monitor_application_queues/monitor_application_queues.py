from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python_operator import PythonOperator
import requests
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path+"/helpers")
from aws_helpers import assume_role

app_name = "monitor-mart-5-min-delivery"
cluster_id = "j-1HHXQM194OUAM"

args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 7, 18)
}

dag = DAG(
    app_name,
    default_args=args,
    max_active_runs=1,
    schedule_interval='*/2 * * * *'
)


def get_files():
    url = "http://emr-master.twdu5-term-july-team-b.training:8088/ws/v1/cluster/apps/application_1595941188025_0009/queue"
    res = requests.get(url, json={"key": "value"}, headers={'Content-type': 'application/json; charset=utf-8'})
    return res.json()

def execute():
    return True


modified_in_last_5mins = PythonOperator(
    task_id='check_file_was_created_within_5_mins',
    python_callable=execute,
    dag=dag,
)

modified_in_last_5mins
