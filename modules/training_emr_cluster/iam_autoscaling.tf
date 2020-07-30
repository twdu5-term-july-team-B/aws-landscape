resource "aws_iam_role" "emr_autoscaling" {
  name = "emr-service-${var.deployment_identifier}-autoscaling"
  assume_role_policy = "${data.aws_iam_policy_document.autoscale_role_assume.json}"
}

data "aws_iam_policy_document" "autoscale_role_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["ec2.amazonaws.com"]
      type = "Service"
    }
  }
}

resource "aws_iam_role_policy_attachment" "autoscale" {
  role = "${aws_iam_role.emr_node.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforAutoScalingRole"
}