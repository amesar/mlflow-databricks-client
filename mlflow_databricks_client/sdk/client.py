from databricks.sdk import WorkspaceClient


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
    pass
