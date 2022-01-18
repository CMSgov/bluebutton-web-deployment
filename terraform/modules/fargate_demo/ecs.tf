resource "aws_ecr_repository" "fargate_demo" {
  name = "bb2-fargate-demo"
}

resource "aws_ecs_cluster" "fargate_demo" {
  name = "${var.namespace}-${var.env}-ecs-cluster"
}

resource "aws_ecs_service" "fargate_demo" {
  name            = "${var.namespace}-${var.env}-ecs-service"
  # task_definition = aws_ecs_task_definition.fargate_demo.arn
  cluster         = aws_ecs_cluster.fargate_demo.id
  launch_type     = "FARGATE"
 }

resource "aws_ecs_task_definition" "fargate_demo" {
  family = "${var.namespace}-${var.env}"
   # These are the minimum values for Fargate containers.
  cpu = 256
  memory = 512
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"

  container_definitions = <<EOF
  [
    {
      "name": "${var.namespace}-${var.env}",
      "image": "${aws_ecr_repository.fargate_demo.repository_url}:latest",
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-region": "us-east-1",
          "awslogs-group": "/ecs/${var.namespace}-${var.env}",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
  EOF
}