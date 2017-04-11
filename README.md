# hhs_ansible
Ansible Configuration and Playbooks for HHS Blue Button on FHIR API.

Ansible is used as a management server to enable automated updates to the 
machines deployed in the CMS Blue Button on FHIR API front-end platform.

## Keeping variables safe
Configuration variables and sensitive values are now stored in this repository
using ansible-vault. hhs_Ansible uses a cascading set of variable files:

- ./vars/envs/common.yaml: For frequently used variables across all environments.
- ./vars/all-var.yml: All variables used across any platform. Environment specific 
variables are embedded inside the variable defined in this file. Environment specific
variables are prefixed with "env_".
- ./vars/env/{environment_name}/env.yml: Non-sensitive environment specific variables are 
stored in this file. Sensitive environment variables are embedded within env_{variable_name} variables
and are prefixed with "vault_".

Variable files can't embed other variable files as includes. Therefore the 
playbook must load the variables files as includes. A typical include section 
in a playbook would be:

Where the playbook is found in: ./playbook/{role}/playbook.yml

      ```
  vars_files:
    - "./../../vars/common.yml"
    - "./../../vault/env/{{ env }}/vault.yml"
    - "./../../vars/env/{{ env }}/env.yml"
    - "./../../vars/all_var.yml"
      
      ```  
{env} is a variable passed at run time to the playbook.

for example:
In all_var.yml:
aws_secret_key: "{{ env_aws_secret_key }}"

In ./vars/env/{{ env }}/env.yml:
env_aws_secret_key: "{{ vault_env_aws_secret_key }}"

In ./vault/env/{{ env }}/vault.yml:
vault_env_aws_secret_key: "what_ever_the_secret_should_be"


## Status
This is an early development version of an Ansible deployment. The initial 
platform deployment is handled by a series of AWS CloudFormation scripts that
are maintained in the https://github.com/transparenthealth/hhs_oauth_Server
repository.

The AWS CloudFormation Scripts are found in:

hhs_oauth_server/examples/devops/cloudformation/in_prod folder.

## Installation

cd /
git clone https://github.com/TransparentHealth/hhs_ansible.git

Create the /hhs_ansible/vars/playbook/vars.yml

Add your hosts to /etc/ansible/hosts

## Host Configuration

Hosts fall into the following groups:
 - loadbalancers
 - appprimeserver
 - appleadservers
 - appfollowerservers
 - dbservers
 - mgmtservers

Appservers are LEADER or FOLLOWer Servers. If multiple environments are 
installed place one of the LEADER servers into the _appprimeserver_ group, the
other LEADERs go in the _appleadservers_ group. All FOLLOWers go in the
_appfollowerservers_ group.

## var.yml 

The var.yml file stores settings and is not included in this repository.
This file is used to store sensitive configuration information.


    # # Remote user access account
    # ## AWS RHEL: ec2-user
    # ## Ubuntu: ubuntu
    remote_user_account: ec2-user                           
    
    # Project directory for virtualenv and git clone
    project_dir: hhs_o_server 
    
    # a unix path-friendly name (IE, no spaces or special characters)
    project_name: hhs_oauth_server

    # Virtual Environment location
    venv: "/var/virtualenv/{{ project_dir }}"

    # git branch to deploy
    git_branch: develop
    
    # the base path to install to. You should not need to change this.
    # git installs the repo in a folder beneath this path
    # files and folders excluded from the repository can be installed here
    # in files and folders alongside the repo.
    install_root: "/parent/folder/{{ project_dir }}"
    
    # the git repository URL for the project
    # project_repo: git@github.com:transparenthealth/hhs_oauth_server.git
    project_repo: https://github.com/transparenthealth/hhs_oauth_server.git
    
    # The value of your django project's STATIC_ROOT settings.
    # This will be the directory that django's `collectstatic` management command
    # copies static files to, and it must be an absolute path. The default value 
    # here assumes that STATIC_ROOT is set in your settings.py like so:
    # STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
    static_root: "{{ install_root }}/{{ project_name }}/static"    
    
---
