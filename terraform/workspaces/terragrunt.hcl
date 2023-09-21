# terragrunt.hcl
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = "bucket_name"

    key = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "db_name"
  }
}


terraform {
  extra_arguments "common_vars" {
    # commands = get_terraform_commands_that_need_vars() - helper for getting all commands that use vars
    commands = ["plan", "apply"]

    arguments = [
      "-var-file=../../../region.tfvars"
    ]
  }
}