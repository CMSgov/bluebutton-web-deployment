# CloudWatch Log Subscription Filter Workspace

For the CWL SUBSCRIP FILTER terraform setup, we use workspaces - one for each environment.
- test
- impl
- prod

To plan or apply changes to an environments' CWL SUBSCRIP FILTER, change to the proper workspace before beginning:
```
//show list of workspaces and the * indicates current one in use
terraform workspace list
//select the workspace to use
terraform workspace select <workspace_name>
//create a new workspace
terraform workspace new <workspace_name>
```

All terraform commands run after selecting a workspace will be applied only to that environment.