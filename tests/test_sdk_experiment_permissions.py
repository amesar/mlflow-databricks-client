from databricks.sdk.service.ml import ExperimentAccessControlRequest, ExperimentPermissionLevel

from mlflow_databricks_client.sdk.client import DatabricksMlflowClient
from . import common_test
from . common_test import cfg, func_name
from . sdk_test_utils import dump_rsp

client = DatabricksMlflowClient()

experiment_name = cfg["experiment"]
experiment_id = client._get_experiment_id(experiment_name)
principal = cfg["principal"]

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


acl = [ ExperimentAccessControlRequest(
             user_name = principal,
             permission_level = ExperimentPermissionLevel.CAN_MANAGE
      ) ]

def test_set_experiment_permissions():
    rsp = client.set_experiment_permissions(experiment_id, acl)
    dump_rsp(rsp, func_name(), as_json)
    

def test_update_experiment_permissions():
    rsp = client.update_experiment_permissions(experiment_id, acl)
    dump_rsp(rsp, func_name(), as_json)
