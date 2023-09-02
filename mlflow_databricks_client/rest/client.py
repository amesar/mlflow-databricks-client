"""
REST client for Databricks-specific MLflow API.
"""

# pylint: disable=W0613 # Unused argument

from mlflow_databricks_client.base_client import BaseDatabricksMlflowClient as _BaseDatabricksMlflowClient
from mlflow_databricks_client.base_client import DatabricksMlflowClient as _DatabricksMlflowClient
from . http_client import HttpClient


class BaseDatabricksMlflowClient(_BaseDatabricksMlflowClient):
    """
    Common endpoints shared between non Unity Catalog and Unity Catalog implementations.
    """

    def __init__(self, api_prefix):
        """
        :param api_prefix: Resource prefix such as "api/2.0" or "api/2.1" or "api/2.0/mlflow/unity-catalog".
        """
        self._client = HttpClient(api_prefix)


    def _get_experiment_permissions(self, experiment_id):
        """
        See https://docs.databricks.com/api/workspace/experiments/getexperimentpermissions
        """
        resource = f"permissions/experiments/{experiment_id}"
        return self._client.get(resource)

    def _get_experiment_permission_levels(self, experiment_id):
        """
        See https://docs.databricks.com/api/workspace/experiments/getexperimentpermissionlevels
        """
        resource = f"permissions/experiments/{experiment_id}/permissionLevels"
        return self._client.get(resource)


    def _get_experiment_id(self, experiment_id_or_name):
        """ Gets an experiment either by ID or name.  """
        if not "/" in experiment_id_or_name:
            return experiment_id_or_name
        resource = "mlflow/experiments/get-by-name"
        rsp = self._client.get(resource, { "experiment_name": experiment_id_or_name })
        return rsp["experiment"]["experiment_id"]


    def _set_experiment_permissions(self, experiment_id, access_control_list):
        """
        See https://docs.databricks.com/api/workspace/experiments/setexperimentpermissions
        """
        resource = f"permissions/experiments/{experiment_id}"
        return self._client.put(resource, { "access_control_list": access_control_list })

    def _update_experiment_permissions(self, experiment_id, access_control_list):
        """
        See https://docs.databricks.com/api/workspace/experiments/updateexperimentpermissions
        """
        resource = f"permissions/experiments/{experiment_id}"
        return self._client.patch(resource, { "access_control_list": access_control_list })


    def _get_registered_model_id(self, model_name):
        model = self.get_registered_model_databricks(model_name)
        model = model["registered_model_databricks"]
        return model["id"]


    def _delete_runs(self, experiment_id, max_timestamp_millis, max_runs=None):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.delete_runs
        """
        resource = "mlflow/databricks/runs/delete-runs"
        params = { "experiment_id": experiment_id, "max_timestamp_millis": max_timestamp_millis, "max_runs": max_runs }
        return self._client.post(resource, params)

    def _restore_runs(self, experiment_id, min_timestamp_millis, max_runs=None):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.restore_runs
        """
        resource = "mlflow/databricks/runs/restore-runs"
        params = { "experiment_id": experiment_id, "min_timestamp_millis": min_timestamp_millis, "max_runs": max_runs }
        return self._client.post(resource, params)


    def __repr__(self):
        return str(self._client)


class DatabricksMlflowClient(BaseDatabricksMlflowClient, _DatabricksMlflowClient):
    """
    Endpoints that only apply to non Unity Catalog registered models.
    """
    def __init__(self):
        super().__init__("api/2.0")


    def get_registered_model_databricks(self, model_name):
        """
        See https://docs.databricks.com/api/workspace/modelregistry/getmodel
        """
        return self._client.get("mlflow/databricks/registered-models/get", { "name": model_name })


    def get_registered_model_permissions(self, model_id):
        """
        See https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissions
        """
        resource = f"permissions/registered-models/{model_id}"
        return self._client.get(resource)


    def get_registered_model_permission_levels(self, model_id):
        """
        See https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissionlevels
        """
        resource = f"permissions/registered-models/{model_id}/permissionLevels"
        return self._client.get(resource)


    def set_registered_model_permissions(self, model_id, access_control_list=None):
        """
        See https://docs.databricks.com/api/workspace/modelregistry/setregisteredmodelpermissions
        """
        resource = f"permissions/registered-models/{model_id}"
        return self._client.put(resource, { "access_control_list": access_control_list })

    def update_registered_model_permissions(self, model_id, access_control_list=None):
        """
        See https://docs.databricks.com/api/workspace/modelregistry/updateregisteredmodelpermissions
        """
        resource = f"permissions/registered-models/{model_id}"
        return self._client.patch(resource, { "access_control_list": access_control_list })


