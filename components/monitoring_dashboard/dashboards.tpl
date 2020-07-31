{
  "widgets": [
    {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 12,
      "height": 3,
      "properties": {
        "metrics": [
          [ "System/Linux", "MemoryUtilization", "InstanceId", "${kafka_instance_id}", { "label": "MemoryUtilization" } ],
          [ ".", "DiskSpaceUtilization", "MountPath", "/", "InstanceId", "${kafka_instance_id}", "Filesystem", "/dev/xvda1" ]
        ],
        "view": "singleValue",
        "region": "${aws_region}",
        "title": "Kafka",
        "period": 300
      }
    },
    {
      "type": "metric",
      "x": 12,
      "y": 3,
      "width": 12,
      "height": 9,
      "properties": {
        "metrics": [
          [ "AWS/ElasticMapReduce", "HDFSUtilization", "JobFlowId", "${emr_cluster_id}" ],
          [ ".", "AppsRunning", ".", "." ],
          [ ".", "AppsPending", ".", "." ],
          [ ".", "YARNMemoryAvailablePercentage", ".", "." ]
        ],
        "view": "singleValue",
        "stacked": false,
        "region": "${aws_region}",
        "period": 300,
        "title": "EMR HDFS"
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 3,
      "width": 12,
      "height": 6,
      "properties": {
        "metrics": [
          [ { "expression": "m2+m3", "label": "MemoryUsed", "id": "e1", "color": "#d62728" } ],
          [ "AWS/ElasticMapReduce", "MemoryTotalMB", "JobFlowId", "${emr_cluster_id}", { "id": "m1", "color": "#1f77b4" } ],
          [ ".", "MemoryReservedMB", ".", ".", { "id": "m2", "color": "#bcbd22" } ],
          [ ".", "MemoryAllocatedMB", ".", ".", { "id": "m3", "color": "#ff7f0e" } ]
        ],
        "view": "timeSeries",
        "stacked": false,
        "region": "${aws_region}",
        "period": 300,
        "title": "EMR Cluster Memory Usage"
      }
    },
    {
      "type": "metric",
      "x": 12,
      "y": 0,
      "width": 12,
      "height": 3,
      "properties": {
        "metrics": [
          [ "System/Linux", "DiskSpaceUtilization", "MountPath", "/", "InstanceId", "${kafka_instance_id}", "Filesystem", "/dev/xvda1", { "label": "DiskSpaceUtilization" } ],
          [ ".", "MemoryUtilization", "InstanceId", "${kafka_instance_id}" ]
        ],
        "view": "timeSeries",
        "stacked": false,
        "region": "${aws_region}",
        "title": "Kafka Status",
        "period": 300,
        "yAxis": {
          "left": {
            "max": 100,
            "min": 0
          }
        }
      }
    },
    {
      "type": "metric",
      "x": 0,
      "y": 9,
      "width": 12,
      "height": 6,
      "properties": {
        "metrics": [
          [ "AWS/ElasticMapReduce", "AppsRunning", "JobFlowId", "${emr_cluster_id}" ],
          [ ".", "AppsPending", ".", "." ],
          [ ".", "ContainerReserved", ".", "." ]
        ],
        "view": "timeSeries",
        "stacked": false,
        "region": "${aws_region}",
        "period": 300
      }
    },
    {
      "type": "metric",
      "x": 12,
      "y": 9,
      "width": 12,
      "height": 3,
      "properties": {
        "view": "timeSeries",
        "stacked": false,
        "metrics": [
          [ "System/Linux", "MemoryUtilization", "InstanceId", "${ingester_instance_id}" ]
        ],
        "region": "${aws_region}",
        "title": "Ingester Memory Usage",
        "period": 300,
        "yAxis": {
          "left": {
            "min": 0,
            "max": 100
          }
        }
      }
    },
    {
      "type": "metric",
      "x": 12,
      "y": 9,
      "width": 12,
      "height": 3,
      "properties": {
        "metrics": [
          [ "Linux System", "DiskSpaceUtilization", "InstanceId", "${kafka_instance_id}", "MountPath", "/", "Filesystem", "/dev/xvda1", { "stat": "Average", "visible": false } ],
          [ "System/Linux", ".", "MountPath", "/", "InstanceId", "${kafka_instance_id}", ".", ".", { "stat": "Average" } ]
        ],
        "region": "eu-central-1",
        "view": "timeSeries",
        "stacked": false,
        "period": 5,
        "annotations": {
          "horizontal": [
            {
              "label": "DiskSpaceUtilization >= 90 for 2 datapoints within 4 minutes",
              "value": 90
            }
          ]
        },
        "title": "Kafka Disk Space Utilization"
      }
    },
    {
      "type": "metric",
      "x": 12,
      "y": 9,
      "width": 12,
      "height": 3,
      "properties": {
        "region": "eu-central-1",
        "metrics": [
          [ "Custom", "hdfs-station-mart-file-exists", "JobFlowId", "${emr_cluster_id}", { "stat": "Minimum" } ]
        ],
        "view": "timeSeries",
        "stacked": false,
        "period": 600,
        "annotations": {
          "horizontal": [
            {
              "label": "hdfs-station-mart-file-exists <= 0.5 for 2 datapoints within 20 minutes",
              "value": 0.5
            }
          ]
        },
        "title": "HDFS Station Mart File Exists"
      }
    },
    {
      "type": "metric",
      "x": 12,
      "y": 9,
      "width": 12,
      "height": 3,
      "properties": {
        "view": "timeSeries",
        "stacked": false,
        "metrics": [
          [ "Custom", "kafkaConsumerRunning", "ConsumerName", "StationApp" ],
          [ "...", "StationDataMarseilleSaverApp" ],
          [ "...", "StationDataSFSaverApp" ],
          [ "...", "StationInformationSaverApp" ],
          [ "...", "StationStatusSaverApp" ],
          [ "...", "StationTransformerNYC" ]
        ],
        "region": "eu-central-1",
        "title": "Kafka Consumers / Yarn Applications Running"
      }
    }
  ]
}