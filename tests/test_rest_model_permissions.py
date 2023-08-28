from mlflow_databricks_client.rest.client import DatabricksMlflowClient
from mlflow_databricks_client.common.utils import dump_as_json
from . import common_test
from . common_test import func_name

client = DatabricksMlflowClient()
model_name = common_test.cfg["workspace_registry"]["model"]

#  "object_id": "/registered-models/94abcb7b9c49465f92a5fb459c26898a",
#  "object_type": "registered-model",


def test_get_registered_model_permissions_by_name():
    perms = client.get_registered_model_permissions(model_name)
    dump_as_json(perms, func_name())
    common_test.do_test_get_registered_model_permissions(perms)

def test_get_registered_model_permissions_by_id():
    model_id = client._get_registered_model_id(model_name)
    perms = client.get_registered_model_permissions(model_id, is_model_id=True)
    dump_as_json(perms, func_name())
    common_test.do_test_get_registered_model_permissions(perms)
    common_test.check_object_id(model_id, perms)


def test_get_registered_model_permission_levels_by_name():
    perms = client.get_registered_model_permission_levels(model_name)
    dump_as_json(perms, func_name())
    common_test.do_test_get_experiment_permission_levels(perms)

def test_get_registered_model_permission_levels_by_id():
    model_id = client._get_registered_model_id(model_name)
    perms = client.get_registered_model_permission_levels(model_id, is_model_id=True)
    common_test.do_test_get_experiment_permission_levels(perms)
