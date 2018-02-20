provider "aws" {
  region = "us-east-1"
}

module "asg" {
  source = "../modules/asg"

  app           = "${var.app}"
  stack         = "${var.stack}"
  env           = "${var.env}"
  vpc_id        = "${var.vpc_id}"
  key_name      = "${var.key_name}"
  ami_id        = "${var.ami_id}"
  instance_type = "${var.instance_type}"
  elb_name      = "${var.elb_name}"
  asg_min       = "${var.asg_min}"
  asg_max       = "${var.asg_max}"
  asg_desired   = "${var.asg_desired}"
  azs           = ["${var.azs}"]
  ci_cidrs      = ["${var.ci_cidrs}"]
  app_sg_id     = "${var.app_sg_id}"
  vpn_sg_id     = "${var.vpn_sg_id}"
}
