resource "aws_s3_bucket" "emr_logs" {
  bucket = "${var.deployment_identifier}-${var.env}-emr-logs"
  acl    = "private"

  tags = "${merge(
    local.common_tags,
    map(
      "Name", "${var.deployment_identifier}-emr-logs"
    )
  )}"
}

resource "aws_s3_bucket" "emr_hdfs_backups" {
  bucket = "${var.deployment_identifier}-${var.env}-emr-hdfs-backups"
  acl    = "private"

  tags = "${merge(
    local.common_tags,
    map(
      "Name", "${var.deployment_identifier}-emr-hdfs-backups"
    )
  )}"
}