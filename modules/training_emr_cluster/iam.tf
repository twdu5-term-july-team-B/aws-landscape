resource "aws_iam_role" "emr_service" {
  name = "emr-service-${var.deployment_identifier}"

  # TODO: Replace this with data resource
  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "elasticmapreduce.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "emr_service_managed" {
  name = "emr-service-managed-${var.deployment_identifier}"
  roles = ["${aws_iam_role.emr_service.name}"]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

resource "aws_iam_instance_profile" "emr_node" {
  name = "emr-node-${var.deployment_identifier}"
  role = "${aws_iam_role.emr_node.name}"
}

resource "aws_iam_role" "emr_node" {

  name = "emr-node-${var.deployment_identifier}"

  # TODO: Replace this with data resource
  assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "emr_node_managed" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
  role = "${aws_iam_role.emr_node.name}"
}

data "aws_iam_policy_document" "backup-to-s3" {
  statement {
    actions = ["s3:*"]
    resources = ["${aws_s3_bucket.emr_hdfs_backups.arn}"]
  }
}

resource "aws_iam_policy" "backup-to-s3" {
  policy = "${data.aws_iam_policy_document.backup-to-s3.json}"
  name = "emr-backup-to-s3"
}

resource "aws_iam_role_policy_attachment" "backup-to-s3" {
  role = "${aws_iam_role.emr_node.name}"
  policy_arn = "${aws_iam_policy.backup-to-s3.arn}"
}

