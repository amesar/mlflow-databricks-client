from mlflow_databricks_client.rest.client import DatabricksMlflowClient
#from mlflow_databricks_client.common.utils import dump_as_json
from . import common_test

client = DatabricksMlflowClient()
model_name = common_test.cfg["workspace_registry"]["model"]

#  "object_id": "/registered-models/94abcb7b9c49465f92a5fb459c26898a",
#  "object_type": "registered-model",

def test_get_registered_model_permissions_by_name():
    perms = client.get_registered_model_permissions(model_name)
    #dump_as_json(perms)
    assert perms.get("object_type") == "registered-model"
    acl = perms.get("access_control_list")
    assert acl
    assert len(acl) > 0

def test_get_registered_model_permissions_by_id():
    model_id = client._get_registered_model_id(model_name)
    perms = client.get_registered_model_permissions(model_id, is_model_id=True)
    assert perms.get("object_type") == "registered-model"
    acl = perms.get("access_control_list")
    assert acl
    assert len(acl) > 0
    common_test._check_object_id(model_id, perms)


def test_get_registered_model_permission_levels_by_name():
    perms = client.get_registered_model_permission_levels(model_name)
    levels = perms.get("permission_levels")
    assert levels
    assert len(levels) > 0

def test_get_registered_model_permission_levels_by_id():
    model_id = client._get_registered_model_id(model_name)
    perms = client.get_registered_model_permission_levels(model_id, is_model_id=True)
    levels = perms.get("permission_levels")
    assert levels
    assert len(levels) > 0
