resource "aws_config_config_rule" "sg_attached" {
  name = "ec2-security-group-attached-to-eni-periodic"

  source {
    owner             = "AWS"
    source_identifier = "EC2_SECURITY_GROUP_ATTACHED_TO_ENI_PERIODIC"
  }
}

resource "aws_iam_role" "aws_config_sg_attached_remediation_role" {
  name = "aws_config_sg_attached_remediation_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ssm.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "aws_config_sg_attached_remediation_policy" {
  name        = "aws_config_sg_attached_remediation_policy"
  path        = "/"
  description = "aws_config_sg_attached_remediation_policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ssm:ExecuteAutomation",
        "ssm:GetAutomationExecution",
        "ec2:DescribeSecurityGroups",
        "ec2:DeleteSecurityGroup"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "aws_config_sg_attached_remediation_attachment" {
  name       = "aws_config_sg_attached_remediation_attachment"
  roles      = [aws_iam_role.aws_config_sg_attached_remediation_role.name]
  policy_arn = aws_iam_policy.aws_config_sg_attached_remediation_policy.arn
}

resource "aws_config_remediation_configuration" "sg_attached" {
  config_rule_name = aws_config_config_rule.sg_attached.name
  resource_type    = "AWS::EC2::SecurityGroup"
  target_type      = "SSM_DOCUMENT"
  target_id        = "AWSConfigRemediation-DeleteUnusedSecurityGroup"
  target_version   = "1"
  parameter {
    name         = "AutomationAssumeRole"
    static_value = aws_iam_role.aws_config_sg_attached_remediation_role.arn
  }

  parameter {
    name           = "GroupId"
    resource_value = "RESOURCE_ID"
  }

}