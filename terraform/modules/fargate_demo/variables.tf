variable "namespace" {
  type    = string
  default = "bb2-fargate-demo"
}

variable "env" {
  type    = string
  default = "test"
}

variable "cms_vpn_cidrs" {
    type = list(string)
}
