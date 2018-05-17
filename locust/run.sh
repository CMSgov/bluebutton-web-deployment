#!/bin/bash

#set -e

###
# Usage:
#
# Export values for the following env variables.
#
# Required:
# BB_CLIENT_ID (application's client id)
# BB_CLIENT_SECRET (application's client secret)
# BB_SUB_DOMAIN (sub domain to test against, e.g., sandbox.bluebutton.cms.gov)
#
# Optional:
# BB_NUM_BENES (number of synthetic benes, default: 5)
# BB_LOAD_TEST_DURATION (number of seconds, default: 20)
# BB_LOAD_TEST_HATCH_RATE (hatch rate for clients added per second, default: 1)
# BB_LOAD_TEST_CONCURRENCY (how many clients make requests at once, default: 1)
###

docker build -f ./Dockerfiles/Dockerfile.tkns -t bb_tkns .
docker build -f ./Dockerfiles/Dockerfile.locust -t bb_locust .

echo "Get access tokens..."
docker run --rm -it bb_tkns \
  -id $BB_CLIENT_ID \
  -secret $BB_CLIENT_SECRET \
  -url https://${BB_SUB_DOMAIN} \
  -redirect-url http://localhost:8080/ \
  -n ${BB_NUM_BENES:-5} > tkns.txt

echo "Run locust tests..."
docker run \
  -v "$(pwd):/code" \
  -e BB_TKNS_FILE=/code/tkns.txt \
  -e BB_LOAD_TEST_BASE_URL=https://${BB_SUB_DOMAIN} \
  --rm -it bb_locust \
  --host https://${BB_SUB_DOMAIN} \
  --no-web \
  -c ${BB_LOAD_TEST_CONCURRENCY:-1} \
  -r ${BB_LOAD_TEST_HATCH_RATE:-1} \
  -t ${BB_LOAD_TEST_DURATION:-20}