class DatabricksUcMlflowClient:
    """
    Endpoints that only apply to Unity Catalog registered models.
    """
    def __init__(self):
        self._client_21 = HttpClient("api/2.1")
        self._client_20 = HttpClient("api/2.0/mlflow/unity-catalog")

    # ==== api/2.1 - UC permissions API

    def get_registered_model_effective_permissions(self, model_name):
        """
        See https://docs.databricks.com/api/workspace/grants/geteffective
        """
        resource =  f"unity-catalog/effective-permissions/function/{model_name}"
        return self._client_21.get(resource) 

    def get_registered_model_permissions(self, model_name):
        """
        See https://docs.databricks.com/api/workspace/grants/get
        """
        resource =  f"unity-catalog/permissions/function/{model_name}"
        return self._client_21.get(resource) 

    def update_registered_model_permissions(self, model_name, changes):
        """
        See https://docs.databricks.com/api/workspace/grants/update
        """
        resource = f"unity-catalog/permissions/function/{model_name}"
        return self._client_21.patch(resource, changes) 


    # ==== api/2.0/mlflow/unity-catalog - Standard OSS methods. Forwards to new endpoint - unchanged signature from non-UC.

    # ==== Registered Model

    def get_registered_model(self, name):
        """
        See https://mlflow.org/docs/latest/rest-api.html#create-registeredmodel
        """
        return self._client_20.get("registered-models/get", _clean(locals()))

    def create_registered_model(self, name, tags=None, description=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#create-registeredmodel
        """
        return self._client_20.post("registered-models/create", _clean(locals()))

    def update_registered_model(self, name, description=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#update-registeredmodel
        """
        # NOTE: though doc says description is optional, error is returned if not specified
        # ERROR:  { error_code: "INVALID_PARAMETER_VALUE","message":"UpdateRegisteredModel Nothing to update" }
        return self._client_20.patch("registered-models/update", _clean(locals()))

    def delete_registered_model(self, name):
        """
        See https://www.mlflow.org/docs/latest/rest-api.html#delete-registeredmodel
        """
        return self._client_20.delete("registered-models/delete", _clean(locals()))

    def search_registered_model_versions(self, filter, max_results=None, order_by=None, page_token=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#search-modelversions
        """
        return self._client_20.get("registered-models/search", _clean(locals()))

    def search_registered_models(self, filter=None, max_results=None, order_by=None, page_token=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#search-registeredmodels
        """
        return self._client_20.get("registered-models/search", _clean(locals()))


    # ==== Regisered Model Alias

    def get_registered_model_by_alias(self, name, alias):
        """
        See https://www.mlflow.org/docs/latest/rest-api.html#get-model-version-by-alias
        <br>
        See https://www.mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.get_model_version_by_alias
        """
        resource = "registered-models/alias"
        return self._client_20.get(resource, _clean(locals()))

    def set_registered_model_alias(self, name, alias, version):
        """
        See https://www.mlflow.org/docs/latest/rest-api.html#set-registered-model-alias
        <br>
        See https://www.mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.set_registered_model_alias
        """
        resource = "registered-models/alias"
        return self._client_20.post(resource, _clean(locals()))

    def delete_registered_model_alias(self, name, alias, version):
        """
        See https://www.mlflow.org/docs/latest/rest-api.html#delete-registered-model-alias
        <br>
        See https://www.mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.delete_registered_model_alias
        """
        resource = "registered-models/alias"
        return self._client_20.delete(resource, _clean(locals()))


    # ==== Model Version

    def get_model_version(self, name, version):
        return self._client_20.get("model-versions/get", _clean(locals()))

    def create_model_version(self, name, source, run_id=None, tags=None, run_link=None, description=None, await_creation_for=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#create-modelversion
        <br>
        See https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.create_model_version
        """
        return self._client_20.post("model-versions/create", _clean(locals()))

    def update_model_version(self, name, version, description=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#update-modelversion
        """
        return self._client_20.patch("model-versions/update", _clean(locals()))

    def delete_model_version(self, name, version):
        """
        See https://mlflow.org/docs/latest/rest-api.html#delete-modelversion
        """
        return self._client_20.delete("model-versions/delete", _clean(locals()))

    def set_model_version_tag(self, name, version=None, key=None, value=None, stage=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#set-model-version-tag
        <br>
        See https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.set_model_version_tag
        """
        return self._client_20.post("model-versions/set-tag", _clean(locals()))
        # NOTE: MLflow Python doc strangely says key and value are optional i
        # ERROR: "{g"error_code":"INVALID_PARAMETER_VALUE","message":"Tag name  is not valid","details":[{"@type":"type.googleapis.com/google.rpc.RequestInfo","request_id":"85d1bcc6-ae37-4afb-b8b6-f9da7c612d13","serving_data":""}]}"}

    def search_model_versions(self, filter=None, max_results=None, order_by=None, page_token=None):
        """
        See https://mlflow.org/docs/latest/rest-api.html#search-modelversions
        <br>
        See https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.search_model_versions
        """
        # NOTE: Per MLflow doc, filter is optional but Databricks requires it (no documentation).
        # ERROR: { "error_code":"INVALID_PARAMETER_VALUE","message":"Missing filter: please specify a filter parameter in the format `name = 'model_name'`."}"}
        return self._client_20.get("model-versions/search", _clean(locals()))


    def __repr__(self):
        msg = { "client_20": self._client_20, "client_21": self._client_21 }
        return str(msg)


def _clean(args):
    args.pop("self", None)
    return args
