terraform {
  backend "s3" {}
}

provider "aws" {
  region  = "${var.aws_region}"
  version = "~> 2.0"
}


data "terraform_remote_state" "training_kafka" {
  backend = "s3"
  config {
    key    = "training_kafka.tfstate"
    bucket = "tw-dataeng-${var.cohort}-tfstate"
    region = "${var.aws_region}"
  }
}

data "terraform_remote_state" "training_emr_cluster" {
  backend = "s3"
  config {
    key    = "training_emr_cluster.tfstate"
    bucket = "tw-dataeng-${var.cohort}-tfstate"
    region = "${var.aws_region}"
  }
}

data "terraform_remote_state" "ingester" {
  backend = "s3"
  config {
    key    = "ingester.tfstate"
    bucket = "tw-dataeng-${var.cohort}-tfstate"
    region = "${var.aws_region}"
  }
}

data "template_file" "dashboard" {
  template = "${file("${path.module}/dashboards.tpl")}"
  vars = {
    kafka_instance_id = "${data.terraform_remote_state.training_kafka.kafka_instance_id}"
    emr_cluster_id = "${data.terraform_remote_state.training_emr_cluster.emr_cluster_id}"
    aws_region = "${var.aws_region}"
    ingester_instance_id = "${data.terraform_remote_state.ingester.ingester_instance_id}"
  }
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "2wheelers"
  dashboard_body = "${data.template_file.dashboard.rendered}"
}
