provider "aws" {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {
}

resource "aws_cloudwatch_metric_alarm" "ses_alerts" {
  alarm_name          = "bb-prod-ses-bounce-rate-high"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  alarm_actions       = ["arn:aws:sns:us-east-1:${data.aws_caller_identity.current.account_id}:slack-topic"]
  alarm_description   = "SES bounce rate average is greater than or equal to .01% in a 1 hour time period"
  datapoints_to_alarm = "1"
  metric_name         = "Reputation.BounceRate"
  namespace           = "AWS/SES"
  period              = "3600"
  statistic           = "Average"
  threshold           = ".01"
}

