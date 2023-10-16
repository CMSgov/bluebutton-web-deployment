variable "cms_vpn_cidrs" {
  type = list(string)
}

variable "akamai_prod_cidrs" {
  type = list(string)
}

variable "akamai_staging_cidrs" {
  type = list(string)
}

variable "aws_region" {}
