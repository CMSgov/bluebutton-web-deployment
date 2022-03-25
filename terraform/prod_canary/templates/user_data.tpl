#!/bin/bash

set -e

exec 2> >(tee -a /var/log/boot.log >&2)

aws s3 cp s3://${bucket}/${env}/REPO_URI .

aws secretsmanager get-secret-value --secret-id /bb2/test/app/www_key_file --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/key.pem

aws secretsmanager get-secret-value --secret-id /bb2/test/app/www_combined_crt --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/cert.pem

ansible-playbook \
  -i "localhost" \
  -e "env=${env}" \
  -e "repo=$(cat REPO_URI)" \
  /var/pyapps/hhs_o_server/env_config.yml

rm REPO_URI
