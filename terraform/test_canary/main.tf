provider "aws" {
  region = "us-east-1"
}

data "template_file" "user_data" {
  template = file("${path.module}/templates/user_data.tpl")

  vars = {
    env                   = lower(var.env)
    bucket                = var.app_config_bucket
    static_content_bucket = var.static_content_bucket
  }
}

data "aws_ec2_managed_prefix_list" "canary_sg_pl" {
  filter {
    name   = "prefix-list-name"
    values = ["cmscloud-oc-management-subnets"]
  }
}



resource "aws_instance" "test_canary_app" {

  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name

  subnet_id = var.subnet_id
  #user_data = "${file("${path.module}/templates/user_data")}"


  user_data            = data.template_file.user_data.rendered
  iam_instance_profile = var.iam_instance_profile

  vpc_security_group_ids = [
    var.vpc_sg_id,
    aws_security_group.allow_ci_ssh.id
  ]
metadata_options {
    http_tokens = "optional"  # Allow both IMDSv1 and IMDSv2
  }
  associate_public_ip_address = false

  tags = {
    Name = "bb-test-canary"
  }
}

# create the CI security group for canary deploy.
# Once canary instance is manually/automatically 
# terminates the AWS config rule will remove this SG.
resource "aws_security_group" "allow_ci_ssh" {
  name        = "ci-to-canary-test-servers"
  description = "Allow SSH inbound traffic for CI builds"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH from test canary CI"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ci_cidrs
  }

  ingress {
    description     = "HTTPS from CI"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    prefix_list_ids = ["${data.aws_ec2_managed_prefix_list.canary_sg_pl.id}"]
  }

  tags = {
    Name = "allow_ssh"
    env  = "test_canary"
  }
}

#Assign Private IP to Output variable

output "private_ip" {
  value = aws_instance.test_canary_app.private_ip
}
