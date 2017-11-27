# Appserver build process

## Preparatory steps

1. login to MGMT Server
2. su to root
3. source go_ansible
4. git pull origin master

## Build a base virtual machine

ansible-playbook playbook/appherd/1_create_appserver.yml \
    --vault-password-file { vault password file } \
    --private-key { pem file } \
    --extra-vars 'env={ dev | test | impl | prod } \
                  azone={ az1| az2 | az3 } \
                  cf_app_instance_type={ m3.medium .. or larger. } \
                  ami_app_gold_image={ ami-5a6ac120 .. or newer gold image. } \
                  build_target=appservers \
                  cf_platform_version={ nn }'
                  
                  