#!/bin/bash
sudo su -

set -ex
setenforce 0
exec 2> >(tee -a /var/log/boot.log >&2)

aws s3 cp s3://${bucket}/${env}/REPO_URI .

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_key_file --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/key.pem
aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/www_combined_crt --query 'SecretString' --output text |base64 -d > /etc/ssl/certs/cert.pem
chmod 0640 /etc/ssl/certs/cert.pem
chmod 0640 /etc/ssl/certs/key.pem

aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_cert_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.cert.pem
aws secretsmanager get-secret-value --secret-id /bb2/${env}/app/fhir_key_pem --query 'SecretString' --output text |base64 -d > /var/pyapps/hhs_o_server/certstore/ca.key.nocrypt.pem
chown pyapps:www-data /var/pyapps/hhs_o_server/certstore/ca.* && chmod 0640 /var/pyapps/hhs_o_server/certstore/ca.*

# Get master branch versions of CSS files then -> copy to content S3 bucket for the deployed environment
wget https://raw.githubusercontent.com/CMSgov/bluebutton-css/master/legacy-preserved.css -O /tmp/legacy-preserved.css
wget https://raw.githubusercontent.com/CMSgov/bluebutton-css/master/dist/sandbox-main.css -O /tmp/sandbox-main.css
wget https://raw.githubusercontent.com/CMSgov/bluebutton-css/master/dist/static-main.css -O /tmp/static-main.css

aws s3 cp /tmp/legacy-preserved.css s3://${static_content_bucket}/static/legacy-preserved.css
aws s3 cp /tmp/sandbox-main.css s3://${static_content_bucket}/static/dist/sandbox-main.css
aws s3 cp /tmp/static-main.css s3://${static_content_bucket}/static/dist/static-main.css

ansible-playbook \
  -i "localhost" \
  -e "env=${env}" \
  -e "repo=$(cat REPO_URI)" \
  /var/pyapps/hhs_o_server/env_config.yml

rm REPO_URI
