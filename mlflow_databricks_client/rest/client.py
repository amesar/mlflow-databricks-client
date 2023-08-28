from . http_client import HttpClient

class BaseDatabricksMlflowClient:
    """
    Common resources shared between non Unity Catalog and Unity Catalog implementations.
    """

    def __init__(self, api_prefix):
        self.client = HttpClient(api_prefix)


    def get_experiment_permissions(self, experiment_id_or_name):
        # https://docs.databricks.com/api/workspace/experiments/getexperimentpermissions
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        resource = f"permissions/experiments/{experiment_id}"
        return self.client.get(resource)

    def get_experiment_permission_levels(self, experiment_id_or_name):
        # https://docs.databricks.com/api/workspace/experiments/getexperimentpermissionlevels
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        resource = f"permissions/experiments/{experiment_id}/permissionLevels"
        return self.client.get(resource)

    def _get_experiment_id(self, experiment_id_or_name):
        """ Gets an experiment either by ID or name.  """
        if not "/" in experiment_id_or_name:
            return experiment_id_or_name
        resource = "mlflow/experiments/get-by-name"
        rsp = self.client.get(resource, { "experiment_name": experiment_id_or_name })
        return rsp["experiment"]["experiment_id"]


    def set_experiment_permissions(self, experiment_id_or_name, access_control_list):
        # https://docs.databricks.com/api/workspace/experiments/setexperimentpermissions
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        resource = f"permissions/experiments/{experiment_id}"
        return self.client.put(resource, { "access_control_list": access_control_list })

    def update_experiment_permissions(self, experiment_id_or_name, access_control_list):
        # https://docs.databricks.com/api/workspace/experiments/updateexperimentpermissions
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        resource = f"permissions/experiments/{experiment_id}"
        return self.client.patch(resource, { "access_control_list": access_control_list })


    def _get_registered_model_id(self, model_name_or_id, is_model_id=False):
        if is_model_id:
            model_id = model_name_or_id
        else:
            model = self.get_registered_model_databricks(model_name_or_id)
            model = model["registered_model_databricks"]
            model_id =  model["id"]
        return model_id


    def __repr__(self):
        return str(self.client)


class DatabricksMlflowClient(BaseDatabricksMlflowClient):
    """
    Endpoints that apply only to non Unity Catalog registered models.
    """
    def __init__(self):
        super().__init__("api/2.0")

    def get_registered_model_databricks(self, model_name):
        # https://docs.databricks.com/api/workspace/modelregistry/getmodel
        return self.client.get("mlflow/databricks/registered-models/get", { "name": model_name })

    def get_registered_model_permissions(self, model_name_or_id, is_model_id=False):
        # https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissions
        model_id = self._get_registered_model_id(model_name_or_id, is_model_id)
        resource = f"permissions/registered-models/{model_id}"
        return self.client.get(resource)

    def get_registered_model_permission_levels(self, model_name_or_id, is_model_id=False):
        # https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissionlevels
        model_id = self._get_registered_model_id(model_name_or_id, is_model_id)
        resource = f"permissions/registered-models/{model_id}/permissionLevels"
        return self.client.get(resource)


