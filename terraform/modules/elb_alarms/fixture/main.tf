# Test fixture for kitchen-terraform
#
# This configuration is what kitchen-terraform runs against, so here you can
# define any resources that your module depends on as well as your module itself
# so that it can all be set up automatically.

provider "aws" {
  region = "${var.aws_region}"
}

terraform {
  backend "s3" {}
}

# Test harness variables
#
# These are automatically set by the test boilerplate, and can be used or not
# used by the module being tested.
variable "vpc_name" {
  description = "The name of the temporary test vpc"
}

variable "environment_name" {
  description = "The name of the temporary test environment"
}

variable "aws_region" {
  description = "The region to deploy to"
  default     = "us-east-1"
}

resource "aws_sns_topic" "alarm_topic" {
  name = "${var.vpc_name}"
}

resource "aws_vpc" "base" {
  cidr_block = "10.0.0.0/16"
}

data "aws_availability_zones" "available" {}

resource "aws_subnet" "base" {
  count             = 2
  vpc_id            = "${aws_vpc.base.id}"
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = "${data.aws_availability_zones.available.names[count.index]}"
}

resource "aws_security_group" "allow_all" {
  name        = "${var.vpc_name}"
  vpc_id      = "${aws_vpc.base.id}"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "${var.vpc_name}"
  }
}

resource "aws_elb" "alarmed_balancer" {
  name            = "terraform-harness-load-balancer"
  subnets         = ["${aws_subnet.base.*.id}"]
  security_groups = ["${aws_security_group.allow_all.id}"]
  internal        = true

  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

  tags {
    created_by = "terraform-harness"
    vpc_name   = "${var.vpc_name}"
  }
}

module "cloudwatch_alarms" {
  # Here you can use "../../../test-module" to pull in the module from the local
  # directory.  Remember that it needs to be relative to where test kitchen
  # copies this fixture, which is in ".kitchen".
  source = "../../../test-module"

  vpc_name                    = "${var.vpc_name}"
  cloudwatch_notification_arn = "${aws_sns_topic.alarm_topic.arn}"
  load_balancer_name          = "${aws_elb.alarmed_balancer.name}"
}
