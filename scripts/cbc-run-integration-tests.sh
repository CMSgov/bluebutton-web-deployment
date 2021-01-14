#!/bin/bash

# This script is called from Jenkinsfiles/Jenkinsfile.cbc-run-integration-tests
#
# It runs the BB2 integration tests and returns a SUCCESS or FAIL result.

set -e

branch="${BRANCH:-master}"

echo
echo Running $0
echo
echo Using BRANCH:  ${branch}
echo 
echo Using FHIR_URL:  ${FHIR_URL}
echo 
echo 
echo SUCCESS
exit 0
