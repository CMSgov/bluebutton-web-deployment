provider "aws" {
  region = "us-east-1"
}

module "fargate_demo" {
  source = "../modules/fargate_demo"

  # TODO: replace with any needed vars
}
