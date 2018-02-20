variable "vpc_name" {
  description = "Name of the VPC these alarms are for."
  type        = "string"
}

variable "load_balancer_name" {
  description = "Name of the ELB these alarms are for."
  type        = "string"
}

variable "cloudwatch_healthy_hosts_min" {
  description = "Minimum number of hosts that must be healthy."
  type        = "string"
  default     = "1"
}

variable "cloudwatch_max_latency_secs" {
  description = "Maximum average latency threshold."
  type        = "string"
  default     = "2"
}

variable "cloudwatch_max_latency_window_secs" {
  description = "Maximum average latency average window size in seconds."
  type        = "string"
  default     = "900"
}

variable "cloudwatch_notification_arn" {
  description = "The CloudWatch notification ARN."
  type        = "string"
}
