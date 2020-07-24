from airflow import DAG
from datetime import timedelta, datetime
import time
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
    'start_date': datetime(2020, 7, 18),
    'schedule_interval': '*/2 * * * *'
}

dag = DAG(
    app_name,
    default_args=args,
    max_active_runs=1
)


def time_difference_since_last_modified(response_data):
    modification_time = ""
    file_statuses = response_data["FileStatuses"]
    for file_status in file_statuses["FileStatus"]:
        if str(file_status["pathSuffix"]).endswith("csv"):
            modification_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(file_status["modificationTime"])/1000))
    time_difference = datetime.now() - datetime.strptime(modification_time, "%Y-%m-%d %H:%M:%S")
    return time_difference


def get_modification_times():
    url = "http://emr-master.twdu5-term-july-team-b.training:50070/webhdfs/v1/tw/stationMart/data?op=LISTSTATUS"
    res = requests.get(url)
    check_five_minute_delivery(res.text)
    return res.text


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


def calculate_metric_data_value(has_been_created_in_last_five_min):
    return 1.0 if has_been_created_in_last_five_min else 0.0


def check_five_minute_delivery():
    return time_difference_since_last_modified(get_modification_times()) < timedelta(minutes=5)


modified_in_last_5mins = PythonOperator(
    task_id='is_5_mins_ago',
    python_callable=check_five_minute_delivery,
    dag=dag,
)

modified_in_last_5mins
