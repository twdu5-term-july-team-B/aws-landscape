variable "deployment_identifier" {
  description = "An identifier for this instantiation."
}

variable "vpc_id" {
  description = "VPC in which to launch cluster"
}

variable "subnet_id" {
  description = "Subnet in which to launch cluster"
}

variable "dns_zone_id" {
  description = "DNS zone in which to create records"
}

variable "ec2_key_pair" {
  description = "EC2 key pair to use to SSH into bastion"
}

variable "master_type" {
  description = "Instance type of master node"
}

variable "core_type" {
  description = "Instance type of core node"
}

variable "min_core_count" {
  description = "Min number of core nodes"
}

variable "max_core_count" {
  description = "Max number of core nodes"
}

variable "bastion_security_group_id" {
  description = "Id of bastion security group to allow SSH ingress"
}

variable "airflow_security_group_id" {
  description = "Id of the Airflow security group to allow access to WebHdfs"
}

variable "alerting_sns_topic" {
  description = "ARN of the SNS topic that alerts the team"
}

variable "kafka_consumers_to_monitor" {
  type = "list"
  description = "Names of Kafka Consumers (Yarn Applications) to monitor"
}

variable "env" {
  type = "string"
}