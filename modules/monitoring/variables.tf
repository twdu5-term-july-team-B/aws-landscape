variable "aws_region" {
  type = "string"
  description = "The AWS region"
}

variable "steve_the_cloudwatcher_trusted_entities" {
  type = "list"
  default = []
  description = "The entities allowed to assume the Steve the Cloudwatcher role"
}