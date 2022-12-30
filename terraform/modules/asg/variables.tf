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

variable "app_config_bucket" {}

variable "static_content_bucket" {}

variable "azs" {
  type = list(string)
}

variable "ci_cidrs" {
  type = list(string)
}

variable "sns_topic_arn" {
  default = ""
}
