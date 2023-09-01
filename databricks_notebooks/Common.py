# Databricks notebook source
# Common

# COMMAND ----------

import os
import mlflow
from databricks import sdk

print("Versions:")
print("  DBR:           ", os.environ.get("DATABRICKS_RUNTIME_VERSION"))
print("  mlflow.version:", mlflow.__version__)
print("  sdk.version:   ", sdk.version.__version__)

# COMMAND ----------

# MAGIC %pip install git+https:///github.com/amesar/mlflow-databricks-client/#egg=mlflow-databricks-client

# COMMAND ----------

# NOTE: Default SDK with DBR 13.3 LTS is 0.1.6 which does not support automatic authentication in notebooks.

%pip install -U databricks-sdk

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import os
import mlflow
from databricks import sdk

print("After install of latest SDK:")
print("  sdk.version:   ", sdk.version.__version__)

# COMMAND ----------

from mlflow_databricks_client.rest.client import DatabricksMlflowClient
rest_client = DatabricksMlflowClient()
from mlflow_databricks_client import rest
#rest_client = rest.client.DatabricksMlflowClient()
print("rest_client:", rest_client)

# COMMAND ----------

from mlflow_databricks_client import rest
rest_uc_client = rest.client.DatabricksUcMlflowClient()
print("rest_uc_client:", rest_uc_client)

# COMMAND ----------

from mlflow_databricks_client.sdk.client import DatabricksMlflowClient
sdk_client = DatabricksMlflowClient()
print("sdk_client:", sdk_client)

# COMMAND ----------

from mlflow_databricks_client.sdk.client import DatabricksUcMlflowClient
sdk_uc_client = DatabricksUcMlflowClient()
print("sdk_uc_client:", sdk_uc_client)

# COMMAND ----------

from mlflow_databricks_client.common.utils import dump_as_json

# COMMAND ----------

def assert_widget(value, name):
    if len(value.rstrip())==0:
        raise RuntimeError(f"ERROR: '{name}' widget is required")
