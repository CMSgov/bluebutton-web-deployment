variable "app" {}

variable "stack" {}

variable "env" {}

variable "vpc_id" {}

variable "key_name" {}

variable "ami_id" {}

variable "instance_type" {}

variable "elb_name" {}

variable "app_sg_id" {}

variable "vpn_sg_id" {}

variable "asg_min" {}

variable "asg_max" {}

variable "asg_desired" {}

variable "azs" {
  type = "list"
}

variable "ci_cidrs" {
  type = "list"
}

variable "cloudwatch_max_latency_secs" {
  description = "Maximum average latency threshold."
  type        = "string"
  default     = "2"
}

