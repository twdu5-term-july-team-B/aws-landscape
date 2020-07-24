import boto3
from boto3.session import Session

def assume_role(arn, session_name):
  client = boto3.client('sts')

  response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)

  return Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
          aws_secret_access_key=response['Credentials']['SecretAccessKey'],
          aws_session_token=response['Credentials']['SessionToken'])