from databricks.sdk import WorkspaceClient

sdk_client = WorkspaceClient()

from . common_test import func_name, cfg
from . sdk_test_utils import dump_rsp

# ==== Setup

as_json = True

experiment_name = cfg["experiment"]
rsp = sdk_client.experiments.get_by_name(experiment_name)
experiment_id = rsp.experiment.experiment_id

model_name = cfg["workspace_registry"]["model"]
rsp = sdk_client.model_registry.get_model(model_name)
model_id = rsp.registered_model_databricks.id

uc_model_name = cfg["unity_catalog_registry"]["model"]

principal = cfg["principal"]


# ==== Experiment Permisions

# Get experiment permissions

def test_get_experiments_permissions():
    rsp = sdk_client.experiments.get_experiment_permissions(experiment_id)
    dump_rsp(rsp, func_name(), as_json)

def test_get_experiments_permission_levels():
    rsp = sdk_client.experiments.get_experiment_permission_levels(experiment_id)
    dump_rsp(rsp, func_name(), as_json)


# Set/update experiment permissions

from databricks.sdk.service.ml import ExperimentAccessControlRequest, ExperimentPermissionLevel

acl = [ 
   ExperimentAccessControlRequest(
     user_name = principal,
     permission_level = ExperimentPermissionLevel.CAN_MANAGE
  ) 
]

def test_set_experiments_permission():
    rsp = sdk_client.experiments.set_experiment_permissions(experiment_id, access_control_list=acl)
    dump_rsp(rsp, func_name(), as_json)

def test_update_experiments_permission():
    rsp = sdk_client.experiments.update_experiment_permissions(experiment_id, access_control_list=acl)
    dump_rsp(rsp, func_name(), as_json)


# ==== Registered Model Permissions

# Get registered model permissions

def test_get_registered_model_permissions():
    rsp = sdk_client.model_registry.get_registered_model_permissions(model_id)
    dump_rsp(rsp, func_name(), as_json)

def test_get_registered_model_permission_levels():
    rsp = sdk_client.model_registry.get_registered_model_permission_levels(model_id)
    dump_rsp(rsp, func_name(), as_json)


# Set/update registered model permissions

from databricks.sdk.service.ml import RegisteredModelAccessControlRequest, RegisteredModelPermissionLevel

acl = [
  RegisteredModelAccessControlRequest(
    user_name = principal,
    permission_level = RegisteredModelPermissionLevel.CAN_MANAGE
  )
]

def test_set_registered_model_permission():
    rsp = sdk_client.model_registry.set_registered_model_permissions(model_id, access_control_list=acl)
    dump_rsp(rsp, func_name(), as_json)

def test_update_registered_model_permission():
    rsp = sdk_client.model_registry.update_registered_model_permissions(model_id, access_control_list=acl)
    dump_rsp(rsp, func_name(), as_json)


# ==== Registered Model Permissions - Unity Catalog

from databricks.sdk.service import catalog

def test_uc_get_registered_model_effective_permissions():
    rsp = sdk_client.grants.get_effective(catalog.SecurableType.FUNCTION, uc_model_name)
    dump_rsp(rsp, func_name(), as_json)

def test_uc_set_registered_model_permission():
    rsp = sdk_client.grants.get(catalog.SecurableType.FUNCTION, uc_model_name)
    dump_rsp(rsp, func_name(), as_json)

def test_uc_update_registered_model_permission():
    changes = [
        catalog.PermissionsChange(add=[catalog.Privilege.APPLY_TAG], principal=principal)
    ]
    rsp = sdk_client.grants.update(catalog.SecurableType.FUNCTION, uc_model_name, changes=changes)
    dump_rsp(rsp, func_name(), as_json)
