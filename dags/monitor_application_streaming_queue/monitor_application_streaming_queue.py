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

class MonitorApplicationStreamingQueue:
    app_name = "monitor-applications-in-streaming-queue"
    allowed_applications = sorted(["StationInformationSaverApp",
                                 "StationStatusSaverApp",
                                 "StationDataSFSaverApp",
                                 "StationDataMarseilleSaverApp",
                                 "StationApp",
                                 "StationTransformerNYC"])
    url = "http://emr-master.twdu5-term-july-team-b.training:8088/ws/v1/cluster/apps"


    def get_applications(self):
        res = requests.get(self.url, json={"key": "value"}, headers={'Content-type': 'application/json; charset=utf-8'})
        return res.json()


    def parse(self, response_data):
        return sorted(map(lambda x: x.get("name"),
                                filter(lambda x: x.get("state") == "RUNNING" and x.get("queue") == "streaming", response_data["apps"]["app"])))

    def aws_session(self):
        return assume_role("arn:aws:iam::534731679169:role/steve-the-cloudwatcher", "airflow-" + self.app_name)

    def cloudwatch_client(self):
        return create_aws_cloudwatch_client(self.aws_session(), "eu-central-1")

    def report(self, applications_in_streaming_queue):
        self.postToCloudWatch(self.cloudwatch_client(), "streaming", applications_in_streaming_queue <= self.allowed_applications)

    def postToCloudwatch(self, client, queue, True):
        value = 1.0 if True else 0.0
        send_metrics_to_cloudwatch(client, "Custom", "yarnApplicationRunningInCorrectQueue", [
            {
                'Name': 'QueueName',
                'Value': queue
            },
        ], value)

    def execute(self):
        applications_in_queue = self.parse(self.get_applications())
        self.report(applications_in_queue)


monitor_application_streaming_queue_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 7, 18)
}
monitor_application_streaming_queue = MonitorApplicationStreamingQueue()
monitor_application_streaming_queue_dag = DAG(
    monitor_application_streaming_queue.app_name,
    default_args=monitor_application_streaming_queue_args,
    max_active_runs=1,
    schedule_interval='*/10 * * * *'
)

monitor_application_streaming_queue_task = PythonOperator(
    task_id='monitor_application_streaming_queue',
    python_callable=monitor_application_streaming_queue.execute,
    dag=monitor_application_streaming_queue_dag,
)

monitor_application_streaming_queue_task
