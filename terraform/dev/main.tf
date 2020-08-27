provider "aws" {
  region = "us-east-1"
}

resource "aws_sns_topic" "cloudwatch_alarms_topic" {
  name = "bluebutton-${var.stack}-cloudwatch-alarms"
}

module "asg" {
  source = "../modules/asg"

  app               = "${var.app}"
  stack             = "${var.stack}"
  env               = "${var.env}"
  vpc_id            = "${var.vpc_id}"
  key_name          = "${var.key_name}"
  ami_id            = "${var.ami_id}"
  instance_type     = "${var.instance_type}"
  elb_names         = ["${var.elb_names}"]
  asg_min           = "${var.asg_min}"
  asg_max           = "${var.asg_max}"
  asg_desired       = "${var.asg_desired}"
  azs               = ["${var.azs}"]
  ci_cidrs          = ["${var.ci_cidrs}"]
  app_sg_id         = "${var.app_sg_id}"
  vpn_sg_id         = "${var.vpn_sg_id}"
  ent_tools_sg_id   = "${var.ent_tools_sg_id}"
  sns_topic_arn     = "${aws_sns_topic.cloudwatch_alarms_topic.arn}"
  app_config_bucket = "${var.app_config_bucket}"
}

module "cloudwatch_alarms_elb_http" {
  source = "../modules/elb_http_alarms"

  app = "${var.app}"
  env = "${var.env}"
  vpc_name                    = "${var.vpc_id}"
  cloudwatch_notification_arn = "${aws_sns_topic.cloudwatch_alarms_topic.arn}"
  load_balancer_name          = "${var.elb_names[0]}"

  alarm_elb_no_backend_enable       = "${var.alarm_elb_no_backend_enable}"
  alarm_elb_no_backend_eval_periods = "${var.alarm_elb_no_backend_eval_periods}"
  alarm_elb_no_backend_period       = "${var.alarm_elb_no_backend_period}"
  alarm_elb_no_backend_threshold    = "${var.alarm_elb_no_backend_threshold}"

  alarm_elb_high_latency_enable       = "${var.alarm_elb_high_latency_enable}"
  alarm_elb_high_latency_eval_periods = "${var.alarm_elb_high_latency_eval_periods}"
  alarm_elb_high_latency_period       = "${var.alarm_elb_high_latency_period}"
  alarm_elb_high_latency_threshold    = "${var.alarm_elb_high_latency_threshold}"

  alarm_elb_spillover_count_enable       = "${var.alarm_elb_spillover_count_enable}"
  alarm_elb_spillover_count_eval_periods = "${var.alarm_elb_spillover_count_eval_periods}"
  alarm_elb_spillover_count_period       = "${var.alarm_elb_spillover_count_period}"
  alarm_elb_spillover_count_threshold    = "${var.alarm_elb_spillover_count_threshold}"

  alarm_elb_surge_queue_length_enable       = "${var.alarm_elb_surge_queue_length_enable}"
  alarm_elb_surge_queue_length_eval_periods = "${var.alarm_elb_surge_queue_length_eval_periods}"
  alarm_elb_surge_queue_length_period       = "${var.alarm_elb_surge_queue_length_period}"
  alarm_elb_surge_queue_length_threshold    = "${var.alarm_elb_surge_queue_length_threshold}"

  alarm_backend_4xx_enable       = "${var.alarm_backend_4xx_enable}"
  alarm_backend_4xx_eval_periods = "${var.alarm_backend_4xx_eval_periods}"
  alarm_backend_4xx_period       = "${var.alarm_backend_4xx_period}"
  alarm_backend_4xx_threshold    = "${var.alarm_backend_4xx_threshold}"

  alarm_backend_5xx_enable       = "${var.alarm_backend_5xx_enable}"
  alarm_backend_5xx_eval_periods = "${var.alarm_backend_5xx_eval_periods}"
  alarm_backend_5xx_period       = "${var.alarm_backend_5xx_period}"
  alarm_backend_5xx_threshold    = "${var.alarm_backend_5xx_threshold}"

  alarm_elb_5xx_enable       = "${var.alarm_elb_5xx_enable}"
  alarm_elb_5xx_eval_periods = "${var.alarm_elb_5xx_eval_periods}"
  alarm_elb_5xx_period       = "${var.alarm_elb_5xx_period}"
  alarm_elb_5xx_threshold    = "${var.alarm_elb_5xx_threshold}"
}

module "cloudwatch_alarms_ec2" {
  source = "../modules/ec2_alarms"

  app = "${var.app}"
  env = "${var.env}"
  cloudwatch_notification_arn = "${aws_sns_topic.cloudwatch_alarms_topic.arn}"
  asg_name = "${module.asg.asg_id}"

  alarm_status_check_failed_enable       = "${var.alarm_status_check_failed_enable}"
  alarm_status_check_failed_eval_periods = "${var.alarm_status_check_failed_eval_periods}"
  alarm_status_check_failed_period       = "${var.alarm_status_check_failed_period}"
  alarm_status_check_failed_threshold    = "${var.alarm_status_check_failed_threshold}"

  alarm_status_check_failed_instance_enable       = "${var.alarm_status_check_failed_instance_enable}"
  alarm_status_check_failed_instance_eval_periods = "${var.alarm_status_check_failed_instance_eval_periods}"
  alarm_status_check_failed_instance_period       = "${var.alarm_status_check_failed_instance_period}"
  alarm_status_check_failed_instance_threshold    = "${var.alarm_status_check_failed_instance_threshold}"

