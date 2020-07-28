resource "aws_emr_cluster" "training_cluster" {
  name          = "${local.cluster_name}"
  release_label = "emr-5.15.0"
  applications = [
    "Spark", "Hue", "Hive", "Ganglia", "Pig", "Flink", "Oozie", "Zeppelin"
  ]
  log_uri = "s3://${aws_s3_bucket.emr_logs.id}/emr/"

  keep_job_flow_alive_when_no_steps = true

  step {
    action_on_failure = "TERMINATE_CLUSTER"
    name              = "Setup Hadoop Debugging"

    hadoop_jar_step {
      jar  = "command-runner.jar"
      args = ["state-pusher-script"]
    }
  }

  lifecycle {
    ignore_changes = ["step"]
  }

  ebs_root_volume_size = 40

  ec2_attributes {
    subnet_id                         = "${var.subnet_id}"
    emr_managed_master_security_group = "${aws_security_group.master.id}"
    emr_managed_slave_security_group  = "${aws_security_group.core.id}"
    service_access_security_group     = "${aws_security_group.service.id}"
    additional_master_security_groups = "${aws_security_group.emr_shared.id}"
    additional_slave_security_groups  = "${aws_security_group.emr_shared.id}"
    instance_profile                  = "${aws_iam_instance_profile.emr_node.arn}"
    key_name                          = "${var.ec2_key_pair}"
  }

  service_role = "${aws_iam_role.emr_service.arn}"

  additional_info = <<EOF
[
  {
  "Classification": "capacity-scheduler",
  "Properties": {
       "yarn.scheduler.capacity.root.queues": "default,streaming,monitoring",
       "yarn.scheduler.capacity.root.default.capacity": "25",
       "yarn.scheduler.capacity.root.streaming.capacity": "70",
       "yarn.scheduler.capacity.root.monitoring.capacity": "5",
       "yarn.scheduler.capacity.root.default.state": "RUNNING",
       "yarn.scheduler.capacity.root.streaming.state": "RUNNING",
       "yarn.scheduler.capacity.root.monitoring.state": "RUNNING",
     }
   },
   {
     "Classification": "yarn-site",
     "Properties": {
       "yarn.resourcemanager.scheduler.class": "org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler"
     }
   }
]

EOF

  master_instance_group {
    instance_type = "${var.master_type}"
  }

  core_instance_group {
    instance_type  = "${var.core_type}"
    instance_count = "${var.core_count}"

    ebs_config {
      iops                 = 0
      size                 = "500"
      type                 = "gp2"
      volumes_per_instance = 1
    }
// TODO: Error: Instance Group () Auto Scaling Policy: ValidationException: Instance group id '' is not valid.
// This is probably caused by migrating from `instance_groups` to `core/master_instance_group`
//
//    autoscaling_policy = <<EOF
//{
//"Constraints": {
//  "MinCapacity": 3,
//  "MaxCapacity": 6
//},
//"Rules": [
//  {
//    "Name": "ScaleOutMemoryPercentage",
//    "Description": "Scale out if YARNMemoryAvailablePercentage is less than 15",
//    "Action": {
//      "SimpleScalingPolicyConfiguration": {
//        "AdjustmentType": "CHANGE_IN_CAPACITY",
//        "ScalingAdjustment": 1,
//        "CoolDown": 300
//      }
//    },
//    "Trigger": {
//      "CloudWatchAlarmDefinition": {
//        "ComparisonOperator": "LESS_THAN",
//        "EvaluationPeriods": 1,
//        "MetricName": "YARNMemoryAvailablePercentage",
//        "Namespace": "AWS/ElasticMapReduce",
//        "Period": 300,
//        "Statistic": "AVERAGE",
//        "Threshold": 15.0,
//        "Unit": "PERCENT"
//      }
//    }
//  }
//]
//}
//EOF
    }


  tags = "${merge(
    local.common_tags,
    map(
      "Name", local.cluster_name
    )
  )}"
}
