#!/usr/bin/env bash

DOCKER_TAG=${1:-py36-an27-tf11}

docker build --file Dockerfile.cbc-build \
  --build-arg PYTHON_VERSION=${2:-3.6} \
  --build-arg ANSIBLE_VERSION=${3:-2.7.18} \
  --build-arg PACKER_VERSION=${4:-1.6.5} \
  --build-arg TERRAFORM_VERSION=${5:-0.11.15} \
  --tag public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG} \
  .

docker push public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG}
