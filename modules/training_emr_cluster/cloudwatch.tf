resource "aws_cloudwatch_metric_alarm" "hdfs-station-mart-file-exists" {
  alarm_name                = "hdfs-station-mart-file-exists"
  comparison_operator       = "LessThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "hdfs-station-mart-file-exists"
  namespace                 = "Custom"
  period                    = "600"
  statistic                 = "Minimum"
  threshold                 = "0.5"
  alarm_description         = "This metric sends alarm when the disk utilization is more than 90%"
  datapoints_to_alarm       = "2"
  insufficient_data_actions = []
  ok_actions = ["${var.alerting_sns_topic}"]
  alarm_actions = ["${var.alerting_sns_topic}"]
  dimensions = {
    JobFlowId = "${aws_emr_cluster.training_cluster.id}"
  }
}