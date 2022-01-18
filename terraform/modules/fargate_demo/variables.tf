variable "namespace" {
  type    = string
}

variable "env" {
  type    = string
}

variable "cms_vpn_cidrs" {
    type = list(string)
}
