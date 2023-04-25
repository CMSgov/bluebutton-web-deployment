variable "env" {}

variable "app_config_bucket" {}

variable "vpc_id" {}

variable "ci_cidrs" {
  type = list(string)
}

variable "prefix_lists" {
  type = list(string)
}

variable "ami_id" {}

variable "instance_type" {}

variable "key_name" {}

variable "subnet_id" {}

variable "iam_instance_profile" {}

variable "vpc_sg_id" {}

variable "instance_name" {}

variable "static_content_bucket" {}
