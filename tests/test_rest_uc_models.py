from mlflow_databricks_client.rest.client import DatabricksUcMlflowClient
from . common_test import cfg


client = DatabricksUcMlflowClient()

model_name = cfg["unity_catalog_registry"]["model"]
principal = cfg["principal"]


def test_get_registered_model_effective_permissions():
    rsp = client.get_registered_model_effective_permissions(model_name)
    privilege_assignments = rsp.get("privilege_assignments")
    assert privilege_assignments
    assert len(privilege_assignments) > 0
    privileges = privilege_assignments[0].get("privileges")
    assert privileges
    assert len(privileges) > 0


def test_get_registered_model_permissions():
    client.get_registered_model_permissions(model_name)
    # NOTE: seems to always be empty
