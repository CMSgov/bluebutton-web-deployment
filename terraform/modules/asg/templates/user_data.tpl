#!/bin/bash

set -e

exec 2> >(tee -a /var/log/boot.log >&2)

aws s3 cp s3://${bucket}/${env}/VAULT_PW .
aws s3 cp s3://${bucket}/${env}/REPO_URI .

ansible-playbook --vault-password-file=./VAULT_PW \
  -i "localhost" \
  -e "env=${env}" \
  -e "repo=$(cat REPO_URI)" \
  /var/pyapps/hhs_o_server/env_vars.yml
