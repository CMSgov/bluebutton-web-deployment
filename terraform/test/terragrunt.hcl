# workspaces/elb/terragrunt.hcl
locals {
  s3_bucket = "bb2-terraform-state-dev"  # Adjust per environment
}
include "root" {
  path = find_in_parent_folders()
}