provider "aws" {
  region = "us-east-1"
}

data "aws_caller_identity" "current" {}

module "elb_akamai" {
  source = "../../modules/elb_akamai"
  
  cms_vpn_cidrs         = var.cms_vpn_cidrs
  akamai_prod_cidrs     = var.akamai_prod_cidrs
  akamai_staging_cidrs  = var.akamai_staging_cidrs
  env                   = "test"
  ssl_certificate_id    = "arn:aws:acm:us-east-1:${data.aws_caller_identity.current.account_id}:certificate/5adaf3f9-3046-4e39-a355-97050920ff1a"
}