variable "vpc_name" {
  description = "Name of the VPC these alarms are for."
  type        = string
}

variable "load_balancer_name" {
  description = "Name of the ELB these alarms are for."
  type        = string
}

variable "cloudwatch_notification_arn" {
  description = "The CloudWatch notification ARN."
  type        = string
}

variable "app" {}
variable "stack" {}

variable "env" {}

variable "alarm_elb_no_backend_enable" { 
  type        = bool
}

variable "alarm_elb_no_backend_eval_periods" {}
variable "alarm_elb_no_backend_period" {}
variable "alarm_elb_no_backend_threshold" {}
