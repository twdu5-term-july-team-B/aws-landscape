output "airflow_address" {
  description = "The DNS address of the airflow instance."
  value       = "${aws_route53_record.airflow.fqdn}"
}

output "airflow_security_group_id" {
  description = "The Security Group of the Airflow instance"
  value       = "${aws_security_group.airflow.id}"
}