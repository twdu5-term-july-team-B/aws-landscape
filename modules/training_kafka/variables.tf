variable "deployment_identifier" {
  description = "An identifier for this instantiation."
}

variable "vpc_id" {
  description = "VPC in which to provision Kafka"
}

variable "subnet_id" {
  description = "Subnet in which to provision Kafka"
}

variable "ec2_key_pair" {
  description = "EC2 key pair to use to SSH into Kafka instance"
}

variable "dns_zone_id" {
  description = "DNS zone in which to create records"
}

variable "instance_type" {
  description = "EC2 instance type for Kafka"
}

variable "bastion_security_group_id" {
  description = "Id of bastion security group to allow SSH ingress"
}

variable "emr_security_group_id" {
  description = "Id of EMR cluster security group to Kafka & Zookeeper ingress"
}

variable "subdomain" {
  description = "Subdomain where kafka is available at"
}

variable "root_block_device" {
  type = "map"
  default = {
    volume_size = 8
  }
  description = "Root Block Device configuration"
}

variable "alerting_sns_topic" {
  type = "string"
  description = "The SNS ARN that team members are subscribed to in order to get operations alerts"
}