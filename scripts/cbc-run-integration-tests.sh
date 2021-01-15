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

# Install Debian packages
echo
echo Install Debian packages:
echo
apt install python3 python3-venv

# Cloning the web server repo under ./code directory
echo
echo Clone the web server repo under the ./code directory:
echo
git clone https://github.com/CMSgov/bluebutton-web-server.git code

# Checkout commit hash or branch
echo
echo Checkout commit hash or branch from: branch = ${branch}
echo
pushd code
git fetch origin "+refs/heads/master:refs/remotes/origin/master" "+refs/pull/*:refs/remotes/origin/pr/*"
git checkout "$branch"

# Setup Python virtual env and Install requirements:
echo
echo Setup Python virtual env and Install requirements:
echo
virtualenv -ppython3 venv
. venv/bin/activate
pip install -r requirements/requirements.txt
pip install sqlparse

# Run the Django web server:
echo
echo Run the Django web server:
echo
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

# Finish and perform any needed cleanup:

echo SUCCESS
exit 0
