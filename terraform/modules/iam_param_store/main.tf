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
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecretVersionIds"
            ],
            "Resource": "arn:aws:secretsmanager:us-east-1:${data.aws_caller_identity.current.account_id}:secret:/bb2/${var.env}/app/*"
        },
       {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "secretsmanager:ListSecrets",
            "Resource": "*"
       }
    ]
}
EOF
}


resource "aws_iam_role_policy_attachment" "app_param_store" {
  role       = data.aws_iam_role.app.id
  policy_arn = aws_iam_policy.app_secrets_mgr.arn
}