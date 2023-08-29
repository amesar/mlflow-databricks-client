from databricks.sdk import WorkspaceClient

from databricks.sdk.service import catalog

class BaseDatabricksMlflowClient:
    """
    Common resources shared between non Unity Catalog and Unity Catalog implementations.
    """

    def __init__(self):
        self.client = WorkspaceClient()


    def get_experiment_permissions(self, experiment_id_or_name):
        # https://docs.databricks.com/api/workspace/experiments/getexperimentpermissions
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.get_experiment_permissions

        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self.client.permissions.get(
            request_object_type="experiments",
            request_object_id=experiment_id
        )

    def get_experiment_permission_levels(self, experiment_id_or_name):
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.get_experiment_permission_levels
        # https://docs.databricks.com/api/workspace/experiments/getexperimentpermissionlevels

        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self.client.permissions.get_permission_levels(
            request_object_type="experiments",
            request_object_id=experiment_id
        )


    def set_experiment_permissions(self, experiment_id_or_name, access_control_list):
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.set_experiment_permissions
        # https://docs.databricks.com/api/workspace/experiments/setexperimentpermissions

        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self.client.permissions.set_permission(experiment_id, access_control_list)

    def update_experiment_permissions(self, experiment_id_or_name, access_control_list):
        # https://docs.databricks.com/api/workspace/experiments/updateexperimentpermissions
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.update_experiment_permissions

        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self.client.permissions.update_permission(experiment_id, access_control_list)


    def _get_experiment_id(self, experiment_id_or_name):
        """
        Gets an experiment either by ID or name.
        """
        if not "/" in experiment_id_or_name:
            return experiment_id_or_name
        rsp = self.client.experiments.get_by_name(experiment_id_or_name)
        return rsp.experiment.experiment_id


class DatabricksMlflowClient(BaseDatabricksMlflowClient):

    def get_registered_model_permissions(self, registered_model_id):
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.get_registered_model_permissions
        # https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissions
        return self.client.model_registry.get_registered_model_permissions(registered_model_id)

    def get_registered_model_permissions_by_name(self, registered_model_name):
        model_id = self.get_registered_model_id(registered_model_name)
        return self.client.model_registry.get_registered_model_permissions(model_id)


    def get_registered_model_permission_levels(self, registered_model_id):
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.get_registered_model_permission_levels
        return self.client.model_registry.get_registered_model_permission_levels(registered_model_id)

    def get_registered_model_permissions_levels_by_name(self, registered_model_name):
        model_id = self.get_registered_model_id(registered_model_name)
        return self.client.model_registry.get_registered_model_permission_levels(model_id)


    def set_registered_model_permissions(self, registered_model_id, access_control_list):
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.set_registered_model_permissions
        return self.client.model_registry.set_registered_model_permissions(registered_model_id, access_control_list=access_control_list)

    def update_registered_model_permissions(self, registered_model_id, access_control_list):
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.update_registered_model_permissions
        return self.client.model_registry.update_registered_model_permissions(registered_model_id, access_control_list=access_control_list)

    def get_registered_model_id(self, registered_model_name):
        model = self.client.model_registry.get_model(registered_model_name)
        model = model.registered_model_databricks
        return model.id


class DatabricksUcMlflowClient(BaseDatabricksMlflowClient):

    def get_registered_model_effective_permissions(self, model_name):
        # https://docs.databricks.com/api/workspace/grants/geteffective
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html#GrantsAPI.get
        return self.client.grants.get_effective(catalog.SecurableType.FUNCTION, model_name)

    def get_registered_model_permissions(self, model_name):
        # https://docs.databricks.com/api/workspace/grants/get
        # https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html#GrantsAPI.get_effective
        return self.client.grants.get(catalog.SecurableType.FUNCTION, model_name)

    def update_registered_model_permissions(self, model_name, changes):
        return self.client.grants.update(catalog.SecurableType.FUNCTION, model_name, changes=changes)
