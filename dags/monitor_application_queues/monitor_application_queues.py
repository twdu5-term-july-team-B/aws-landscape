from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python_operator import PythonOperator
import requests
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path+"/helpers")
from aws_helpers import assume_role
from aws_cloudwatch_helpers import create_aws_cloudwatch_client, send_metrics_to_cloudwatch

class MonitorApplicationQueues:
    app_name = "monitor-consumers-running"
    expected_consumers = sorted(["StationInformationSaverApp",
                                 "StationStatusSaverApp",
                                 "StationDataSFSaverApp",
                                 "StationDataMarseilleSaverApp",
                                 "StationApp",
                                 "StationTransformerNYC"])
    url = "http://emr-master.twdu5-term-july-team-b.training:8088/ws/v1/cluster/apps"


    def get_consumers(self):
        res = requests.get(self.url, json={"key": "value"}, headers={'Content-type': 'application/json; charset=utf-8'})
        return res.json()


    def parse(self, response_data):
        running_consumers = map(lambda x: x.get("name"),
                                filter(lambda x: x.get("state") == "RUNNING" and x.get("queue") == "streaming", response_data["apps"]["app"]))
        running_consumers.sort()
        return running_consumers

    def aws_session(self):
        return assume_role("arn:aws:iam::534731679169:role/steve-the-cloudwatcher", "airflow-" + self.app_name)

    def cloudwatch_client(self):
        return create_aws_cloudwatch_client(self.aws_session(), "eu-central-1")


    def postToCloudwatch(self, client, consumer_name, True):
        value = 1.0 if True else 0.0
        send_metrics_to_cloudwatch(client, "Custom", "yarnApplicationRunningInCorrectQueue", [
            {
                'Name': 'ConsumerName',
                'Value': consumer_name
            },
        ], value)

def execute():
    return True


monitor_application_queues_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 7, 18)
}
monitor_application_queues = MonitorApplicationQueues()
monitor_application_queues_dag = DAG(
    monitor_application_queues.app_name,
    default_args=monitor_application_queues_args,
    max_active_runs=1,
    schedule_interval='*/1 * * * *'
)