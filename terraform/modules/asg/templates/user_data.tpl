#!/bin/bash

set -e

exec > >(tee -a /var/log/user_data.log 2>&1)

aws s3 cp s3://${bucket}/${env}/VAULT_PW .

ansible-playbook --vault-password-file=./VAULT_PW \
  -i "localhost" \
  -e "env=${env}" \
  /var/pyapps/hhs_o_server/env_config.yml

rm VAULT_PW
