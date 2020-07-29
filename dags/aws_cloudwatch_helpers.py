def create_aws_cloudwatch_client(aws_session, region):
    return aws_session.client('cloudwatch', region_name=region)


def send_metrics_to_cloudwatch(cloudwatch_client, namespace, metric_name, dimensions, value):
  cloudwatch_client.put_metric_data(
      Namespace=namespace,
      MetricData=[
        {
          'MetricName': metric_name,
          'Dimensions': dimensions,
          'Value': value,
        },
      ]
  )