  alarm_status_check_failed_system_enable       = "${var.alarm_status_check_failed_system_enable}"
  alarm_status_check_failed_system_eval_periods = "${var.alarm_status_check_failed_system_eval_periods}"
  alarm_status_check_failed_system_period       = "${var.alarm_status_check_failed_system_period}"
  alarm_status_check_failed_system_threshold    = "${var.alarm_status_check_failed_system_threshold}"
}

module "cloudwatch_alarms_rds" {
  source = "../modules/rds_alarms"

  app = "${var.app}"
  env = "${var.env}"
  cloudwatch_notification_arn = "${aws_sns_topic.cloudwatch_alarms_topic.arn}"
  rds_name = "${var.rds_name}"

  alarm_rds_high_cpu_enable       = "${var.alarm_rds_high_cpu_enable}"
  alarm_rds_high_cpu_eval_periods = "${var.alarm_rds_high_cpu_eval_periods}"
  alarm_rds_high_cpu_period       = "${var.alarm_rds_high_cpu_period}"
  alarm_rds_high_cpu_threshold    = "${var.alarm_rds_high_cpu_threshold}"

  alarm_rds_free_storage_enable       = "${var.alarm_rds_free_storage_enable}"
  alarm_rds_free_storage_eval_periods = "${var.alarm_rds_free_storage_eval_periods}"
  alarm_rds_free_storage_period       = "${var.alarm_rds_free_storage_period}"
  alarm_rds_free_storage_threshold    = "${var.alarm_rds_free_storage_threshold}"

  alarm_rds_write_latency_enable       = "${var.alarm_rds_write_latency_enable}"
  alarm_rds_write_latency_eval_periods = "${var.alarm_rds_write_latency_eval_periods}"
  alarm_rds_write_latency_period       = "${var.alarm_rds_write_latency_period}"
  alarm_rds_write_latency_threshold    = "${var.alarm_rds_write_latency_threshold}"

  alarm_rds_read_latency_enable       = "${var.alarm_rds_read_latency_enable}"
  alarm_rds_read_latency_eval_periods = "${var.alarm_rds_read_latency_eval_periods}"
  alarm_rds_read_latency_period       = "${var.alarm_rds_read_latency_period}"
  alarm_rds_read_latency_threshold    = "${var.alarm_rds_read_latency_threshold}"

  alarm_rds_swap_usage_enable       = "${var.alarm_rds_swap_usage_enable}"
  alarm_rds_swap_usage_eval_periods = "${var.alarm_rds_swap_usage_eval_periods}"
  alarm_rds_swap_usage_period       = "${var.alarm_rds_swap_usage_period}"
  alarm_rds_swap_usage_threshold    = "${var.alarm_rds_swap_usage_threshold}"

  alarm_rds_disk_queue_depth_enable       = "${var.alarm_rds_disk_queue_depth_enable}"
  alarm_rds_disk_queue_depth_eval_periods = "${var.alarm_rds_disk_queue_depth_eval_periods}"
  alarm_rds_disk_queue_depth_period       = "${var.alarm_rds_disk_queue_depth_period}"
  alarm_rds_disk_queue_depth_threshold    = "${var.alarm_rds_disk_queue_depth_threshold}"

  alarm_rds_free_memory_enable       = "${var.alarm_rds_free_memory_enable}"
  alarm_rds_free_memory_eval_periods = "${var.alarm_rds_free_memory_eval_periods}"
  alarm_rds_free_memory_period       = "${var.alarm_rds_free_memory_period}"
  alarm_rds_free_memory_threshold    = "${var.alarm_rds_free_memory_threshold}"
}

module "cloudwatch_alarms_nat" {
  source = "../modules/nat_alarms"

  app = "${var.app}"
  env = "${var.env}"
  cloudwatch_notification_arn = "${aws_sns_topic.cloudwatch_alarms_topic.arn}"
  nat_gw_name = "${var.nat_gw_name}"

  alarm_nat_error_port_alloc_enable       = "${var.alarm_nat_error_port_alloc_enable}"
  alarm_nat_error_port_alloc_eval_periods = "${var.alarm_nat_error_port_alloc_eval_periods}"
  alarm_nat_error_port_alloc_period       = "${var.alarm_nat_error_port_alloc_period}"
  alarm_nat_error_port_alloc_threshold    = "${var.alarm_nat_error_port_alloc_threshold}"

  alarm_nat_packets_drop_count_enable       = "${var.alarm_nat_packets_drop_count_enable}"
  alarm_nat_packets_drop_count_eval_periods = "${var.alarm_nat_packets_drop_count_eval_periods}"
  alarm_nat_packets_drop_count_period       = "${var.alarm_nat_packets_drop_count_period}"
  alarm_nat_packets_drop_count_threshold    = "${var.alarm_nat_packets_drop_count_threshold}"
}

module "cloudwatch_dashboard" {
  source = "../modules/bb_dashboard"

  app = "${var.app}"
  env = "${var.env}"
  vpc_name = "${var.vpc_id}"
  load_balancer_name = "${var.elb_names[0]}"
  asg_name = "${module.asg.asg_id}"
  rds_name = "${var.rds_name}"
  nat_gw_name = "${var.nat_gw_name}"
  dashboard_enable = "${var.dashboard_enable}"
}
