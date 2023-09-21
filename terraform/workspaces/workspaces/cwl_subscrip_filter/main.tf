# provider "aws" {
#   region = "us-east-1"
# }

# Copy/paste & customize variables to add new subscription filters for BFD insights
#
# NOTE: this subscription filter module is setup for the BFD account, if BFD is not
# the desired account, we should add some logic here for the account number

module "cwl_subscrip_filter" {
  source         = "../../../modules/cwl_subscrip_filter"
  filter_name    = "${terraform.workspace}-perf-mon"
  bfd_acct       = var.bfd_acct
  log_group_name = "/bb/${terraform.workspace}/app/perf_mon.log"
}
