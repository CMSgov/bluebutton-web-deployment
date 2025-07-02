variable "kms_key_names" {
  type        = list(string)
  description = "List of KMS key names"
  default     = ["db", "app", "sns"]
}
variable "stack" {}
variable "env" {}