# Data sources

data "aws_vpc" "fargate_demo" {
  filter {
    name   = "tag:Name"
    values = ["bluebutton-${var.env}"]
  }
}

data "aws_subnet_ids" "fargate_demo" {
  vpc_id = data.aws_vpc.fargate_demo.id

  filter {
    name   = "tag:Name"
    values = ["bluebutton-${var.env}-az?-dmz"]
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

# Resources

resource "aws_security_group" "fargate_demo" {
  name        = "${var.namespace}-${var.env}-lb-sg"
  description = "Security group for CMS VPN traffic to fargate demo load balancer"
  vpc_id      = data.aws_vpc.fargate_demo.id

  ingress {
    from_port   = data.aws_ssm_parameter.fargate_demo_port.value
    to_port     = data.aws_ssm_parameter.fargate_demo_port.value
    protocol    = "tcp"
    cidr_blocks = var.cms_vpn_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.namespace}-${var.env}-lb-sg"
    Environment = "${upper(var.env)}"
  }
}

resource "aws_lb" "fargate_demo" {
  name = "${var.namespace}-${var.env}-lb"

  internal           = true
  load_balancer_type = "application"

  security_groups = 
  subnets         = data.aws_subnet_ids.fargate_demo.ids

  tags = {
    Name        = "${var.namespace}-${var.env}-lb"
    Environment = "${upper(var.env)}"
  }
}

resource "aws_acm_certificate" "fargate_demo" {
  private_key      = data.aws_ssm_parameter.fargate_demo_key.value
  certificate_body = data.aws_ssm_parameter.fargate_demo_cert.value
}

resource "aws_lb_listener" "fargate_demo" {
  load_balancer_arn = aws_lb.fargate_demo.arn
  port              = data.aws_ssm_parameter.fargate_demo_port.value
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01" 
  certificate_arn   = aws_acm_certificate.fargate_demo.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.fargate_demo.arn
  }
}

resource "aws_lb_target_group" "fargate_demo" {
  name        = "${var.namespace}-${var.env}-lb-tg"
  port        = data.aws_ssm_parameter.fargate_demo_port.value
  protocol    = "HTTPS"
  target_type = "ip"
  vpc_id      = data.aws_vpc.fargate_demo.id
}
