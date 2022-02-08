data "aws_caller_identity" "current" {}

data "aws_iam_role" "app" {
  name = "bb-${var.env}-app-role"
}

resource "aws_iam_policy" "app_param_store" {
  name        = "bb-${var.env}-app-parameter-store"
  description = "Read-only permissions to environment scoped parameter store variables"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeParameters",
                "ssm:GetParameterHistory",
                "ssm:GetParametersByPath",
                "ssm:GetParameters",
                "ssm:GetParameter"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:${data.aws_caller_identity.current.account_id}:parameter/bb2/${var.env}/app/*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "app_param_store" {
  role       = data.aws_iam_role.app.id
  policy_arn = aws_iam_policy.app_param_store.arn
}
