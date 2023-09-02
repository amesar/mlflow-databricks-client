
from abc import abstractmethod, ABCMeta

class BaseDatabricksMlflowClient(metaclass=ABCMeta):
    """
    Methods shared between non Unity Catalog and Unity Catalog implementations.
    """

    def get_experiment_permissions(self, experiment_id_or_name):
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self._get_experiment_permissions(experiment_id)

    def get_experiment_permission_levels(self, experiment_id_or_name):
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self._get_experiment_permission_levels(experiment_id)


    def set_experiment_permissions(self, experiment_id_or_name, access_control_list):
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self._set_experiment_permissions(experiment_id, access_control_list)

    def update_experiment_permissions(self, experiment_id_or_name, access_control_list):
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self._update_experiment_permissions(experiment_id, access_control_list)


    def delete_runs(self, experiment_id_or_name, max_timestamp_millis, max_runs=None):
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self._delete_runs(experiment_id, max_timestamp_millis, max_runs=max_runs)

    def restore_runs(self, experiment_id_or_name, min_timestamp_millis, max_runs=None):
        experiment_id = self._get_experiment_id(experiment_id_or_name)
        return self._restore_runs(experiment_id, min_timestamp_millis, max_runs=max_runs)


    @abstractmethod
    def _get_experiment_permissions(self, experiment_id):
        pass

    @abstractmethod
    def _get_experiment_permission_levels(self, experiment_id):
        pass


    @abstractmethod
    def _set_experiment_permissions(self, experiment_id, access_control_list):
        pass

    @abstractmethod
    def _update_experiment_permissions(self, experiment_id, access_control_list):
        pass


    @abstractmethod
    def _delete_runs(self, experiment_id, max_timestamp_millis, max_runs=None):
        pass

    @abstractmethod
    def _restore_runs(self, experiment_id, min_timestamp_millis, max_runs=None):
        pass


    @abstractmethod
    def _get_experiment_id(self, experiment_id_or_name):
        pass


class DatabricksMlflowClient(BaseDatabricksMlflowClient):
    """
    Methods that only apply to non Unity Catalog registered models.
    """ 

    @abstractmethod
    def get_registered_model_databricks(self, model_name):
        pass


    @abstractmethod
    def get_registered_model_permissions(self, model_id):
        pass

    def get_registered_model_permissions_by_name(self, model_name):
        model_id = self._get_registered_model_id(model_name)
        return self.get_registered_model_permissions(model_id)


    @abstractmethod
    def get_registered_model_permission_levels(self, model_id):
        pass

    def get_registered_model_permission_levels_by_name(self, model_name):
        model_id = self._get_registered_model_id(model_name)
        return self.get_registered_model_permission_levels(model_id)


    @abstractmethod
    def set_registered_model_permissions(self, model_id, access_control_list=None):
        pass

    @abstractmethod
    def update_registered_model_permissions(self, model_id, access_control_list=None):
        pass


    @abstractmethod
    def _get_registered_model_id(self, model_name):
        pass


class DatabricksUcMlflowClient(BaseDatabricksMlflowClient):
    """ 
    Methods that only apply to Unity Catalog registered models.
    """ 

    @abstractmethod
    def get_registered_model_effective_permissions(self, model_name):
        pass

    @abstractmethod
    def get_registered_model_permissions(self, model_name):
        pass

    @abstractmethod
    def update_registered_model_permissions(self, model_name, changes):
        pass
