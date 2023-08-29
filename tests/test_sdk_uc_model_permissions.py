from databricks.sdk.service import catalog

from mlflow_databricks_client.sdk.client import DatabricksUcMlflowClient
from . common_test import func_name, cfg
from . sdk_test_utils import dump_rsp


client = DatabricksUcMlflowClient()

principal = cfg["principal"]
model_name = cfg["unity_catalog_registry"]["model"]

as_json = True


def test_get_registered_model_effective_permissions():
    perms = client.get_registered_model_effective_permissions(model_name)
    dump_rsp(perms, func_name(), as_json)


def test_get_registered_model_permissions():
    perms = client.get_registered_model_permissions(model_name)
    dump_rsp(perms, func_name(), as_json)


def test_update_registered_model_permissions():
    changes = [
        catalog.PermissionsChange(add=[catalog.Privilege.APPLY_TAG], principal=principal)
    ]
    rsp = client.update_registered_model_permissions(model_name, changes)
    dump_rsp(rsp, func_name(), as_json)
