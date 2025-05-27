resource "aws_kms_key" "key" {
  for_each                = toset(var.kms_key_names)
  description             = "bb-${var.stack}-${each.key}-key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
  tags                    = {
    "Name" = "bb-${var.stack}-${each.key}-key"
  }
}

resource "aws_kms_alias" "alias" {
  for_each      = toset(var.kms_key_names)
  name          = "alias/bb-${var.stack}-${each.key}-key-alias"
  target_key_id = aws_kms_key.key[each.key].key_id
}