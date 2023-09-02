# Databricks notebook source
# MAGIC %md ## Unity Catalog Registered Model Permissions
# MAGIC
# MAGIC Get and update Unity Catalog registered model permissions with both REST and SDK clients.

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Registered model", "")
model_name = dbutils.widgets.get("1. Registered model")

dbutils.widgets.text("2. Principal", user)
principal = dbutils.widgets.get("2. Principal")

model_name, principal

# COMMAND ----------

assert_widget(model_name, "Registered model")

# COMMAND ----------

# MAGIC %md ### Get permissions 

# COMMAND ----------

# MAGIC %md #### Get permissions with REST client

# COMMAND ----------

perms = rest_uc_client.get_registered_model_effective_permissions(model_name)
dump_as_json(perms)

# COMMAND ----------

perms = rest_uc_client.get_registered_model_permissions(model_name)
dump_as_json(perms)

# COMMAND ----------

# MAGIC %md #### Get permissions with SDK client

# COMMAND ----------

perms = sdk_uc_client.get_registered_model_effective_permissions(model_name)
perms

# COMMAND ----------

dump_as_json(perms.as_dict())

# COMMAND ----------

perms = sdk_uc_client.get_registered_model_permissions(model_name)
perms

# COMMAND ----------

#dump_as_json(perms.as_dict()) # AttributeError: 'str' object has no attribute 'value'

# COMMAND ----------

# MAGIC %md ### Update permissions 

# COMMAND ----------

# MAGIC %md #### Update permissions with REST client

# COMMAND ----------

changes = {
  "changes": [
    {   
      "principal": principal,
      "add": [ "APPLY_TAG" ]
    }   
  ]   
} 

# COMMAND ----------

rsp = rest_uc_client.update_registered_model_permissions(model_name, changes)
dump_as_json(rsp)

# COMMAND ----------

# MAGIC %md #### Update permissions with SDK client

# COMMAND ----------

from databricks.sdk.service import catalog

changes = [
    catalog.PermissionsChange(add=[catalog.Privilege.APPLY_TAG], principal=principal)
]
rsp = sdk_uc_client.update_registered_model_permissions(model_name, changes)
rsp 

# COMMAND ----------

# NOTE: AttributeError: 'str' object has no attribute 'value'
# rsp.as_dict() 
