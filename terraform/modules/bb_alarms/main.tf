##
#
# NOTE: This module is for defining CloudWatch alarms
#
##


resource "aws_cloudwatch_metric_alarm" "status_check_failed" {
  count               = "${var.alarm_status_check_failed_enable}"
  alarm_name          = "${var.app}-${var.env}-status_check_failed"
  comparison_operator = "GreaterThanOrEqualToThreshold"

  evaluation_periods  = "${var.alarm_status_check_failed_eval_periods}"
  metric_name         = "StatusCheckFailed"
  namespace           = "AWS/EC2"
  period              = "${var.alarm_status_check_failed_period}"
  statistic           = "Sum"


  dimensions {
    AutoScalingGroupName = "${var.asg_name}"
  }

  alarm_description = "Both instance and system status checks have FAILED for ${var.asg_name} ASG in APP-ENV: ${var.app}-${var.env}"

  threshold         = "${var.alarm_status_check_failed_threshold}"
  unit              = "Count"
  treat_missing_data = "notBreaching"

  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}


resource "aws_cloudwatch_metric_alarm" "status_check_failed_instance" {
  count               = "${var.alarm_status_check_failed_instance_enable}"
  alarm_name          = "${var.app}-${var.env}-status_check_instance"
  comparison_operator = "GreaterThanOrEqualToThreshold"

  evaluation_periods  = "${var.alarm_status_check_failed_instance_eval_periods}"
  metric_name         = "StatusCheckFailed_Instance"
  namespace           = "AWS/EC2"
  period              = "${var.alarm_status_check_failed_instance_period}"
  statistic           = "Sum"

  dimensions {
    AutoScalingGroupName = "${var.asg_name}"
  }

  alarm_description = "Instance status check has FAILED for ${var.asg_name} ASG in APP-ENV: ${var.app}-${var.env}"

  threshold         = "${var.alarm_status_check_failed_instance_threshold}"
  unit              = "Count"
  treat_missing_data = "notBreaching"

  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "status_check_failed_system" {
  count               = "${var.alarm_status_check_failed_system_enable}"
  alarm_name          = "${var.app}-${var.env}-status_check_system"
  comparison_operator = "GreaterThanOrEqualToThreshold"

  evaluation_periods  = "${var.alarm_status_check_failed_system_eval_periods}"
  metric_name         = "StatusCheckFailed_System"
  namespace           = "AWS/EC2"
  period              = "${var.alarm_status_check_failed_system_period}"
  statistic           = "Sum"


  dimensions {
    AutoScalingGroupName = "${var.asg_name}"
  }

  alarm_description = "System status check has FAILED for ${var.asg_name} ASG in APP-ENV: ${var.app}-${var.env}"

  threshold         = "${var.alarm_status_check_failed_system_threshold}"
  unit              = "Count"
  treat_missing_data = "notBreaching"

  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}



resource "aws_cloudwatch_metric_alarm" "healthy_hosts" {
  count               = "${var.alarm_elb_no_backend_enable}"
  alarm_name          = "${var.load_balancer_name}-elb-no-backend"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "${var.alarm_elb_no_backend_eval_periods}"
  metric_name         = "HealthyHostCount"
  namespace           = "AWS/ELB"
  period              = "${var.alarm_elb_no_backend_period}"
  statistic           = "Average"
  threshold           = "${var.alarm_elb_no_backend_threshold}"

  alarm_description   = "No backends available for ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  # We should always have a measure of the number of healthy hosts - alert if not
  treat_missing_data = "breaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "high_latency" {
  count               = "${var.alarm_elb_high_latency_enable}"
  alarm_name          = "elb-${var.load_balancer_name}-high-latency"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_elb_high_latency_eval_periods}"
  metric_name         = "Latency"
  namespace           = "AWS/ELB"
  period              = "${var.alarm_elb_high_latency_period}"
  statistic           = "Average"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "${var.alarm_elb_high_latency_threshold}"
  unit              = "Seconds"
  alarm_description = "High latency for ELB ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  # "Missing data" means that we haven't had any measure of latency - alert if we don't
  treat_missing_data = "breaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "spillover_count" {
  count               = "${var.alarm_elb_spillover_count_enable}"
  alarm_name          = "elb-${var.load_balancer_name}-spillover-count"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_elb_spillover_count_eval_periods}"
  metric_name         = "SpilloverCount"
  namespace           = "AWS/ELB"
  period              = "${var.alarm_elb_spillover_count_period}"
  statistic           = "Maximum"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }


  threshold         = "${var.alarm_elb_spillover_count_threshold}"
  unit              = "Count"
  alarm_description = "Spillover alarm for ELB ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  # A missing spillover count means that we haven't spillover - that's good! Don't alert.
  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "surge_queue_exceeded" {
  count               = "${var.alarm_elb_surge_queue_length_enable}"
  alarm_name          = "elb-${var.load_balancer_name}-surge-queue-length"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_elb_surge_queue_length_eval_periods}"
  metric_name         = "SurgeQueueLength"
  namespace           = "AWS/ELB"
  period              = "${var.alarm_elb_surge_queue_length_period}"
  statistic           = "Maximum"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "${var.alarm_elb_surge_queue_length_threshold}"
  unit              = "Count"
  alarm_description = "Surge queue exceeded for ELB ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  # An undefined surge queue length is good - we haven't had to queue any requests recently, so
  # don't alert
  treat_missing_data = "notBreaching"

  alarm_actions = ["${var.cloudwatch_notification_arn}"]
  ok_actions    = ["${var.cloudwatch_notification_arn}"]
}


