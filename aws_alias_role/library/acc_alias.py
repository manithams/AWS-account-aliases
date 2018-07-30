#!/usr/bin/python

# __author__ = "Manitha Silva"

from ansible.module_utils.basic import *
import os
import boto3
from boto3 import client as aws_client

SERVICE = "iam"

def boto_exception(err):
  '''generic error message handler'''
  if hasattr(err, "error_message"):
    error = err.error_message
  elif hasattr(err, "message"):
    error = err.message
  else:
    error = "%s: %s" % (Exception, err)

  return error

def get_account_alias(module, client):
  """
  Get the aws account alias 
  """
  try:
    response = client.list_account_aliases()
    aliases = response["AccountAliases"]

    if aliases:
      alias = aliases[0]
    else:
      alias = ""

  except Exception as err:
      error_message = boto_exception(err)
      module.fail_json(msg=error_message)

  return alias

def set_account_alias(module, client, alias):
  """
  Set the new alias to the account name
  """
  changed = False
  try:
    resp = client.create_account_alias(AccountAlias=alias)
    changed = True
  except Exception as err:
    error_message = boto_exception(err)
    module.fail_json(msg=str(err))

  return changed

def delete_account_alias(module, client, alias):
  """
  Remove the alias form the exisiting name
  """
  changed = False
  try:
    resp = client.delete_account_alias(AccountAlias=alias)
    changed = True
  except Exception as err:
    error_message = boto_exception(err)
    module.fail_json(msg=str(err))

  return changed

def get_user_id(module, client):
  """
  Get User id by taking module and client as parameters
  """
  try:
    resp = client.get_user()
    user_id = resp["User"]["UserId"]
  except Exception as err:
    error_message = boto_exception(err)
    module.fail_json(msg=error_message)

  return user_id


def main():
  argument_spec = dict(
    aws_account_alias=dict(default=None, required=False),
    aws_account_state=dict(default=None, required=True, choices=['present', 'absent']),
    aws_access_key=dict(default=None, required=False),
    aws_secret_key=dict(default=None, required=False),
    )  

  module = AnsibleModule(argument_spec=argument_spec)  
  

  aws_account_alias = module.params.get('aws_account_alias')
  aws_account_state = module.params.get('aws_account_state')
  aws_access_key = module.params.get('aws_access_key')
  aws_secret_key = module.params.get('aws_secret_key')

  if not aws_access_key:
    try:
      aws_access_key = os.environ["AWS_ACCESS_KEY_ID"]
    except:
      module.fail_json(msg="Empty value for required argument: aws_access_key")

  if not aws_secret_key:
    try:
      aws_secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    except:
      module.fail_json(msg="Empty value for required argument: aws_secret_key")

  client = aws_client(
    SERVICE,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
    )

  current_account_alias = get_account_alias(module, client)
  changed = False
  user_id = get_user_id(module, client)

  if aws_account_alias:
    if aws_account_alias != current_account_alias and aws_account_state=="present":
      changed = set_account_alias(module, client, aws_account_alias)
      current_account_alias = aws_account_alias

    elif aws_account_alias == current_account_alias and aws_account_state=="absent":
      changed = delete_account_alias(module, client, aws_account_alias)
      current_account_alias = get_account_alias(module, client)
  
  # Set module exit Output
  module.exit_json(
    changed=changed,
    aws_account_id=get_user_id(module, client),
    aws_account_alias=current_account_alias
    )
    

if __name__ == '__main__':
    main()
