provider "aws" {
  region = "us-east-1"
}

resource "aws_sns_topic" "cloudwatch_alarms_topic" {
  name = "bluebutton-${var.stack}-cloudwatch-alarms"
}

module "asg" {
  source = "../modules/asg"

  app               = var.app
  stack             = var.stack
  env               = var.env
  vpc_id            = var.vpc_id
  key_name          = var.key_name
  ami_id            = var.ami_id
  instance_type     = var.instance_type
  elb_names         = var.elb_names
  asg_min           = var.asg_min
  asg_max           = var.asg_max
  asg_desired       = var.asg_desired
  azs               = var.azs
  ci_cidrs          = var.ci_cidrs
  app_sg_id         = var.app_sg_id
  vpn_sg_id         = var.vpn_sg_id
  ent_tools_sg_id   = var.ent_tools_sg_id
  sns_topic_arn     = aws_sns_topic.cloudwatch_alarms_topic.arn
  app_config_bucket = var.app_config_bucket
}

module "cloudwatch_alarms_elb_http" {
  source = "../modules/elb_http_alarms"

  app                               = var.app
  env                               = var.env
  vpc_name                          = var.vpc_id
  cloudwatch_notification_arn       = aws_sns_topic.cloudwatch_alarms_topic.arn
  load_balancer_name                = var.elb_names[0]

  alarm_elb_no_backend_enable       = var.alarm_elb_no_backend_enable
  alarm_elb_no_backend_eval_periods = var.alarm_elb_no_backend_eval_periods
  alarm_elb_no_backend_period       = var.alarm_elb_no_backend_period
  alarm_elb_no_backend_threshold    = var.alarm_elb_no_backend_threshold
}
