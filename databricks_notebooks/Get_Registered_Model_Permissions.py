# Databricks notebook source
# MAGIC %md ## Get Registered Model Permissions
# MAGIC
# MAGIC Call both REST and SDK clients to get registered model permissions.

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("Registered model", "")
model_name = dbutils.widgets.get("Registered model")
model_name

# COMMAND ----------

assert_widget(model_name, "Registered model")

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
