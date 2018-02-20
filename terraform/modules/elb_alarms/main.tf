##
#
# NOTE: this module was copied from https://github.com/CMSgov/tf-elb-alarms.
#
# It's not publicly available as of yet. Please avoid making modifications to this module directly to ensure migration to the public module is possible at a later date.
#
# Contact @rnagle or @sverchdotgov with questions.
#
##
resource "aws_cloudwatch_metric_alarm" "healthy_hosts" {
  alarm_name          = "${var.load_balancer_name}-elb-no-backend"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "HealthyHostCount"
  namespace           = "AWS/ELB"
  period              = "60"
  statistic           = "Average"
  threshold           = "${var.cloudwatch_healthy_hosts_min}"
  alarm_description   = "No backends available for ${var.load_balancer_name} in ${var.vpc_name}"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  # We should always have a measure of the number of healthy hosts - alert if not
  treat_missing_data = "breaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "high_latency" {
  alarm_name          = "elb-${var.load_balancer_name}-high-latency"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "Latency"
  namespace           = "AWS/ELB"
  period              = "${var.cloudwatch_max_latency_window_secs}"
  statistic           = "Average"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "${var.cloudwatch_max_latency_secs}"
  unit              = "Seconds"
  alarm_description = "High latency for ELB ${var.load_balancer_name} in ${var.vpc_name}."

  # "Missing data" means that we haven't had any measure of latency - alert if we don't
  treat_missing_data = "breaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "spillover_count" {
  alarm_name          = "elb-${var.load_balancer_name}-spillover-count"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "SpilloverCount"
  namespace           = "AWS/ELB"
  period              = "60"
  statistic           = "Maximum"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "3"
  unit              = "Count"
  alarm_description = "Spillover alarm for ELB ${var.load_balancer_name} in ${var.vpc_name}. Add nodes."

  # A missing spillover count means that we haven't spillover - that's good! Don't alert.
  treat_missing_data = "notBreaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
}

resource "aws_cloudwatch_metric_alarm" "surge_queue_exceeded" {
  alarm_name          = "elb-${var.load_balancer_name}-surge-queue-length"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "3"
  metric_name         = "SurgeQueueLength"
  namespace           = "AWS/ELB"
  period              = "60"
  statistic           = "Maximum"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  threshold         = "300"
  unit              = "Count"
  alarm_description = "Surge queue exceeded for ELB ${var.load_balancer_name} in ${var.vpc_name}. Add nodes."

  # An undefined surge queue length is good - we haven't had to queue any requests recently, so
  # don't alert
  treat_missing_data = "notBreaching"

  alarm_actions = ["${var.cloudwatch_notification_arn}"]
  ok_actions    = ["${var.cloudwatch_notification_arn}"]
}
