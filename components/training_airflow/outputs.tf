output "airflow_address" {
  description = "The DNS address of the airflow instance."
  value       = "${module.training_airflow.airflow_address}"
}

output "airflow_security_group_id" {
  description = "The security group id for airflow"
  value = "${module.training_airflow.airflow_security_group_id}"
}

output "airflow_instance_profile_role_arn" {
  value = "${module.training_airflow.airflow_instance_profile_role_arn}"
}