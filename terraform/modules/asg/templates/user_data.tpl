#!/bin/bash
sudo su -
set -e

exec > >(tee -a /var/log/user_data.log 2>&1)
# Disable SELinux enforcement at bootup
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

# Configure firewall to allow HTTPS
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
sudo systemctl start splunk
# Optional: check status
systemctl status splunk
# Restart Nginx to apply changes
sudo systemctl restart nginx

# Confirm firewall rules
sudo firewall-cmd --list-all
# Workaround for openssl until the IDM team upgrades TLS
echo "Applying workaround to /etc/pki/tls/openssl.cnf"
sudo sed -i 's/^openssl_conf = openssl_init/openssl_conf = default_conf/' /etc/pki/tls/openssl.cnf

sudo tee -a /etc/pki/tls/openssl.cnf > /dev/null <<EOL
[default_conf]
ssl_conf = ssl_section
[ssl_section]
system_default = system_default_section
[system_default_section]
providers = provider_sect
ssl_conf = ssl_module
MaxProtocol = TLSv1.2
CipherString = ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:...
Ciphersuites =
EOL
echo "Firewall rules updated successfully!"
sudo update-crypto-policies --set FIPS:NO-ENFORCE-EMS

export PATH=$PATH:/usr/local/bin

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
  /var/pyapps/hhs_o_server/env_config.yml

