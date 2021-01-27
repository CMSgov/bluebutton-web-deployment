#!/bin/bash

# This script is called from Jenkinsfiles/Jenkinsfile.cbc-run-integration-tests
#
# It runs the BB2 integration tests and returns a SUCCESS or FAIL result.

# Echo function that includes script name on each line for console log readability
echo_msg () {
  echo "$(basename $0): $*"
}


# main
set -e

branch="${BRANCH:-master}"

echo_msg
echo_msg "Running script: $0"
echo_msg
echo_msg "Using ENV/environment variables:"
echo_msg
echo_msg "      BRANCH:  ${branch}"
echo_msg 
echo_msg "    FHIR_URL:  ${FHIR_URL}"
echo_msg 
echo_msg "   CERT_FILE: ${CERT_FILE}" 
echo_msg 
echo_msg "    KEY_FILE: ${KEY_FILE}" 
echo_msg

# Cloning the web server repo under ./code directory.
echo_msg
echo_msg "Clone the web server repo under the ./code directory:"
echo_msg
git clone https://github.com/CMSgov/bluebutton-web-server.git code

# Checkout commit hash or branch.
echo_msg
echo_msg "Checkout commit hash or branch from: branch = ${branch}"
echo_msg
cd code
git fetch origin "+refs/heads/master:refs/remotes/origin/master" "+refs/pull/*:refs/remotes/origin/pr/*"
git checkout "$branch"

# Copy cert files to DJANGO_FHIR_CERTSTORE location
export DJANGO_FHIR_CERTSTORE=./certstore/
export FHIR_CERT_FILE="cert.pem"
export FHIR_KEY_FILE="key.pem"
echo_msg
echo_msg "Copy CERT files in to DJANGO_FHIR_CERTSTORE: ${DJANGO_FHIR_CERTSTORE}"
echo_msg
echo_msg "   Copying cert file to FHIR_CERT_FILE: ${FHIR_CERT_FILE}"
echo_msg "   Copying key file to  FHIR_KEY_FILE: ${FHIR_KEY_FILE}"
echo_msg
mkdir ${DJANGO_FHIR_CERTSTORE}
cp "${CERT_FILE}" "${DJANGO_FHIR_CERTSTORE}/${FHIR_CERT_FILE}"
cp "${KEY_FILE}" "${DJANGO_FHIR_CERTSTORE}/${FHIR_KEY_FILE}"
ls -ld "${DJANGO_FHIR_CERTSTORE}/cert.pem"
ls -ld "${DJANGO_FHIR_CERTSTORE}/key.pem"

# Call run tests script from webserver repo.
sh docker-compose/run_integration_tests_inside_cbc_build_docker.sh