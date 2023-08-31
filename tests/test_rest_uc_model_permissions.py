from mlflow_databricks_client.rest.client import DatabricksUcMlflowClient
from . common_test import cfg
from mlflow_databricks_client.common.utils import dump_as_json

client = DatabricksUcMlflowClient()
print("client:", client)

model_name = cfg["unity_catalog_registry"]["model"]
principal = cfg["principal"]


# ==== Test Get Endpoints

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


# ==== Test Update Endpoints

def test_update_registered_model_permissions_add():
    privilege = "APPLY_TAG"
    perms = {
      "changes": [
        {
          "principal": principal,
          "add": [ privilege ]
        }
      ]
    }
    dump_as_json(perms, "Permissions to update")
    rsp = client.update_registered_model_permissions(model_name, perms)
    dump_as_json(rsp,"update_registered_model_permissions")
    _check_privelege_update(rsp, privilege)

    rsp = client.get_registered_model_effective_permissions(model_name)
    dump_as_json(rsp, "get_registered_model_effective_permissions")
    _check_privelege_get(rsp, privilege)


def test_update_registered_model_permissions_remove():
    # NOTE: depends upon results from test_update_registered_model_permissions_add
    privilege = "APPLY_TAG"
    rsp = client.get_registered_model_effective_permissions(model_name)
    dump_as_json(rsp, "get_registered_model_effective_permissions")
    _check_privelege_get(rsp, privilege)

    perms = {
      "changes": [
        {
          "principal": principal,
          "remove": [ privilege ]
        }
      ]
    }
    dump_as_json(perms, "Permissions to update")
    rsp = client.update_registered_model_permissions(model_name, perms)
    dump_as_json(rsp,"update_registered_model_permissions")

    rsp = client.get_registered_model_effective_permissions(model_name)
    dump_as_json(rsp, "get_registered_model_effective_permissions")
    _check_privelege_get(rsp, privilege, False)


def _check_privelege_update(rsp, privilege_name):
    privileges = _get_privileges(rsp)
    matches = [ pr for pr in privileges if pr == privilege_name ]
    assert len(matches) > 0

def _check_privelege_get(rsp, privilege_name, equals=True):
    privileges = _get_privileges(rsp)
    matches = [ pr for pr in privileges if pr["privilege"] == privilege_name ]
    if equals:
        assert len(matches) > 0
    else:
        assert len(matches) == 0

def _get_privileges(rsp):
    privilege_assignments = rsp.get("privilege_assignments")
    assert privilege_assignments
    privileges = privilege_assignments[0].get("privileges")
    assert privileges
    assert len(privileges) > 0
    return privileges
