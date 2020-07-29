resource "aws_cloudwatch_metric_alarm" "hdfs-station-mart-file-exists" {
  alarm_name                = "hdfs-station-mart-file-exists"
  comparison_operator       = "LessThanOrEqualToThreshold"
  evaluation_periods        = "1"
  metric_name               = "hdfs-station-mart-file-exists"
  namespace                 = "Custom"
  period                    = "300"
  statistic                 = "Maximum"
  threshold                 = "0.5"
  alarm_description         = "This metric sends alarm when a file has not been written to StationMart within the last 5 minutes"
  datapoints_to_alarm       = "1"
  insufficient_data_actions = []
  ok_actions = ["${var.alerting_sns_topic}"]
  alarm_actions = ["${var.alerting_sns_topic}"]
  dimensions = {
    JobFlowId = "${aws_emr_cluster.training_cluster.id}"
  }
}

resource "aws_cloudwatch_metric_alarm" "kafka-consumer-running" {
  count = "${length(var.kafka_consumers_to_monitor)}"
  alarm_name                = "${var.kafka_consumers_to_monitor[count.index]}"
  comparison_operator       = "LessThanOrEqualToThreshold"
  evaluation_periods        = "1"
  metric_name               = "${var.kafka_consumers_to_monitor[count.index]}-is-running"
  namespace                 = "Custom"
  period                    = "300"
  statistic                 = "Maximum"
  threshold                 = "0.5"
  alarm_description         = "This metric sends alarm when a Kafka Consumer/Yarn application (${var.kafka_consumers_to_monitor[count.index]}) is not running"
  datapoints_to_alarm       = "1"
  insufficient_data_actions = []
  ok_actions = ["${var.alerting_sns_topic}"]
  alarm_actions = ["${var.alerting_sns_topic}"]
  dimensions = {
    ConsumerName = "${var.kafka_consumers_to_monitor[count.index]}"
  }
}