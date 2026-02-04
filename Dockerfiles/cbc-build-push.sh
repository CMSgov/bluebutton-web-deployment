#!/usr/bin/env bash

# TO-DO: pin versions on boto3 and botocore if requested.
# Versions at time of BB2-1124 dev: boto3==1.21.28 botocore==1.24.28

DOCKER_TAG=${1:-py312-ans11-awscol620-ot10-tgrunt85-boto3-botocore-V4}

docker build \
  --platform "linux/amd64" \
  --file Dockerfile.cbc-build \
  --build-arg PYTHON_VERSION=${2:-3.12.8} \
  --build-arg ANSIBLE_VERSION=${3:-11.0.0} \
  --build-arg PACKER_VERSION=${4:-1.11.2} \
  --build-arg TERRAFORM_VERSION=${5:-1.13.3} \
  --build-arg TOFU_VERSION=${6:-1.10.6} \
  --build-arg AWS_COLLECTION_VERSION=${7:-9.1.0} \
  --build-arg TERRAGRUNT_VERSION=${8:-0.89.1} \
  --tag public.ecr.aws/q8j7a4l4/bb2-cbc-build:${DOCKER_TAG} \
  .

docker push public.ecr.aws/q8j7a4l4/bb2-cbc-build:${DOCKER_TAG}

