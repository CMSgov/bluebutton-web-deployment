provider "aws" {
  region = "us-east-1"
}

locals {
  env = terraform.workspace

  domain_name_value = {
    "test" = "test.bluebutton.cms.gov"
    "impl" = "sandbox.bluebutton.cms.gov"
    "prod" = "api.bluebutton.cms.gov"
  }

  domain_name = lookup(local.domain_name_value, terraform.workspace, "")
}

data "aws_caller_identity" "current" {}

data "aws_acm_certificate" "cert" {
  domain   = local.domain_name
  statuses = ["ISSUED"]
}

module "elb_akamai" {
  source = "../../modules/elb_akamai"

  cms_vpn_cidrs        = var.cms_vpn_cidrs
  akamai_prod_cidrs    = var.akamai_prod_cidrs
  akamai_staging_cidrs = var.akamai_staging_cidrs
  env                  = local.env
  ssl_certificate_id   = data.aws_acm_certificate.cert.arn
}

output "env" {
  value = local.env
}

output "subdomain" {
  value = local.domain_name
}