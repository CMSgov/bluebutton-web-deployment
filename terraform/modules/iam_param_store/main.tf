data "aws_caller_identity" "current" {}

data "aws_iam_role" "app" {
  name = "bb-${var.env}-app-role"
}

resource "aws_iam_policy" "app_secrets_mgr" {
  name        = "bb-${var.env}-app-secrets-mgr"
  description = "Read-only permissions to environment scoped secrets manager variables"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:ListSecrets",
                "secretsmanager:DescribeSecret",
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:${data.aws_caller_identity.current.account_id}:secret:/bb2/test/app/*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "app_param_store" {
  role       = data.aws_iam_role.app.id
  policy_arn = aws_iam_policy.app_secrets_mgr.arn
}
