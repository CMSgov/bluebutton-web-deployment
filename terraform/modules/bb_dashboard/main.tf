##
#
# NOTE: This module is for defining a main CloudWatch dashboard
#
##

resource "aws_cloudwatch_dashboard" "main-dash" {
   count          = "${var.dashboard_enable}"

   dashboard_name = "MainDashboard-${var.app}-${var.env}"
   dashboard_body = <<EOF
{
    "widgets": [
        {
            "type": "text",
            "x": 0,
            "y": 0,
            "width": 24,
            "height": 6,
            "properties": {
                "markdown": "\n# AWS Metrics Dashboard - ${var.app}-${var.env}\n\nA link to this dashboard: [MainDashboard-${var.app}-${var.env}](#dashboards:name=MainDashboard-${var.app}-${var.env}).\n\n## Dashboard Sections\nSection | Description | Reference-Link\n----|-----\nELB | Elastic Load Balancing |https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/elb-metricscollected.html\nASG | Auto Scaling Group | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/as-metricscollected.html\nEC2 | Elastic Compute Cloud ASG Aggregated | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GetMetricAutoScalingGroup.html\nRDS | Relational Database Service | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/rds-metricscollected.html\nNAT | Network Address Translation Gateway | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/nat-gateway-metricscollected.html\n"
            }
        },
        {
            "type": "text",
            "x": 0,
            "y": 6,
            "width": 24,
            "height": 3,
            "properties": {
                "markdown": "\n# ${var.app}-${var.env}\n## ELB - Elastic Load Balancing - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/elb-metricscollected.html\n"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 9,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/ELB", "HealthyHostCount", "LoadBalancerName", "${var.load_balancer_name}" ]
                ],
                "period": 300
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 9,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/ELB", "RequestCount", "LoadBalancerName", "${var.load_balancer_name}", { "stat": "Sum" } ]
                ],
                "period": 300,
                "title": "LB RequestCount"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 15,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/ELB", "RequestCount", "LoadBalancerName", "${var.load_balancer_name}", "AvailabilityZone", "us-east-1a", { "stat": "Sum" } ],
                    [ "...", "us-east-1c", { "stat": "Sum" } ],
                    [ "...", "us-east-1b", { "stat": "Sum" } ]
                ],
                "period": 300,
                "title": "Per AZ RequestCount"
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 15,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/ELB", "EstimatedALBActiveConnectionCount", "LoadBalancerName", "${var.load_balancer_name}" ]
                ],
                "period": 300
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 21,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-P3D",
                "end": "P0D",
                "metrics": [
                    [ "AWS/ELB", "HTTPCode_Backend_2XX", "LoadBalancerName", "${var.load_balancer_name}", { "stat": "Sum" } ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 21,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-P3D",
                "end": "P0D",
                "metrics": [
                    [ "AWS/ELB", "HTTPCode_Backend_5XX", "LoadBalancerName", "${var.load_balancer_name}", { "stat": "Sum" } ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 6,
            "y": 21,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-P3D",
                "end": "P0D",
                "metrics": [
                    [ "AWS/ELB", "HTTPCode_ELB_5XX", "LoadBalancerName", "${var.load_balancer_name}", { "stat": "Sum" } ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 6,
            "y": 27,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-P3D",
                "end": "P0D",
                "metrics": [
                    [ "AWS/ELB", "HTTPCode_Backend_4XX", "LoadBalancerName", "${var.load_balancer_name}", { "stat": "Sum" } ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 27,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-P3D",
                "end": "P0D",
                "metrics": [
                    [ "AWS/ELB", "HTTPCode_Backend_3XX", "LoadBalancerName", "${var.load_balancer_name}", { "stat": "Sum" } ]
                ]
            }
        },


        {
            "type": "text",
            "x": 0,
            "y": 33,
            "width": 24,
            "height": 3,
            "properties": {
                "markdown": "\n# ${var.app}-${var.env}\n## Auto Scaling Group (ASG) - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/as-metricscollected.html\n\nGroup Name: ${var.asg_name}\n"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 36,
            "width": 24,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "metrics": [
                    [ "AWS/AutoScaling", "GroupDesiredCapacity", "AutoScalingGroupName", "${var.asg_name}" ],
                    [ ".", "GroupMaxSize", ".", "." ],
                    [ ".", "GroupMinSize", ".", "." ],
                    [ ".", "GroupInServiceInstances", ".", "." ]
                ],
                "region": "us-east-1"
            }
        },

        {
            "type": "text",
            "x": 0,
            "y": 42,
            "width": 24,
            "height": 3,
            "properties": {
                "markdown": "\n# ${var.app}-${var.env}\n## Elastic Compute Cloud (EC2) ASG Aggregated - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/GetMetricAutoScalingGroup.html\n\nGroup Name: ${var.asg_name}\n"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 45,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/EC2", "CPUUtilization", "AutoScalingGroupName", "${var.asg_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 45,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/EC2", "StatusCheckFailed_Instance", "AutoScalingGroupName", "${var.asg_name}" ],
                    [ ".", "StatusCheckFailed_System", ".", "." ],
                    [ ".", "StatusCheckFailed", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 51,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/EC2", "NetworkOut", "AutoScalingGroupName", "${var.asg_name}" ],
                    [ ".", "NetworkIn", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 51,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/EC2", "NetworkPacketsIn", "AutoScalingGroupName", "${var.asg_name}" ],
                    [ ".", "NetworkPacketsOut", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 57,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/EC2", "DiskWriteOps", "AutoScalingGroupName", "${var.asg_name}" ],
                    [ ".", "DiskReadOps", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 57,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/EC2", "DiskReadBytes", "AutoScalingGroupName", "${var.asg_name}" ],
                    [ ".", "DiskWriteBytes", ".", "." ]
                ]
            }
        },


        {
            "type": "text",
            "x": 0,
            "y": 63,
            "width": 24,
            "height": 3,
            "properties": {
                "markdown": "\n# ${var.app}-${var.env}\n## Relational Database Service (RDS) Metrics - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/rds-metricscollected.html\n\nDB INSTANCE:\n* ${var.rds_name}\n"
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 69,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 69,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "DatabaseConnections", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 75,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "NetworkReceiveThroughput", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 75,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "NetworkTransmitThroughput", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 81,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "DiskQueueDepth", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 87,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "ReadIOPS", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 18,
            "y": 87,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "WriteIOPS", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 81,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "ReadLatency", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 18,
            "y": 81,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "WriteLatency", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 87,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "ReadThroughput", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 6,
            "y": 87,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "WriteThroughput", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 6,
            "y": 93,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "FreeableMemory", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 93,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "FreeStorageSpace", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 93,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "start": "-PT12H",
                "end": "P0D",
                "metrics": [
                    [ "AWS/RDS", "SwapUsage", "DBInstanceIdentifier", "${var.rds_name}" ]
                ]
            }
        },

        {
            "type": "text",
            "x": 0,
            "y": 99,
            "width": 24,
            "height": 3,
            "properties": {
                "markdown": "\n# ${var.app}-${var.env}\n## Network Address Translation (NAT) Gateway Metrics - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/nat-gateway-metricscollected.html\n\nNAT GATEWAY ID: ${var.nat_gw_name}\n"
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 102,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "metrics": [
                    [ "AWS/NATGateway", "ActiveConnectionCount", "NatGatewayId", "${var.nat_gw_name}" ]
                ],
                "region": "us-east-1"
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 102,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "ConnectionAttemptCount", "NatGatewayId", "${var.nat_gw_name}" ],
                    [ ".", "ConnectionEstablishedCount", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 108,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "PacketsInFromDestination", "NatGatewayId", "${var.nat_gw_name}" ],
                    [ ".", "PacketsOutToSource", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 108,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "PacketsOutToDestination", "NatGatewayId", "${var.nat_gw_name}" ],
                    [ ".", "PacketsInFromSource", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 120,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "IdleTimeoutCount", "NatGatewayId", "${var.nat_gw_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 6,
            "y": 120,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "ErrorPortAllocation", "NatGatewayId", "${var.nat_gw_name}" ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 0,
            "y": 114,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "BytesInFromDestination", "NatGatewayId", "${var.nat_gw_name}" ],
                    [ ".", "BytesOutToSource", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 114,
            "width": 12,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "BytesOutToDestination", "NatGatewayId", "${var.nat_gw_name}" ],
                    [ ".", "BytesInFromSource", ".", "." ]
                ]
            }
        },
        {
            "type": "metric",
            "x": 12,
            "y": 120,
            "width": 6,
            "height": 6,
            "properties": {
                "view": "timeSeries",
                "stacked": false,
                "region": "us-east-1",
                "metrics": [
                    [ "AWS/NATGateway", "PacketsDropCount", "NatGatewayId", "${var.nat_gw_name}" ]
                ]
            }
        }

    ]


}
 EOF
}
