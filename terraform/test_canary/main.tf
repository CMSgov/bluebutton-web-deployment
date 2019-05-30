provider "aws" {
  region = "us-east-1"
}

data "template_file" "user_data" {
  template = "${file("${path.module}/templates/user_data.tpl")}"

  vars {
    env    = "${lower(var.env)}"
    bucket = "${var.app_config_bucket}"
  }
}



resource "aws_instance" "test_canary_app" {

  ami           = "${var.ami_id}"
  instance_type = "${var.instance_type}"
  key_name      = "${var.key_name}"

  subnet_id     = "${var.subnet_id}"
  #user_data = "${file("${path.module}/templates/user_data")}"


  user_data                   = "${data.template_file.user_data.rendered}"
  iam_instance_profile        = "${var.iam_instance_profile}"

  #   For canary, just needing one for ssh access: vpn

  vpc_security_group_ids = [
    "${var.vpc_sg_id}"
  ]

  associate_public_ip_address = false

  tags {
    Name = "bb-test-canary"
  }
}

#Assign Private IP to Output variable

  output "private_ip" {
    value = "${aws_instance.test_canary_app.private_ip}"
  }
