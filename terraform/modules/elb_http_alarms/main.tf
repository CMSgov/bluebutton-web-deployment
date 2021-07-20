##
#
# NOTE: This module is for defining ELB - HTTP CloudWatch alarms
#
##

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

  alarm_description = "No backends available for ${var.load_balancer_name} in ${var.vpc_name} in APP-ENV: ${var.app}-${var.env}"

  dimensions {
    LoadBalancerName = "${var.load_balancer_name}"
  }

  # We should always have a measure of the number of healthy hosts - alert if not
  treat_missing_data = "breaching"
  alarm_actions      = ["${var.cloudwatch_notification_arn}"]
  ok_actions         = ["${var.cloudwatch_notification_arn}"]
  datapoints_to_alarm = "1"
}
