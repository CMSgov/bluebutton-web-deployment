#!/usr/bin/env bash

set -euo pipefail

exec 2> >(tee -a /var/log/boot.log >&2)

echo 'Defaults:ec2-user !requiretty' > /etc/sudoers.d/999-provisioning
