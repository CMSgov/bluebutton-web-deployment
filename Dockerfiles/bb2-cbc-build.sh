#!/usr/bin/env bash

PYTHON_VERSION=${1:-3.6}
ANSIBLE_VERSION=${2:-2.7.18}
PACKER_VERSION=${3:-1.6.5}
TERRAFORM_VERSION=${4:-0.11.14}
DOCKER_TAG=${5:-py36-tf11-an27}

docker build -f Dockerfile.bb2-cbc-build -t public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG} .
docker push public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG}