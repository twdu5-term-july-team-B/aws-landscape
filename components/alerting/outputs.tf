output "sns_arn" {
  value = "${aws_sns_topic.team-alerts.arn}}"
}