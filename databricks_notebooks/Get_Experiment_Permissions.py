# Databricks notebook source
# MAGIC %md ## Get Experiment Permissions
# MAGIC
# MAGIC Call both REST and SDK clients to get experiment permissions.

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("Experiment name", "")
experiment_name = dbutils.widgets.get("Experiment name")

experiment_name

# COMMAND ----------

assert_widget(experiment_name, "Experiment name")

# COMMAND ----------

# MAGIC %md #### Get permissions with REST client

# COMMAND ----------

    perms = rest_client.get_experiment_permissions(experiment_name)
    dump_as_json(perms)

# COMMAND ----------

# MAGIC %md #### Get permissions with SDK client

# COMMAND ----------

perms = sdk_client.get_experiment_permissions(experiment_name)
perms

# COMMAND ----------

dump_as_json(perms.as_dict())
