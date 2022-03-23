#!/bin/bash

set -e

exec > >(tee -a /var/log/user_data.log 2>&1)

export PATH=$PATH:/usr/local/bin

ansible-playbook \
  -i "localhost" \
  -e "env=${env}" \
  /var/pyapps/hhs_o_server/env_config.yml

