# Migrate Data from EC2 Postgres to RDS

This is the process to migrate a Python/Django application from an EC2
Postgres database instance to Postgres running in AWS RDS.

### Assumptions

* RDS Postgres instance has been created with a database name that matches the database being migrated.

## Process for Data Migration

* Connect to the APPServer via SSH
* sudo /bin/bash
* Check version of postgres client utilities
    - psql --version
* upgrade postgres client tools to 9.6 to match server

    
    yum install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-redhat96-9.6-3.noarch.rpm
    yum install postgresql96    
 
* Create a working directory for the migration 


    mkdir /root/migration
    cd /root/migration
    
    
* Create a script to perform dump and restore:


    vi /root/migration/dump_n_restore.sh

* Create the script:

Gather information for the script from:

- hhs_ansible env.yml or vault.yml files
- RDS Console
- AWS Console


    #!/bin/bash
    # init
    function pause(){
       read -p "$*"
    }
    
    PG_VERSION_HOME={location of cli utilities: /usr/pgsql-9.6/bin}/
    SOURCE_DB_NAME={source DB name}
    SOURCE_HOST={Source DB IP Address}
    SOURCE_PORT=15432
    SOURCE_USER={Master Password}
    TARGET_DB_NAME=$SOURCE_DB_NAME
    TARGET_HOST={target db from RDS Console}
    TARGET_PORT=$SOURCE_PORT
    TARGET_USER=$SOURCE_USER
    
    echo taking $SOURCE_DB_NAME dump from $SOURCE_HOST
    $PG_VERSION_HOME./pg_dump -Fc -v --host=$SOURCE_HOST -p $SOURCE_PORT -U $SOURCE_USER $SOURCE_DB_NAME  > $SOURCE_DB_NAME.dump
    echo createdb $TARGET_DB_NAME
    
    pause 'Press [Enter] key to continue...'
    
    echo Restoring to $TARGET_DB_NAME on $TARGET_DB_NAME
    $PG_VERSION_HOME./pg_restore -v -h $TARGET_HOST -p $TARGET_PORT -U $TARGET_USER -d $TARGET_DB_NAME $SOURCE_DB_NAME.dump
    

* make the script executable:


    chmod +x /root/migration/dump_n_restore.sh
    df
    
* Check that there is enough space available to dump the database
* Run the script


    /root/migration/dump_n_restore.sh
    
* update the hhs_ansible var/env.yml and env/vault.yml files with thesettings used to connect to the RDS instance.
* run the ansible refresh_code script to update the appserver with new settings.


    

    
    