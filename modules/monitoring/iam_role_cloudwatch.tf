resource "aws_iam_role" "steve-the-cloudwatcher" {
  name               = "steve-the-cloudwatcher"
  description        = "Role to push metrics to Cloudwatch"
  assume_role_policy = "${data.aws_iam_policy_document.steve-the-cloudwatcher-assume-role.json}"
}

data "aws_iam_policy_document" "steve-the-cloudwatcher-assume-role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals = {
      type = "AWS"
      identifiers = ["${var.steve_the_cloudwatcher_trusted_entities}"]
    }
  }
}

data "aws_iam_policy_document" "cloudwatch" {
  statement {
    actions = [
      "cloudwatch:PutMetricData",
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "cloudwatch" {
  name        = "steve-the-cloudwatcher"
  description = "Policy for Steve the Cloudwatcher"
  policy      = "${data.aws_iam_policy_document.cloudwatch.json}"
}

resource "aws_iam_role_policy_attachment" "cloudwatch" {
  policy_arn = "${aws_iam_policy.cloudwatch.arn}"
  role = "${aws_iam_role.steve-the-cloudwatcher.id}"
}