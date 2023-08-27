from mlflow_databricks_client.rest.client import DatabricksMlflowClient
from . import common_test

client = DatabricksMlflowClient()

experiment_name = common_test.cfg["experiment"]


def test_get_experiment_permissions_by_id():
    experiment_id = client._get_experiment_id(experiment_name)
    perms = client.get_experiment_permissions(experiment_id)
    common_test._check_object_id(experiment_id, perms)
    assert perms.get("object_type") == "mlflowExperiment"

def test_get_experiment_permissions_by_name():
    perms = client.get_experiment_permissions(experiment_name)
    assert perms.get("object_type") == "mlflowExperiment"


def test_get_experiment_permission_levels_by_id():
    experiment_id = client._get_experiment_id(experiment_name)
    perms = client.get_experiment_permission_levels(experiment_id)
    _run_get_experiment_permission_levels(perms)

def test_get_experiment_permission_levels_by_name():
    perms = client.get_experiment_permission_levels(experiment_name)
    _run_get_experiment_permission_levels(perms)


def _run_get_experiment_permission_levels(perms):
    perms = perms.get("permission_levels")
    assert perms 
    assert len(perms) > 0
    matches = [ p for p in perms if p["permission_level"] == "CAN_READ" ]
    assert len(matches) == 1