class DatabricksUcMlflowClient:
    def __init__(self):
        self.client_21 = HttpClient("api/2.1")
        self.client_20 = HttpClient("api/2.0/mlflow/unity-catalog")

    # ==== api/2.1 - UC permissions API

    def get_registered_model_effective_permissions(self, model_name):
        # https://docs.databricks.com/api/workspace/grants/geteffective
        resource =  f"unity-catalog/effective-permissions/function/{model_name}"
        return self.client_21.get(resource) 

    def get_registered_model_permissions(self, model_name):
        # https://docs.databricks.com/api/workspace/grants/get
        resource =  f"unity-catalog/permissions/function/{model_name}"
        return self.client_21.get(resource) 

    def update_registered_model_permissions(self, model_name, permissions):
        # https://docs.databricks.com/api/workspace/grants/update
        resource = f"unity-catalog/permissions/function/{model_name}"
        return self.client_21.patch(resource, permissions) 


    # ==== api/2.0/mlflow/unity-catalog - Standard OSS methods. Forwards to new endpoint - unchanged signature from non-UC.

    # ==== Registered Model

    def get_registered_model(self, name):
        # https://mlflow.org/docs/latest/rest-api.html#create-registeredmodel
        return self.client_20.get("registered-models/get", _clean(locals()))

    def create_registered_model(self, name, tags=None, description=None):
        # https://mlflow.org/docs/latest/rest-api.html#create-registeredmodel
        return self.client_20.post("registered-models/create", _clean(locals()))

    def update_registered_model(self, name, description=None):
        # https://mlflow.org/docs/latest/rest-api.html#update-registeredmodel
        # NOTE: though doc says description is optional, error is returned not specified
        # ERROR:  { error_code: "INVALID_PARAMETER_VALUE","message":"UpdateRegisteredModel Nothing to update" }
        return self.client_20.patch("registered-models/update", _clean(locals()))

    def delete_registered_model(self, name):
        # https://www.mlflow.org/docs/latest/rest-api.html#delete-registeredmodel
        return self.client_20.delete("registered-models/delete", _clean(locals()))

    def search_registered_model_versions(self, filter, max_results=None, order_by=None, page_token=None):
        return self.client_20.get("registered-models/search", _clean(locals()))

    def search_registered_models(self, filter=None, max_results=None, order_by=None, page_token=None):
        return self.client_20.get("registered-models/search", _clean(locals()))


    # ==== Regisered Model Alias

    def get_registered_model_by_alias(self, name, alias):
        # https://www.mlflow.org/docs/latest/rest-api.html#get-model-version-by-alias
        # https://www.mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.get_model_version_by_alias
        resource = f"registered-models/alias"
        return self.client_20.get(resource, _clean(locals()))

    def set_registered_model_alias(self, name, alias, version):
        # https://www.mlflow.org/docs/latest/rest-api.html#set-registered-model-alias
        # https://www.mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.set_registered_model_alias
        resource = f"registered-models/alias"
        return self.client_20.post(resource, _clean(locals()))

    def delete_registered_model_alias(self, name, alias, version):
        # https://www.mlflow.org/docs/latest/rest-api.html#delete-registered-model-alias
        # https://www.mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.delete_registered_model_alias
        resource = f"registered-models/alias"
        return self.client_20.delete(resource, _clean(locals()))


    # ==== Model Version

    def get_model_version(self, name, version):
        return self.client_20.get("model-versions/get", _clean(locals()))

    def create_model_version(self, name, source, run_id=None, tags=None, run_link=None, description=None, await_creation_for=None):
        # https://mlflow.org/docs/latest/rest-api.html#create-modelversion
        # https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.create_model_version
        return self.client_20.post("model-versions/create", _clean(locals()))

    def update_model_version(self, name, version, description=None):
        # https://mlflow.org/docs/latest/rest-api.html#update-modelversion
        return self.client_20.patch("model-versions/update", _clean(locals()))

    def delete_model_version(self, name, version):
        # https://mlflow.org/docs/latest/rest-api.html#delete-modelversion
        return self.client_20.delete("model-versions/delete", _clean(locals()))

    def set_model_version_tag(self, name, version=None, key=None, value=None, stage=None):
        # https://mlflow.org/docs/latest/rest-api.html#set-model-version-tag
        # https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.set_model_version_tag
        return self.client_20.post("model-versions/set-tag", _clean(locals()))
        # NOTE: MLflow Python doc strangely says key and value are optional i
        # ERROR: "{g"error_code":"INVALID_PARAMETER_VALUE","message":"Tag name  is not valid","details":[{"@type":"type.googleapis.com/google.rpc.RequestInfo","request_id":"85d1bcc6-ae37-4afb-b8b6-f9da7c612d13","serving_data":""}]}"}

    def search_model_versions(self, filter=None, max_results=None, order_by=None, page_token=None):
        # https://mlflow.org/docs/latest/rest-api.html#search-modelversions
        # https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.search_model_versions
        # NOTE: Per MLflow doc, filter is optional but Databricks requires it (no documentation).
        # ERROR: { "error_code":"INVALID_PARAMETER_VALUE","message":"Missing filter: please specify a filter parameter in the format `name = 'model_name'`."}"}
        return self.client_20.get("model-versions/search", _clean(locals()))

    # ==== 

def _clean(args):
    args.pop("self", None)
    return args
