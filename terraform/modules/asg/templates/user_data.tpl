#!/bin/bash

set -e

exec > >(tee -a /var/log/user_data.log 2>&1)

export PATH=$PATH:/usr/local/bin

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_key_file --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/key.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_combined_crt --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/cert.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_cert_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.cert.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_key_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.key.nocrypt.pem

ansible-playbook \
  -i "localhost" \
  -e "env=${env}" \
  /var/pyapps/hhs_o_server/env_config.yml

