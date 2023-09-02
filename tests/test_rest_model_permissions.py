from mlflow_databricks_client.rest.client import DatabricksMlflowClient
from mlflow_databricks_client.common.utils import dump_as_json
from . import common_test
from . common_test import func_name, cfg

client = DatabricksMlflowClient()

model_name = cfg["workspace_registry"]["model"]
model_id = client._get_registered_model_id(model_name)
principal = cfg["principal"]

#  "object_id": "/registered-models/94abcb7b9c49465f92a5fb459c26898a",
#  "object_type": "registered-model",


def test_get_registered_model_databricks():
    model = client.get_registered_model_databricks(model_name)
    dump_as_json(model, func_name())


def test_get_registered_model_permissions_by_name():
    perms = client.get_registered_model_permissions(model_id)
    dump_as_json(perms, func_name())
    common_test.do_test_get_registered_model_permissions(perms)

def test_get_registered_model_permissions_by_id():
    perms = client.get_registered_model_permissions(model_id)
    dump_as_json(perms, func_name())
    common_test.do_test_get_registered_model_permissions(perms)
    common_test.check_object_id(model_id, perms)


def test_get_registered_model_permission_levels_by_name():
    perms = client.get_registered_model_permission_levels(model_name)
    dump_as_json(perms, func_name())
    common_test.do_test_get_experiment_permission_levels(perms)

def test_get_registered_model_permission_levels_by_id():
    perms = client.get_registered_model_permission_levels(model_id)
    common_test.do_test_get_experiment_permission_levels(perms)


_access_control_list = [
  {
    "user_name": principal,
    "permission_level": "CAN_MANAGE"
  }
]

def test_set_registered_model_permission():
    perms = client.set_registered_model_permissions(model_id, _access_control_list)
    dump_as_json(perms, func_name())

def test_update_registered_model_permission():
    perms = client.update_registered_model_permissions(model_id, _access_control_list)
    dump_as_json(perms, func_name())
