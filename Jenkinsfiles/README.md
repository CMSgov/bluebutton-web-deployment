## Deployment procedures

### Creating a new AMI

See: [build ami](https://cloudbeesjenkins.cms.gov/dev-master/job/Blue%20Button/job/build%20ami/build?delay=0sec) Jenkins job

Parameters:

- BRANCH: Can be a git branch, git commit or git tag (e.g., develop) of the bluebutton-web-server repo
- BUILD_BRANCH: Can be a git branch, git commit or git tag (e.g., master) of the bluebutton-deployment-repo used to orchestrate the AMI build
- AMI_ID: The ID of the Gold Image AMI to be used as the foundation for the Blue Button AMI. View a list of Gold Image AMIs in the [AWS Console](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Images:visibility=private-images;search=Gold%20Image;name=EAST-RH%207-4%20*;sort=desc:creationDate).
- SUBNET_ID: The subnet where the AMI build EC2 instance should be launched. In lieu of a shared VPC for running build and deploy tasks, the recommended approach would be to use a management subnet for a given environment.
- INSTANCE_CLASS: The instance class/type (e.g., m3.medium, m4.large, etc.) to use for the build.
- ENV: Which environment are building for? Determines the variables and secrets used to configure the Django application.

Steps:

1. Fill in the job parameters with appropriate values.
2. Click "build" and wait for the job to finish.
3. View the end of console output for the job to see the ID of newly created AMI.

Notes:

- The job will notify the "Blue Button API Alerts" HipChat room on job start and end (with an indication of success or failure)
- **IMPORTANT**: In Jenkins, there are also `build ami (${env})` jobs defined as a matter of convenience. The majority of the parameters named above are pre-defined, leaving the option to pass a value for `BRANCH` before running the job.

### Deploying a new AMI

See: [deploy ami](https://cloudbeesjenkins.cms.gov/dev-master/job/Blue%20Button/job/deploy%20ami/build?delay=0sec) Jenkins job

Parameters:

- DEPLOY_BRANCH: Can be a git branch, git commit or git tag (e.g., master) of the bluebutton-deployment-repo used to orchestrate the deployment
- AMI_ID: This is the ID of the Blue Button AMI created as an artifact of the "build ami" job described above. View the end of the output for "build ami" to see the ID of the AMI created by that job.
- INSTANCE_CLASS: The instance class/type (e.g., m3.medium, m4.large, etc.) to use for the deployment. This has a direct effect on the site's ability to handle traffic. Larger instances can endure higher throughput.
- ENV: Which environment are we deploying to?
- MIGRATE: Run Django migrations after bringing up new servers?
- COLLECT_STATIC: Run Django collectstatic after bringing up new servers?

Steps:

1. Fill in the job parameters with appropriate values.
2. Click "build" and wait for the job to finish.

Notes:

- The job will notify the "Blue Button API Alerts" HipChat room on job start and end (with an indication of success or failure)
- **IMPORTANT**: In Jenkins, there are also `deploy ami (${env})`jobs defined for convenience. These jobs have the majority of parameters pre-defined, leaving the option to set values for `AMI_ID`, `MIGRATE` and `COLLECT_STATIC` before running the job.

### Refresh code on running servers

See: [deploy to app servers](https://cloudbeesjenkins.cms.gov/dev-master/job/Blue%20Button/job/deploy%20to%20app%20servers/build?delay=0sec) Jenkins job

There are many parameters available for this job, but refreshing code on running servers only requires a subset. Here are the relevant parameters and details for each:

- BRANCH: Can be a git branch, git commit or git tag (e.g., develop) of the bluebutton-web-server repo
- MIGRATE: Default of "no" can be changed to have migrations applied after code has been deployed to running app servers.
- COLLECT_STATIC: Default of "yes" can be changed to prevent the job from running Django's `collectstatic` command in cases where it is not necessary.
- REFRESH_ONLY: Leave this checked. Indicates that Jenkins should only refresh code on existing servers, not create new ones.

WARNING: the only acceptable method of deploying to upper environments (e.g., `IMPL` and `PROD`) is to use the "build ami" and "deploy ami" jobs. Since the `IMPL` and `PROD` environments use autoscaling to accommodate varying levels of traffic automatically, it is possible that any running server may be terminated and replaced without notice.

It is also possible that, if code _is_ refreshed on `IMPL` or `PROD` instances, if the autoscaling group adds a new instance to meet higher demand, the newest instance will be running a stale version of the application.

TL;DR: do not deploy to `IMPL` or `PROD` using this strategy.


### Run a nested playbook on an ephemeral EC2 instance

See: [run_playbook](https://cloudbeesjenkins.cms.gov/dev-master/job/Blue%20Button/job/run%20playbook/build?delay=0sec) Jenkins job

Parameters:

- PLAYBOOK: The name of the nested playbook to run with in the EC2 ephemeral instance.
- EC2_KEYPAIR_NAME: The AWS EC2 keypair name to use for the EC2 instance.
- INSTANCE_SSH_KEY_ID: The CBJ credentials ID with the SSH key .pem file to use for the EC2 instance.
- AMI_ID: The EC2 Image AMI id that will be used for the EC2 ephemeral instance.
- SUBNET_ID: The subnet ID where the EC2 instance will be launched.
- INSTANCE_CLASS: The class/size of the ec2 instance to launch.
- ENV: The environment to deploy to. 

Usage:

The run_playbook Jenkins CB project and run_playbook Ansible playbook work together to provide a method for running a nested playbook with in an ephemeral EC2 instance.

1. Although job parameters can be filled in with appropriate values and built, this is meant to be used as a downstream (sub-) project.
2. An upstream project references this sub-project under the built-triggers (projects to build) section as "Blue Button/run playbook"
3. An upstream project also defines the job parameters in the build predefined parameters section specific to the job run needs.
4. The parameters specific to the nested playbook are configured in this upstream project's "This project is parameterized" section. This is for setting the project's build parameters. 
5. These playbook parameters are prefixed by "PB_" so that they can be passed through to the nested playbook via ansible, without a need to custom configure the run_playbook sub-project. 
6. When adding new playbooks to be run under an ephemeral EC2 instance, you will only need to custom configure a new upstream project, with no need to confgure the run_playbook sub-project.  

For an example, see the loadtest upstream project: [run_playbook (loadtest)](https://cloudbeesjenkins.cms.gov/dev-master/job/Blue%20Button/job/run%20playbook%20(loadtest)/build?delay=0sec) Jenkins job

This is currently restricted to running in the DEV and TEST enviornments only.

TL;DR: do not deploy to `IMPL` or `PROD` using this strategy.