resource "aws_cloudwatch_metric_alarm" "httpcode_backend_4xx" {
  count               = "${var.alarm_backend_4xx_enable}"
  alarm_name          = "elb-${var.load_balancer_name}-httpcode-backend-4xx"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_backend_4xx_eval_periods}"
  metric_name         = "HTTPCode_Backend_4XX"
  namespace           = "AWS/ELB"
  period              = "${var.alarm_backend_4xx_period}"
  statistic           = "Sum"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "${var.alarm_backend_4xx_threshold}"
  unit              = "Count"
  alarm_description = "HTTP Backend 4xx response codes exceeded for ELB ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  treat_missing_data = "notBreaching"

  alarm_actions = ["${var.cloudwatch_notification_arn}"]
  ok_actions    = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "httpcode_backend_5xx" {
  count               = "${var.alarm_backend_5xx_enable}"
  alarm_name          = "elb-${var.load_balancer_name}-httpcode-backend-5xx"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_backend_5xx_eval_periods}"
  metric_name         = "HTTPCode_Backend_5XX"
  namespace           = "AWS/ELB"
  period              = "${var.alarm_backend_5xx_period}"
  statistic           = "Sum"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "${var.alarm_backend_5xx_threshold}"
  unit              = "Count"
  alarm_description = "HTTP Backend 5xx response codes exceeded for ELB ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  treat_missing_data = "notBreaching"

  alarm_actions = ["${var.cloudwatch_notification_arn}"]
  ok_actions    = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "httpcode_elb_5xx" {
  count               = "${var.alarm_elb_5xx_enable}"
  alarm_name          = "elb-${var.load_balancer_name}-httpcode-elb-5xx"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_elb_5xx_eval_periods}"
  metric_name         = "HTTPCode_ELB_5XX"
  namespace           = "AWS/ELB"
  period              = "${var.alarm_elb_5xx_period}"
  statistic           = "Sum"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "${var.alarm_elb_5xx_threshold}"
  unit              = "Count"
  alarm_description = "HTTP ELB 5xx response codes exceeded for ELB ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  treat_missing_data = "notBreaching"

  alarm_actions = ["${var.cloudwatch_notification_arn}"]
  ok_actions    = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "rds_high_cpu" {
  count               = "${var.alarm_rds_high_cpu_enable}"
  alarm_name          = "${var.rds_name}-rds-high-cpu"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_rds_high_cpu_eval_periods}"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "${var.alarm_rds_high_cpu_period}"
  statistic           = "Average"
  threshold           = "${var.alarm_rds_high_cpu_threshold}"

  alarm_description   = "RDS - CPU Utilization is high for ${var.rds_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.rds_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "rds_free_storage" {
  count               = "${var.alarm_rds_free_storage_enable}"
  alarm_name          = "${var.rds_name}-rds-free-storage"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_rds_free_storage_eval_periods}"
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  period              = "${var.alarm_rds_free_storage_period}"
  statistic           = "Average"
  threshold           = "${var.alarm_rds_free_storage_threshold}"

  alarm_description   = "RDS - Free storage space is low for ${var.rds_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.rds_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "rds_write_latency" {
  count               = "${var.alarm_rds_write_latency_enable}"
  alarm_name          = "${var.rds_name}-rds-write-latency"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_rds_write_latency_eval_periods}"
  metric_name         = "WriteLatency"
  namespace           = "AWS/RDS"
  period              = "${var.alarm_rds_write_latency_period}"
  statistic           = "Average"
  threshold           = "${var.alarm_rds_write_latency_threshold}"

  alarm_description   = "RDS - Write latency is high for ${var.rds_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.rds_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "rds_read_latency" {
  count               = "${var.alarm_rds_read_latency_enable}"
  alarm_name          = "${var.rds_name}-rds-read-latency"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_rds_read_latency_eval_periods}"
  metric_name         = "ReadLatency"
  namespace           = "AWS/RDS"
  period              = "${var.alarm_rds_read_latency_period}"
  statistic           = "Average"
  threshold           = "${var.alarm_rds_read_latency_threshold}"

  alarm_description   = "RDS - Read latency is high for ${var.rds_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.rds_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "rds_swap_usage" {
  count               = "${var.alarm_rds_swap_usage_enable}"
  alarm_name          = "${var.rds_name}-rds-swap-usage"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "${var.alarm_rds_swap_usage_eval_periods}"
  metric_name         = "SwapUsage"
  namespace           = "AWS/RDS"
  period              = "${var.alarm_rds_swap_usage_period}"
  statistic           = "Sum"
  threshold           = "${var.alarm_rds_swap_usage_threshold}"

  alarm_description   = "RDS - Swap Usage is high for ${var.rds_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.rds_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "rds_disk_queue_depth" {
  count               = "${var.alarm_rds_disk_queue_depth_enable}"
  alarm_name          = "${var.rds_name}-rds-disk-queue-depth"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_rds_disk_queue_depth_eval_periods}"
  metric_name         = "DiskQueueDepth"
  namespace           = "AWS/RDS"
  period              = "${var.alarm_rds_disk_queue_depth_period}"
  statistic           = "Average"
  threshold           = "${var.alarm_rds_disk_queue_depth_threshold}"

  alarm_description   = "RDS - Disk queue depth is high for ${var.rds_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.rds_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "rds_free_memory" {
  count               = "${var.alarm_rds_free_memory_enable}"
  alarm_name          = "${var.rds_name}-rds-free-memory"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "${var.alarm_rds_free_memory_eval_periods}"
  metric_name         = "FreeableMemory"
  namespace           = "AWS/RDS"
  period              = "${var.alarm_rds_free_memory_period}"
  statistic           = "Average"
  threshold           = "${var.alarm_rds_free_memory_threshold}"

  alarm_description   = "RDS - Free memory is low for ${var.rds_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.rds_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}


