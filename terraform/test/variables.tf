variable "app" {}

variable "stack" {}

variable "env" {}

variable "vpc_id" {}

variable "key_name" {}

variable "ami_id" {}

variable "instance_type" {}

variable "elb_names" {
  type = list(string)
}

variable "app_sg_id" {}

variable "vpn_sg_id" {}

variable "ent_tools_sg_id" {}

variable "asg_min" {}

variable "asg_max" {}

variable "asg_desired" {}

variable "azs" {
  type = list(string)
}

variable "ci_cidrs" {
  type = list(string)
}

variable "asg_name" {
  default = ""
}

variable "app_config_bucket" {}

variable "static_content_bucket" {}

variable "alarm_elb_no_backend_enable" {
  type    = bool
}

variable "alarm_elb_no_backend_eval_periods" {}
variable "alarm_elb_no_backend_period" {}
variable "alarm_elb_no_backend_threshold" {}
