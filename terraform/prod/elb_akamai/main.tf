provider "aws" {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {}

module "elb_akamai" {
  source = "../../modules/elb_akamai"

  cms_vpn_cidrs         = "${var.cms_vpn_cidrs}"
  akamai_prod_cidrs     = "${var.akamai_prod_cidrs}"
  akamai_staging_cidrs  = "${var.akamai_staging_cidrs}"
  env                   = "prod"
  ssl_certificate_id    = "arn:aws:acm:us-east-1:${data.aws_caller_identity.current.account_id}:certificate/cce86be9-2241-4b26-80be-b33bbf6a21d3"
}
