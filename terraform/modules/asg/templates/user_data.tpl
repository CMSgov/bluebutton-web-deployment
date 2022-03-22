#!/bin/bash

set -e

export PATH=$PATH:/usr/local/bin

exec > >(tee -a /var/log/user_data.log 2>&1)

ansible-playbook \
  -i "localhost" \
  -e "env=${env}" \
  /var/pyapps/hhs_o_server/env_config.yml

