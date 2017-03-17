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
