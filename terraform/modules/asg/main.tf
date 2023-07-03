##
# Data providers
##
data "aws_vpc" "selected" {
  id = var.vpc_id
}

data "aws_subnets" "app" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }

  tags = {
    Layer       = "app"
    stack       = var.stack
    application = var.app
  }
}

data "aws_ami" "image" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "image-id"
    values = [var.ami_id]
  }
}

data "aws_ec2_managed_prefix_list" "sg_prefix_list" {
  filter {
    name   = "prefix-list-name"
    values = ["cmscloud-oc-management-subnets"]
  }
}

##
# Security groups
##
resource "aws_security_group" "ci" {
  name        = "ci-to-app-servers"
  description = "Allow CI access to app servers"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ci_cidrs
  }

  ingress {
    description      = "HTTPS from CI"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    prefix_list_ids  = ["${data.aws_ec2_managed_prefix_list.sg_prefix_list.id}"]
  }
}

##
# Launch template
##
resource "aws_launch_template" "app" {
  vpc_security_group_ids = [
    var.app_sg_id,
    var.vpn_sg_id,
    var.ent_tools_sg_id,
    "${aws_security_group.ci.id}",
  ]

  key_name                    = var.key_name
  image_id                    = var.ami_id
  instance_type               = var.instance_type
  name_prefix                 = "bb-${var.stack}-app-"
  user_data                   = filebase64("${path.module}/templates/user_data_64.tpl")
  iam_instance_profile {
    name                      = "bb-${lower(var.env)}-app-profile"
  }

  lifecycle {
    create_before_destroy = true
  }
}


##
# Autoscaling group
##
resource "aws_autoscaling_group" "main" {
  name                      = "asg-${aws_launch_template.app.name}"
  desired_capacity          = var.asg_desired
  max_size                  = var.asg_max
  min_size                  = var.asg_min
  min_elb_capacity          = var.asg_min
  health_check_grace_period = 400
  health_check_type         = "ELB"
  wait_for_capacity_timeout = "30m"
  vpc_zone_identifier       = data.aws_subnets.app.ids

  launch_template {
    id      = aws_launch_template.app.id
    version = aws_launch_template.app.latest_version
  }

  load_balancers            = var.elb_names

  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupPendingInstances",
    "GroupStandbyInstances",
    "GroupTerminatingInstances",
    "GroupTotalInstances",
  ]

  tag {
    key                 = "Name"
    value               = "bb-${var.stack}-app"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.env
    propagate_at_launch = true
  }

  tag {
    key                 = "Function"
    value               = "app-AppServer"
    propagate_at_launch = true
  }

  tag {
    key                 = "Release"
    value               = lookup(data.aws_ami.image.tags, "Release", "none")
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

##
# Autoscaling policies and Cloudwatch alarms
##
resource "aws_autoscaling_policy" "high-cpu" {
  name                   = "${var.app}-${var.env}-high-cpu-scaleup"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 400
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_cloudwatch_metric_alarm" "high-cpu" {
  alarm_name          = "${var.app}-${var.env}-high-cpu"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.main.name
  }

  alarm_description = "CPU usage for ${aws_autoscaling_group.main.name} ASG"
  alarm_actions     = [aws_autoscaling_policy.high-cpu.arn]
}

resource "aws_autoscaling_policy" "low-cpu" {
  name                   = "${var.app}-${var.env}-low-cpu-scaledown"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 400
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_cloudwatch_metric_alarm" "low-cpu" {
  alarm_name          = "${var.app}-${var.env}-low-cpu"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "20"

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.main.name
  }

  alarm_description = "CPU usage for ${aws_autoscaling_group.main.name} ASG"
  alarm_actions     = [aws_autoscaling_policy.low-cpu.arn]
}

##
# Autoscaling notifications
##
resource "aws_autoscaling_notification" "asg_notifications" {
  count = var.sns_topic_arn != "" ? 1 : 0

  group_names = [
    aws_autoscaling_group.main.name,
  ]

  notifications = [
    "autoscaling:EC2_INSTANCE_LAUNCH",
    "autoscaling:EC2_INSTANCE_TERMINATE",
    "autoscaling:EC2_INSTANCE_LAUNCH_ERROR",
  ]

  topic_arn = var.sns_topic_arn
}

output "asg_id" {
  value = aws_autoscaling_group.main.name
}
