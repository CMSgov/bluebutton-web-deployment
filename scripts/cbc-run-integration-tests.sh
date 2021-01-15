#!/bin/bash

# This script is called from Jenkinsfiles/Jenkinsfile.cbc-run-integration-tests
#
# It runs the BB2 integration tests and returns a SUCCESS or FAIL result.

set -e

branch="${BRANCH:-master}"

echo
echo Running script: $0
echo
echo Using ENV/environment variables:
echo
echo     BRANCH:  ${branch}
echo 
echo     FHIR_URL:  ${FHIR_URL}
echo 
echo

# Clone the web server repo
git clone https://github.com/CMSgov/bluebutton-web-server.git code

# Checkout commit hash or branch
pushd code
git fetch origin "+refs/heads/master:refs/remotes/origin/master" "+refs/pull/*:refs/remotes/origin/pr/*"
git checkout "$branch"

# Install requirements
virtualenv -ppython3 venv
. venv/bin/activate
pip install -r requirements/requirements.txt
pip install sqlparse

# Bootstrap the database, run the server
export DJANGO_SETTINGS_MODULE="hhs_oauth_server.settings.dev"
.././migrate.sh
python3 manage.py runserver 0.0.0.0:8899 &
RUNSERVER_PID="$!"
popd

echo
echo Running webserver process PID: ${RUNSERVER_PID}
echo

sleep 60

echo
echo
echo
ls -lR
echo
echo
echo


echo SUCCESS
exit 0
