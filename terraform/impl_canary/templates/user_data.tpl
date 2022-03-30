#!/bin/bash

set -e

exec 2> >(tee -a /var/log/boot.log >&2)

aws s3 cp s3://${bucket}/${env}/REPO_URI .

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_key_file --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/key.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_combined_crt --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/cert.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_cert_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.cert.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_key_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.key.nocrypt.pem

chown pyapps:www-data /var/pyapps/hhs_o_server/certstore/ca.* && chmod 0640 /var/pyapps/hhs_o_server/certstore/ca.*

ansible-playbook \
  -i "localhost" \
  -e "env=${env}" \
  -e "repo=$(cat REPO_URI)" \
  /var/pyapps/hhs_o_server/env_config.yml

rm REPO_URI
