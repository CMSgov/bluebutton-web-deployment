/*   Private Subnets */


data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }

  filter {
    name   = "tag:Name"
    values = ["*private*"]
  }
}
data "aws_acm_certificate" "selected" {
  domain   = var.acm_domain_search_string
  statuses = ["ISSUED"]
  most_recent = true
}

resource "aws_elb" "default" {
  name = "bb-${var.stack}-clb-akamai"

  access_logs {
    bucket   = "cms-cloud-926529379239-us-east-1"
    interval = 60
  }

  security_groups = [
    var.akamai_prod_cidrs,
    var.cms_vpn_cidrs
  ]

  subnets = data.aws_subnets.default.ids

  listener {
    instance_port      = 80
    instance_protocol  = "http"
    lb_port            = 80
    lb_protocol        = "http"
  }

  listener {
    instance_port      = 443
    instance_protocol  = "https"
    lb_port            = 443
    lb_protocol        = "https"
    ssl_certificate_id = data.aws_acm_certificate.selected.arn
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
    Name        = "bb-${var.stack}-clb-akamai"
    Function    = "ClassicLoadBalancer"
    Environment = upper(var.env)
    Application = "bluebutton"
    Business    = "OEDA"
  }
}

resource "aws_load_balancer_policy" "default-ssl-tls-1-2" {
  load_balancer_name = aws_elb.default.name
  policy_name        = "${aws_elb.default.name}-ssl"
  policy_type_name   = "SSLNegotiationPolicyType"

  policy_attribute {
    name  = "Reference-Security-Policy"
    value = "ELBSecurityPolicy-TLS-1-2-2017-01"
  }
}

resource "aws_load_balancer_listener_policy" "default-listener-policies-443" {
  load_balancer_name = aws_elb.default.name
  load_balancer_port = 443

  policy_names = [
    aws_load_balancer_policy.default-ssl-tls-1-2.policy_name
  ]
}
