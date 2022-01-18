provider "aws" {
  region = "us-east-1"
}

locals {
  namespace = "bb2-fargate-demo"
  env       = "test"
}

module "fargate_demo" {
  source = "../modules/fargate_demo"

  namespace     = local.namespace
  env           = local.env
  cms_vpn_cidrs = var.cms_vpn_cidrs
}
