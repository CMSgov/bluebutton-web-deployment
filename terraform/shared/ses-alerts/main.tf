provider "aws" {
  region = "us-east-1"
}

resource "aws_cloudwatch_metric_alarm" "ses_alerts" {
    alarm_name              = "bluebutton-SES-bounce-rate-high"
    comparison_operator     = "GreaterThanThreshold"
    evaluation_periods      = "1"
    alarm_actions           = ["arn:aws:sns:us-east-1:501705132200:slack-topic"]
    alarm_description       = "SES bounce rate exceeds 2 in 1 hour"
    datapoints_to_alarm     = "1"
    metric_name             = "Bounce"
    namespace               = "AWS/SES"
    period                  = "3600"
    statistic               = "Average"
    threshold               = "2"
}