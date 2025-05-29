provider "aws" {
  region = "us-east-1"
}
module "alb" {
  source = "../modules/elb_akamai"
  acm_domain_search_string = var.acm_domain_search_string
  vpc_id                = var.vpc_id
  env                   = var.env
  cms_vpn_cidrs         = var.cms_vpn_cidrs
  akamai_prod_cidrs     = var.akamai_prod_cidrs
  stack                 = var.stack

}
resource "aws_sns_topic" "cloudwatch_alarms_topic" {
  name              = "bb-${var.stack}-cloudwatch-alarms"
  kms_master_key_id = "alias/aws/sns"
}

module "asg" {
  source = "../modules/asg"

  app                   = var.app
  stack                 = var.stack
  env                   = var.env
  vpc_id                = var.vpc_id
  key_name              = var.key_name
  ami_id                = var.ami_id
  instance_type         = var.instance_type
  elb_names             = var.elb_names
  asg_min               = var.asg_min
  asg_max               = var.asg_max
  asg_desired           = var.asg_desired
  azs                   = var.azs
  ci_cidrs              = var.ci_cidrs
  app_sg_id             = var.app_sg_id
  vpn_sg_id             = var.vpn_sg_id
  ent_tools_sg_id       = var.ent_tools_sg_id
  sns_topic_arn         = aws_sns_topic.cloudwatch_alarms_topic.arn
  app_config_bucket     = var.app_config_bucket
  static_content_bucket = var.static_content_bucket
}

module "cloudwatch_alarms_elb_http" {
  source = "../modules/elb_http_alarms"

  app                         = var.app
  env                         = var.env
  vpc_name                    = var.vpc_id
  cloudwatch_notification_arn = aws_sns_topic.cloudwatch_alarms_topic.arn
  load_balancer_name          = var.elb_names[0]

  alarm_elb_no_backend_enable       = var.alarm_elb_no_backend_enable
  alarm_elb_no_backend_eval_periods = var.alarm_elb_no_backend_eval_periods
  alarm_elb_no_backend_period       = var.alarm_elb_no_backend_period
  alarm_elb_no_backend_threshold    = var.alarm_elb_no_backend_threshold
}

module "iam_param_store" {
  source = "../modules/iam_param_store"

  env = lower(var.env)
}
module "kms" {
  source = "../modules/kms"
  stack  = var.stack
}
