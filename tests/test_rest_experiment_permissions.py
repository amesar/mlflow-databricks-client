from mlflow_databricks_client.rest.client import DatabricksMlflowClient
from mlflow_databricks_client.common.utils import dump_as_json
from . import common_test
from . common_test import func_name

client = DatabricksMlflowClient()
experiment_name = common_test.cfg["experiment"]


def test_get_experiment_permissions_by_id():
    experiment_id = client._get_experiment_id(experiment_name)
    perms = client.get_experiment_permissions(experiment_id)
    dump_as_json(perms, func_name())
    common_test.check_object_id(experiment_id, perms)
    assert perms.get("object_type") == "mlflowExperiment"

def test_get_experiment_permissions_by_name():
    perms = client.get_experiment_permissions(experiment_name)
    dump_as_json(perms, func_name())
    assert perms.get("object_type") == "mlflowExperiment"


def test_get_experiment_permission_levels_by_id():
    experiment_id = client._get_experiment_id(experiment_name)
    perms = client.get_experiment_permission_levels(experiment_id)
    dump_as_json(perms, func_name())
    common_test.do_test_get_experiment_permission_levels(perms)

def test_get_experiment_permission_levels_by_name():
    perms = client.get_experiment_permission_levels(experiment_name)
    dump_as_json(perms, func_name())
    common_test.do_test_get_experiment_permission_levels(perms)
