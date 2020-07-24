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
    url = "http://emr-master.twdu5-term-july-team-b.training:50070/webhdfs/v1/tw/stationMart/data?op=LISTSTATUS"
    res = requests.get(url)
    return res.text


def get_last_modification_epoch(response_data):
    file_statuses = response_data["FileStatuses"]
    for file_status in file_statuses["FileStatus"]:
        if str(file_status["pathSuffix"]).endswith("csv"):
            modification_time = file_status["modificationTime"]

    return modification_time


def is_within_five_minute_delivery(modification_time_in_millis):
    time_five_mins_ago_in_epoch = (datetime.now() - timedelta(minutes=5) - datetime(1970,1,1)).total_seconds()
    return modification_time_in_millis/1000 > time_five_mins_ago_in_epoch

def calculate_metric_data_value(has_been_created_in_last_five_min):
    return 1.0 if has_been_created_in_last_five_min else 0.0

def send_metrics_to_cloudwatch(has_been_created_in_last_five_min):
    session = assume_role("arn:aws:iam::534731679169:role/steve-the-cloudwatcher", "airflow-monitor-5min")
    value = calculate_metric_data_value(has_been_created_in_last_five_min)
    session.client('cloudwatch', region_name="eu-central-1").put_metric_data(
        Namespace='Custom',
        MetricData=[
            {
                'MetricName': 'hdfs-station-mart-file-exists',
                'Dimensions': [
                    {
                        'Name': 'JobFlowId',
                        'Value': 'j-1HHXQM194OUAM'
                    },
                ],
                'Value': value,
            },
        ]
    )




def execute():
    send_metrics_to_cloudwatch(
        calculate_metric_data_value(
            is_within_five_minute_delivery(get_last_modification_epoch(get_files()))
        )
    )


modified_in_last_5mins = PythonOperator(
    task_id='check_file_was_created_within_5_mins',
    python_callable=execute,
    dag=dag,
)

modified_in_last_5mins
