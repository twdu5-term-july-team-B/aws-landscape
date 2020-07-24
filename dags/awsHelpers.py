import boto3
from boto3.session import Session

def assume_role(arn, session_name):
  client = boto3.client('sts')
  account_id = client.get_caller_identity()["Account"]
  print(account_id)

  response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)
  # response = client.assume_role(RoleArn="arn:aws:iam::534731679169:role/stevethepug-test", RoleSessionName="airflow-monitor")

  Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
          aws_secret_access_key=response['Credentials']['SecretAccessKey'],
          aws_session_token=response['Credentials']['SessionToken'])