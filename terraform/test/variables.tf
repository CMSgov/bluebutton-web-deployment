variable "app" {}

variable "stack" {}

variable "env" {}

variable "vpc_id" {}

variable "key_name" {}

variable "ami_id" {}

variable "instance_type" {}

variable "elb_names" {
  type = "list"
}

variable "app_sg_id" {}

variable "vpn_sg_id" {}

variable "ent_tools_sg_id" {}

variable "asg_min" {}

variable "asg_max" {}

variable "asg_desired" {}

variable "azs" {
  type = "list"
}

variable "ci_cidrs" {
  type = "list"
}

variable "asg_name" {
  default = ""
}

variable "app_config_bucket" {}

# variable "rds_name" {}
# variable "nat_gw_name" {}

variable "dashboard_enable" {}

variable "alarm_elb_no_backend_enable" {}
variable "alarm_elb_no_backend_eval_periods" {}
variable "alarm_elb_no_backend_period" {}
variable "alarm_elb_no_backend_threshold" {}

# variable "alarm_elb_high_latency_enable" {}
# variable "alarm_elb_high_latency_eval_periods" {}
# variable "alarm_elb_high_latency_period" {}
# variable "alarm_elb_high_latency_threshold" {}

# variable "alarm_elb_spillover_count_enable" {}
# variable "alarm_elb_spillover_count_eval_periods" {}
# variable "alarm_elb_spillover_count_period" {}
# variable "alarm_elb_spillover_count_threshold" {}

# variable "alarm_elb_surge_queue_length_enable" {}
# variable "alarm_elb_surge_queue_length_eval_periods" {}
# variable "alarm_elb_surge_queue_length_period" {}
# variable "alarm_elb_surge_queue_length_threshold" {}

# variable "alarm_backend_4xx_enable" {}
# variable "alarm_backend_4xx_eval_periods" {}
# variable "alarm_backend_4xx_period" {}
# variable "alarm_backend_4xx_threshold" {}

# variable "alarm_backend_5xx_enable" {}
# variable "alarm_backend_5xx_eval_periods" {}
# variable "alarm_backend_5xx_period" {}
# variable "alarm_backend_5xx_threshold" {}

# variable "alarm_elb_5xx_enable" {}
# variable "alarm_elb_5xx_eval_periods" {}
# variable "alarm_elb_5xx_period" {}
# variable "alarm_elb_5xx_threshold" {}

# variable "alarm_status_check_failed_enable" {}
# variable "alarm_status_check_failed_eval_periods" {}
# variable "alarm_status_check_failed_period" {}
# variable "alarm_status_check_failed_threshold" {}

# variable "alarm_status_check_failed_instance_enable" {}
# variable "alarm_status_check_failed_instance_eval_periods" {}
# variable "alarm_status_check_failed_instance_period" {}
# variable "alarm_status_check_failed_instance_threshold" {}

# variable "alarm_status_check_failed_system_enable" {}
# variable "alarm_status_check_failed_system_eval_periods" {}
# variable "alarm_status_check_failed_system_period" {}
# variable "alarm_status_check_failed_system_threshold" {}

# variable "alarm_rds_high_cpu_enable" {}
# variable "alarm_rds_high_cpu_eval_periods" {}
# variable "alarm_rds_high_cpu_period" {}
# variable "alarm_rds_high_cpu_threshold" {}

# variable "alarm_rds_free_storage_enable" {}
# variable "alarm_rds_free_storage_eval_periods" {}
# variable "alarm_rds_free_storage_period" {}
# variable "alarm_rds_free_storage_threshold" {}

# variable "alarm_rds_write_latency_enable" {}
# variable "alarm_rds_write_latency_eval_periods" {}
# variable "alarm_rds_write_latency_period" {}
# variable "alarm_rds_write_latency_threshold" {}

# variable "alarm_rds_read_latency_enable" {}
# variable "alarm_rds_read_latency_eval_periods" {}
# variable "alarm_rds_read_latency_period" {}
# variable "alarm_rds_read_latency_threshold" {}

# variable "alarm_rds_swap_usage_enable" {}
# variable "alarm_rds_swap_usage_eval_periods" {}
# variable "alarm_rds_swap_usage_period" {}
# variable "alarm_rds_swap_usage_threshold" {}

# variable "alarm_rds_disk_queue_depth_enable" {}
# variable "alarm_rds_disk_queue_depth_eval_periods" {}
# variable "alarm_rds_disk_queue_depth_period" {}
# variable "alarm_rds_disk_queue_depth_threshold" {}

# variable "alarm_rds_free_memory_enable" {}
# variable "alarm_rds_free_memory_eval_periods" {}
# variable "alarm_rds_free_memory_period" {}
# variable "alarm_rds_free_memory_threshold" {}

# variable "alarm_nat_error_port_alloc_enable" {}
# variable "alarm_nat_error_port_alloc_eval_periods" {}
# variable "alarm_nat_error_port_alloc_period" {}
# variable "alarm_nat_error_port_alloc_threshold" {}

# variable "alarm_nat_packets_drop_count_enable" {}
# variable "alarm_nat_packets_drop_count_eval_periods" {}
# variable "alarm_nat_packets_drop_count_period" {}
# variable "alarm_nat_packets_drop_count_threshold" {}
