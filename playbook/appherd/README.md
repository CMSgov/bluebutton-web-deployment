# appherd Playbook

The objective of this playbook is to re-engineer the creation of 
appservers.


Steps:

    1. Create Server 
    2. Update packages
    3. Install and configure Apache, Python, Mod_Wsgi
    4. Install supporting software code (eg. Swagger UI)
    5. Implement VirtualEnv and deploy AppServer Code, create log filesm,
       Set Variables, Update Apache to launch app, Install SSL Certificates
    6. Test server is operational 
    7. Add Server to fleet
    
    8. Remove Server from fleet to update/destroy

Features to include:

- Enable easy upgrade to new RHEL Gold Image
- Set size of boot drive
- Attach a variable sized /var volume
- Attach a variable sized /tmp volume

- Isolate code dependencies

- Take Snapshot of operational server
- Clone from Snapshot and add to fleet

 
Approach:

the Appserver playbook has many of the necessary elements. They will be copied 
in to this playbook as the modules are defined.


Fixes to apply:

When changing versions of Python if installed from source go to source 
directory. run: 

    make clean
    make uninstall
    make -n install
    
Then go to mod_wsgi source:

    make clean
    .configure \
    --with-python=/usr/local/bin/python{{ python_ver }} \
    --with-apxs=/usr/bin/apxs 

    make
    make install
    



