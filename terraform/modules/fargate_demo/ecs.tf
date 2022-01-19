resource "aws_ecr_repository" "fargate_demo" {
  name = "bb2-fargate-demo"
}

resource "aws_ecs_cluster" "fargate_demo" {
  name               = "${var.namespace}-${var.env}-ecs-cluster"
  capacity_providers = ["FARGATE"]

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_security_group" "fargate_demo_ecs" {
  name        = "${var.namespace}-${var.env}-ecs-sg"
  description = "Security group for load balancer traffic to ECS tasks"
  vpc_id      = data.aws_vpc.fargate_demo.id

  ingress {
    from_port       = data.aws_ssm_parameter.fargate_demo_port.value
    to_port         = data.aws_ssm_parameter.fargate_demo_port.value
    protocol        = "tcp"
    security_groups = [aws_security_group.fargate_demo_lb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.namespace}-${var.env}-ecs-sg"
    Environment = "${upper(var.env)}"
  }
}

resource "aws_ecs_service" "fargate_demo" {
  name            = "${var.namespace}-${var.env}-ecs-service"
  cluster         = aws_ecs_cluster.fargate_demo.id
  task_definition = aws_ecs_task_definition.fargate_demo.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.fargate_demo_lb.arn
    container_name   = "${var.namespace}-${var.env}"
    container_port   = data.aws_ssm_parameter.fargate_demo_port.value
  }

  network_configuration {
    subnets         = data.aws_subnet_ids.fargate_demo_ecs.ids
    security_groups = [aws_security_group.fargate_demo_ecs.id]
  }
}

resource "aws_iam_role" "fargate_demo_ecs" {
  name = "${var.namespace}-${var.env}-ecs-role"

  assume_role_policy = jsonencode({
    Version = "2008-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "fargate_demo_ecs_base" {
  role       = aws_iam_role.fargate_demo_ecs.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_policy" "fargate_demo_ecs_ssm" {
  name = "${var.namespace}-${var.env}-ecs-ssm-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameters"
        ]
        Resource = [
          "${data.aws_ssm_parameter.fargate_demo_port.arn}",
          "${data.aws_ssm_parameter.fargate_demo_key.arn}",
          "${data.aws_ssm_parameter.fargate_demo_cert.arn}"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "fargate_demo_ecs_ssm" {
  role       = aws_iam_role.fargate_demo_ecs.name
  policy_arn = aws_iam_policy.fargate_demo_ecs_ssm.arn
}

resource "aws_ecs_task_definition" "fargate_demo" {
  family = "${var.namespace}-${var.env}"
  execution_role_arn = aws_iam_role.fargate_demo_ecs.arn
  cpu = 256
  memory = 512
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"

  #"containerPort": "${data.aws_ssm_parameter.fargate_demo_port.value}"
  container_definitions = jsonencode([
    {
      name      = "${var.namespace}-${var.env}"
      image     = "${aws_ecr_repository.fargate_demo.repository_url}:latest"
      cpu       = 256
      memory    = 512
      essential = true
      secrets = [
        {
          SERVER_PORT = "${data.aws_ssm_parameter.fargate_demo_port.arn}",
          SERVER_KEY = "${data.aws_ssm_parameter.fargate_demo_key.arn}",
          SERVER_CERT = "${data.aws_ssm_parameter.fargate_demo_cert.arn}"
        }
      ],
      portMappings = [
        {
          containerPort = tonumber(data.aws_ssm_parameter.fargate_demo_port.value)
        }
      ],
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-region = "us-east-1",
          awslogs-group = "/ecs/${var.namespace}-${var.env}",
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}