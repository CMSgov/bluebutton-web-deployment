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
- improved ability to allocate servers across zones
- improved ability to increment launch version and include in name

FIXES:

- Newer RHEL 7.4 images appear to have enabled FIPS 140-2 encryption. 
This disables MD5 checksums which is used by ALL python packages.
We therefore need to update ALL pip commands to add the following parameter:


    -i https://pypi.org/simple/

The above parameter will have to be added using the following change to 
ansible:


    extra_args: "-i https://pypi.org/simple/"
 
This is best performed using a variable to allow consistent implementation
across all commands. 

eg. pip_extra_args added to all_var.yml


    extra_args: "{{ pip_extra_args }}"    
 
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
    --with-python={{ python_bin_dir }}/python{{ python_ver }} \
    --with-apxs=/usr/bin/apxs 

    make
    make install
    


