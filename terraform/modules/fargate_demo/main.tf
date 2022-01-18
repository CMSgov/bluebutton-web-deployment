# Shared data sources

data "aws_vpc" "fargate_demo" {
  filter {
    name   = "tag:Name"
    values = ["bluebutton-${var.env}"]
  }
}

data "aws_ssm_parameter" "fargate_demo_port" {
  name = "/bb2/test/python-simple-https-server/server-port"
}

data "aws_ssm_parameter" "fargate_demo_key" {
  name = "/bb2/test/python-simple-https-server/server-key"
}

data "aws_ssm_parameter" "fargate_demo_cert" {
  name = "/bb2/test/python-simple-https-server/server-cert"
}

# Data sources for load balancer

data "aws_subnet_ids" "fargate_demo_lb" {
  vpc_id = data.aws_vpc.fargate_demo.id

  filter {
    name   = "tag:Name"
    values = ["bluebutton-${var.env}-az?-dmz"]
  }
}

# Data sources for ECS

data "aws_subnet_ids" "fargate_demo_ecs" {
  vpc_id = data.aws_vpc.fargate_demo.id

  filter {
    name   = "tag:Name"
    values = ["bluebutton-${var.env}-az?-app"]
  }
}