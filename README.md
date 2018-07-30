aws_alias_role
========================

## Introduction
This role was developed to manage AWS account aliases. It can set, update or remove account alias from the given AWS account. This will assign an alias for the aws account name allocated for each team. This alias name reflects the team name. The ansible role is responsible of taking AWS alias names as parameters and take care of compliance. 


The ansible role takes AWS alias name as a parameter and customizes it according to the team name.
## Parameters 

- **Role Name:** aws_alias_role
- **Parameters:**
      Please set the following variables in `manithams-automation-test/aws_alias_role/vars/main.yaml`  before proceeding. 

  * **aws_account_alias:** If set, changes AWS account alias name.
                         If this parameter is not set, role does
                         nothing
  * **aws_account_state:** If set to absent, removes account alias.
                         Accepts 'present', 'absent', defaults to 'present'
  * **aws_access_key   :** AWS account access key ID, defaults to AWS_ACCESS_KEY_ID
                         environment variable
  * **aws_secret_key   :** AWS account access key secret, defaults to AWS_SECRET_ACCESS_KEY
                         environment variable
                     
  ## Usage 
  ```
  ansible-playbook /root/manithams-automation-test/aws_alias_role.yaml
  ```
  
  ## Output 
 
 ```
  {
    "changed" : true,
    "aws_account_id": 123123123,
    "aws_account_alias": "SuperTeamA"
  }
```

* **changed -** boolean, reflects if account alias name changed.
* **aws_account_id -** The AWS account ID.
* **aws_account_alias -** The current account alias, as known to AWS.

Module register the variable to aws_alias_status with the result of the task module:
  ```
      - name: Ensure AWS alias name
        YourSuperModule:
          name="{{ SuperTeamVarName }}"
        register: aws_alias_status
  ```
