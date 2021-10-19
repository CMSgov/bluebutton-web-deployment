data "aws_vpc" "default" {
  filter {
    name   = "tag:Name"
    values = ["bluebutton-${var.env}"]
  }
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "tag:Name"
    values = ["bluebutton-${var.env}-az?-dmz"]
  }
}

resource "aws_security_group" "akamai_prod" {
  name          = "bb-sg-${var.env}-clb-akamai-prod"
  description   = "Security group for akamai prod traffic to ${var.env} classic load balancer"
  vpc_id        = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.akamai_prod_cidrs
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.akamai_prod_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bb-sg-${var.env}-clb-akamai-prod"
  }
}

resource "aws_security_group" "akamai_staging" {
  name          = "bb-sg-${var.env}-clb-akamai-staging"
  description   = "Security group for akamai staging traffic to ${var.env} classic load balancer"
  vpc_id        = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.akamai_staging_cidrs
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.akamai_staging_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bb-sg-${var.env}-clb-akamai-staging"
  }
}

resource "aws_security_group" "cms_vpn" {
  name          = "bb-sg-${var.env}-clb-cms-vpn"
  description   = "Security group for cms vpn traffic to ${var.env} classic load balancer"
  vpc_id        = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.cms_vpn_cidrs
  }

  ingress {
    from_port   = 443
    to_port     = 443
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
    Name = "bb-sg-${var.env}-clb-cms-vpn"
  }
}

resource "aws_elb" "default" {
  name = "bb-${var.env}-clb-akamai"

  access_logs {
    bucket   = "bb-${var.env}-logs-lb-access"
    interval = 60
  }

  security_groups = ["${aws_security_group.akamai_prod.id}", "${aws_security_group.akamai_staging.id}", "${aws_security_group.cms_vpn.id}"]

  subnets = data.aws_subnet_ids.default.ids

  listener {
    instance_port             = 80
    instance_protocol         = "http"
    lb_port                   = 80
    lb_protocol               = "http"
  }

  listener {
    instance_port             = 443
    instance_protocol         = "https"
    lb_port                   = 443
    lb_protocol               = "https"
    ssl_certificate_id        = var.ssl_certificate_id
  }

  health_check {
    healthy_threshold         = 2
    unhealthy_threshold       = 10
    timeout                   = 5
    target                    = "HTTPS:443/health"
    interval                  = 60
  }

  cross_zone_load_balancing   = true
  idle_timeout                = 60
  connection_draining         = true
  connection_draining_timeout = 300

  tags = {
    Name                      = "bb-${var.env}-clb-akamai"
    Function                  = "ClassicLoadBalancer"
    Environment               = "${upper(var.env)}"
    Application               = "bluebutton"
    Business                  = "OEDA"
  }
}


resource "aws_load_balancer_policy" "default-ssl-tls-1-2" {
  load_balancer_name  = aws_elb.default.name
  policy_name         = "${aws_elb.default.name}-ssl"
  policy_type_name    = "SSLNegotiationPolicyType"

  policy_attribute {
    name              = "Reference-Security-Policy"
    value             = "ELBSecurityPolicy-TLS-1-2-2017-01"
  }
}

resource "aws_load_balancer_listener_policy" "default-listener-policies-443" {
  load_balancer_name  = aws_elb.default.name
  load_balancer_port  = 443

  policy_names = [
    "${aws_load_balancer_policy.default-ssl-tls-1-2.policy_name}"
  ]
}