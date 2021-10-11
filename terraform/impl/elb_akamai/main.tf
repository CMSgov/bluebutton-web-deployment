provider "aws" {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {}

module "elb_akamai" {
  source = "../../modules/elb_akamai"

  cms_vpn_cidrs         = "${var.cms_vpn_cidrs}"
  akamai_prod_cidrs     = "${var.akamai_prod_cidrs}"
  akamai_staging_cidrs  = "${var.akamai_staging_cidrs}"
  env                   = "impl"
  ssl_certificate_id    = "arn:aws:acm:us-east-1:${data.aws_caller_identity.current.account_id}:certificate/c1d8ff01-58c1-4df2-9a2a-755dd6290027"
}