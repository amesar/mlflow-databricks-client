"""
Databricks SDK client for Databricks-specific MLflow API.
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import catalog
from mlflow_databricks_client.base_client import BaseDatabricksMlflowClient as _BaseDatabricksMlflowClient
from mlflow_databricks_client.base_client import DatabricksMlflowClient as _DatabricksMlflowClient


class BaseDatabricksMlflowClient(_BaseDatabricksMlflowClient):
    """
    Common endpoints shared between non Unity Catalog and Unity Catalog implementations.
    """

    def __init__(self):
        self._client = WorkspaceClient()


    def _get_experiment_permissions(self, experiment_id):
        """
        See https://docs.databricks.com/api/workspace/experiments/getexperimentpermissions
        <br>
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.get_experiment_permissions
        """
        return self._client.experiments.get_experiment_permissions(experiment_id)

    def _get_experiment_permission_levels(self, experiment_id):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.get_experiment_permission_levels
        <br>
        See https://docs.databricks.com/api/workspace/experiments/getexperimentpermissionlevels
        """
        return self._client.experiments.get_experiment_permission_levels(experiment_id)


    def _set_experiment_permissions(self, experiment_id, access_control_list):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.set_experiment_permissions
        <br>
        See https://docs.databricks.com/api/workspace/experiments/setexperimentpermissions
        """
        return self._client.experiments.set_experiment_permissions(experiment_id, access_control_list=access_control_list)

    def _update_experiment_permissions(self, experiment_id, access_control_list):
        """
        See https://docs.databricks.com/api/workspace/experiments/updateexperimentpermissions
        <br>
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.update_experiment_permissions
        """
        return self._client.experiments.update_experiment_permissions(experiment_id, access_control_list=access_control_list)


    def _delete_runs(self, experiment_id, max_timestamp_millis, max_runs=None):
        """
        See https://docs.databricks.com/api/workspace/experiments/deleteruns
        <br>
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.delete_runs
        """
        return self._client.experiments.delete_runs(experiment_id, max_timestamp_millis, max_runs=max_runs)

    def _restore_runs(self, experiment_id, min_timestamp_millis, max_runs=None):
        """
        See https://docs.databricks.com/api/workspace/experiments/restoreruns
        <br>
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/experiments.html#ExperimentsAPI.restore_runs
        """
        return self._client.experiments.restore_runs(experiment_id, min_timestamp_millis, max_runs=max_runs)


    def _get_experiment_id(self, experiment_id_or_name):
        """
        Returns an experiment either by ID or name.
        """
        if not "/" in experiment_id_or_name:
            return experiment_id_or_name
        rsp = self._client.experiments.get_by_name(experiment_id_or_name)
        return rsp.experiment.experiment_id


    def __repr__(self):
        return self._client.config._inner.get("host")


class DatabricksMlflowClient(BaseDatabricksMlflowClient, _DatabricksMlflowClient):
    """
    Endpoints that only apply to non Unity Catalog registered models.
    """

    def get_registered_model_databricks(self, model_name):
        return self._client.model_registry.get_model(model_name)


    def get_registered_model_permissions(self, model_id):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.get_registered_model_permissions
        <br>
        See https://docs.databricks.com/api/workspace/modelregistry/getregisteredmodelpermissions
        """
        return self._client.model_registry.get_registered_model_permissions(model_id)

    def get_registered_model_permissions_by_name(self, model_name):
        model_id = self._get_registered_model_id(model_name)
        return self._client.model_registry.get_registered_model_permissions(model_id)


    def get_registered_model_permission_levels(self, model_id):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.get_registered_model_permission_levels
        """
        return self._client.model_registry.get_registered_model_permission_levels(model_id)

    def get_registered_model_permissions_levels_by_name(self, model_name):
        model_id = self._get_registered_model_id(model_name)
        return self._client.model_registry.get_registered_model_permission_levels(model_id)


    def set_registered_model_permissions(self, model_id, access_control_list=None):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.set_registered_model_permissions
        """
        return self._client.model_registry.set_registered_model_permissions(model_id, access_control_list=access_control_list)

    def update_registered_model_permissions(self, model_id, access_control_list=None):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.update_registered_model_permissions
        """
        return self._client.model_registry.update_registered_model_permissions(model_id, access_control_list=access_control_list)


    def _get_registered_model_id(self, model_name):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/model_registry.html#ModelRegistryAPI.get_model
        """
        model = self._client.model_registry.get_model(model_name)
        model = model.registered_model_databricks
        return model.id


class DatabricksUcMlflowClient(BaseDatabricksMlflowClient):
    """
    Endpoints that only apply to Unity Catalog registered models.
    """

    def get_registered_model_effective_permissions(self, model_name):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html#GrantsAPI.get_effective
        <br>
        See https://docs.databricks.com/api/workspace/grants/geteffective
        """
        return self._client.grants.get_effective(catalog.SecurableType.FUNCTION, model_name)

    def get_registered_model_permissions(self, model_name):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html#GrantsAPI.get
        <br>
        See https://docs.databricks.com/api/workspace/grants/get
        """
        return self._client.grants.get(catalog.SecurableType.FUNCTION, model_name)

    def update_registered_model_permissions(self, model_name, changes):
        """
        See https://databricks-sdk-py.readthedocs.io/en/latest/workspace/grants.html#GrantsAPI.update
        <br>
        See https://docs.databricks.com/api/workspace/grants/update
        """
        return self._client.grants.update(catalog.SecurableType.FUNCTION, model_name, changes=changes)