resource "aws_cloudwatch_metric_alarm" "nat_error_port_alloc" {
  count               = "${var.alarm_nat_error_port_alloc_enable}"
  alarm_name          = "${var.rds_name}-nat-error-port-alloc"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "${var.alarm_nat_error_port_alloc_eval_periods}"
  metric_name         = "ErrorPortAllocation"
  namespace           = "AWS/NATGateway"
  period              = "${var.alarm_nat_error_port_alloc_period}"
  statistic           = "Sum"
  threshold           = "${var.alarm_nat_error_port_alloc_threshold}"

  alarm_description   = "NAT GATEWAY - Port allocation error count is high for ${var.nat_gw_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.nat_gw_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "nat_packets_drop_count" {
  count               = "${var.alarm_nat_packets_drop_count_enable}"
  alarm_name          = "${var.rds_name}-nat-packets-drop-count"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "${var.alarm_nat_packets_drop_count_eval_periods}"
  metric_name         = "PacketsDropCount"
  namespace           = "AWS/NATGateway"
  period              = "${var.alarm_nat_packets_drop_count_period}"
  statistic           = "Sum"
  threshold           = "${var.alarm_nat_packets_drop_count_threshold}"

  alarm_description   = "NAT GATEWAY - Packets drop count is high for ${var.nat_gw_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    DBInstanceIdentifier = "${var.nat_gw_name}"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

