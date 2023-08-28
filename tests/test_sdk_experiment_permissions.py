from mlflow_databricks_client.sdk.client import DatabricksMlflowClient
from . import common_test
from . common_test import func_name
from . sdk_test_utils import dump_rsp

client = DatabricksMlflowClient()

experiment_name = common_test.cfg["experiment"]
experiment_id = client._get_experiment_id(experiment_name)

as_json = True


def test_get_experiment_permissions_by_id():
    perms = client.get_experiment_permissions(experiment_id)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.check_object_id(experiment_id, perms)

def test_get_experiment_permissions_by_name():
    perms = client.get_experiment_permissions(experiment_name)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.check_object_id(experiment_id, perms)

def test_get_experiment_permission_levels_by_id():
    perms = client.get_experiment_permission_levels(experiment_id)
    perms = dump_rsp(perms, func_name(), as_json)
    common_test.do_test_get_experiment_permission_levels(perms)

def set_experiment_permissions(): # TODO
    pass

def update_experiment_permissions(): # TODO
    pass
