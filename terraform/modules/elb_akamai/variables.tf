variable "env" {}
variable "stack" {}
variable "acm_domain_search_string" {
  description = "Domain search string to find matching ACM certificate"
  type        = string
}
variable "vpc_id" {}
variable "vpn_sg_id" {
  description = "List of VPN security group IDs"
  type        = list(string)
}
variable "cms_vpn_cidrs" {
  description = "Security group ID for CMS VPN"
  type        = string
}

variable "akamai_prod_cidrs" {
  description = "Security group ID for Akamai Prod"
  type        = string
}

