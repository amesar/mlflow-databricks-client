from databricks.sdk.service.ml import RegisteredModelAccessControlRequest, RegisteredModelPermissionLevel

from mlflow_databricks_client.sdk.client import DatabricksMlflowClient
from . import common_test
from . common_test import cfg, func_name
from . sdk_test_utils import dump_rsp

client = DatabricksMlflowClient()

model_name = cfg["workspace_registry"]["model"]
model_id = client._get_registered_model_id(model_name)
principal = cfg["principal"]

as_json = True

def test_get_registered_model_databricks():
    model = client.get_registered_model_databricks(model_name)
    dump_rsp(model, func_name(), as_json)


def test_get_registered_model_permissions():
    perms = client.get_registered_model_permissions(model_id)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_registered_model_permissions(perms)
    common_test.check_object_id(model_id, perms)

def test_get_registered_model_permissions_by_name():
    perms = client.get_registered_model_permissions_by_name(model_name)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_registered_model_permissions(perms)


def test_get_registered_model_permission_levels():
    perms = client.get_registered_model_permission_levels(model_id)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_experiment_permission_levels(perms)

def test_get_registered_model_permission_levels_by_name():
    perms = client.get_registered_model_permission_levels(model_name)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_experiment_permission_levels(perms)


acl = [
  RegisteredModelAccessControlRequest(
    user_name = principal,
    permission_level = RegisteredModelPermissionLevel.CAN_MANAGE
  )
]

def test_set_registered_model_permissions():
    rsp = client.set_registered_model_permissions(model_id, acl)
    rsp = dump_rsp(rsp, func_name(), as_json)

def test_update_registered_model_permissions():
    rsp = client.update_registered_model_permissions(model_id, acl)
    rsp = dump_rsp(rsp, func_name(), as_json)
