#!/bin/bash

set -e

exec > >(tee -a /var/log/user_data.log 2>&1)

export PATH=$PATH:/usr/local/bin

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_key_file --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/key.pem
aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_combined_crt --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/cert.pem
chmod 0640 /etc/ssl/certs/cert.pem
chmod 0640 /etc/ssl/certs/key.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_cert_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.cert.pem
aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_key_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.key.nocrypt.pem
chown pyapps:www-data /var/pyapps/hhs_o_server/certstore/ca.* && chmod 0640 /var/pyapps/hhs_o_server/certstore/ca.*


# Get master branch versions of CSS files then -> copy to content S3 bucket for the deployed environment
wget https://github.com/CMSgov/bluebutton-css/blob/master/legacy-preserved.css -O /tmp/legacy-preserved.css
wget https://github.com/CMSgov/bluebutton-css/blob/master/dist/sandbox-main.css -O /tmp/sandbox-main.css
wget https://github.com/CMSgov/bluebutton-css/blob/master/dist/static-main.css -O /tmp/static-main.css

aws s3 cp /tmp/legacy-preserved.css s3://${static_content_bucket}/static/legacy-preserved.css
aws s3 cp /tmp/sandbox-main.css s3://${static_content_bucket}/static/dist/sandbox-main.css
aws s3 cp /tmp/static-main.css s3://${static_content_bucket}/static/dist/static-main.css

# cleanup CSS files
rm /tmp/legacy-preserved.css /tmp/legacy-preserved.css /tmp/static-main.css

ansible-playbook \
  -i "localhost" \
  -e "env=${env}" \
  /var/pyapps/hhs_o_server/env_config.yml

