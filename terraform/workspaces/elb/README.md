# ELB Workspace

For the ELB terraform setup, we use workspaces - one for each environment.
- test
- impl
- prod

To plan or apply changes to an environments' ELB, change to the proper workspace before beginning:
```
//show list of workspaces and the * indicates current one in use
terraform workspace list

//select the workspace to use
terraform workspace select <workspace_name>

//create a new workspace
terraform workspace new <workspace_name>
```

## Variable map for domains
Each environment has a KV pair in the map 'domain_name_value' in the main.tf locals block. This is due to the fact that the environment name does not match the sub-domain name. If additional environments are added, you will also need to add a KV to the map.

```
domain_name_value = {
  "test"  = "test.bluebutton.cms.gov"
  "impl"   = "sandbox.bluebutton.cms.gov"
  "prod"  = "api.bluebutton.cms.gov"
}
```