# Postgres on RDS

In order to improve the resilience of the Front-end application the CMS 
Blue Button API Front-end OAuth platform is migrating from Postgres on EC2
to using Postgres on AWS RDS.

The version of Postgres is unchanged: Postgresql 9.6

The advantages of switching to Postgres running on AWS RDS are:

    - Easy configuration for High Availability across multiple availability zones.
    - Encryption is easily configured
    - Servers can be resized through a console change
    
    
## Configuring Blue Button API Front-end Database Service

The Blue Button API uses the Python/Django framework. The framework uses a 
database to store accont and other configuration information. The AWS 
implementation of Blue Button API is using Postgres for the database platform.

This document will detail the setup for Postgres on AWS RDS. The configuration 
will be applied manually into each environment (DEV, TEST, IMPL, PROD).

### 1. Prepare subnet groups

The first step before creating a database instance is to create DB Subnet 
groups.

The following subnet groups have been created:

    - bb-subnet-group-dev-db-rds
    - bb-subnet-group-test-db-rds
    - bb-subnet-group-impl-db-rds
    - bb-subnet-group-prod-db-rds
    
Each subnet group is configured to include the DATA subnets from each of the
three availability zones in the respective DEV, TEST, IMPL and PROD Virtual 
Private Clouds.

### 2. Launching a DB Instance

(Using the new console design in AWS)

- Goto the AWS Console and choose the RDS Service.
- Click "Launch a DB instance"
- Select PostgreSQL ... Next
- Choose the Production Use Case ... Next
- Specify DB Details:
    - postgreql-license
    - Engine Version: PostgreSQL 9.6.3-R1
    - DB Instance Class. Choose a size of server (see below)
    - Multi-AZ deployment - YES - create a replica in a different zone
    - Storage Type - Provisioned IOPS 100GB / Provisioned IOPS 1000
    (choose size and performance appropriate for role)
    
    
#### TEST Instance: 
Details: db.m3.medium
Type: Standard - Current Generation
vCPU: 1 vCPU
Memory:	3.75 GiB
EBS Optimized: No
Network Performance: Moderate
Free Tier Eligible:	No

#### IMPL Instance: 
Details: db.m3.large
Type: Standard - Current Generation
vCPU: 2 vCPU
Memory:	7.5 GiB
EBS Optimized: No
Network Performance: Moderate
Free Tier Eligible:	No


- DB Instance Identifier - If migrating from an existing instance you may want 
to use an existing instance name.

    - DB Instance Identifier Name format needs to be unique in the account
    - hyphens are allowed
    - Underscores are not allowed
    - This is different from the database name
    
#### instance naming format

    bb-fe-{env}-pg-{nn}
    

- Master Username
- Master Password

- Virtual Private Cloud: bluebutton-{env}
- subnet should automatically pick the correct subnet group: bb-subnet-group-{env}-db-rds
- Public Accessibility: No
- Availability Zone: No preference
- VPC Security Groups - Select Existing Security Groups: BB-SG-{env}-DATA-ALLZONE (VPC) 

- Database Options - Database Name: bb_fe_{env}_pg_{nn}
- Database Port: 15432
- DB Parameter Group Info: Default
- Option Group Info: Default
- Encryption: ENABLE
- Master Key: BB-{ENV}-platform
- Backup: 7 Days
- Enable Enhanced Monitoring: Yes
- Monitoring Role: Default
- Granularity: 60 seconds - default
- Maintenance: Enable auto minor version upgrade
- Maintenance Window: Select Window
- Choose Day: {Saturday | Sunday}
- Start Time: {02:00 UTC}
- Duration: 0.5 Hrs


LAUNCH INSTANCE!

