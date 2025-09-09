BlueButton Web Deployment

# Project Description
Ansible Configuration and Playbooks for Blue Button API.

# About the Project
The [Blue Button 2.0 API](https://bluebutton.cms.gov/) provides Medicare enrollee claims data to applications using the [OAuth2.0 authorization flow](https://datatracker.ietf.org/doc/html/rfc6749). We aim to provide a developer-friendly, standards-based API that enables people with Medicare to connect their claims data to the applications, services, and research programs they trust.

# Core Team
A list of core team members responsible for the code and documentation in this repository can be found in [COMMUNITY.md](COMMUNITY.md).

# Repository Structure
```
├── Dockerfiles
├── inventory
├── Jenkinsfiles
├── newrelic
├── ops
├── packer
├── playbook
│   ├── build_app_ami_amzn2
│   ├── build_platinum_ami_amzn2
│   ├── run_django_command
├── roles
├── terraform
│   ├── prod
│   ├── test
├── vars
```

# Development and Software Delivery Lifecycle
The following guide is for members of the project team who have access to the repository as well as code contributors. The main difference between internal and external contributions is that external contributors will need to fork the project and will not be able to merge their own pull requests. For more information on contributing, see: [CONTRIBUTING.md](./CONTRIBUTING.md).

# Local Development

## Installation (Redhat / Centos / Fedora)<a id="installation"></a>

To enable ec2 support you must install python-boto:

    sudo yum install -y python-pip
    sudo pip install --upgrade pip
    sudo yum -y install git
    sudo yum -y install ansible
    sudo yum -y install python-boto

NOTE: if FIPS is enabled add an additional parameter to pip command:
-i https://pypi.org/simple/

Install hhs_ansible:

    mkdir /hhs_ansible
    cd /hhs_ansible
    git clone https://github.com/CMSGov/bluebutton-web-deployment.git

Updating the Application Load Balancers requires a newer version of awscli.
Install updated version as follows:

    sudo /bin/bash
    cd /root
    pip install --upgrade --user awscli -i https://pypi.org/simple/

this will install the updated version to

    /root/.local/bin

Then add your hosts to

    /etc/ansible/hosts

Edit the config file:

    /etc/ansible/ansible.cfg

The public keys from ec2-user (id_rsa.pub and id_ecdsa.pub) need to be
generated on the Management Server so that they can be copied to the
remote machines in the base_patch role. As the **ec2-user** on the Management
Server generate two sets of keys with no passphrase:

    ssh-keygen -t rsa
    ssh-keygen -t ecdsa

- Do not enter a passphrase. Hit enter to step pass the prompt
- Do not change the default filenames id_rsa and id_ecdsa.


As a minimum, if you are using AWS you will probably want to change:
    ' #remote_user = root'

to the remote user account used to connect to a server.

## Keeping variables safe
Configuration variables and sensitive values are stored in AWS Parameter Store and AWS Secrets Manager. hhs_Ansible uses a cascading set of variable files:

- ./vars/envs/common.yaml: For frequently used variables across all environments.
- ./vars/all-var.yml: All variables used across any platform. Environment specific
variables are embedded inside the variable defined in this file. Environment specific
variables are prefixed with "env_".
- ./vars/env/{environment_name}/env.yml: A mix of Sensitive and Non-sensitive environment specific variables are
stored in this file. With use of the Ansible "lookup" plugin, values are pulled from aws_secret during CI/CD.

Variable files can't embed other variable files as includes. Therefore the
playbook must load the variables files as includes. A typical include section
in a playbook would be:

Where the playbook is found in: ./playbook/{role}/playbook.yml

    ```
    vars_files:
      - "./../../vars/common.yml"
      - "./../../vars/env/{{ env }}/env.yml"
      - "./../../vars/all_var.yml"

    ```  
{env} is a variable passed at run time to the playbook using
--extra-vars env=dev | test | impl | prod

for example:
In all_var.yml:
db_name: "{{ env_db_name }}"

In ./vars/env/{{ env }}/env.yml:
env_db_name: "{{ lookup('aws_secret', '/bb2/impl/app/db_name', region='us-east-1') }}"


## Host Configuration

Hosts fall into the following groups:
 - mgmtservers (The ansible management server)
 - appservers
 - dbservers

When creating a MGMT server instance in ec2 to run ansible add the following
tags to the instance:

 - Managed = "BB-MANAGED-{{ env|upper }}"
 - Environment = {{ env|upper }} eg. DEV | TEST | IMPL | PROD
 - Layer = "MGMT"

These fields are added to each ec2 instance to be managed. These instances
will automatically be grouped in to the relevant group in /etc/anasible/hosts
based upon their Layer setting (MGMT | APP | DATA)

# Coding Style and Linters

Each application has its own linting and testing guidelines. Lint and code tests are run on each commit, so linters and tests should be run locally before committing.

# Branching Model
This project follows standard GitHub flow practices:

* Make changes in feature branches and merge to `main` frequently
* Pull-requests are reviewed before merging
* Tests should be written for changes introduced
* Each change should be deployable to production

Make changes on a new branch and create pull requests to merge them into the master branch when ready.

When creating a new branch, use the naming convention `[your-github-username]/[jira-ticket-number]-[description]`. For example, `mrengy/BB2-1511-layout-narrow-browser`.

You'll need to [use a Github Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) instead of a password in order to push changes.

# Contributing
Thank you for considering contributing to an Open Source project of the US Government! For more information about our contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

# Community
The Blue Button Web Server team is taking a community-first and open source approach to the product development of this tool. We believe government software should be made in the open and be built and licensed such that anyone can download the code, run it themselves without paying money to third parties or using proprietary software, and use it as they will.

We know that we can learn from a wide variety of communities, including those who will use or will be impacted by the tool, who are experts in technology, or who have experience with similar technologies deployed in other spaces. We are dedicated to creating forums for continuous conversation and feedback to help shape the design and development of the tool.

We also recognize capacity building as a key part of involving a diverse open source community. We are doing our best to use accessible language, provide technical and process documents, and offer support to community members with a wide variety of backgrounds and skillsets.

# Community Guidelines
Principles and guidelines for participating in our open source community are can be found in [COMMUNITY.md](COMMUNITY.md). Please read them before joining or starting a conversation in this repo or one of the channels listed below. All community members and participants are expected to adhere to the community guidelines and code of conduct when participating in community spaces including: code repositories, communication channels and venues, and events.

# Governance
For more information about our governance, see [GOVERNANCE.md](GOVERNANCE.md).

# Feedback
If you have ideas for how we can improve or add to our capacity building efforts and methods for welcoming people into our community, please let us know at **opensource@cms.hhs.gov**. If you would like to comment on the tool itself, please let us know by filing an **issue on our GitHub repository.**

# Policites

### Open Source Policy

We adhere to the [CMS Open Source Policy](https://github.com/CMSGov/cms-open-source-policy). If you have any questions, just [shoot us an email](mailto:opensource@cms.hhs.gov).

### Security and Responsible Disclosure Policy
_Submit a vulnerability:_ Vulnerability reports can be submitted through [Bugcrowd](https://bugcrowd.com/cms-vdp). Reports may be submitted anonymously. If you share contact information, we will acknowledge receipt of your report within 3 business days.

For more information about our Security, Vulnerability, and Responsible Disclosure Policies, see [SECURITY.md](SECURITY.md).

### Software Bill of Materials (SBOM)
A Software Bill of Materials (SBOM) is a formal record containing the details and supply chain relationships of various components used in building software.

In the spirit of [Executive Order 14028 - Improving the Nation's Cyber Security](https://www.gsa.gov/technology/it-contract-vehicles-and-purchasing-programs/information-technology-category/it-security/executive-order-14028), a SBOM for this repository is provided here: https://github.com/CMSGov/bluebutton-web-server/network/dependencies.

For more information and resources about SBOMs, visit: https://www.cisa.gov/sbom.

# Public Domain
This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/) as indicated in [LICENSE](LICENSE).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request or issue, you are agreeing to comply with this waiver of copyright interest.
