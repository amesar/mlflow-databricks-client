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


class DatabricksUcMlflowClient(BaseDatabricksMlflowClient):
    def __init__(self):
        super().__init__("api/2.1")

    def get_registered_model_effective_permissions(self, model_name):
        # https://docs.databricks.com/api/workspace/grants/geteffective
        resource =  f"unity-catalog/effective-permissions/function/{model_name}"
        return self.client.get(resource) 

    def get_registered_model_permissions(self, model_name):
        # https://docs.databricks.com/api/workspace/grants/get
        resource =  f"unity-catalog/permissions/function/{model_name}"
        return self.client.get(resource) 
