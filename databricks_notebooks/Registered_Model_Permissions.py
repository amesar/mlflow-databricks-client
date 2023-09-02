# Databricks notebook source
# MAGIC %md ## Get Registered Model Permissions
# MAGIC
# MAGIC Call both REST and SDK clients to get and update/set registered model permissions.
# MAGIC
# MAGIC Get and update registered model permissions:
# MAGIC * [Get registered model permissions](https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissions)
# MAGIC * [Get registered model permission levels](https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissionlevels)
# MAGIC * [Update registered model permissions](https://docs.databricks.com/api/workspace/modelregistry/updateregisteredmodelpermissions) - PATCH
# MAGIC * [Set registered model permissions](https://docs.databricks.com/api/workspace/modelregistry/setregisteredmodelpermissions)- PUT

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

perms = rest_client.get_registered_model_permissions(model_name)
dump_as_json(perms)

# COMMAND ----------

# MAGIC %md #### Get permissions with SDK client

# COMMAND ----------

perms = sdk_client.get_registered_model_permissions_by_name(model_name)
perms

# COMMAND ----------

dump_as_json(perms.as_dict())

# COMMAND ----------

# MAGIC %md ### Update and set permissions

# COMMAND ----------

acl = [
  {
    "user_name": user,
    "permission_level": "CAN_MANAGE"
  }
]
acl

# COMMAND ----------

# MAGIC %md #### REST client - update and set permissions

# COMMAND ----------

# MAGIC %md ##### Update permissions

# COMMAND ----------

rsp = rest_client.update_registered_model_permissions(model_name, acl)
dump_as_json(rsp)

# COMMAND ----------

# MAGIC %md #### Set permissions

# COMMAND ----------

rsp = rest_client.set_registered_model_permissions(model_name, acl)
dump_as_json(rsp)

# COMMAND ----------

perms = rest_client.get_registered_model_permissions(model_name)
dump_as_json(perms)

# COMMAND ----------

# MAGIC %md #### SDK client - update and set permissions - TODO
# MAGIC
# MAGIC * No examples or doc links to create `RegisteredModelAccessControlRequest`

# COMMAND ----------

# MAGIC %md #### Update permissions
# MAGIC * https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.update_registered_model_permissions
# MAGIC * https://docs.databricks.com/api/workspace/modelregistry/updateregisteredmodelpermissions

# COMMAND ----------

#sdk_client.model_registry.update_registered_model_permissions(model_id, acl)   

# COMMAND ----------

# MAGIC %md #### Set permissions
# MAGIC * https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.set_registered_model_permissions
# MAGIC * https://docs.databricks.com/api/workspace/modelregistry/setregisteredmodelpermissions

# COMMAND ----------

# sdk_client.model_registry.set_registered_model_permissions(model_id, acl)  
