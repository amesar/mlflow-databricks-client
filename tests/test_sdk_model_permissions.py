from mlflow_databricks_client.sdk.client import DatabricksMlflowClient
from . import common_test
from . common_test import func_name
from . sdk_test_utils import dump_rsp

client = DatabricksMlflowClient()

model_name = common_test.cfg["workspace_registry"]["model"]
model_id = client.get_registered_model_id(model_name)

as_json = True


def test_get_registered_model_permissions():
    perms = client.get_registered_model_permissions(model_id)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_registered_model_permissions(perms)
    common_test.check_object_id(model_id, perms)

def _test_get_registered_model_permissions_by_name():
    perms = client.get_registered_model_permissions_by_name(model_name)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_registered_model_permissions(perms)


def test_get_registered_model_permission_levels():
    model_id = client.get_registered_model_id(model_name)
    perms = client.get_registered_model_permission_levels(model_id)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_experiment_permission_levels(perms)

def test_get_registered_model_permission_levels_by_name():
    perms = client.get_registered_model_permission_levels(model_name)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_experiment_permission_levels(perms)
