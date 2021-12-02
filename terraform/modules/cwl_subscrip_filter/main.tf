provider "aws" {
  region = "us-east-1"
}

locals {
  dest_arn = "arn:aws:logs:us-east-1:${var.bfd_acct}:destination:bfd-insights-bb2-${var.filter_name}-firehose-destination"
}

resource "aws_cloudwatch_log_subscription_filter" "cwl_subscription_filter" {
  name            = var.filter_name
  log_group_name  = var.log_group_name
  filter_pattern  = ""
  destination_arn = local.dest_arn
}