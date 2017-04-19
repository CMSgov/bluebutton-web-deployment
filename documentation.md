# hhs_ansible: Install/Update hhs_oauth_server in AWS
## Features
*  Install Database Server 
* Update App Server
* Update App Server configuration scripts

## Cross Environment Features
* Use Ansible-vault for sensitive values ( "vault_env_" variable name prefix
* Use {{ env }} to define environment to act upon
	* submit to playbook using --extra-vars env=dev | test | impl | prod

### Install Database Server
Runs AWS CloudFormation Script from:
	 * templates/dataserver.
supplies variables from:
	* vars/all_var.yml using environment specific settings from...
	* vars/env/{{ env }}/env.yml using sensitive settings from...
	* vault/env/{{ env }}/vault.yml

### Update App Servers
Runs Ansible script to get latest git branch (defined in {{ env }}/env.yml.
Performs: 
	* manage.py migrate
	* manage.py collect static
	* restart apache server

### Update App Servers Configuration Scripts
Runs Ansible script to apply:
	* templates/appserver/*.j2
Restarts Apache Server to load configuration settings.

	