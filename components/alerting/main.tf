terraform {
  backend "s3" {}
}

provider "aws" {
  region  = "${var.aws_region}"
  version = "~> 2.0"
}

resource "aws_sns_topic" "team-alerts" {
  name = "twdu5-b-team"
}