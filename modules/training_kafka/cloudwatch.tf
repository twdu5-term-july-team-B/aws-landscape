resource "aws_cloudwatch_metric_alarm" "disk_space_utilization" {
  alarm_name                = "kafka-running-out-of-space"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "DiskSpaceUtilization"
  namespace                 = "System/Linux"
  period                    = "120"
  statistic                 = "Average"
  threshold                 = "90"
  alarm_description         = "This metric sends alarm when the disk utilization is more than 90%"
  insufficient_data_actions = []
  ok_actions = ["${var.alerting_sns_topic}"]
  alarm_actions = ["${var.alerting_sns_topic}"]
  dimensions = {
    InstanceId = "${aws_instance.kafka.id}"
    MountPath = "/"
    Filesystem = "/dev/xvda1"
  }
}