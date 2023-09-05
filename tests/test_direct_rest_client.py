from mlflow_databricks_client.rest.http_client import HttpClient
from mlflow_databricks_client.common.utils import dump_as_json
from . common_test import func_name, cfg


# ==== Setup

client = HttpClient("")

def _get_experiment_id(experiment_name):
    resource = "api/2.0/mlflow/experiments/get-by-name"
    rsp = client.get(resource, { "experiment_name": experiment_name })
    return rsp["experiment"]["experiment_id"]

def _model_id(model_name):
    rsp = client.get("api/2.0/mlflow/databricks/registered-models/get", { "name": model_name })
    return rsp["registered_model_databricks"]["id"]

experiment_name = cfg["experiment"]
experiment_id = _get_experiment_id(experiment_name)

model_name = cfg["workspace_registry"]["model"]
model_id = _model_id(model_name)

uc_model_name = cfg["unity_catalog_registry"]["model"]

principal = cfg["principal"]


# ==== Experiment Permisions
    
# == Get experiment permissions

def test_get_experiment_permissions():
    resource = f"api/2.0/permissions/experiments/{experiment_id}"
    perms =  client.get(resource)
    dump_as_json(perms, func_name())

def test_get_experiment_permission_levels():
    resource = f"api/2.0/permissions/experiments/{experiment_id}/permissionLevels"
    perms =  client.get(resource)
    dump_as_json(perms, func_name())

# == Set/update experiment permissions

acl = [
  {
    "user_name": principal,
    "permission_level": "CAN_MANAGE"
  }
]

def test_set_experiment_permissions():
    resource = f"api/2.0/permissions/experiments/{experiment_id}"
    rsp = client.put(resource, { "access_control_list": acl })
    dump_as_json(rsp, func_name())

def test_update_experiment_permissions():
    resource = f"api/2.0/permissions/experiments/{experiment_id}"
    rsp = client.patch(resource, { "access_control_list": acl })
    dump_as_json(rsp, func_name())

# ==== Registered Model Permissions

# == Get registered model permissions

def test_get_registered_model_permissions():
    rsp = client.get(f"api/2.0/permissions/registered-models/{model_id}")
    dump_as_json(rsp, func_name())

def test_get_registered_model_permission_levels():
    rsp = client.get(f"api/2.0/permissions/registered-models/{model_id}/permissionLevels")
    dump_as_json(rsp, func_name())

# == Set/update registered model permissions

acl = [
  {
    "user_name": principal,
    "permission_level": "CAN_MANAGE"
  }
]

def test_set_registered_model_permission():
    rsp = client.put(f"api/2.0/permissions/registered-models/{model_id}")
    dump_as_json(rsp, func_name())

def test_update_registered_model_permission():
    rsp = client.patch(f"api/2.0/permissions/registered-models/{model_id}")
    dump_as_json(rsp, func_name())


# ==== Registered Model Permissions - Unity Catalog

# == Get registered model permissions

def test_uc_get_registered_model_effective_permissions():
    rsp = client.get(f"api/2.1/unity-catalog/effective-permissions/function/{uc_model_name}")
    dump_as_json(rsp, func_name())

def test_uc_set_registered_model_permissions():
    rsp = client.get(f"api/2.1/unity-catalog/permissions/function/{uc_model_name}")
    dump_as_json(rsp, func_name())


# == Update registered model permissions

changes = [
    {
      "principal": principal,
      "add": [ "APPLY_TAG" ]
    }
]

def test_uc_update_registered_model_permission():
    rsp = client.patch(f"api/2.1/unity-catalog/permissions/function/{uc_model_name}", {"changes": changes})
    dump_as_json(rsp, func_name())
