from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
import requests
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(dir_path+"/helpers")
from aws_helpers import assume_role
from aws_cloudwatch_helpers import create_aws_cloudwatch_client, send_metrics_to_cloudwatch

class MonitorConsumersRunning:
    app_name = "monitor-consumers-running"
    expected_consumers = sorted(["StationInformationSaverApp",
                               "StationStatusSaverApp",
                               "StationDataSFSaverApp",
                               "StationDataMarseilleSaverApp",
                               "StationApp",
                               "StationTransformerNYC"])

    def get_consumers(self):
        url = "http://emr-master.twdu5-term-july-team-b.training:8088/ws/v1/cluster/apps"
        res = requests.get(url, json={"key": "value"}, headers={'Content-type': 'application/json; charset=utf-8'})
        return res.json()


    def parse(self, response_data):
        running_consumers = map(lambda x: x.get("name"),
            filter(lambda x: x.get("state") == "RUNNING" and x.get("queue") == "streaming", response_data["apps"]["app"]))
        running_consumers.sort()
        return running_consumers


    def report_running(self, running_consumers):
        for consumer in set(self.expected_consumers).intersection(running_consumers):
            self.postToCloudwatch(self.cloudwatch_client(), consumer, True)


    def report_not_running(self, running_consumers):
        for consumer in set(self.expected_consumers).difference(running_consumers):
            self.postToCloudwatch(self.cloudwatch_client(), consumer, False)

    def aws_session(self):
        return assume_role("arn:aws:iam::534731679169:role/steve-the-cloudwatcher", "airflow-" + self.app_name)

    def cloudwatch_client(self):
        return create_aws_cloudwatch_client(self.aws_session(), "eu-central-1")


    def postToCloudwatch(self, client, consumer_name, running):
        value = 1.0 if running else 0.0
        send_metrics_to_cloudwatch(client, "Custom", "kafkaConsumerRunning", [
            {
                'Name': 'ConsumerName',
                'Value': consumer_name
            },
        ], value)

    def execute(self):
        running_consumers = self.parse(self.get_consumers())
        self.report_running(running_consumers)
        self.report_not_running(running_consumers)


monitor_consumers_running_args = {
        'owner': 'airflow',
        'start_date': datetime(2020, 7, 18)
}

monitor_consumers_running = MonitorConsumersRunning()
monitor_consumers_running_dag = DAG(
    monitor_consumers_running.app_name,
    default_args=monitor_consumers_running_args,
    max_active_runs=1,
    schedule_interval='*/1 * * * *'
)
monitor_consumers_running_task = PythonOperator(
    task_id='monitor_consumers_running',
    python_callable=monitor_consumers_running.execute,
    dag=monitor_consumers_running_dag,
)

monitor_consumers_running_task
