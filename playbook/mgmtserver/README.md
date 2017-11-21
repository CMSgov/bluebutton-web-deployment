# Create Ansible Management Server

This is the process to setup an Ansible Management Server in one of the 
Blue Button API Virtual Private Clouds:

    - DEV
    - TEST
    - IMPL
    - PROD

## Launch an Instance

* Access the AWS EC2 Console
* Choose a Red Hat Enterprise Linux v7.x Gold Image
    - My AMIs
    - You can filter by: "Shared with me", "64-bit" and "EAST-RH 7-"
    - Choose the latest v7.x Gold Image
* Choose Instance size: m3.medium ... Next
* Configure Instance:
    - Number of Instances: 1
    - Choose VPC: bluebutton-{env}
    - Choose a Management Subnet: bluebutton-{env}-{az1 | az2 | az3}-management
    - IAM Role: None
    - Shutdown behavior: Stop
    - Enable Termination Protection: True
    - Monitoring: Enable CloudWatch detailed Monitoring
    - Tenancy: Dedicated
    - Network: eth0 - leave at defaults
    - Advanced Details: None
    ... Next
* Storage: 
    - Drive 1
        - Root 
        - /dev/sda1  
        - 50 GiB 
        - General Purpose SSD
        - Delete on Termination: Yes
    - Drive 2
        - EBS
        - /dev/sdb
        - 50 GiB
        - General Purpose SSD
        - Delete on Termination: Yes
        - Encrypt: Yes
     - Drive 3
        - EBS
        - /dev/sdf
        - 50 GiB
        - General Purpose SSD
        - Delete on Termination: Yes
        - Encrypt: Yes
     ... Next
     
* Add Tags:
    - business: OEDA
    - application: bluebutton
    - environment: {env}
    - function: MGMT-ANSIBLE
    ... Next

* Configure Security Groups:
    - Select Existing Security Group
    - Choose Security Group by Name: BB-SG-{env}-MGMT-ALLZONE
    ... Review and Launch
    ... Launch
* Select Key Pair:
    - Choose an Existing Key Pair: bb-fe-mgmt-nonprod
    - Check you have the necessary key and acknowledge
    ... Launch
    ... View Instances

* Set Instance Name:
    - Add name to Instance: bb-{impl}-{az1|az2|az3}-mgmt-{nn}






