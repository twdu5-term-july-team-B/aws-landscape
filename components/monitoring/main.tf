terraform {
  backend "s3" {}
}

provider "aws" {
  region  = "${var.aws_region}"
  version = "~> 2.0"
}

data "terraform_remote_state" "training_airflow" {
  backend = "s3"
  config {
    key    = "training_airflow.tfstate"
    bucket = "tw-dataeng-${var.cohort}-tfstate"
    region = "${var.aws_region}"
  }
}

module "monitoring" {
  source = "../../modules/monitoring"

  aws_region = "${var.aws_region}"
  steve_the_cloudwatcher_trusted_entities = ["${data.terraform_remote_state.training_airflow.airflow_instance_profile_role_arn}"]
}