# hhs_ansible
Ansible Configuration and Playbooks for HHS Blue Button on FHIR API.

Ansible is used as a management server to enable automated updates to the 
machines deployed in the CMS Blue Button on FHIR API front-end platform.

## Keeping variables safe
Configuration variables and sensitive values are not stored in this repository.

These can either be supplied to Ansible at runtime or referenced from 
a vars.yml file that is **outside** this repository.

It is recommended that the vars.yml files are stored in a *vars* folder 
structure that is located in an adjacent folder from the head of this 
repository.

ie. if this repository is in:

~/my_ansible_repo/hhs_ansible

then the vars should be stored in:

~/my_ansible_repo/vars

## Status
This is an early development version of an Ansible deployment. The initial 
platform deployment is handled by a series of AWS CloudFormation scripts that
are maintained in the https://github.com/transparenthealth/hhs_oauth_Server
repository.

The AWS CloudFormation Scripts are found in:

hhs_oauth_server/examples/devops/cloudformation/in_prod folder.

