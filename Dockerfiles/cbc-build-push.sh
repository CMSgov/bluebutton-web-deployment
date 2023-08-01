#!/usr/bin/env bash

# TO-DO: pin versions on boto3 and botocore if requested.
# Versions at time of BB2-1124 dev: boto3==1.21.28 botocore==1.24.28

DOCKER_TAG=${1:-py38-ans29-tf12-boto3-botocore}

docker build --file Dockerfile.cbc-build \
  --build-arg PYTHON_VERSION=${2:-3.8} \
  --build-arg ANSIBLE_VERSION=${3:-2.9} \
  --build-arg PACKER_VERSION=${4:-1.6.5} \
  --build-arg TERRAFORM_VERSION=${5:-0.12.31} \
  --tag public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG} \
  .

docker push public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG}

