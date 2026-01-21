#!/usr/bin/env bash

# TO-DO: pin versions on boto3 and botocore if requested.
# Versions at time of BB2-1124 dev: boto3==1.21.28 botocore==1.24.28

# Should we update the docker tag? It was 311; 312 is more accurate.
# However, this should not break anything? Or, perhaps it will push/pull
# against a tag we do not want to overwrite?
DOCKER_TAG=${1:-py312-ans29-awscol620-tf18-tgrunt-boto3-botocore}

docker build --file Dockerfile.cbc-build \
  --build-arg PYTHON_VERSION=${2:-3.12} \
  --build-arg ANSIBLE_VERSION=${3:-2.9.22} \
  --build-arg PACKER_VERSION=${4:-1.6.5} \
  --build-arg TERRAFORM_VERSION=${5:-1.8.2} \
  --build-arg AWS_COLLECTION_VERSION=${6:-6.2.0} \
  --build-arg TERRAGRUNT_VERSION=${7:-0.51.9} \
  --tag public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG} \
  .

docker push public.ecr.aws/f5g8o1y9/bb2-cbc-build:${DOCKER_TAG}

